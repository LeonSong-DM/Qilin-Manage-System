import { useEffect, useMemo, useState } from 'react'
import dayjs from 'dayjs'
import 'dayjs/locale/zh-cn'
import Alert from '@mui/material/Alert'
import CircularProgress from '@mui/material/CircularProgress'
import Snackbar from '@mui/material/Snackbar'
import {
  closestCenter,
  DndContext,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
} from '@dnd-kit/core'
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  useSortable,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import { CalendarDays, GripVertical } from 'lucide-react'
import { getOrderReferences } from '../services/businessMeta'
import { getOrders } from '../services/orders'
import { getSchedules } from '../services/schedules'
import './SchedulePage.css'

const scheduleStatusLabels = {
  in_production: '生产中',
  completed: '已完成',
}

function formatScheduleDate(value) {
  const date = dayjs(value)

  return date.isValid() ? date.format('YYYY年MM月DD日') : value
}

function formatWeekday(value) {
  const date = dayjs(value)

  return date.isValid() ? date.format('dddd') : ''
}

function getFriendlyScheduleError(error) {
  const message = error?.message ?? String(error ?? '')

  if (/401|登录|token|认证|过期/i.test(message)) {
    return '登录状态已失效，请重新登录后再试。'
  }

  if (/network|fetch|网络|连接/i.test(message)) {
    return '网络连接异常，排产列表暂时无法加载。'
  }

  return '排产列表加载失败，请稍后重试。'
}

function ScheduleErrorSnackbar({ message, onClose }) {
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

function SortableScheduleCard({ schedule, order, clientName, methodName, unitName }) {
  const {
    attributes,
    isDragging,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({
    id: String(schedule.id),
    data: { scheduleDate: schedule.schedule_date },
  })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  }

  return (
    <article
      ref={setNodeRef}
      className={`schedule-item${isDragging ? ' is-dragging' : ''}`}
      style={style}
    >
      <button
        className="schedule-drag-handle"
        type="button"
        aria-label={`拖动排产 ${schedule.production_schedule_number}`}
        {...attributes}
        {...listeners}
      >
        <GripVertical size={20} strokeWidth={2} />
      </button>
      <div className="schedule-item-order">
        <span className="schedule-item-number">{schedule.production_schedule_number}</span>
        <strong>{order?.order_number ?? `订单 #${schedule.order_id}`}</strong>
        <span>{clientName}</span>
      </div>
      <div className="schedule-item-process">
        <span>处理方式</span>
        <strong>{methodName}</strong>
      </div>
      <div className="schedule-item-quantity">
        <span>排产数量</span>
        <strong>
          {schedule.quantity}
          <em>{unitName}</em>
        </strong>
      </div>
      <span className={`schedule-status schedule-status-${schedule.schedule_status}`}>
        {scheduleStatusLabels[schedule.schedule_status] ?? schedule.schedule_status}
      </span>
    </article>
  )
}

export function SchedulePage() {
  const [schedules, setSchedules] = useState([])
  const [orders, setOrders] = useState([])
  const [references, setReferences] = useState({
    clients: [],
    units: [],
    processMethods: [],
  })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 6 } }),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates }),
  )

  useEffect(() => {
    let ignore = false

    async function loadSchedules() {
      setLoading(true)
      setError('')

      try {
        const [scheduleResult, orderResult, referenceResult] = await Promise.all([
          getSchedules(),
          getOrders({ skip: 0, limit: 100 }),
          getOrderReferences(),
        ])

        if (!ignore) {
          setSchedules(scheduleResult)
          setOrders(orderResult)
          setReferences(referenceResult)
        }
      } catch (loadError) {
        if (!ignore) {
          setError(getFriendlyScheduleError(loadError))
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    loadSchedules()

    return () => {
      ignore = true
    }
  }, [])

  const orderMap = useMemo(
    () => new Map(orders.map((order) => [order.id, order])),
    [orders],
  )
  const clientMap = useMemo(
    () => new Map(references.clients.map((client) => [client.id, client.client_name])),
    [references.clients],
  )
  const unitMap = useMemo(
    () => new Map(references.units.map((unit) => [unit.id, unit.name])),
    [references.units],
  )
  const methodMap = useMemo(
    () =>
      new Map(
        references.processMethods.map((method) => [method.id, method.method_name]),
      ),
    [references.processMethods],
  )

  const groupedSchedules = useMemo(() => {
    const groups = new Map()

    schedules.forEach((schedule) => {
      const currentGroup = groups.get(schedule.schedule_date) ?? []
      currentGroup.push(schedule)
      groups.set(schedule.schedule_date, currentGroup)
    })

    return Array.from(groups.entries()).sort(([left], [right]) =>
      left.localeCompare(right),
    )
  }, [schedules])

  function handleDragEnd({ active, over }) {
    if (!over || active.id === over.id) {
      return
    }

    const activeDate = active.data.current?.scheduleDate
    const overDate = over.data.current?.scheduleDate

    if (!activeDate || activeDate !== overDate) {
      return
    }

    setSchedules((current) => {
      const dateSchedules = current.filter(
        (schedule) => schedule.schedule_date === activeDate,
      )
      const oldIndex = dateSchedules.findIndex((schedule) => String(schedule.id) === active.id)
      const newIndex = dateSchedules.findIndex((schedule) => String(schedule.id) === over.id)

      if (oldIndex < 0 || newIndex < 0) {
        return current
      }

      const reordered = arrayMove(dateSchedules, oldIndex, newIndex)
      let dateIndex = 0

      return current.map((schedule) => {
        if (schedule.schedule_date !== activeDate) {
          return schedule
        }

        return reordered[dateIndex++]
      })
    })
  }

  return (
    <section className="schedule-page" aria-label="排产管理">
      <div className="schedule-page-header">
        <div>
          <span className="schedule-page-eyebrow">生产计划</span>
          <h1>排产管理</h1>
          <p>按日期查看生产安排，拖动卡片调整当天的前端展示顺序。</p>
        </div>
        <div className="schedule-total">
          <strong>{schedules.length}</strong>
          <span>条排产记录</span>
        </div>
      </div>

      {loading ? (
        <div className="schedule-loading">
          <CircularProgress size={24} />
          <span>正在加载排产列表</span>
        </div>
      ) : groupedSchedules.length > 0 ? (
        <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
          <div className="schedule-day-list">
            {groupedSchedules.map(([scheduleDate, daySchedules]) => (
              <section className="schedule-day-section" key={scheduleDate}>
                <header className="schedule-day-header">
                  <div className="schedule-day-title">
                    <CalendarDays size={19} strokeWidth={2.1} />
                    <div>
                      <strong>{formatScheduleDate(scheduleDate)}</strong>
                      <span>{formatWeekday(scheduleDate)}</span>
                    </div>
                  </div>
                  <span>{daySchedules.length} 条安排</span>
                </header>
                <SortableContext
                  items={daySchedules.map((schedule) => String(schedule.id))}
                  strategy={verticalListSortingStrategy}
                >
                  <div className="schedule-day-items">
                    {daySchedules.map((schedule) => {
                      const order = orderMap.get(schedule.order_id)

                      return (
                        <SortableScheduleCard
                          key={schedule.id}
                          schedule={schedule}
                          order={order}
                          clientName={
                            clientMap.get(order?.client_id) ?? `客户 #${order?.client_id ?? '-'}`
                          }
                          methodName={
                            methodMap.get(order?.goods_processing_method_id) ?? '-'
                          }
                          unitName={unitMap.get(order?.goods_unit_id) ?? ''}
                        />
                      )
                    })}
                  </div>
                </SortableContext>
              </section>
            ))}
          </div>
        </DndContext>
      ) : (
        <div className="schedule-empty">
          <CalendarDays size={28} strokeWidth={1.8} />
          <strong>暂无排产记录</strong>
          <span>当前还没有从后端获取到排产安排。</span>
        </div>
      )}

      <ScheduleErrorSnackbar message={error} onClose={() => setError('')} />
    </section>
  )
}
