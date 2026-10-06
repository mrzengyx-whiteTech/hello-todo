"""任务 API 集成测试。

说明：测试用 SQLite 内存库（StaticPool 共享连接），仅用于替代 PG 跑用例，
生产与部署环境始终是 PostgreSQL 16 —— 这是测试替身，不是技术栈变更。
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """每个用例一张全新空表，互不污染。"""
    Base.metadata.create_all(engine)

    def override_get_db() -> Generator:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


def test_health(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_task_crud_flow(client: TestClient) -> None:
    """创建 → 列表 → 勾选完成 → 删除 的完整链路。"""
    create_resp = client.post("/api/tasks", json={"title": "  写交付报告  "})
    assert create_resp.status_code == 201
    task = create_resp.json()
    # 业务规则：标题入库前去除首尾空白
    assert task["title"] == "写交付报告"
    assert task["done"] is False

    list_resp = client.get("/api/tasks")
    assert list_resp.status_code == 200
    assert [t["id"] for t in list_resp.json()] == [task["id"]]

    patch_resp = client.patch(f"/api/tasks/{task['id']}", json={"done": True})
    assert patch_resp.status_code == 200
    assert patch_resp.json()["done"] is True

    del_resp = client.delete(f"/api/tasks/{task['id']}")
    assert del_resp.status_code == 204
    assert client.get("/api/tasks").json() == []


def test_create_task_with_blank_title_returns_400(client: TestClient) -> None:
    resp = client.post("/api/tasks", json={"title": "   "})
    assert resp.status_code == 400


def test_operate_missing_task_returns_404(client: TestClient) -> None:
    assert client.patch("/api/tasks/999", json={"done": True}).status_code == 404
    assert client.delete("/api/tasks/999").status_code == 404
