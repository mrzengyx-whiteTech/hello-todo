# 部署操作手册

> 最后更新：2026-10-07 ｜ 相关决策：docs/adr/0001（本地优先）；云端目标见设计方案 ADR-0001/0002

## 1. 环境清单

| 环境 | 位置 | 入口 | 用途 |
|---|---|---|---|
| dev（本手册当前环境） | 本机 Windows + Docker Desktop (WSL2) | http://localhost | 日常演练与交付验证 |
| prod（待启动） | 腾讯云轻量 2核4G（设计方案 ADR-0001） | 待定（先 IP，域名备案后切换） | 正式对外 |

## 2. 前置条件

- Docker Desktop 已安装并启用 WSL2 后端（`docker --version` 可用）
- 仓库根目录有 `.env`（从 `.env.example` 复制并填值；**.env 只存在于本机/服务器，永不入库**）
- 本机 80 端口未被占用

## 3. 首次部署步骤

```bash
cp .env.example .env          # 按需修改密码等值
docker compose up -d --build  # 构建镜像并启动 web/api/db
docker compose ps             # 三个服务应均为 running（db 为 healthy）
```

## 4. 日常发版步骤

```bash
git checkout main && git pull        # main 是受保护分支，只拉不推
docker compose up -d --build         # 有代码变更的服务会重建并滚动替换
```

CI 阶段（GitHub Actions，已配 `.github/workflows/ci.yml`）：PR 与 push 到 main 时跑前端 eslint+vitest+build、后端 ruff+pytest、`docker compose build` 构建验证；本阶段不做自动部署。建议在仓库 Settings 把三个 job 设为 main 的必过检查（分支保护）。

## 5. 回滚

```bash
git checkout <上一个可用提交>         # 代码级回滚
docker compose up -d --build          # 重新构建发布
# 数据库回滚走 alembic downgrade（属红线，需老板批准）
```

## 6. 部署后验证（冒烟清单）

1. `curl http://localhost/health` 经 web 反代返回 `{"status":"ok"}`
2. 浏览器打开 http://localhost 能看到待办页面
3. 新增一条任务 → 刷新页面仍在（验证 db 持久化）
4. 勾选完成、删除各操作一次无报错
5. `docker compose logs api --tail 50` 无 ERROR

## 7. 备份（dev 环境从简）

- db 数据在命名卷 `hello-todo_pgdata` 中；演练项目无需定时备份
- 上云后启用：每日 `pg_dump | gzip` 保留 30 天 + 轻量控制台自动快照（见设计方案 ADR-0001）

## 8. 故障排查速查

```bash
docker compose ps                 # 看服务状态
docker compose logs -f api        # 跟 api 日志
docker compose logs -f db         # 跟 db 日志
docker compose down && docker compose up -d --build   # 全量重启重建
```

- **80 端口被占用**：改 docker-compose.yml 中 web 的 ports，如 `"8080:80"`，访问 http://localhost:8080
- **api 起不来报数据库连接失败**：等 db healthy 后自动重试，或 `docker compose restart api`
- **迁移失败**：`docker compose run --rm api alembic current` 查看当前版本，报错信息贴给 Linus 处理（schema 变更属红线）
