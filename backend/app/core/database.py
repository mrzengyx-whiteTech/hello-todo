"""数据库连接与会话管理。"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """全部模型的声明式基类。"""


def get_db() -> Generator[Session, None, None]:
    """FastAPI 依赖：每请求一个会话，用完关闭。

    Yields:
        当前请求的 SQLAlchemy Session。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
