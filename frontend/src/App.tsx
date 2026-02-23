import { Navigate, Route, Routes } from 'react-router-dom'
import { MainLayout } from './layouts/MainLayout'
import { ChannelsPage } from './pages/ChannelsPage'
import { DashboardPage } from './pages/DashboardPage'
import { StubPage } from './pages/StubPage'

export function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/channels" element={<ChannelsPage />} />
        <Route path="/campaigns" element={<StubPage title="Кампании" description="Сравнение кампаний, групп и объявлений с фильтрацией." />} />
        <Route path="/funnel" element={<StubPage title="Воронка" description="Waterfall график по этапам: визит → корзина → заказ → оплата." />} />
        <Route path="/cohorts" element={<StubPage title="Когорты" description="Retention heatmap и когортный анализ по месяцу первого заказа." />} />
        <Route path="/forecast" element={<StubPage title="Прогноз" description="Прогнозы на 7/30/90 дней по выручке, заказам, трафику и расходам." />} />
        <Route path="/reports" element={<StubPage title="Отчеты" description="Сохранение шаблонов, генерация HTML отчета, история выгрузок." />} />
        <Route path="/integrations" element={<StubPage title="Интеграции" description="Подключение Яндекс Метрики, Директа, VK Рекламы и универсальных CSV/XLSX/JSON коннекторов." />} />
        <Route path="/settings" element={<StubPage title="Настройки" description="Управление ролями пользователей, токенами интеграций и политикой доступа." />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
