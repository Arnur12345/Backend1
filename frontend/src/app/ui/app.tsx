import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from '../../lib/auth/AuthContext'
import Layout from '../../shared/ui/Layout'
import LoginPage from '../../modules/auth/pages/LoginPage'
import { RegisterPage } from '../../modules/auth/pages/RegisterPage'
import TasksPage from '../../modules/tasks/pages/TasksPage'
import ProtectedRoute from '../../shared/ui/ProtectedRoute'

function App() {
  return (
    <AuthProvider>
      <Layout>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route 
            path="/" 
            element={
              <ProtectedRoute>
                <TasksPage />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/tasks" 
            element={
              <ProtectedRoute>
                <TasksPage />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </Layout>
    </AuthProvider>
  )
}

export default App 