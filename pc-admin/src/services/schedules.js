import { authHeaders, request } from './http'
import { getStoredToken } from './auth'

export async function getSchedules({ scheduleDate, orderId, status, skip = 0, limit = 100 } = {}) {
  const params = new URLSearchParams({
    skip: String(skip),
    limit: String(limit),
  })

  if (scheduleDate) {
    params.set('schedule_date', scheduleDate)
  }

  if (orderId !== undefined && orderId !== null) {
    params.set('order_id', String(orderId))
  }

  if (status) {
    params.set('schedule_status', status)
  }

  return request(`/schedules/?${params.toString()}`, {
    headers: authHeaders(getStoredToken()),
  })
}
