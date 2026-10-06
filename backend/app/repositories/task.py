"""数据访问层：任务的 CRUD（只允许本层碰 SQLAlchemy）。"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task


def list_tasks(db: Session) -> list[Task]:
    """按创建时间倒序返回全部任务。

    Args:
        db: 当前请求的数据库会话。

    Returns:
        任务列表（可能为空）。
    """
    return list(db.scalars(select(Task).order_by(Task.created_at.desc())).all())


def get_task(db: Session, task_id: int) -> Task | None:
    """按主键取任务，不存在返回 None。"""
    return db.get(Task, task_id)


def create_task(db: Session, *, title: str) -> Task:
    """插入新任务并返回持久化后的实体。"""
    task = Task(title=title)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task: Task, *, title: str | None, done: bool | None) -> Task:
    """按非 None 字段部分更新任务。"""
    if title is not None:
        task.title = title
    if done is not None:
        task.done = done
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    """删除任务。"""
    db.delete(task)
    db.commit()
