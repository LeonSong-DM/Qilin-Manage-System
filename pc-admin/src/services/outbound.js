import { authHeaders, request } from './http'
import { getStoredToken } from './auth'

export async function getOutboundRecords(orderId, { skip = 0, limit = 100 } = {}) {
  const params = new URLSearchParams({
    skip: String(skip),
    limit: String(limit),
  })

  return request(`/orders/${orderId}/outbound-records/?${params.toString()}`, {
    headers: authHeaders(getStoredToken()),
  })
}
