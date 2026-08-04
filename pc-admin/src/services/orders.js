import { authHeaders, request } from './http'
import { getStoredToken } from './auth'

export const orderPriorityLabels = {
  p0: 'P0',
  p1: 'P1',
  p2: 'P2',
  p3: 'P3',
}

export const orderStatusLabels = {
  scheduling: '待排产',
  finished: '已完成',
}

export const outboundStatusLabels = {
  not_outbound: '未出库',
  partially_outbound: '部分出库',
  fully_outbound: '已出库',
}

export async function getOrders({ skip = 0, limit = 100 } = {}) {
  const params = new URLSearchParams({
    skip: String(skip),
    limit: String(limit),
  })

  return request(`/orders/?${params.toString()}`, {
    headers: authHeaders(getStoredToken()),
  })
}

export async function updateOrder(orderId, payload) {
  return request(`/orders/${orderId}`, {
    method: 'PATCH',
    headers: authHeaders(getStoredToken()),
    body: JSON.stringify(payload),
  })
}
