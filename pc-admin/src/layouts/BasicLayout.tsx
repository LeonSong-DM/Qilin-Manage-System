import {
  AppstoreOutlined,
  CalendarOutlined,
  ControlOutlined,
  FileTextOutlined,
  LogoutOutlined,
  TruckOutlined,
  UserOutlined,
} from '@ant-design/icons'
import type { MenuDataItem } from '@ant-design/pro-components'
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
      fixSiderbar
      fixedHeader
      layout="mix"
      location={{ pathname: '/overview' }}
      menu={{
        type: 'group',
      }}
      menuItemRender={(item: MenuDataItem, dom) => (
        <button
          className="layout-menu-button"
          type="button"
          onClick={() => {
            if (item.path !== '/overview') {
              return
            }
          }}
        >
          {dom}
        </button>
      )}
      route={route}
      title="骐临电镀生产管理系统"
      token={{
        bgLayout: '#F5F6F8',
        colorBgAppListIconHover: '#EFECEF',
        colorPrimary: '#4B3D4F',
        sider: {
          colorBgMenuItemSelected: '#FFFFFF',
          colorMenuBackground: '#4B3D4F',
          colorTextMenu: 'rgba(255, 255, 255, 0.82)',
          colorTextMenuActive: '#111827',
          colorTextMenuSelected: '#111827',
        },
      }}
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
