import { useState } from 'react'
import type { Task, TaskUpdate } from '../../../lib/types'
import { apiClient } from '../../../lib/api'

interface TaskItemProps {
  task: Task
  onTaskUpdated: (task: Task) => void
  onTaskDeleted: (taskId: number) => void
  onToggleComplete: (taskId: number, completed: boolean) => void
}

export default function TaskItem({ 
  task, 
  onTaskUpdated, 
  onTaskDeleted, 
  onToggleComplete 
}: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [editTitle, setEditTitle] = useState(task.title)
  const [editDescription, setEditDescription] = useState(task.description)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSave = async () => {
    if (!editTitle.trim()) {
      setError('Название задачи обязательно')
      return
    }

    setIsLoading(true)
    setError('')

    try {
      const updateData: TaskUpdate = {
        title: editTitle.trim(),
        description: editDescription.trim()
      }
      
      const updatedTask = await apiClient.updateTask(task.id, updateData)
      onTaskUpdated(updatedTask)
      setIsEditing(false)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка обновления задачи')
    } finally {
      setIsLoading(false)
    }
  }

  const handleCancel = () => {
    setEditTitle(task.title)
    setEditDescription(task.description)
    setIsEditing(false)
    setError('')
  }

  const handleDelete = async () => {
    if (!confirm('Вы уверены, что хотите удалить эту задачу?')) {
      return
    }

    setIsLoading(true)
    try {
      await apiClient.deleteTask(task.id)
      onTaskDeleted(task.id)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка удаления задачи')
    } finally {
      setIsLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (isEditing) {
    return (
      <div className="bg-white p-4 rounded-lg shadow border">
        {error && (
          <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}
        
        <div className="space-y-3">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Название задачи"
          />
          
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="Описание задачи"
          />
          
          <div className="flex justify-end space-x-2">
            <button
              onClick={handleCancel}
              className="px-3 py-1 text-sm border border-gray-300 rounded text-gray-700 hover:bg-gray-50"
            >
              Отменить
            </button>
            <button
              onClick={handleSave}
              disabled={isLoading}
              className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {isLoading ? 'Сохранение...' : 'Сохранить'}
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`bg-white p-4 rounded-lg shadow border transition-opacity ${
      task.completed ? 'opacity-75' : ''
    }`}>
      {error && (
        <div className="mb-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}
      
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3 flex-1">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={(e) => onToggleComplete(task.id, e.target.checked)}
            className="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          
          <div className="flex-1">
            <h3 className={`text-lg font-medium ${
              task.completed ? 'line-through text-gray-500' : 'text-gray-900'
            }`}>
              {task.title}
            </h3>
            
            {task.description && (
              <p className={`mt-1 text-sm ${
                task.completed ? 'text-gray-400' : 'text-gray-600'
              }`}>
                {task.description}
              </p>
            )}
            
            <div className="mt-2 text-xs text-gray-500">
              Создано: {formatDate(task.created_at)}
              {task.updated_at !== task.created_at && (
                <span className="ml-2">
                  • Обновлено: {formatDate(task.updated_at)}
                </span>
              )}
            </div>
          </div>
        </div>
        
        <div className="flex space-x-2 ml-4">
          <button
            onClick={() => setIsEditing(true)}
            className="text-blue-600 hover:text-blue-800 text-sm"
          >
            Редактировать
          </button>
          <button
            onClick={handleDelete}
            disabled={isLoading}
            className="text-red-600 hover:text-red-800 text-sm disabled:opacity-50"
          >
            {isLoading ? 'Удаление...' : 'Удалить'}
          </button>
        </div>
      </div>
    </div>
  )
} 