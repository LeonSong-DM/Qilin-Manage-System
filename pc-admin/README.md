# Qilin PC Admin

PC 管理端当前从旧 `pc-ui` 迁移而来，保留原登录页和基础侧边栏样式。

## Commands

```bash
npm install
npm run dev
npm run build
npm run lint
```

## Environment

默认后端地址为 `http://localhost:8000`。如需修改，在 `pc-admin/.env.local` 中配置：

```bash
VITE_API_BASE_URL=http://localhost:8000
```

默认管理员账号：

```text
手机号：13800000001
密码：admin123456
```
