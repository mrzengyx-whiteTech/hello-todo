# 后端镜像：python 3.12 + uv（多阶段保持镜像精简）
FROM python:3.12-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# 先装依赖（利用层缓存：仅依赖清单变化才重装）
COPY pyproject.toml ./
RUN uv pip install --system --no-cache \
    "fastapi>=0.115" "uvicorn[standard]>=0.30" "sqlalchemy>=2.0" \
    "alembic>=1.13" "psycopg[binary]>=3.2" "pydantic>=2.7" "pydantic-settings>=2.4"

# 再拷代码
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./

EXPOSE 8000

# 启动：先跑迁移（schema 变更只走 Alembic），再拉起服务
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
