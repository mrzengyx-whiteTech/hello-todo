# 交付报告：hello-todo 项目脚手架（数字员工体系首次交付）

- 日期：2026-10-07 ｜ 分支：feature/hello-todo-init ｜ PR：待推送（本地仓库尚未关联远端）
- 需求复述：搭建一人公司 hello 级演练项目（待办全栈应用 + 数字员工角色档案 + 文档体系），验证 Linus 的 SOP 全流程

## 验收标准对照

| 验收标准 | 结果 |
|---|---|
| 角色档案 .kimi-code/agents/linus.md 可用 | ✅ 已创建（含边界/SOP/双轨/文档义务） |
| AGENTS.md 项目约定可用 | ✅ 已创建 |
| docs 五件套初始化 | ✅ architecture / adr-0001 / comment-style / deployment / 本报告 |
| 待办 API（CRUD + /health） | ✅ FastAPI 分层实现 + Alembic 初始迁移 |
| 前端页面（列表/新增/勾选/删除） | ✅ Vue3 + Pinia + Router + Tailwind |
| 本地一键部署 | ✅ docker compose up -d --build（web+api+db） |
| 测试通过 | 后端 pytest（SQLite 内存库）、前端 Vitest（详见验证步骤） |

## 变更说明

- 新增：数字员工体系全套文件（角色档案、AGENTS.md、docs 五件套）
- 新增：backend/（FastAPI 分层应用 + Alembic + pytest + Dockerfile）
- 新增：frontend/（Vue3 + Vite + Tailwind 4 + Pinia + Router + axios + Vitest + 多阶段 Dockerfile + Caddyfile）
- 新增：根级 docker-compose.yml、.env.example、.gitignore、.editorconfig

## 如何验证（老板自测步骤）

1. `cd hello-todo && cp .env.example .env`
2. `docker compose up -d --build`，待 `docker compose ps` 全部 running
3. 按 docs/deployment.md §6 冒烟清单逐项过（/health、页面、增删改、日志）
4. 后端单测：`cd backend && uv venv && uv pip install -r pyproject.toml && uv run pytest -q`
5. 前端单测：`cd frontend && pnpm install && pnpm test`

## 测试与自检

- 后端：tests/test_tasks.py 覆盖 CRUD 全流程 + 空标题 400 + 不存在 404（SQLite 内存库，测试专用，生产仍 PG16）
- 前端：TaskItem.spec.js 组件测试（渲染 + toggle 事件）
- 审查清单：正确性 ✅（边界与异常处理）/ 规范 ✅（JSDoc、类型注解、无死代码）/ 安全 ✅（无硬编码密钥、ORM 参数化、入参校验）/ 可维护 ✅（分层、注释讲为什么、测试通过）

## 文档更新

- docs/architecture.md（新建）、docs/adr/0001（新建）、docs/comment-style.md（新建）、docs/deployment.md（新建）

## 遗留与建议

- 未接鉴权（hello 级不需要）；真实业务项目启用 PyJWT + passlib（宪法扩展组件已批）
- GitHub Actions CI 工作流建议作为下一个任务（测试 + 构建验证，本阶段不部署）
- 建议老板验收后，将仓库推送 GitHub 并保护 main 分支

## 补记：容器化部署冒烟（2026-10-07 凌晨，vibe 轨道）

**构建修复（2 个文件）**：pnpm 12 默认 `strictDepBuilds=true`，esbuild 安装脚本未审批导致 `ERR_PNPM_IGNORED_BUILDS` 构建失败；且 `onlyBuiltDependencies` 已在 pnpm 11 废弃（package.json 的 pnpm 字段也不再被读取）。修复：新增 `frontend/pnpm-workspace.yaml` 写入 `allowBuilds: { esbuild: true }`；`frontend/Dockerfile` 的 COPY 行补带该文件。教训已固化：今后 pnpm 设置一律写 pnpm-workspace.yaml。

**冒烟结果（docs/deployment.md §6 全过）**：

- 三容器 up（db healthy）；`/health` 返回 `{"status":"ok"}`；首页 HTML 正常
- API 全链路：新增（标题首尾空格被服务端规则清洗）→ 列表 → 勾选 → 删除 → 空列表
- 参数校验：空标题返回 400
- 持久化：新增任务后 `docker compose restart` 全量重启，数据仍在（pgdata 卷生效）
- api 日志 30 行无 ERROR

本地验证补充：后端 pytest 4 passed（覆盖率 95%）、前端 Vitest 3 passed。Windows 本地 `pnpm install` 时 esbuild 校验脚本因托管 Node 运行时文件锁（EBUSY）失败，属本机环境特殊性，不影响 Linux 容器与 CI。
