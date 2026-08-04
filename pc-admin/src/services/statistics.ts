import { http } from './http'

export interface StatisticsOverview {
  total_orders: number
  total_clients: number
  total_production_schedules: number
  total_outbound_records: number
  scheduling_orders: number
  finished_orders: number
  not_outbound_orders: number
  partially_outbound_orders: number
  fully_outbound_orders: number
  in_production_schedules: number
  completed_schedules: number
  pending_harvest_orders: number
  total_order_quantity: number
  total_remaining_quantity: number
  total_outbound_quantity: number
  total_outbound_weight: number
}

export interface CountMetric {
  name: string
  count: number
}

export interface StatisticsDistribution {
  order_status: CountMetric[]
  outbound_status: CountMetric[]
  order_priority: CountMetric[]
  schedule_status: CountMetric[]
}

export async function getStatisticsOverview() {
  const response = await http.get<StatisticsOverview>('/statistics/overview')
  return response.data
}

export async function getStatisticsDistribution() {
  const response = await http.get<StatisticsDistribution>(
    '/statistics/distributions',
  )
  return response.data
}
