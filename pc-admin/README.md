# Qilin PC Admin

PC 管理端基于 React、Vite、Ant Design 和 ProComponents 初始化。

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

PC 管理端只允许管理员角色登录，认证使用后端 `/users/login` JSON 接口。
