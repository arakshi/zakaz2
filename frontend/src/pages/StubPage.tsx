interface StubPageProps { title: string; description: string }

export function StubPage({ title, description }: StubPageProps) {
  return (
    <section className="chart-card">
      <h2>{title}</h2>
      <p>{description}</p>
      <p>Страница содержит фильтры, таблицы, экспорт в CSV/PDF и графики в промышленной версии.</p>
    </section>
  )
}
