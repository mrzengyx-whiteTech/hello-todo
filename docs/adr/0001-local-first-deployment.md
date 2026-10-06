# ADR-0001：本地优先部署，compose 同构上云

- 状态：已接受
- 日期：2026-10-07
- 决策人：Linus（整理）→ 老板（拍板，2026-10-07 确认）

## 背景

本项目是一人公司第一个演练项目。生产目标是腾讯云轻量服务器（设计方案 ADR-0001），但服务器尚未购买；需要一个零等待的部署环境先跑通 SOP 全流程（设计方案 ADR-0002）。

## 备选方案

1. 本地 Docker Desktop（WSL2）+ docker compose：零成本零等待；缺点是只能本机/局域网访问
2. 直接购机上云：一步到位；缺点是购机与初始化阻塞演练开始
3. 仅 pnpm dev / uvicorn 起前后端进程：最快；缺点是不经过 Docker，验证不了部署链路

## 决定

第一阶段本地部署：同一套 docker-compose（web = Caddy + 前端产物、api、db = PostgreSQL 16），`docker compose up -d --build` 一键发布到本机，浏览器访问 http://localhost。GitHub Actions 此阶段只做 CI（测试 + 构建验证）。上云在 hello 项目端到端跑通后按设计方案 ADR-0001 执行。

## 理由

- 零成本零等待，当天即可开始演练
- compose 文件本地/云端同构：上云只换机器与 .env，不推翻任何产物
- 先跑通流程再花钱，符合一人公司成本纪律

## 影响

- 对代码：无侵入；前端构建产物经多阶段 Dockerfile 进入 web 镜像
- 对文档：docs/deployment.md 按「本地 + prod（待启动）」双环境维护
- 后续动作：hello 项目验收通过后，老板执行购机与服务器初始化（设计方案 ADR-0001 待办清单）
