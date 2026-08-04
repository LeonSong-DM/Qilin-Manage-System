import { useEffect, useState } from 'react'
import {
  BarChartOutlined,
  FileTextOutlined,
  ScheduleOutlined,
  TeamOutlined,
  TruckOutlined,
} from '@ant-design/icons'
import { ProCard, StatisticCard } from '@ant-design/pro-components'
import { Alert, App, Skeleton } from 'antd'
import {
  type StatisticsDistribution,
  type StatisticsOverview,
  getStatisticsDistribution,
  getStatisticsOverview,
} from '../services/statistics'
import './OverviewPage.css'

const statusLabels: Record<string, string> = {
  scheduling: '待排产',
  finished: '已完成',
  not_outbound: '未出库',
  partially_outbound: '部分出库',
  fully_outbound: '已出库',
  in_production: '生产中',
  completed: '已生产',
  p0: 'P0',
  p1: 'P1',
  p2: 'P2',
  p3: 'P3',
}

function getMetricLabel(name: string) {
  return statusLabels[name] ?? name
}

export function OverviewPage() {
  const { message } = App.useApp()
  const [overview, setOverview] = useState<StatisticsOverview | null>(null)
  const [distribution, setDistribution] =
    useState<StatisticsDistribution | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadStatistics() {
      try {
        const [overviewResult, distributionResult] = await Promise.all([
          getStatisticsOverview(),
          getStatisticsDistribution(),
        ])
        setOverview(overviewResult)
        setDistribution(distributionResult)
      } catch {
        message.error('统计数据加载失败')
      } finally {
        setLoading(false)
      }
    }

    loadStatistics()
  }, [message])

  if (loading) {
    return <Skeleton active paragraph={{ rows: 8 }} />
  }

  if (!overview || !distribution) {
    return <Alert message="暂无统计数据" type="warning" />
  }

  return (
    <div className="overview-page">
      <ProCard gutter={16} wrap>
        <StatisticCard
          colSpan={{ xs: 24, sm: 12, lg: 6 }}
          statistic={{
            icon: <FileTextOutlined />,
            title: '订单数量',
            value: overview.total_orders,
          }}
        />
        <StatisticCard
          colSpan={{ xs: 24, sm: 12, lg: 6 }}
          statistic={{
            icon: <TeamOutlined />,
            title: '客户数量',
            value: overview.total_clients,
          }}
        />
        <StatisticCard
          colSpan={{ xs: 24, sm: 12, lg: 6 }}
          statistic={{
            icon: <ScheduleOutlined />,
            title: '排产订单',
            value: overview.total_production_schedules,
          }}
        />
        <StatisticCard
          colSpan={{ xs: 24, sm: 12, lg: 6 }}
          statistic={{
            icon: <TruckOutlined />,
            title: '出库记录',
            value: overview.total_outbound_records,
          }}
        />
      </ProCard>

      <ProCard gutter={16} wrap>
        <StatisticCard
          colSpan={{ xs: 24, md: 8 }}
          statistic={{
            title: '待排产订单',
            value: overview.scheduling_orders,
          }}
        />
        <StatisticCard
          colSpan={{ xs: 24, md: 8 }}
          statistic={{
            title: '生产中排产',
            value: overview.in_production_schedules,
          }}
        />
        <StatisticCard
          colSpan={{ xs: 24, md: 8 }}
          statistic={{
            title: '待回收单据',
            value: overview.pending_harvest_orders,
          }}
        />
      </ProCard>

      <ProCard gutter={16} wrap>
        <StatisticCard
          colSpan={{ xs: 24, md: 8 }}
          statistic={{
            title: '订单总数量',
            value: overview.total_order_quantity,
          }}
        />
        <StatisticCard
          colSpan={{ xs: 24, md: 8 }}
          statistic={{
            title: '剩余数量',
            value: overview.total_remaining_quantity,
          }}
        />
        <StatisticCard
          colSpan={{ xs: 24, md: 8 }}
          statistic={{
            title: '出库重量',
            value: overview.total_outbound_weight,
          }}
        />
      </ProCard>

      <ProCard
        className="distribution-panel"
        title={
          <span>
            <BarChartOutlined /> 状态分布
          </span>
        }
      >
        <div className="distribution-grid">
          {distribution.order_status.map((item) => (
            <div className="distribution-item" key={`order-${item.name}`}>
              <span>{getMetricLabel(item.name)}</span>
              <strong>{item.count}</strong>
            </div>
          ))}
          {distribution.outbound_status.map((item) => (
            <div className="distribution-item" key={`outbound-${item.name}`}>
              <span>{getMetricLabel(item.name)}</span>
              <strong>{item.count}</strong>
            </div>
          ))}
        </div>
      </ProCard>
    </div>
  )
}
