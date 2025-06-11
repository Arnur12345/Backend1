import type { Task } from '../../../lib/types'
import TaskItem from './TaskItem'

interface TaskListProps {
  tasks: Task[]
  onTaskUpdated: (task: Task) => void
  onTaskDeleted: (taskId: number) => void
  onToggleComplete: (taskId: number, completed: boolean) => void
}

export default function TaskList({ 
  tasks, 
  onTaskUpdated, 
  onTaskDeleted, 
  onToggleComplete 
}: TaskListProps) {
  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onTaskUpdated={onTaskUpdated}
          onTaskDeleted={onTaskDeleted}
          onToggleComplete={onToggleComplete}
        />
      ))}
    </div>
  )
} 