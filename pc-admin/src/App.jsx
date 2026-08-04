import { useEffect, useState } from 'react'
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
import { clearAuth, getCurrentUser, login, storeAuth } from './services/auth'
import './App.css'

const navItems = [
  { key: 'overview', label: '数据概览', icon: <AppstoreOutlined /> },
  { key: 'orders', label: '客户订单', icon: <FileTextOutlined /> },
  { key: 'schedule', label: '排产管理', icon: <CalendarOutlined /> },
  { key: 'outbound', label: '出库记录', icon: <TruckOutlined /> },
  { key: 'information', label: '信息管理', icon: <ControlOutlined /> },
]

function App() {
  const [currentUser, setCurrentUser] = useState(null)
  const [activeNav, setActiveNav] = useState(navItems[0].key)
  const [loginLoading, setLoginLoading] = useState(false)
  const [authChecking, setAuthChecking] = useState(true)
  const activeNavItem = navItems.find((item) => item.key === activeNav) ?? navItems[0]

  useEffect(() => {
    let ignore = false

    async function restoreSession() {
      try {
        const user = await getCurrentUser()
        if (!ignore && user?.role === 'admin') {
          setCurrentUser(user)
        }
      } catch {
        if (!ignore) {
          setCurrentUser(null)
        }
      } finally {
        if (!ignore) {
          setAuthChecking(false)
        }
      }
    }

    restoreSession()

    return () => {
      ignore = true
    }
  }, [])

  const handleLogin = async (values) => {
    setLoginLoading(true)

    try {
      const { token, user } = await login({
        phone_number: values.phone_number,
        password: values.password,
      })

      if (user.role !== 'admin') {
        message.error('PC 管理端只允许管理员登录')
        return
      }

      storeAuth(token, user)
      setCurrentUser(user)
    } catch (error) {
      message.error(error.message || '账号或密码错误')
    } finally {
      setLoginLoading(false)
    }
  }

  const handleLogout = () => {
    clearAuth()
    setCurrentUser(null)
  }

  const isLoggedIn = currentUser?.role === 'admin'
  const userInitial = currentUser?.name?.slice(0, 1) ?? '管'

  if (authChecking) {
    return (
      <main className="auth-checking-page" aria-label="登录状态检查">
        <span>正在检查登录状态</span>
      </main>
    )
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
                  {userInitial}
                </div>
                <div className="sidebar-user-meta">
                  <div className="sidebar-user-label">
                    <UserOutlined />
                    <span>账户</span>
                  </div>
                  <div className="sidebar-username">{currentUser?.name}</div>
                </div>
                <button
                  className="sidebar-logout"
                  type="button"
                  aria-label="退出登录"
                  onClick={handleLogout}
                >
                  <LogoutOutlined />
                </button>
              </div>
            </div>
          </aside>

          <section className="dashboard-content" aria-label="管理端内容">
            <div className="data-panel">
              {activeNav === 'overview' ? (
                <header className="data-panel-header">
                  <h1>{activeNavItem.label}</h1>
                </header>
              ) : null}
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
                label="手机号"
                name="phone_number"
                rules={[
                  { required: true, message: '请输入手机号' },
                  { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号' },
                ]}
              >
                <Input
                  size="large"
                  autoComplete="username"
                  placeholder="请输入管理员手机号"
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
                loading={loginLoading}
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
