import { useState, useEffect } from 'react'
import type { Task } from '../../../lib/types'
import { apiClient } from '../../../lib/api'
import TaskList from '../components/TaskList'
import TaskForm from '../components/TaskForm'
import TaskFilters from '../components/TaskFilters'

type FilterType = 'all' | 'pending' | 'completed'

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [filter, setFilter] = useState<FilterType>('all')
  const [showForm, setShowForm] = useState(false)

  useEffect(() => {
    loadTasks()
  }, [])

  useEffect(() => {
    filterTasks()
  }, [tasks, filter])

  const loadTasks = async () => {
    try {
      setIsLoading(true)
      const data = await apiClient.getTasks()
      setTasks(data)
      setError('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка загрузки задач')
    } finally {
      setIsLoading(false)
    }
  }

  const filterTasks = () => {
    switch (filter) {
      case 'pending':
        setFilteredTasks(tasks.filter(task => !task.completed))
        break
      case 'completed':
        setFilteredTasks(tasks.filter(task => task.completed))
        break
      default:
        setFilteredTasks(tasks)
    }
  }

  const handleTaskCreated = (newTask: Task) => {
    setTasks(prev => [newTask, ...prev])
    setShowForm(false)
  }

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(prev => prev.map(task => 
      task.id === updatedTask.id ? updatedTask : task
    ))
  }

  const handleTaskDeleted = (taskId: number) => {
    setTasks(prev => prev.filter(task => task.id !== taskId))
  }

  const handleToggleComplete = async (taskId: number, completed: boolean) => {
    try {
      const updatedTask = completed 
        ? await apiClient.markTaskCompleted(taskId)
        : await apiClient.markTaskPending(taskId)
      
      handleTaskUpdated(updatedTask)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка обновления задачи')
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Мои задачи</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
        >
          {showForm ? 'Отменить' : 'Добавить задачу'}
        </button>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {showForm && (
        <div className="bg-white p-6 rounded-lg shadow">
          <TaskForm onTaskCreated={handleTaskCreated} onCancel={() => setShowForm(false)} />
        </div>
      )}

      <TaskFilters currentFilter={filter} onFilterChange={setFilter} />

      <TaskList
        tasks={filteredTasks}
        onTaskUpdated={handleTaskUpdated}
        onTaskDeleted={handleTaskDeleted}
        onToggleComplete={handleToggleComplete}
      />

      {filteredTasks.length === 0 && !isLoading && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">
            {filter === 'all' ? 'У вас пока нет задач' : 
             filter === 'pending' ? 'Нет незавершенных задач' : 
             'Нет завершенных задач'}
          </p>
        </div>
      )}
    </div>
  )
} 