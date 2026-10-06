"""路由层：/api/tasks（只做 IO，业务规则全在 services）。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.core.database import get_db
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services import task as task_service
from app.services.task import EmptyTitleError, TaskNotFoundError

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskOut])
async def list_tasks(db: Session = Depends(get_db)) -> list[TaskOut]:
    """任务列表（创建时间倒序）。"""
    # SQLAlchemy 同步会话是阻塞 IO，宪法要求阻塞操作放线程池，避免卡住事件循环
    return await run_in_threadpool(task_service.list_tasks, db)


@router.post("", response_model=TaskOut, status_code=201)
async def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> TaskOut:
    """新增任务。"""
    try:
        return await run_in_threadpool(task_service.create_task, db, payload)
    except EmptyTitleError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.patch("/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)) -> TaskOut:
    """部分更新任务（改标题或勾选完成）。"""
    try:
        return await run_in_threadpool(task_service.update_task, db, task_id, payload)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except EmptyTitleError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    """删除任务。"""
    try:
        await run_in_threadpool(task_service.delete_task, db, task_id)
    except TaskNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
