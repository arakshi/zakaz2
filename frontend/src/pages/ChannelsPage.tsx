import { useEffect, useState } from 'react'
import { Bar, BarChart, CartesianGrid, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { apiClient } from '../api/client'
import { ChannelRow } from '../types'

export function ChannelsPage() {
  const [rows, setRows] = useState<ChannelRow[]>([])
  const [recommendations, setRecommendations] = useState<string[]>([])

  useEffect(() => {
    apiClient
      .get('/analytics/channels', { params: { date_from: '2026-01-01', date_to: '2026-01-31' } })
      .then((res) => {
        setRows(res.data.items)
        setRecommendations(res.data.recommendations)
      })
      .catch(() => {
        setRows([
          { channel: 'Яндекс.Директ', visits: 12000, orders: 700, revenue: 3400000, cost: 1100000, conversion: 0.058, romi: 2.09 },
          { channel: 'VK Реклама', visits: 9000, orders: 420, revenue: 1900000, cost: 760000, conversion: 0.047, romi: 1.5 }
        ])
        setRecommendations(['Рекомендуется увеличить бюджет на Яндекс.Директ на 10%'])
      })
  }, [])

  return (
    <section>
      <h2>Каналы продвижения</h2>
      <div className="charts-grid">
        <div className="chart-card">
          <h3>Выручка по каналам</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={rows}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="channel" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="revenue" fill="#1f9d8b" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="chart-card">
          <h3>Доля затрат</h3>
          <ResponsiveContainer width="100%" height={240}>
            <PieChart>
              <Pie data={rows} dataKey="cost" nameKey="channel" outerRadius={80} fill="#8f6bff" />
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
      <table className="data-table">
        <thead>
          <tr><th>Канал</th><th>Визиты</th><th>Заказы</th><th>Выручка</th><th>Расход</th><th>ROMI</th></tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.channel}>
              <td>{row.channel}</td><td>{row.visits}</td><td>{row.orders}</td><td>{row.revenue}</td><td>{row.cost}</td><td>{row.romi}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="comments"><h3>Рекомендации</h3><ul>{recommendations.map((item) => <li key={item}>{item}</li>)}</ul></div>
    </section>
  )
}
