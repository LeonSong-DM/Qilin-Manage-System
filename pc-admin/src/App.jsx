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
import dataViewLeft from './assets/data_view_left.jpg'
import dataViewRight from './assets/data_view_right.jpg'
import { OrdersPage } from './pages/OrdersPage'
import { clearAuth, getCurrentUser, login, storeAuth } from './services/auth'
import { AUTH_EXPIRED_EVENT } from './services/http'
import './App.css'

const navItems = [
  { key: 'overview', label: '数据概览', icon: <AppstoreOutlined /> },
  { key: 'orders', label: '客户订单', icon: <FileTextOutlined /> },
  { key: 'schedule', label: '排产管理', icon: <CalendarOutlined /> },
  { key: 'outbound', label: '出库记录', icon: <TruckOutlined /> },
  { key: 'information', label: '信息管理', icon: <ControlOutlined /> },
]

const kpiMetrics = [
  {
    key: 'orders',
    title: '订单数量',
    value: '128',
    trend: '+12.8%',
    tone: 'violet',
    sparkline: '4,42 22,34 40,38 58,24 76,28 94,14 112,18',
  },
  {
    key: 'clients',
    title: '客户数量',
    value: '46',
    trend: '+8.4%',
    tone: 'blue',
    sparkline: '4,38 22,30 40,34 58,22 76,26 94,18 112,12',
  },
  {
    key: 'schedules',
    title: '排产订单',
    value: '32',
    trend: '+5.6%',
    tone: 'green',
    sparkline: '4,40 22,36 40,28 58,32 76,18 94,22 112,10',
  },
  {
    key: 'outbound',
    title: '出库记录',
    value: '87',
    trend: '+9.1%',
    tone: 'rose',
    sparkline: '4,36 22,40 40,26 58,30 76,20 94,16 112,8',
  },
]

function Sparkline({ points }) {
  return (
    <svg className="kpi-sparkline" viewBox="0 0 116 48" aria-hidden="true">
      <polyline points={points} />
    </svg>
  )
}

function TrendValue({ value }) {
  const sign = value.slice(0, 1)
  const percentage = value.endsWith('%') ? value.slice(1, -1) : value.slice(1)

  return (
    <div className="kpi-card-trend">
      <span>{sign}</span>
      <strong>{percentage}</strong>
      <em>%</em>
    </div>
  )
}

function App() {
  const [currentUser, setCurrentUser] = useState(null)
  const [activeNav, setActiveNav] = useState(navItems[0].key)
  const [loginLoading, setLoginLoading] = useState(false)
  const [authChecking, setAuthChecking] = useState(true)

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

  useEffect(() => {
    function handleAuthExpired() {
      clearAuth()
      setCurrentUser(null)
      setActiveNav(navItems[0].key)
      message.warning('登录已过期，请重新登录')
    }

    window.addEventListener(AUTH_EXPIRED_EVENT, handleAuthExpired)

    return () => {
      window.removeEventListener(AUTH_EXPIRED_EVENT, handleAuthExpired)
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
              <div className="data-panel-inner">
                {activeNav === 'overview' ? (
                  <>
                    <div className="overview-image-row">
                      <figure className="overview-image-card overview-image-card-left">
                        <img src={dataViewLeft} alt="金属件生产展示" />
                        <figcaption className="overview-image-mask">
                          <strong>Welcome Back</strong>
                          <span>{currentUser?.name}</span>
                        </figcaption>
                      </figure>
                      <figure className="overview-image-card overview-image-card-right">
                        <img src={dataViewRight} alt="金属材料展示" />
                      </figure>
                    </div>

                    <section className="kpi-card-grid" aria-label="核心指标">
                      {kpiMetrics.map((metric) => (
                        <article
                          className={`kpi-card kpi-card-${metric.tone}`}
                          key={metric.key}
                        >
                          <div className="kpi-card-main">
                            <span className="kpi-card-title">{metric.title}</span>
                            <div className="kpi-card-value-row">
                              <strong className="kpi-card-value">{metric.value}</strong>
                              <TrendValue value={metric.trend} />
                            </div>
                          </div>
                          <div className="kpi-chart-area">
                            <Sparkline points={metric.sparkline} />
                          </div>
                        </article>
                      ))}
                    </section>
                  </>
                ) : null}
                {activeNav === 'orders' ? <OrdersPage /> : null}
              </div>
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
