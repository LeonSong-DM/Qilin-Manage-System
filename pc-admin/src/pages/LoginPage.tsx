import { LockOutlined, LoginOutlined, UserOutlined } from '@ant-design/icons'
import { App, Button, Checkbox, Form, Input } from 'antd'
import type { AxiosError } from 'axios'
import { login } from '../services/auth'
import { type CurrentUser, storeAuth } from '../services/authStorage'
import './LoginPage.css'

interface LoginFormValues {
  phone_number: string
  password: string
  remember: boolean
}

interface ErrorResponse {
  detail?: string
  message?: string
}

interface LoginPageProps {
  onLogin: (user: CurrentUser) => void
}

function getErrorMessage(error: unknown) {
  const axiosError = error as AxiosError<ErrorResponse>
  return (
    axiosError.response?.data?.detail ??
    axiosError.response?.data?.message ??
    '登录失败，请检查账号和密码'
  )
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const { message } = App.useApp()

  const handleLogin = async (values: LoginFormValues) => {
    try {
      const result = await login({
        phone_number: values.phone_number,
        password: values.password,
      })

      if (result.user.role !== 'admin') {
        message.error('PC 管理端只允许管理员登录')
        return
      }

      storeAuth(result.token, result.user)
      onLogin(result.user)
    } catch (error) {
      message.error(getErrorMessage(error))
    }
  }

  return (
    <main className="login-page">
      <div className="login-bg" aria-hidden="true" />

      <aside className="login-card" aria-label="登录表单">
        <div className="login-card-header">
          <p className="system-title">骐临电镀生产管理系统</p>
          <h1>Welcome Back</h1>
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
              placeholder="请输入密码"
              prefix={<LockOutlined />}
            />
          </Form.Item>

          <div className="form-row">
            <Form.Item name="remember" valuePropName="checked" noStyle>
              <Checkbox>记住登录状态</Checkbox>
            </Form.Item>
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
  )
}
