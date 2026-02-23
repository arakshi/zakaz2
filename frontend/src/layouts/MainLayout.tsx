import { Link, Outlet, useLocation } from 'react-router-dom'

const menu = [
  ['/', 'Дашборд'],
  ['/channels', 'Каналы'],
  ['/campaigns', 'Кампании'],
  ['/funnel', 'Воронка'],
  ['/cohorts', 'Когорты'],
  ['/forecast', 'Прогноз'],
  ['/reports', 'Отчеты'],
  ['/integrations', 'Интеграции'],
  ['/settings', 'Настройки']
]

export function MainLayout() {
  const location = useLocation()

  return (
    <div className="layout">
      <aside className="sidebar">
        <h2>FUP Analytics</h2>
        <nav>
          {menu.map(([href, title]) => (
            <Link key={href} className={location.pathname === href ? 'active' : ''} to={href}>
              {title}
            </Link>
          ))}
        </nav>
      </aside>
      <main>
        <header className="topbar">
          <div>
            <h1>Маркетинговая аналитика</h1>
            <p>ООО «Фабрика универсальных покрытий»</p>
          </div>
          <div className="actions">
            <button>Быстрый импорт</button>
            <button>Создать отчет</button>
            <button>Переключить тему</button>
          </div>
        </header>
        <Outlet />
      </main>
    </div>
  )
}
