import { useState } from 'react'
import { App as AntdApp, ConfigProvider } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import { BasicLayout } from './layouts/BasicLayout'
import { LoginPage } from './pages/LoginPage'
import { OverviewPage } from './pages/OverviewPage'
import { clearAuth, getStoredUser } from './services/authStorage'
import './styles/global.css'

function App() {
  const [user, setUser] = useState(() => getStoredUser())

  const handleLogout = () => {
    clearAuth()
    setUser(null)
  }

  return (
    <ConfigProvider
      locale={zhCN}
      theme={{
        token: {
          colorPrimary: '#4B3D4F',
          borderRadius: 8,
          fontFamily:
            '"Noto Sans SC", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
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
      <AntdApp>
        {user?.role === 'admin' ? (
          <BasicLayout user={user} onLogout={handleLogout}>
            <OverviewPage />
          </BasicLayout>
        ) : (
          <LoginPage onLogin={setUser} />
        )}
      </AntdApp>
    </ConfigProvider>
  )
}

export default App
