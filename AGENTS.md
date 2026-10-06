# AGENTS.md — hello-todo

> 本文件是项目级约定，供 AI 协作者（含数字员工 Linus）从第一轮起遵守。
> 上游约束：资料库「技术宪法 tech-stack」与「工程规范 dev-workflow」，冲突时以资料库原文为准。

## 项目是什么

一人公司 hello 级演练项目：一个待办（Todo）全栈应用，用于端到端验证 1 号数字员工 Linus 的 SOP（需求 → 开发 → 测试 → 文档 → 本地部署）。

- 前端：Vue 3 SPA，任务列表的展示、新增、勾选完成、删除
- 后端：FastAPI REST API，`/api/tasks` CRUD + `/health`
- 数据库：PostgreSQL 16（本地与 Docker Compose 均为容器）
- 部署：本地 Docker Desktop（WSL2）优先；云端（腾讯云轻量）为后续目标

## 数字员工

本仓库配置 1 号数字员工 **Linus**：角色档案见 `.kimi-code/agents/linus.md`。

- 默认走**正规轨** P0-P5 SOP；简单需求（≤3 文件、不碰红线、不涉高风险逻辑）可走**轻轨** vibe
- 红线（任何轨道都需老板批准）：架构级技术变更、删除文件/强推、schema 变更、对外发布部署、main 写操作
- 扩展纪律：可为解决问题引入清单外组件，须在交付报告写明理由并同步技术宪法

## 目录结构

```text
hello-todo/
├── .kimi-code/agents/linus.md   # 数字员工角色档案
├── .github/workflows/ci.yml     # CI：PR/push 到 main 跑前后端检查 + compose 构建验证
├── docker-compose.yml           # 本地一键部署：web + api + db
├── frontend/                    # Vue 3 前端（pnpm）
│   └── src/{api,components,stores,views,router}
├── backend/                     # FastAPI 后端（uv）
│   ├── app/{routers,services,repositories,models,schemas,core}
│   ├── alembic/                 # 数据库迁移
│   └── tests/
└── docs/                        # architecture / adr / comment-style / deployment / delivery
```

## 常用命令

```bash
# 前端
cd frontend && pnpm install
pnpm dev        # 开发服务器（代理 /api → localhost:8000）
pnpm test       # Vitest
pnpm lint       # eslint
pnpm build      # 产物 dist/

# 后端
cd backend && uv venv && uv pip install -r pyproject.toml
uv run pytest           # 测试（SQLite 内存库，无需外部依赖）
uv run ruff check .     # lint
uv run uvicorn app.main:app --reload   # 本地开发（需 DATABASE_URL 指向 PG）

# 本地部署（整套环境）
docker compose up -d --build      # 构建并启动 web/api/db
docker compose logs -f            # 看日志
docker compose down               # 停止
```

## 工程规则摘要

- 分支：`main` 受保护；`feature/<功能名>` / `fix/<缺陷名>` / `refactor/<主题>` / `vibe/<日期>-<主题>`
- 提交：Conventional Commits（feat/fix/refactor/test/docs/chore/style，中文一句话）
- 审查清单（每次交付前过）：正确性（边界/异常不静默）、规范（命名/无死代码/JSDoc 与类型注解）、安全（无硬编码密钥/输入校验/参数化 SQL）、可维护（注释讲为什么/公共逻辑复用/测试通过）
- 数据库变更一律 Alembic 迁移，禁止手改表结构
