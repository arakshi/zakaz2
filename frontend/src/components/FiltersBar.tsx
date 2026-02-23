interface FiltersBarProps {
  onRefresh: () => void
}

export function FiltersBar({ onRefresh }: FiltersBarProps) {
  return (
    <div className="filters-bar">
      <label>Период</label>
      <input type="date" />
      <input type="date" />
      <select>
        <option>Все каналы</option>
        <option>Яндекс.Директ</option>
        <option>VK Реклама</option>
      </select>
      <button onClick={onRefresh}>Обновить</button>
    </div>
  )
}
