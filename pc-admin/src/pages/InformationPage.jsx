import { useEffect, useMemo, useState } from 'react'
import Alert from '@mui/material/Alert'
import Snackbar from '@mui/material/Snackbar'
import { Box, Form, Tabs, UIProvider } from '@yamada-ui/react'
import { BriefcaseBusiness, Cog, Users, Wrench } from 'lucide-react'
import {
  getOrderReferences,
  getUnits,
  getUsers,
} from '../services/businessMeta'
import './InformationPage.css'

const tabs = [
  { key: 'users', label: '员工信息', icon: Users },
  { key: 'units', label: '单位信息', icon: BriefcaseBusiness },
  { key: 'methods', label: '处理方法', icon: Wrench },
  { key: 'options', label: '处理项', icon: Cog },
]

function getFriendlyInformationError(error) {
  const message = error?.message ?? String(error ?? '')

  if (/401|登录|token|认证|过期/i.test(message)) {
    return '登录状态已失效，请重新登录后再试。'
  }

  if (/network|fetch|网络|连接/i.test(message)) {
    return '网络连接异常，信息管理数据暂时无法加载。'
  }

  return '信息管理数据加载失败，请稍后重试。'
}

function InformationErrorSnackbar({ message, onClose }) {
  return (
    <Snackbar
      open={Boolean(message)}
      autoHideDuration={3000}
      onClose={onClose}
      anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
    >
      <Alert onClose={onClose} severity="error" variant="filled" sx={{ width: '100%' }}>
        {message}
      </Alert>
    </Snackbar>
  )
}

function InformationForm({ className = '', title, children }) {
  return (
    <Form.Root className={`information-form ${className}`.trim()} readOnly>
      <Form.Header>
        <div className="information-form-heading">
          <div>
            <Form.Title>{title}</Form.Title>
          </div>
        </div>
      </Form.Header>
      <Form.Body>
        <Form.Group className="information-record-list">{children}</Form.Group>
      </Form.Body>
    </Form.Root>
  )
}

function InformationTable({ headers, rows }) {
  return (
    <div className="information-table-wrap">
      <table>
        <thead>
          <tr>
            {headers.map((header) => (
              <th key={header}>{header}</th>
            ))}
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  )
}

function UsersPanel({ users }) {
  return (
    <InformationForm
      className="information-form-users"
      title="员工列表"
    >
      <InformationTable
        headers={['员工编号', '姓名', '联系电话', '角色', '状态']}
        rows={users.map((user) => (
          <tr key={user.id}>
            <td>{user.user_number}</td>
            <td className="information-employee-name">{user.name}</td>
            <td>{user.phone_number}</td>
            <td>{user.role === 'admin' ? '管理员' : '员工'}</td>
            <td>
              <span
                className={`information-user-status information-user-status-${user.status}`}
              >
                {user.status === 'normal' ? '正常' : '已禁用'}
              </span>
            </td>
          </tr>
        ))}
      />
    </InformationForm>
  )
}

function UnitsPanel({ units }) {
  return (
    <InformationForm
      title="单位信息"
    >
      <InformationTable
        headers={['单位名称', '单位编号']}
        rows={units.map((unit) => (
          <tr key={unit.id}>
            <td className="information-primary-cell">{unit.name}</td>
            <td>{unit.id}</td>
          </tr>
        ))}
      />
    </InformationForm>
  )
}

function MethodsPanel({ methods }) {
  return (
    <InformationForm
      title="处理方法"
    >
      <InformationTable
        headers={['处理方法', '方法编号']}
        rows={methods.map((method) => (
          <tr key={method.id}>
            <td className="information-primary-cell">{method.method_name}</td>
            <td>{method.id}</td>
          </tr>
        ))}
      />
    </InformationForm>
  )
}

function OptionsPanel({ options, methodMap }) {
  return (
    <InformationForm
      title="处理项"
    >
      <InformationTable
        headers={['处理项', '所属处理方法', '处理项编号']}
        rows={options.map((option) => (
          <tr key={option.id}>
            <td className="information-primary-cell">{option.option_name}</td>
            <td>{methodMap.get(option.process_method_id) ?? '-'}</td>
            <td>{option.id}</td>
          </tr>
        ))}
      />
    </InformationForm>
  )
}

export function InformationPage() {
  const [activeTab, setActiveTab] = useState(0)
  const [users, setUsers] = useState([])
  const [units, setUnits] = useState([])
  const [methods, setMethods] = useState([])
  const [options, setOptions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const methodMap = useMemo(
    () => new Map(methods.map((method) => [method.id, method.method_name])),
    [methods],
  )

  useEffect(() => {
    let ignore = false

    async function loadInformation() {
      setLoading(true)
      setError('')

      try {
        const [userResult, unitResult, references] = await Promise.all([
          getUsers(),
          getUnits(),
          getOrderReferences(),
        ])

        if (!ignore) {
          setUsers(userResult)
          setUnits(unitResult)
          setMethods(references.processMethods)
          setOptions(references.processOptions)
        }
      } catch (loadError) {
        if (!ignore) {
          setError(getFriendlyInformationError(loadError))
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    loadInformation()

    return () => {
      ignore = true
    }
  }, [])

  const panels = [
    <UsersPanel key="users" users={users} />,
    <UnitsPanel key="units" units={units} />,
    <MethodsPanel key="methods" methods={methods} />,
    <OptionsPanel key="options" options={options} methodMap={methodMap} />,
  ]

  return (
    <section className="information-page" aria-label="信息管理">
      <div className="information-page-header">
        <div>
          <h1>信息管理</h1>
        </div>
      </div>

      <UIProvider colorMode="light">
        <Tabs.Root
          className="information-tabs-root"
          index={activeTab}
          onChange={setActiveTab}
          lazy
        >
          <Tabs.List className="information-tabs-list">
            {tabs.map(({ key, label, icon: Icon }, index) => (
              <Tabs.Tab className="information-tab" key={key} index={index}>
                <Icon size={17} strokeWidth={2.1} />
                <span>{label}</span>
              </Tabs.Tab>
            ))}
          </Tabs.List>
          <Tabs.Panels className="information-tabs-panels">
            {loading ? (
              <Box className="information-loading">
                <span className="information-loading-spinner" aria-hidden="true" />
                <span>正在加载基础信息</span>
              </Box>
            ) : (
              panels.map((panel, index) => (
                <Tabs.Panel className="information-tab-panel" key={tabs[index].key} index={index}>
                  {panel}
                </Tabs.Panel>
              ))
            )}
          </Tabs.Panels>
        </Tabs.Root>
      </UIProvider>
      <InformationErrorSnackbar message={error} onClose={() => setError('')} />
    </section>
  )
}
