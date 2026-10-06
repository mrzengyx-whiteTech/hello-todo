"""SQLAlchemy 模型：任务。"""

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

TITLE_MAX_LENGTH = 200


class Task(Base):
    """待办任务表。

    Attributes:
        id: 自增主键。
        title: 任务标题（入库前已清洗，见 services 层）。
        done: 完成状态。
        created_at: 创建时间（数据库侧生成，保证时区一致）。
    """

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(TITLE_MAX_LENGTH), nullable=False)
    done: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
