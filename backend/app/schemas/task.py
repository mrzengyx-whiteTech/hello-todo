"""pydantic 请求/响应模型：任务。"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.task import TITLE_MAX_LENGTH


class TaskCreate(BaseModel):
    """创建任务请求体。"""

    title: str = Field(min_length=1, max_length=TITLE_MAX_LENGTH)


class TaskUpdate(BaseModel):
    """更新任务请求体（部分更新：两个字段至少给一个，由 service 层校验）。"""

    title: str | None = Field(default=None, min_length=1, max_length=TITLE_MAX_LENGTH)
    done: bool | None = None


class TaskOut(BaseModel):
    """任务响应体。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    done: bool
    created_at: datetime
