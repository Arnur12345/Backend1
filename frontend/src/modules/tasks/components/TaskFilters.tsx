type FilterType = 'all' | 'pending' | 'completed'

interface TaskFiltersProps {
  currentFilter: FilterType
  onFilterChange: (filter: FilterType) => void
}

export default function TaskFilters({ currentFilter, onFilterChange }: TaskFiltersProps) {
  const filters = [
    { key: 'all' as FilterType, label: 'Все задачи' },
    { key: 'pending' as FilterType, label: 'В процессе' },
    { key: 'completed' as FilterType, label: 'Завершенные' }
  ]

  return (
    <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
      {filters.map((filter) => (
        <button
          key={filter.key}
          onClick={() => onFilterChange(filter.key)}
          className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
            currentFilter === filter.key
              ? 'bg-white text-blue-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
          }`}
        >
          {filter.label}
        </button>
      ))}
    </div>
  )
} 