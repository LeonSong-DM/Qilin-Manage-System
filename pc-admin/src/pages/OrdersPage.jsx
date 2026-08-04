import { useCallback, useEffect, useMemo, useState } from 'react'
import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import CardHeader from '@mui/material/CardHeader'
import Button from '@mui/material/Button'
import FormControlLabel from '@mui/material/FormControlLabel'
import Menu from '@mui/material/Menu'
import MenuItem from '@mui/material/MenuItem'
import Radio from '@mui/material/Radio'
import RadioGroup from '@mui/material/RadioGroup'
import TextField from '@mui/material/TextField'
import { NumberField } from '@base-ui/react/number-field'
import { DataGrid, useGridApiRef } from '@mui/x-data-grid'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { DatePicker } from '@mui/x-date-pickers/DatePicker'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { zhCN } from '@mui/x-date-pickers/locales'
import { ArrowLeft, MapPin, MoreHorizontal, Phone, UserRound } from 'lucide-react'
import { getOrderReferences } from '../services/businessMeta'
import {
  getOrders,
  orderPriorityLabels,
  orderStatusLabels,
  outboundStatusLabels,
  updateOrder,
} from '../services/orders'
import './OrdersPage.css'

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

function formatDate(value) {
  if (!value) {
    return '-'
  }

  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(value))
}

function StatusPill({ children, tone = 'default' }) {
  return <span className={`orders-status-pill orders-status-${tone}`}>{children}</span>
}

function OrderSummaryItem({ label, value, suffix }) {
  return (
    <div className="order-summary-item">
      <span>{label}</span>
      <strong>
        {value ?? '-'}
        {suffix ? <em>{suffix}</em> : null}
      </strong>
    </div>
  )
}

function formatDateInput(value) {
  if (!value) {
    return ''
  }

  const date = dayjs(value)

  return date.isValid() ? date.format('YYYY-MM-DD') : ''
}

function toNullableNumber(value) {
  if (value === '' || value === null || value === undefined) {
    return null
  }

  const numberValue = Number(value)

  return Number.isFinite(numberValue) ? numberValue : null
}

function toRequiredPositiveInteger(value, label) {
  const numberValue = Number(value)

  if (!Number.isInteger(numberValue) || numberValue <= 0) {
    throw new Error(`${label}必须是大于 0 的整数`)
  }

  return numberValue
}

function toOptionalDateTime(value) {
  if (!value) {
    return null
  }

  const dateValue = dayjs(value)

  if (!dateValue.isValid()) {
    throw new Error('交付时间格式不正确')
  }

  return dateValue.format('YYYY-MM-DDTHH:mm:ss')
}

function createOrderForm(order) {
  return {
    client_id: order.client_id,
    goods_processing_method_id: order.goods_processing_method_id,
    goods_processing_option_id: order.goods_processing_option_id ?? '',
    is_closed: order.is_closed ? 'true' : 'false',
    goods_specification_id: order.goods_specification_id,
    goods_quantity: order.goods_quantity,
    goods_unit_id: order.goods_unit_id,
    goods_weight: order.goods_weight,
    order_priority: order.order_priority,
    order_status: order.order_status,
    order_remarks: order.order_remarks ?? '',
    goods_delivery_time: formatDateInput(order.goods_delivery_time),
  }
}

function addChangedValue(payload, field, nextValue, currentValue) {
  if (nextValue !== currentValue) {
    payload[field] = nextValue
  }
}

function buildOrderUpdatePayload(order, form) {
  const payload = {}
  const nextProcessingMethodId = toRequiredPositiveInteger(
    form.goods_processing_method_id,
    '处理方法',
  )
  const nextProcessingOptionId = toNullableNumber(form.goods_processing_option_id)
  const nextIsClosed = form.is_closed === 'true'
  const nextSpecificationId = toRequiredPositiveInteger(
    form.goods_specification_id,
    '规格型号',
  )
  const nextDeliveryDate = form.goods_delivery_time || ''
  const currentDeliveryDate = formatDateInput(order.goods_delivery_time)
  const nextQuantity = toRequiredPositiveInteger(form.goods_quantity, '数量')
  const nextUnitId = toRequiredPositiveInteger(form.goods_unit_id, '单位')
  const nextWeight = toRequiredPositiveInteger(form.goods_weight, '重量')
  const nextRemarks = form.order_remarks || null

  addChangedValue(
    payload,
    'goods_processing_method_id',
    nextProcessingMethodId,
    order.goods_processing_method_id,
  )
  addChangedValue(
    payload,
    'goods_processing_option_id',
    nextProcessingOptionId,
    order.goods_processing_option_id ?? null,
  )
  addChangedValue(payload, 'is_closed', nextIsClosed, order.is_closed)
  addChangedValue(
    payload,
    'goods_specification_id',
    nextSpecificationId,
    order.goods_specification_id,
  )
  if (nextDeliveryDate !== currentDeliveryDate) {
    payload.goods_delivery_time = toOptionalDateTime(nextDeliveryDate)
  }
  addChangedValue(payload, 'goods_quantity', nextQuantity, order.goods_quantity)
  addChangedValue(payload, 'goods_unit_id', nextUnitId, order.goods_unit_id)
  addChangedValue(payload, 'goods_weight', nextWeight, order.goods_weight)
  addChangedValue(payload, 'order_priority', form.order_priority, order.order_priority)
  addChangedValue(payload, 'order_status', form.order_status, order.order_status)
  addChangedValue(payload, 'order_remarks', nextRemarks, order.order_remarks ?? null)

  return payload
}

function DetailField({
  className = '',
  label,
  value,
  type = 'text',
  select = false,
  options = [],
  readonly = false,
  multiline = false,
  onChange,
}) {
  const isWide = className.split(/\s+/).includes('order-detail-item-wide')

  return (
    <div className={`order-detail-item ${className}`}>
      <div>
        <span>{label}</span>
        {readonly ? (
          <strong>{value ?? '-'}</strong>
        ) : (
          <TextField
            className="order-detail-input"
            fullWidth={isWide}
            size="small"
            type={type}
            select={select}
            value={value ?? ''}
            multiline={multiline}
            minRows={multiline ? 2 : undefined}
            onChange={(event) => onChange(event.target.value)}
            slotProps={{
              inputLabel: type === 'datetime-local' ? { shrink: true } : undefined,
            }}
          >
            {options.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
        )}
      </div>
    </div>
  )
}

function NumberEditField({ label, value, min = 1, onChange }) {
  return (
    <div className="order-detail-item">
      <div>
        <span>{label}</span>
        <NumberField.Root
          className="order-number-field"
          min={min}
          step={1}
          value={value === '' ? null : Number(value)}
          onValueChange={(nextValue) => onChange(nextValue ?? '')}
        >
          <NumberField.Group className="order-number-field-group">
            <NumberField.Input className="order-number-field-input" />
            <div className="order-number-field-actions">
              <NumberField.Increment className="order-number-field-button">
                +
              </NumberField.Increment>
              <NumberField.Decrement className="order-number-field-button">
                -
              </NumberField.Decrement>
            </div>
          </NumberField.Group>
        </NumberField.Root>
      </div>
    </div>
  )
}

function BooleanRadioField({ label, value, onChange }) {
  return (
    <div className="order-detail-item">
      <div>
        <span>{label}</span>
        <RadioGroup
          className="order-radio-group"
          row
          value={value}
          onChange={(event) => onChange(event.target.value)}
        >
          <FormControlLabel value="false" control={<Radio size="small" />} label="否" />
          <FormControlLabel value="true" control={<Radio size="small" />} label="是" />
        </RadioGroup>
      </div>
    </div>
  )
}

function DateEditField({ className = '', label, value, onChange }) {
  return (
    <div className={`order-detail-item ${className}`}>
      <div>
        <span>{label}</span>
        <LocalizationProvider
          dateAdapter={AdapterDayjs}
          adapterLocale="zh-cn"
          localeText={zhCN.components.MuiLocalizationProvider.defaultProps.localeText}
        >
          <DatePicker
            className="order-date-picker"
            format="YYYY年MM月DD日"
            value={value ? dayjs(value) : null}
            onChange={(nextValue) =>
              onChange(nextValue?.isValid?.() ? nextValue.format('YYYY-MM-DD') : '')
            }
            slotProps={{
              textField: {
                className: 'order-date-picker',
                size: 'small',
              },
              popper: {
                className: 'order-date-picker-popper',
              },
            }}
          />
        </LocalizationProvider>
      </div>
    </div>
  )
}

function DetailReadRow({ label, value, suffix }) {
  return (
    <div className="order-read-row">
      <span>{label}</span>
      <strong>
        {value ?? '-'}
        {suffix ? <em>{suffix}</em> : null}
      </strong>
    </div>
  )
}

function DetailSection({ className = '', title, children }) {
  return (
    <section className={`order-read-section ${className}`}>
      <h3>{title}</h3>
      <div className="order-read-section-body">{children}</div>
    </section>
  )
}

function ClientReadRow({ icon: Icon, value, emphasis = false }) {
  return (
    <div className={`client-read-row${emphasis ? ' is-emphasis' : ''}`}>
      <Icon size={18} strokeWidth={2.2} aria-hidden="true" />
      <strong>{value ?? '-'}</strong>
    </div>
  )
}

function buildLookup(items, labelKey) {
  return new Map(items.map((item) => [item.id, item[labelKey]]))
}

function buildEntityLookup(items) {
  return new Map(items.map((item) => [item.id, item]))
}

function normalizeOrder(order, references) {
  const client = references.clientEntities.get(order.client_id)

  return {
    ...order,
    client_name:
      order.client_name ??
      references.clients.get(order.client_id) ??
      `客户 #${order.client_id}`,
    client_phone_number:
      order.client_phone_number ?? client?.contact_phone_number ?? '-',
    client_address: order.client_address ?? client?.address ?? '-',
    method_name:
      order.method_name ??
      order.goods_processing_method_name ??
      references.processMethods.get(order.goods_processing_method_id) ??
      `处理方法 #${order.goods_processing_method_id}`,
    option_name:
      order.option_name ??
      order.goods_processing_option_name ??
      (order.goods_processing_option_id
        ? references.processOptions.get(order.goods_processing_option_id) ??
          `处理选项 #${order.goods_processing_option_id}`
        : '-'),
    unit_name:
      order.unit_name ??
      order.goods_unit_name ??
      references.units.get(order.goods_unit_id) ??
      `单位 #${order.goods_unit_id}`,
    order_priority_label: orderPriorityLabels[order.order_priority] ?? order.order_priority,
    order_status_label: orderStatusLabels[order.order_status] ?? order.order_status,
    outbound_status_label:
      outboundStatusLabels[order.outbound_status] ?? order.outbound_status,
  }
}

function blurActiveCell(event) {
  event.defaultMuiPrevented = true

  window.requestAnimationFrame(() => {
    if (document.activeElement instanceof HTMLElement) {
      document.activeElement.blur()
    }
  })
}

function clearGridFocus(api) {
  api.setState((state) => ({
    ...state,
    focus: {
      cell: null,
      columnHeader: null,
      columnHeaderFilter: null,
      columnGroupHeader: null,
    },
    tabIndex: {
      cell: null,
      columnHeader: state.tabIndex.columnHeader,
      columnHeaderFilter: state.tabIndex.columnHeaderFilter,
      columnGroupHeader: state.tabIndex.columnGroupHeader,
    },
  }))
}

export function OrdersPage() {
  const gridApiRef = useGridApiRef()
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [activeMenu, setActiveMenu] = useState(null)
  const [detailOrder, setDetailOrder] = useState(null)
  const [references, setReferences] = useState({
    clients: [],
    units: [],
    processMethods: [],
    processOptions: [],
  })
  const [orderForm, setOrderForm] = useState(null)
  const [editingOrder, setEditingOrder] = useState(false)
  const [saving, setSaving] = useState(false)
  const [saveError, setSaveError] = useState('')

  const activeMenuOpen = Boolean(activeMenu)

  const handleCellClick = useCallback((params, event) => {
    if (params.field === '__check__') {
      window.requestAnimationFrame(() => {
        if (gridApiRef.current) {
          clearGridFocus(gridApiRef.current)
        }

        if (document.activeElement instanceof HTMLElement) {
          document.activeElement.blur()
        }
      })
      return
    }

    blurActiveCell(event)
  }, [gridApiRef])

  const handleTableMouseDownCapture = useCallback((event) => {
    const columnHeader = event.target.closest?.('.MuiDataGrid-columnHeader')

    if (!columnHeader) {
      return
    }

    if (event.target.closest?.('.MuiDataGrid-sortButton')) {
      return
    }

    event.preventDefault()
  }, [])

  useEffect(() => {
    const api = gridApiRef.current

    if (!api?.subscribeEvent) {
      return undefined
    }

    return api.subscribeEvent(
      'cellMouseDown',
      (params, event) => {
        if (params.field === '__check__') {
          return
        }

        event.defaultMuiPrevented = true
        clearGridFocus(api)
      },
      { isFirst: true },
    )
  }, [gridApiRef])

  useEffect(() => {
    const api = gridApiRef.current

    if (!api?.subscribeEvent) {
      return undefined
    }

    return api.subscribeEvent(
      'columnHeaderClick',
      (_, event) => {
        if (event.target?.closest?.('.MuiDataGrid-sortButton')) {
          return
        }

        event.defaultMuiPrevented = true
      },
      { isFirst: true },
    )
  }, [gridApiRef])

  useEffect(() => {
    let ignore = false

    async function loadOrders() {
      setLoading(true)
      setError('')

      try {
        const [result, references] = await Promise.all([
          getOrders({ skip: 0, limit: 100 }),
          getOrderReferences(),
        ])
        const referenceMaps = {
          clients: buildLookup(references.clients, 'client_name'),
          clientEntities: buildEntityLookup(references.clients),
          units: buildLookup(references.units, 'name'),
          processMethods: buildLookup(references.processMethods, 'method_name'),
          processOptions: buildLookup(references.processOptions, 'option_name'),
        }

        if (!ignore) {
          setReferences(references)
          setOrders(result.map((order) => normalizeOrder(order, referenceMaps)))
        }
      } catch (loadError) {
        if (!ignore) {
          setError(loadError.message || '订单数据加载失败')
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    loadOrders()

    return () => {
      ignore = true
    }
  }, [])

  const closeMenu = useCallback(() => {
    setActiveMenu(null)
  }, [])

  const openOrderMenu = useCallback((event, order) => {
    event.stopPropagation()
    setActiveMenu({
      anchorEl: event.currentTarget,
      order,
    })
  }, [])

  const viewOrderDetail = useCallback(() => {
    const order = activeMenu?.order ?? null

    setDetailOrder(order)
    setOrderForm(order ? createOrderForm(order) : null)
    setEditingOrder(false)
    setSaveError('')
    closeMenu()
  }, [activeMenu, closeMenu])

  const referenceMaps = useMemo(
    () => ({
      clients: buildLookup(references.clients, 'client_name'),
      clientEntities: buildEntityLookup(references.clients),
      units: buildLookup(references.units, 'name'),
      processMethods: buildLookup(references.processMethods, 'method_name'),
      processOptions: buildLookup(references.processOptions, 'option_name'),
    }),
    [references],
  )

  const processOptionsForSelectedMethod = useMemo(
    () =>
      references.processOptions.filter(
        (option) => option.process_method_id === orderForm?.goods_processing_method_id,
      ),
    [orderForm?.goods_processing_method_id, references.processOptions],
  )

  const updateFormField = useCallback((field, value) => {
    setOrderForm((current) => {
      const next = {
        ...current,
        [field]: value,
      }

      if (field === 'goods_processing_method_id') {
        next.goods_processing_option_id = ''
      }

      return next
    })
  }, [])

  const saveOrder = useCallback(async () => {
    if (!detailOrder || !orderForm) {
      return
    }

    setSaving(true)
    setSaveError('')

    try {
      const payload = buildOrderUpdatePayload(detailOrder, orderForm)

      if (Object.keys(payload).length === 0) {
        setEditingOrder(false)
        return
      }

      const updatedOrder = await updateOrder(detailOrder.id, payload)
      const normalizedOrder = normalizeOrder(updatedOrder, referenceMaps)

      setDetailOrder(normalizedOrder)
      setOrderForm(createOrderForm(normalizedOrder))
      setEditingOrder(false)
      setOrders((current) =>
        current.map((order) =>
          order.id === normalizedOrder.id ? normalizedOrder : order,
        ),
      )
    } catch (saveOrderError) {
      setSaveError(saveOrderError.message || '订单保存失败')
    } finally {
      setSaving(false)
    }
  }, [detailOrder, orderForm, referenceMaps])

  const columns = useMemo(
    () => {
      const sortableFields = new Set([
        'order_priority',
        'goods_delivery_time',
        'create_at',
      ])

      return [
      {
        field: 'client_name',
        headerName: '客户名称',
        minWidth: 150,
        flex: 1.15,
      },
      {
        field: 'order_priority',
        headerName: '优先级',
        width: 92,
        align: 'center',
        headerAlign: 'center',
        valueFormatter: (value) => orderPriorityLabels[value] ?? value,
        renderCell: (params) => (
          <StatusPill tone={params.value}>{params.row.order_priority_label}</StatusPill>
        ),
      },
      {
        field: 'method_name',
        headerName: '处理方法',
        minWidth: 112,
        flex: 0.85,
      },
      {
        field: 'option_name',
        headerName: '处理选项',
        minWidth: 112,
        flex: 0.85,
        valueGetter: (value) => (value && value !== '-' ? value : '无'),
      },
      {
        field: 'order_remarks',
        headerName: '备注',
        minWidth: 140,
        flex: 1,
        valueGetter: (value) => value || '-',
      },
      {
        field: 'goods_quantity',
        headerName: '数量',
        width: 88,
        type: 'number',
        align: 'right',
        headerAlign: 'right',
      },
      {
        field: 'unit_name',
        headerName: '单位',
        width: 82,
      },
      {
        field: 'order_status',
        headerName: '订单状态',
        width: 112,
        valueFormatter: (value) => orderStatusLabels[value] ?? value,
        renderCell: (params) => params.row.order_status_label,
      },
      {
        field: 'outbound_status',
        headerName: '出库状态',
        width: 118,
        valueFormatter: (value) => outboundStatusLabels[value] ?? value,
        renderCell: (params) => params.row.outbound_status_label,
      },
      {
        field: 'goods_delivery_time',
        headerName: '交付时间',
        minWidth: 160,
        flex: 1,
        valueFormatter: (value) => formatDateTime(value),
      },
      {
        field: 'create_at',
        headerName: '创建时间',
        minWidth: 160,
        flex: 1,
        valueFormatter: (value) => formatDateTime(value),
      },
      {
        field: 'actions',
        headerName: '',
        width: 62,
        align: 'center',
        headerAlign: 'center',
        cellClassName: 'orders-actions-cell',
        disableColumnMenu: true,
        filterable: false,
        renderCell: (params) => (
          <button
            className="orders-row-action"
            type="button"
            aria-label="订单操作"
            onMouseDown={(event) => {
              event.preventDefault()
              event.stopPropagation()
            }}
            onClick={(event) => openOrderMenu(event, params.row)}
          >
            <MoreHorizontal size={18} strokeWidth={2.3} />
          </button>
        ),
      },
    ].map((column) => ({
      ...column,
      sortable: sortableFields.has(column.field),
    }))
    },
    [openOrderMenu],
  )

  if (detailOrder && orderForm) {
    const priorityOptions = Object.entries(orderPriorityLabels).map(([value, label]) => ({
      value,
      label,
    }))
    const orderStatusOptions = Object.entries(orderStatusLabels).map(([value, label]) => ({
      value,
      label,
    }))
    const methodOptions = references.processMethods.map((method) => ({
      value: method.id,
      label: method.method_name,
    }))
    const optionOptions = [
      { value: '', label: '无' },
      ...processOptionsForSelectedMethod.map((option) => ({
        value: option.id,
        label: option.option_name,
      })),
    ]
    const unitOptions = references.units.map((unit) => ({
      value: unit.id,
      label: unit.name,
    }))
    const processOption = detailOrder.option_name === '-' ? '无' : detailOrder.option_name

    return (
      <section className="orders-page" aria-label="订单详情">
        <div className="order-detail-page">
          <div className="order-detail-header">
            <div className="order-detail-back-row">
              <button
                className="order-back-button"
                type="button"
                onClick={() => {
                  setDetailOrder(null)
                  setOrderForm(null)
                  setEditingOrder(false)
                  setSaveError('')
                }}
              >
                <ArrowLeft size={18} strokeWidth={2.4} />
                返回
              </button>
            </div>
            <div className="order-detail-title">
              <span>{detailOrder.order_number}</span>
              <StatusPill tone={detailOrder.order_status}>
                {detailOrder.order_status_label}
              </StatusPill>
            </div>
          </div>

          <Card className="order-summary-card" elevation={0}>
            <CardContent className="order-summary-content">
              <OrderSummaryItem
                label="交付日期"
                value={formatDate(detailOrder.goods_delivery_time)}
              />
              <OrderSummaryItem
                label="数量"
                value={detailOrder.goods_quantity}
                suffix={detailOrder.unit_name}
              />
              <OrderSummaryItem
                label="重量"
                value={detailOrder.goods_weight}
                suffix="kg"
              />
            </CardContent>
          </Card>

          <div className="order-detail-layout">
            <Card className="order-detail-card order-detail-card-main" elevation={0}>
              <CardHeader
                className="order-detail-card-header"
                title="订单信息"
                action={
                  editingOrder ? (
                    <div className="order-detail-actions">
                      <Button
                        className="order-cancel-button"
                        size="small"
                        disabled={saving}
                        onClick={() => {
                          setOrderForm(createOrderForm(detailOrder))
                          setEditingOrder(false)
                          setSaveError('')
                        }}
                      >
                        取消
                      </Button>
                      <Button
                        className="order-save-button"
                        variant="contained"
                        size="small"
                        disabled={saving}
                        onClick={saveOrder}
                      >
                        {saving ? '保存中' : '保存'}
                      </Button>
                    </div>
                  ) : (
                    <button
                      className="order-edit-button"
                      type="button"
                      onClick={() => setEditingOrder(true)}
                    >
                      编辑
                    </button>
                  )
                }
              />
              <CardContent className="order-detail-card-content">
                {saveError ? <div className="orders-error">{saveError}</div> : null}
                {editingOrder ? (
                  <div className="order-detail-grid">
                    <DetailField
                      label="处理方法"
                      select
                      value={orderForm.goods_processing_method_id}
                      options={methodOptions}
                      onChange={(value) =>
                        updateFormField('goods_processing_method_id', Number(value))
                      }
                    />
                    <DetailField
                      label="处理选项"
                      select
                      value={orderForm.goods_processing_option_id}
                      options={optionOptions}
                      onChange={(value) =>
                        updateFormField('goods_processing_option_id', value)
                      }
                    />
                    <BooleanRadioField
                      label="是否封闭"
                      value={orderForm.is_closed}
                      onChange={(value) => updateFormField('is_closed', value)}
                    />
                    <NumberEditField
                      label="规格型号"
                      value={orderForm.goods_specification_id}
                      min={1}
                      onChange={(value) => updateFormField('goods_specification_id', value)}
                    />
                    <NumberEditField
                      label="数量"
                      value={orderForm.goods_quantity}
                      min={1}
                      onChange={(value) => updateFormField('goods_quantity', value)}
                    />
                    <DetailField
                      label="单位"
                      select
                      value={orderForm.goods_unit_id}
                      options={unitOptions}
                      onChange={(value) => updateFormField('goods_unit_id', Number(value))}
                    />
                    <NumberEditField
                      label="重量"
                      value={orderForm.goods_weight}
                      min={1}
                      onChange={(value) => updateFormField('goods_weight', value)}
                    />
                    <DetailField
                      label="优先级"
                      select
                      value={orderForm.order_priority}
                      options={priorityOptions}
                      onChange={(value) => updateFormField('order_priority', value)}
                    />
                    <DetailField
                      label="订单状态"
                      select
                      value={orderForm.order_status}
                      options={orderStatusOptions}
                      onChange={(value) => updateFormField('order_status', value)}
                    />
                    <DateEditField
                      label="交付时间"
                      value={orderForm.goods_delivery_time}
                      onChange={(value) => updateFormField('goods_delivery_time', value)}
                    />
                    <DetailField
                      label="备注"
                      className="order-detail-item-wide"
                      value={orderForm.order_remarks}
                      multiline
                      onChange={(value) => updateFormField('order_remarks', value)}
                    />
                  </div>
                ) : (
                  <div className="order-read-content">
                    <DetailSection title="基础信息">
                      <DetailReadRow label="处理方式" value={detailOrder.method_name} />
                      <DetailReadRow label="处理选项" value={processOption} />
                      <DetailReadRow label="规格型号" value={detailOrder.goods_specification_id} />
                      <DetailReadRow label="数量" value={detailOrder.goods_quantity} />
                      <DetailReadRow label="单位" value={detailOrder.unit_name} />
                      <DetailReadRow label="重量" value={detailOrder.goods_weight} suffix="kg" />
                      <DetailReadRow label="是否封闭" value={detailOrder.is_closed ? '是' : '否'} />
                      <DetailReadRow label="优先级" value={detailOrder.order_priority_label} />
                    </DetailSection>

                    <DetailSection title="状态">
                      <DetailReadRow label="订单状态" value={detailOrder.order_status_label} />
                      <DetailReadRow label="出库状态" value={detailOrder.outbound_status_label} />
                      <DetailReadRow label="剩余数量" value={detailOrder.goods_remaining_quantity} />
                    </DetailSection>

                    <DetailSection title="备注" className="order-read-section-wide">
                      <p className="order-read-note">{detailOrder.order_remarks || '-'}</p>
                    </DetailSection>

                    <DetailSection title="时间">
                      <DetailReadRow label="交付时间" value={formatDateTime(detailOrder.goods_delivery_time)} />
                      <DetailReadRow label="创建时间" value={formatDateTime(detailOrder.create_at)} />
                    </DetailSection>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card className="order-detail-card order-detail-card-client" elevation={0}>
              <CardHeader
                className="order-detail-card-header"
                title="客户信息"
              />
              <CardContent className="order-detail-card-content">
                <div className="client-read-list">
                  <ClientReadRow icon={UserRound} value={detailOrder.client_name} />
                  <ClientReadRow
                    icon={Phone}
                    value={detailOrder.client_phone_number}
                    emphasis
                  />
                  <ClientReadRow icon={MapPin} value={detailOrder.client_address} />
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className="orders-page" aria-label="订单列表">
      <div className="orders-table-shell" onMouseDownCapture={handleTableMouseDownCapture}>
        <div className="orders-table-header">
          <div>
            <span>订单管理</span>
            <strong>{orders.length}</strong>
          </div>
        </div>

        {error ? <div className="orders-error">{error}</div> : null}

        <DataGrid
          apiRef={gridApiRef}
          className="orders-data-grid"
          columns={columns}
          rows={orders}
          loading={loading}
          showToolbar
          checkboxSelection
          cellSelection={false}
          disableColumnMenu
          disableRowSelectionOnClick
          onCellClick={handleCellClick}
          sortingOrder={['asc', 'desc']}
          getRowClassName={(params) =>
            params.indexRelativeToCurrentPage % 2 === 0
              ? 'orders-row-even'
              : 'orders-row-odd'
          }
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
          }}
        />

        <Menu
          anchorEl={activeMenu?.anchorEl}
          open={activeMenuOpen}
          onClose={closeMenu}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
          transformOrigin={{ vertical: 'top', horizontal: 'right' }}
          slotProps={{
            paper: {
              className: 'orders-action-menu',
            },
          }}
        >
          <MenuItem disabled onClick={closeMenu}>
            加入排产
          </MenuItem>
          <MenuItem onClick={viewOrderDetail}>查看详情</MenuItem>
        </Menu>
      </div>
    </section>
  )
}
