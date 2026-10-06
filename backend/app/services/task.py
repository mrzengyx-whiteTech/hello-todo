"""业务逻辑层：任务规则与异常翻译。"""

from sqlalchemy.orm import Session

from app.models.task import Task
from app.repositories import task as task_repo
from app.schemas.task import TaskCreate, TaskUpdate


class TaskNotFoundError(Exception):
    """任务不存在（路由层翻译为 404）。"""


class EmptyTitleError(ValueError):
    """标题清洗后为空（路由层翻译为 400）。"""


def normalize_title(raw: str) -> str:
    """清洗任务标题。

    Args:
        raw: 用户原始输入。

    Returns:
        去除首尾空白后的标题。

    Raises:
        EmptyTitleError: 清洗后为空字符串时（业务规则：空白标题无意义）。
    """
    title = raw.strip()
    if not title:
        raise EmptyTitleError("任务标题不能为空")
    return title


def list_tasks(db: Session) -> list[Task]:
    """列出全部任务（当前无过滤规则，直接透传；预留给分页/筛选扩展）。"""
    return task_repo.list_tasks(db)


def create_task(db: Session, payload: TaskCreate) -> Task:
    """清洗标题后创建任务。"""
    return task_repo.create_task(db, title=normalize_title(payload.title))


def _must_get(db: Session, task_id: int) -> Task:
    """取任务，不存在抛 TaskNotFoundError。"""
    task = task_repo.get_task(db, task_id)
    if task is None:
        raise TaskNotFoundError(f"任务不存在: {task_id}")
    return task


def update_task(db: Session, task_id: int, payload: TaskUpdate) -> Task:
    """部分更新任务；标题字段同样走清洗规则。"""
    task = _must_get(db, task_id)
    title = normalize_title(payload.title) if payload.title is not None else None
    return task_repo.update_task(db, task, title=title, done=payload.done)


def delete_task(db: Session, task_id: int) -> None:
    """删除任务，不存在抛 TaskNotFoundError。"""
    task_repo.delete_task(db, _must_get(db, task_id))
