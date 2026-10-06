# 前端镜像：node 构建 dist → Caddy 托管 + 反代（多阶段，技术宪法部署基线）
FROM node:22-slim AS build

# pnpm 为宪法指定包管理器；corepack 随 node 22 自带
RUN corepack enable
WORKDIR /app

COPY package.json pnpm-lock.yaml* pnpm-workspace.yaml* ./
RUN pnpm install --frozen-lockfile || pnpm install

COPY . .
RUN pnpm build

FROM caddy:2 AS serve
COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=build /app/dist /usr/share/caddy

EXPOSE 80
