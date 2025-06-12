import React from 'react'
import { useAuth } from '../../lib/auth/AuthContext'
import { useNavigate, useLocation, Link } from 'react-router-dom'

export default function Layout({ children }) {
  const { user, logout, isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const isAuthPage = location.pathname === '/login' || location.pathname === '/register'

  const navigation = [
    { name: 'Задачи', href: '/tasks', current: location.pathname === '/tasks' || location.pathname === '/' },
    { name: 'AI Агенты', href: '/agentic', current: location.pathname === '/agentic' },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {isAuthenticated && !isAuthPage && (
        <header className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center space-x-8">
                <h1 className="text-xl font-semibold text-gray-900">
                  Task Manager
                </h1>
                
                {/* Навигация */}
                <nav className="flex space-x-4">
                  {navigation.map((item) => (
                    <Link
                      key={item.name}
                      to={item.href}
                      className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                        item.current
                          ? 'bg-blue-100 text-blue-700'
                          : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                      }`}
                    >
                      {item.name}
                    </Link>
                  ))}
                </nav>
              </div>
              
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-700">
                  Привет, {user?.username || user?.email}!
                </span>
                <button
                  onClick={handleLogout}
                  className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Выйти
                </button>
              </div>
            </div>
          </div>
        </header>
      )}
      
      <main className={isAuthenticated && !isAuthPage ? "max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8" : ""}>
        {children}
      </main>
    </div>
  )
} 