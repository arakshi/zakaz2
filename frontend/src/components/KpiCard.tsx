interface KpiCardProps {
  title: string
  value: string
  hint?: string
}

export function KpiCard({ title, value, hint }: KpiCardProps) {
  return (
    <div className="kpi-card">
      <p className="kpi-title">{title}</p>
      <h3>{value}</h3>
      {hint ? <small>{hint}</small> : null}
    </div>
  )
}
