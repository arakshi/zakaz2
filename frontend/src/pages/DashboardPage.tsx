import { useEffect, useState } from 'react'
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { apiClient } from '../api/client'
import { FiltersBar } from '../components/FiltersBar'
import { KpiCard } from '../components/KpiCard'
import { OverviewResponse } from '../types'

const fallbackData = Array.from({ length: 14 }).map((_, idx) => ({ day: `${idx + 1}`, revenue: 50000 + idx * 3500 }))

export function DashboardPage() {
  const [overview, setOverview] = useState<OverviewResponse | null>(null)

  const load = async () => {
    try {
      const res = await apiClient.get<OverviewResponse>('/analytics/overview', {
        params: { date_from: '2026-01-01', date_to: '2026-01-31' }
      })
      setOverview(res.data)
    } catch {
      setOverview({ current: { revenue: 1450000, orders: 520, conversion: 0.052, romi: 1.72 }, previous: {}, comments: ['Демо-режим активен'] })
    }
  }

  useEffect(() => {
    void load()
  }, [])

  return (
    <section>
      <FiltersBar onRefresh={load} />
      <div className="kpi-grid">
        <KpiCard title="Выручка" value={`${overview?.current.revenue ?? 0} ₽`} />
        <KpiCard title="Заказы" value={`${overview?.current.orders ?? 0}`} />
        <KpiCard title="Конверсия" value={`${((overview?.current.conversion ?? 0) * 100).toFixed(2)} %`} />
        <KpiCard title="ROMI" value={`${overview?.current.romi ?? 0}`} />
      </div>
      <div className="chart-card">
        <h3>Динамика выручки</h3>
        <ResponsiveContainer width="100%" height={280}>
          <LineChart data={fallbackData}>
            <XAxis dataKey="day" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="revenue" stroke="#4f8cff" strokeWidth={3} />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className="comments">
        <h3>Автокомментарии</h3>
        <ul>
          {(overview?.comments || []).map((comment) => (
            <li key={comment}>{comment}</li>
          ))}
        </ul>
      </div>
    </section>
  )
}
