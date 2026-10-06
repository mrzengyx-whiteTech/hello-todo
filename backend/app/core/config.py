"""应用配置：环境变量唯一入口（技术宪法：代码里只读 config 模块）。"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用设置。

    Attributes:
        database_url: SQLAlchemy 连接串，compose 内指向 db 服务。
        cors_origins: 允许跨域的来源列表（仅开发端口，生产由 Caddy 同源托管）。
    """

    database_url: str = "postgresql+psycopg://todo:todo@localhost:5432/todo"
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
