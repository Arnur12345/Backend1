import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { AuthProvider } from '../../lib/auth/AuthContext'
import Layout from '../../shared/ui/Layout'
import LoginPage from '../../modules/auth/pages/LoginPage'
import { RegisterPage } from '../../modules/auth/pages/RegisterPage'
import TasksPage from '../../modules/tasks/pages/TasksPage'
import AgenticPage from '../../modules/agentic/pages/AgenticPage'
import ProtectedRoute from '../../shared/ui/ProtectedRoute'

function App() {
  return React.createElement(AuthProvider, null,
    React.createElement(Layout, null,
      React.createElement(Routes, null,
        React.createElement(Route, { path: "/login", element: React.createElement(LoginPage) }),
        React.createElement(Route, { path: "/register", element: React.createElement(RegisterPage) }),
        React.createElement(Route, { 
          path: "/", 
          element: React.createElement(ProtectedRoute, null,
            React.createElement(TasksPage)
          )
        }),
        React.createElement(Route, { 
          path: "/tasks", 
          element: React.createElement(ProtectedRoute, null,
            React.createElement(TasksPage)
          )
        }),
        React.createElement(Route, { 
          path: "/agentic", 
          element: React.createElement(ProtectedRoute, null,
            React.createElement(AgenticPage)
          )
        })
      )
    )
  )
}

export default App 