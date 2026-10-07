# 交付报告：PR #1 遗留处理（warning 清零 + Dockerfile 去兜底）

- 日期：2026-10-07 ｜ 分支：fix/frontend-lint-docker-hardening ｜ 轨道：正规轨（老板批准；改动 4 个代码文件超轻轨上限）
- 需求复述：处理 PR #1 交付报告两条遗留——① 前端 15 个 eslint warning 清零并在 CI lint 步骤加 `--max-warnings 0` 防复发；② 删 `frontend/Dockerfile` 的 `pnpm install --frozen-lockfile || pnpm install` 静默兜底
- 老板批示：修代码不修规则；--fix 先行、手动兜底；仅确认误报的规则可调整并说明理由

## 验收标准对照

| 验收标准 | 结果 |
|---|---|
| `pnpm lint` 0 errors / 0 warnings | ✅ 15 个 warning 全部消除 |
| CI lint 步骤带 `--max-warnings 0` | ✅ `.github/workflows/ci.yml` 前端 job |
| Dockerfile 无静默兜底 | ✅ 仅保留 `pnpm install --frozen-lockfile` |
| 锁文件过期时 Docker 构建当场失败 | ✅ 负向实测：`ERR_PNPM_OUTDATED_LOCKFILE` exit 1（见下） |

## 变更说明（文件级清单）

- `frontend/src/components/TaskItem.vue`、`frontend/src/views/HomeView.vue`：`eslint --fix` 自动修复全部 15 个 warning（vue/html-self-closing、vue/singleline-html-element-content-newline、vue/max-attributes-per-line），纯模板排版，无逻辑改动
- `.github/workflows/ci.yml`：前端 job lint 步骤改为 `pnpm lint --max-warnings 0`，warning 即失败
- `frontend/Dockerfile`：删除 `|| pnpm install` 兜底，注释说明「frozen 失败即构建失败」
- 规则零调整：15 个 warning 均为真实可修的排版问题，无误报，无需动 eslint 配置（老板批示的执行结果说明）

## 如何验证（老板自测步骤）

1. 本 PR 的 Checks 三个 job 应全绿（前端 job 现在带 `--max-warnings 0`）
2. 本地：`cd frontend && pnpm lint --max-warnings 0`（应零输出）→ `pnpm test` → `pnpm build`
3. Docker 正向：`docker compose --env-file .env.example build`（本机已实测双镜像成功）
4. Docker 负向（选做）：把 `frontend/package.json` 任一依赖版本号改一下（不动 lockfile），`docker compose build web` 应在 `pnpm install --frozen-lockfile` 步直接报 `ERR_PNPM_OUTDATED_LOCKFILE` 失败——本次已用 axios ^1.7.9→^1.8.0 实测通过，验证后已还原

## 测试与自检结论

- 前端：eslint 0 errors / 0 warnings（`--max-warnings 0` 通过）；vitest 3 passed；build 成功
- Docker：正向双镜像构建成功（api + web，pnpm 12.9.1 frozen 安装真通过，无兜底）；负向过期锁文件当场失败，exit 1
- 后端：本次零改动，CI 后端 job 兜底回归
- 审查清单：正确性 ✅（正/负向均实测）/ 规范 ✅（无死代码、注释讲为什么）/ 安全 ✅（不涉及密钥与输入面）/ 可维护 ✅（门禁收紧、文档同步）

## 文档更新索引

- 本报告（新建）
- `docs/delivery/2026-10-07-ci-github-actions.md`：遗留 ①② 标记已处理并指向本报告

## 遗留与建议

- PR #1 遗留还剩两条未处理：后端 Dockerfile 内联依赖清单与 pyproject 双写（建议改 `uv sync` 系）、main 分支保护设置（需老板在 GitHub 操作，仍是门禁闭环的唯一卡点）
- `vue/html-self-closing` 等排版规则与 prettier 职责有重叠，若后续接入 `prettier --check` 入 CI，可考虑把排版类规则移交 prettier 管理（建议，不着急）
