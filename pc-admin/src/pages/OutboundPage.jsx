import { useEffect, useMemo, useState } from 'react'
import Alert from '@mui/material/Alert'
import Snackbar from '@mui/material/Snackbar'
import {
  DataGrid,
  GridToolbarColumnsButton,
  GridToolbarContainer,
  GridToolbarDensitySelector,
  GridToolbarExport,
  GridToolbarQuickFilter,
} from '@mui/x-data-grid'
import { getOrderReferences, getUsers } from '../services/businessMeta'
import { getOrders } from '../services/orders'
import { getOutboundRecords } from '../services/outbound'
import './OutboundPage.css'

function formatDateTime(value) {
  if (!value) {
    return '-'
  }

  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

function getFriendlyOutboundError(error) {
  const message = error?.message ?? String(error ?? '')

  if (/401|登录|token|认证|过期/i.test(message)) {
    return '登录状态已失效，请重新登录后再试。'
  }

  if (/network|fetch|网络|连接/i.test(message)) {
    return '网络连接异常，出库记录暂时无法加载。'
  }

  return '出库记录加载失败，请稍后重试。'
}

function OutboundErrorSnackbar({ message, onClose }) {
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

function OutboundToolbar() {
  return (
    <div className="orders-grid-toolbar outbound-grid-toolbar">
      <GridToolbarContainer>
        <GridToolbarColumnsButton />
        <GridToolbarDensitySelector />
        <GridToolbarExport />
        <GridToolbarQuickFilter />
      </GridToolbarContainer>
    </div>
  )
}

export function OutboundPage() {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let ignore = false

    async function loadOutboundRecords() {
      setLoading(true)
      setError('')

      try {
        const [orders, references, users] = await Promise.all([
          getOrders({ skip: 0, limit: 100 }),
          getOrderReferences(),
          getUsers(),
        ])
        const outboundOrders = orders.filter((order) => order.outbound_status !== 'not_outbound')
        const userMap = new Map(users.map((user) => [user.id, user.name]))
        const recordResults = await Promise.all(
          outboundOrders.map(async (order) => {
            const records = await getOutboundRecords(order.id)

            return records.map((record) => ({
              ...record,
              order_number: order.order_number ?? `订单 #${order.id}`,
              client_name:
                references.clients.find((client) => client.id === order.client_id)
                  ?.client_name ?? `客户 #${order.client_id}`,
              created_by_name: userMap.get(record.created_by) ?? `用户 #${record.created_by}`,
            }))
          }),
        )

        if (!ignore) {
          setRows(recordResults.flat())
        }
      } catch (loadError) {
        if (!ignore) {
          setError(getFriendlyOutboundError(loadError))
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    loadOutboundRecords()

    return () => {
      ignore = true
    }
  }, [])

  const columns = useMemo(
    () => [
      {
        field: 'outbound_number',
        headerName: '出库编号',
        minWidth: 178,
        flex: 1.1,
      },
      {
        field: 'order_number',
        headerName: '订单编号',
        minWidth: 178,
        flex: 1.1,
      },
      {
        field: 'client_name',
        headerName: '客户名称',
        minWidth: 150,
        flex: 1,
      },
      {
        field: 'created_by_name',
        headerName: '出库人',
        minWidth: 110,
        flex: 0.7,
      },
      {
        field: 'outbound_quantity',
        headerName: '出库数量',
        width: 112,
        type: 'number',
        align: 'right',
        headerAlign: 'right',
      },
      {
        field: 'outbound_weight',
        headerName: '出库重量',
        width: 112,
        type: 'number',
        align: 'right',
        headerAlign: 'right',
        valueFormatter: (value) => `${value ?? '-'} kg`,
      },
      {
        field: 'create_at',
        headerName: '出库时间',
        minWidth: 170,
        flex: 1,
        sortable: true,
        valueFormatter: (value) => formatDateTime(value),
      },
    ],
    [],
  )

  return (
    <section className="orders-page outbound-page" aria-label="出库记录">
      <div className="orders-table-shell outbound-table-shell">
        <DataGrid
          className="orders-data-grid"
          columns={columns}
          rows={rows}
          loading={loading}
          showToolbar
          slots={{ toolbar: OutboundToolbar }}
          checkboxSelection
          disableColumnMenu
          disableRowSelectionOnClick
          rowHeight={54}
          columnHeaderHeight={48}
          pageSizeOptions={[10, 25, 50, 100]}
          initialState={{
            pagination: {
              paginationModel: {
                pageSize: 10,
                page: 0,
              },
            },
            sorting: {
              sortModel: [{ field: 'create_at', sort: 'desc' }],
            },
          }}
        />
      </div>
      <OutboundErrorSnackbar message={error} onClose={() => setError('')} />
    </section>
  )
}
