"""FastAPI 应用入口。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import tasks

app = FastAPI(title="hello-todo API", version="0.1.0")

# CORS 仅放行本地开发端口；生产由 Caddy 同源托管，不需要跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)


@app.get("/health")
async def health() -> dict[str, str]:
    """存活探针（冒烟清单第 1 项）。"""
    return {"status": "ok"}
