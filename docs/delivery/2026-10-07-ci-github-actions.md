# 交付报告：GitHub Actions CI（PR 到 main 自动检查）

- 日期：2026-10-07 ｜ 分支：feature/ci-github-actions ｜ 轨道：正规轨（P0-P4，P5 不涉及，无部署）
- 需求复述：为仓库配置 GitHub Actions CI，PR 到 main 时自动跑前端（eslint + vitest + build）、后端（ruff + pytest）与 docker compose build 构建验证（技术宪法既定基线，补齐缺失的 PR 质量门禁）

## P0 拍板记录（老板已确认）

1. 触发范围：PR 到 main + push 到 main 都跑（合并后再验证一道）
2. Docker 验证深度：仅 `docker compose build`，不起 stack 冒烟（留待 CD 阶段）

## 验收标准对照

| 验收标准 | 结果 |
|---|---|
| PR/push 到 main 自动触发 | ✅ `on: pull_request/push branches:[main]` |
| 前端 eslint + vitest + build | ✅ job `frontend`（Node 22 + pnpm 12.9.1 + 缓存） |
| 后端 ruff + pytest | ✅ job `backend`（uv + Python 3.12，`uv sync --locked`） |
| compose 构建验证 | ✅ job `docker-build`（仅占位 env，不起服务） |

## 变更说明（文件级清单）

- 新增 `.github/workflows/ci.yml`：3 个并行 job；`permissions: contents: read` 最小权限；concurrency 自动取消同 ref 过期运行
- 改 `frontend/package.json`（+1 行）：`packageManager: pnpm@12.9.1` 钉死本地/CI/Docker 三端 pnpm 版本，消除版本漂移根因（上次 pnpm 12 strictDepBuilds 踩坑的同类问题）
- 改 `backend/pyproject.toml`：ruff 配置 `extend-immutable-calls = ["fastapi.Depends"]`，豁免 B008 对 FastAPI 依赖注入标准写法的误报
- 改 `backend/alembic/env.py`、`backend/alembic/versions/0001_create_tasks.py`：ruff I001 导入排序自动修复（纯排序，无逻辑变化）
- 新增 `backend/uv.lock`：锁定依赖版本，CI 用 `uv sync --locked` 断言不漂移（对 P1 方案的修正，见下）
- 同步 `docs/deployment.md` §4、`docs/architecture.md` §8、`AGENTS.md` 目录结构

## P3 发现并处理的两个真问题

1. **pnpm 版本钉住 11.7.0 会把 Docker 构建打挂**：11.7 的「运行脚本前依赖状态检查」基于文件 mtime，`COPY . .` 刷新 lockfile 时间戳后被误判过期，非 TTY 环境直接 abort（`ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY`）。pnpm 12 改用内容比对无此问题，且容器既往冒烟用的就是 12.x。故 pin 改为 12.9.1 并用 compose build 实测通过。
2. **存量代码 ruff 不过（6 个错）+ 依赖无锁**：无 uv.lock 时 `uv sync` 每次解析最新版，本次装到 ruff 0.16.10 直接暴露存量 I001×2 + B008×4（FastAPI `Depends` 惯用法误报）。修复：B008 配置豁免 + 自动修复排序；并**改变 P1「不提交 uv.lock」的决定**——本次偷袭证明无锁 CI 必然漂移，已提交锁文件并改 `uv sync --locked`。

## 如何验证（老板自测步骤）

1. 看 PR 页面 Checks 标签：三个 job（前端/后端/Docker 构建）应全绿
2. 本地复演 CI 命令：`cd frontend && pnpm install --frozen-lockfile && pnpm lint && pnpm test && pnpm build`
3. `cd backend && uv sync --locked && uv run ruff check . && uv run pytest`
4. 根目录 `docker compose --env-file .env.example build`（模拟 CI 的占位 env 方式，不碰本机 .env）
5. **（需老板操作）** 仓库 Settings → Branches → main 分支保护 → 勾选三个 job 为必过检查，门禁才真正生效

## 测试与自检结论

- 前端：eslint 0 errors（15 个既有 warning，不阻塞）；vitest 3 passed；build 成功（本地 pnpm 11.7.0 与容器 12.9.1 双环境验证）
- 后端：ruff All checks passed；pytest 4 passed，覆盖率 95%
- Docker：`hello-todo-api` / `hello-todo-web` 两镜像构建成功（pnpm 12.9.1）
- 审查清单：正确性 ✅（CI 命令全部本地实跑彩排，YAML 解析通过）/ 规范 ✅（注释讲为什么，Conventional Commits 3 个）/ 安全 ✅（最小 permissions、无密钥、env 仅用 .env.example 占位值）/ 可维护 ✅（单 workflow 三 job，版本与仓库配置同源）

## 文档更新索引

- 本报告；`docs/deployment.md` §4（CI 状态 + 分支保护建议）；`docs/architecture.md` §8（后续计划更新）；`AGENTS.md` 目录结构
- 不写 ADR：GitHub Actions 属技术宪法既定决策，无新选型

## 遗留与建议

- 分支保护（必过检查）需老板在 GitHub 设置里开启，我无权操作 main；开完后本门禁闭环
- 前端 15 个 eslint warning（vue 模板风格类）建议下个小任务清零，可考虑 `pnpm lint --max-warnings 0` 收紧
- Dockerfile 里 `pnpm install --frozen-lockfile || pnpm install` 的静默兜底会掩盖锁文件漂移，建议去掉 `|| pnpm install`
- 后端 Dockerfile 仍用 `uv pip install --system` 内联依赖清单，与 pyproject/uv.lock 双写维护，建议后续统一改为 `uv sync` 系
- push 到 main 的 CI 结果目前没有通知渠道，可在上云任务里一并考虑（GitHub 邮件通知默认已够 hello 级）
