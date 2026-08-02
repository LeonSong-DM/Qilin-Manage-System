import { useState } from 'react'
import {
  AppstoreOutlined,
  CalendarOutlined,
  ControlOutlined,
  FileTextOutlined,
  LockOutlined,
  LoginOutlined,
  LogoutOutlined,
  TruckOutlined,
  UserOutlined,
} from '@ant-design/icons'
import { Button, Checkbox, ConfigProvider, Form, Input, message } from 'antd'
import DarkVeil from './DarkVeil'
import './App.css'

const navItems = [
  { key: 'overview', label: '数据概览', icon: <AppstoreOutlined /> },
  { key: 'orders', label: '客户订单', icon: <FileTextOutlined /> },
  { key: 'schedule', label: '排产管理', icon: <CalendarOutlined /> },
  { key: 'outbound', label: '出库记录', icon: <TruckOutlined /> },
  { key: 'information', label: '信息管理', icon: <ControlOutlined /> },
]

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    return localStorage.getItem('qilin_pc_auth') === '1'
  })
  const [activeNav, setActiveNav] = useState(navItems[0].key)
  const activeNavItem = navItems.find((item) => item.key === activeNav) ?? navItems[0]

  const handleLogin = (values) => {
    if (values.account === 'admin' && values.password === 'admin') {
      localStorage.setItem('qilin_pc_auth', '1')
      setIsLoggedIn(true)
      return
    }

    message.error('账号或密码错误')
  }

  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#4B3D4F',
          borderRadius: 8,
          fontFamily:
            '"Noto Sans SC", ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
        },
        components: {
          Button: {
            controlHeightLG: 46,
            fontWeight: 700,
          },
          Input: {
            controlHeightLG: 46,
          },
        },
      }}
    >
      {isLoggedIn ? (
        <main className="dashboard-page">
          <aside className="dashboard-sidebar" aria-label="管理端导航">
            <div className="sidebar-brand">
              <span className="sidebar-brand-mark">
                <ControlOutlined />
              </span>
              <span>骐临电镀生产管理系统</span>
            </div>

            <nav className="sidebar-nav">
              {navItems.map((item) => (
                <button
                  className={`sidebar-nav-item ${activeNav === item.key ? 'is-active' : ''}`}
                  key={item.key}
                  type="button"
                  onClick={() => setActiveNav(item.key)}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </button>
              ))}
            </nav>

            <div className="sidebar-user">
              <div className="sidebar-account">
                <div className="sidebar-avatar" aria-hidden="true">
                  管
                </div>
                <div className="sidebar-user-meta">
                  <div className="sidebar-user-label">
                    <UserOutlined />
                    <span>账户</span>
                  </div>
                  <div className="sidebar-username">username</div>
                </div>
                <button
                  className="sidebar-logout"
                type="button"
                aria-label="退出登录"
                onClick={() => {
                  localStorage.removeItem('qilin_pc_auth')
                  setIsLoggedIn(false)
                }}
              >
                  <LogoutOutlined />
                </button>
              </div>
            </div>
          </aside>

          <section className="dashboard-content" aria-label="管理端内容">
            <div className="data-panel">
              <header className="data-panel-header" key={activeNav}>
                <h1>{activeNavItem.label}</h1>
              </header>
            </div>
          </section>
        </main>
      ) : (
        <main className="login-page">
          <div className="login-bg" aria-hidden="true">
            <DarkVeil
              hueShift={0}
              noiseIntensity={0}
              scanlineIntensity={0}
              speed={0.5}
              scanlineFrequency={0}
              warpAmount={0}
            />
          </div>

          <aside className="login-card" aria-label="登录表单">
            <div className="login-card-header">
              <p className="system-title">骐临电镀生产管理系统</p>
              <h2>Welcome Back</h2>
            </div>

            <Form
              name="pc-login"
              layout="vertical"
              requiredMark={false}
              initialValues={{ remember: true }}
              onFinish={handleLogin}
            >
              <Form.Item
                label="账号"
                name="account"
                rules={[{ required: true, message: '请输入账号' }]}
              >
                <Input
                  size="large"
                  autoComplete="username"
                  placeholder="请输入登录账号"
                  prefix={<UserOutlined />}
                />
              </Form.Item>

              <Form.Item
                label="密码"
                name="password"
                rules={[{ required: true, message: '请输入密码' }]}
              >
                <Input.Password
                  size="large"
                  autoComplete="current-password"
                  placeholder="请输入登录密码"
                  prefix={<LockOutlined />}
                />
              </Form.Item>

              <div className="form-row">
                <Form.Item name="remember" valuePropName="checked" noStyle>
                  <Checkbox>记住登录状态</Checkbox>
                </Form.Item>
                <button className="link-button" type="button">
                  忘记密码
                </button>
              </div>

              <Button
                block
                className="login-submit"
                htmlType="submit"
                icon={<LoginOutlined />}
                size="large"
                type="primary"
              >
                登录系统
              </Button>
            </Form>
          </aside>
        </main>
      )}
    </ConfigProvider>
  )
}

export default App
