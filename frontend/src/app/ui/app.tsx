// import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from '../../lib/auth/AuthContext.tsx'
import Layout from '../../shared/ui/Layout.tsx'
import LoginPage from '../../modules/auth/pages/LoginPage.tsx'
import { RegisterPage } from '../../modules/auth/pages/RegisterPage.tsx'
import TasksPage from '../../modules/tasks/pages/TasksPage.tsx'
import AgenticPage from '../../modules/agentic/pages/AgenticPage.tsx'
import ProtectedRoute from '../../shared/ui/ProtectedRoute.tsx'

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
          <Route 
            path="/agentic" 
            element={
              <ProtectedRoute>
                <AgenticPage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Layout>
    </AuthProvider>
  )
}

export default App 