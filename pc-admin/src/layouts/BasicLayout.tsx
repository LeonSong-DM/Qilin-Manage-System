import {
  AppstoreOutlined,
  CalendarOutlined,
  ControlOutlined,
  FileTextOutlined,
  LogoutOutlined,
  TruckOutlined,
  UserOutlined,
} from '@ant-design/icons'
import { PageContainer, ProLayout } from '@ant-design/pro-components'
import { Button } from 'antd'
import type { ReactNode } from 'react'
import type { CurrentUser } from '../services/authStorage'

const route = {
  path: '/',
  routes: [
    {
      path: '/overview',
      name: '数据概览',
      icon: <AppstoreOutlined />,
    },
    {
      path: '/orders',
      name: '客户订单',
      icon: <FileTextOutlined />,
    },
    {
      path: '/schedules',
      name: '排产管理',
      icon: <CalendarOutlined />,
    },
    {
      path: '/outbound',
      name: '出库记录',
      icon: <TruckOutlined />,
    },
    {
      path: '/business',
      name: '基础信息',
      icon: <ControlOutlined />,
    },
  ],
}

interface BasicLayoutProps {
  children: ReactNode
  user: CurrentUser
  onLogout: () => void
}

export function BasicLayout({ children, user, onLogout }: BasicLayoutProps) {
  return (
    <ProLayout
      colorPrimary="#1677FF"
      contentWidth="Fluid"
      fixSiderbar
      fixedHeader
      layout="side"
      logo="https://gw.alipayobjects.com/zos/rmsportal/KDpgvguMpGfqaHPjicRK.svg"
      location={{ pathname: '/overview' }}
      menu={{
        type: 'sub',
      }}
      navTheme="light"
      route={route}
      splitMenus={false}
      title="骐临电镀生产管理系统"
      avatarProps={{
        icon: <UserOutlined />,
        title: user?.name ?? '管理员',
        render: (_, dom) => (
          <div className="layout-user">
            {dom}
            <Button
              aria-label="退出登录"
              icon={<LogoutOutlined />}
              shape="circle"
              type="text"
              onClick={onLogout}
            />
          </div>
        ),
      }}
    >
      <PageContainer ghost title={false}>
        {children}
      </PageContainer>
    </ProLayout>
  )
}
