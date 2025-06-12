import React, { useState, useEffect, useRef } from 'react'
import { apiClient } from '../../../lib/api'

const AgenticPage = () => {
  const [files, setFiles] = useState([])
  const [selectedFile, setSelectedFile] = useState(null)
  const [chatHistory, setChatHistory] = useState([])
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const chatEndRef = useRef(null)
  const fileInputRef = useRef(null)

  React.useEffect(() => {
    loadFiles()
  }, [])

  React.useEffect(() => {
    scrollToBottom()
  }, [chatHistory])

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const loadFiles = async () => {
    try {
      const filesData = await apiClient.getUploadedFiles()
      setFiles(filesData || [])
    } catch (error) {
      console.error('Ошибка загрузки файлов:', error)
      setFiles([])
    }
  }

  const handleFileUpload = async (file) => {
    // Проверка типа файла
    const allowedTypes = [
      'text/plain',
      'text/csv', 
      'application/json',
      'text/markdown',
      'text/html'
    ]

    if (!allowedTypes.includes(file.type)) {
      setError('Поддерживаются только файлы: .txt, .csv, .json, .md, .html')
      return
    }

    // Проверка размера файла (10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('Размер файла не должен превышать 10MB')
      return
    }

    setIsUploading(true)
    setError(null)

    try {
      const response = await apiClient.uploadFile(file)
      await loadFiles()
      setSelectedFile(response.file_id)
      setChatHistory([])
      
      // Очистка input
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    } catch (error) {
      console.error('Ошибка загрузки файла:', error)
      setError('Ошибка при загрузке файла')
    } finally {
      setIsUploading(false)
    }
  }

  const handleFileSelect = async (fileId) => {
    setSelectedFile(fileId)
    setChatHistory([])
    setError(null)
    
    try {
      const history = await apiClient.getChatHistory(fileId)
      setChatHistory(history.conversations || [])
    } catch (error) {
      console.error('Ошибка загрузки истории чата:', error)
    }
  }

  const handleFileDelete = async (fileId) => {
    if (!confirm('Вы уверены, что хотите удалить этот файл?')) return

    try {
      await apiClient.deleteFile(fileId)
      await loadFiles()
      if (selectedFile === fileId) {
        setSelectedFile(null)
        setChatHistory([])
      }
    } catch (error) {
      console.error('Ошибка удаления файла:', error)
      setError('Ошибка при удалении файла')
    }
  }

  const handleSendMessage = async () => {
    if (!message.trim() || !selectedFile || isLoading) return

    const userMessage = message.trim()
    setMessage('')
    setIsLoading(true)
    setError(null)

    // Добавляем сообщение пользователя в чат
    const newUserMessage = {
      timestamp: new Date().toISOString(),
      question: userMessage,
      answer: '',
      agent_type: 'user'
    }
    setChatHistory(prev => [...prev, newUserMessage])

    try {
      const response = await apiClient.askQuestion({
        file_id: selectedFile,
        question: userMessage
      })

      // Обновляем последнее сообщение с ответом агента
      setChatHistory(prev => {
        const updated = [...prev]
        updated[updated.length - 1] = {
          timestamp: response.response_time,
          question: userMessage,
          answer: response.answer,
          agent_type: response.agent_type
        }
        return updated
      })
    } catch (error) {
      console.error('Ошибка отправки сообщения:', error)
      setError('Ошибка при отправке сообщения')
      // Удаляем сообщение пользователя при ошибке
      setChatHistory(prev => prev.slice(0, -1))
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleQuickQuestion = (question) => {
    setMessage(question)
  }

  const clearChat = async () => {
    if (!selectedFile) return
    
    try {
      setChatHistory([])
      setError(null)
    } catch (error) {
      console.error('Ошибка очистки чата:', error)
    }
  }

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString('ru-RU', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const quickQuestions = [
    "Кратко опиши содержание файла",
    "Какие основные темы затрагиваются?",
    "Выдели ключевые моменты",
    "Есть ли важные даты или числа?",
    "Сделай краткое резюме"
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">🤖 AI Ассистент</h1>
          <p className="text-gray-600">Умный помощник для анализа документов</p>
        </div>
        
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-xl p-4 max-w-2xl mx-auto">
            <div className="flex items-center">
              <svg className="w-5 h-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <p className="text-red-800">{error}</p>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Боковая панель - Файлы */}
          <div className="lg:col-span-1 space-y-6">
            {/* Загрузка файла */}
            <div className="bg-white rounded-xl shadow-sm border p-6">
              <h2 className="text-lg font-semibold mb-4 text-gray-900">📁 Загрузить файл</h2>
              
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-blue-400 transition-colors">
                <input
                  ref={fileInputRef}
                  type="file"
                  onChange={(e) => e.target.files?.[0] && handleFileUpload(e.target.files[0])}
                  accept=".txt,.csv,.json,.md,.html"
                  className="hidden"
                  disabled={isUploading}
                />
                
                <div className="space-y-2">
                  <svg className="mx-auto h-8 w-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                  
                  <button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    disabled={isUploading}
                    className="text-blue-600 hover:text-blue-500 font-medium disabled:opacity-50"
                  >
                    {isUploading ? 'Загрузка...' : 'Выбрать файл'}
                  </button>
                  
                  <p className="text-xs text-gray-500">
                    TXT, CSV, JSON, MD, HTML
                  </p>
                </div>
              </div>
            </div>

            {/* Список файлов */}
            <div className="bg-white rounded-xl shadow-sm border p-6">
              <h2 className="text-lg font-semibold mb-4 text-gray-900">📄 Мои файлы</h2>
              
              {files.length === 0 ? (
                <div className="text-center py-6 text-gray-500">
                  <svg className="mx-auto h-8 w-8 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <p className="text-sm">Нет файлов</p>
                </div>
              ) : (
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {files.map((file) => (
                    <div
                      key={file.file_id}
                      className={`p-3 rounded-lg cursor-pointer transition-all ${
                        selectedFile === file.file_id
                          ? 'bg-blue-50 border-2 border-blue-200'
                          : 'bg-gray-50 hover:bg-gray-100 border-2 border-transparent'
                      }`}
                      onClick={() => handleFileSelect(file.file_id)}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-900 truncate">
                            {file.filename}
                          </p>
                          <p className="text-xs text-gray-500">
                            {formatFileSize(file.file_size)}
                          </p>
                        </div>
                        
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            handleFileDelete(file.file_id)
                          }}
                          className="ml-2 text-red-500 hover:text-red-700 p-1"
                          title="Удалить файл"
                        >
                          <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Быстрые вопросы */}
            {selectedFile && (
              <div className="bg-white rounded-xl shadow-sm border p-6">
                <h2 className="text-lg font-semibold mb-4 text-gray-900">⚡ Быстрые вопросы</h2>
                <div className="space-y-2">
                  {quickQuestions.map((question, index) => (
                    <button
                      key={index}
                      onClick={() => handleQuickQuestion(question)}
                      className="w-full text-left p-2 text-sm bg-gray-50 hover:bg-blue-50 rounded-lg transition-colors"
                    >
                      {question}
                    </button>
                  ))}
                </div>
                
                <button
                  onClick={clearChat}
                  className="w-full mt-4 p-2 text-sm bg-red-50 hover:bg-red-100 text-red-600 rounded-lg transition-colors"
                >
                  🗑️ Очистить чат
                </button>
              </div>
            )}
          </div>

          {/* Основная область - Чат */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-xl shadow-sm border h-[calc(100vh-200px)] flex flex-col">
              {/* Заголовок чата */}
              <div className="p-6 border-b bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-t-xl">
                <h2 className="text-xl font-semibold">💬 Чат с AI Ассистентом</h2>
                <p className="text-blue-100 text-sm mt-1">
                  {selectedFile ? 'Задавайте вопросы о загруженном файле' : 'Выберите файл для начала общения'}
                </p>
              </div>

              {/* Область чата */}
              <div className="flex-1 p-6 overflow-y-auto">
                {!selectedFile ? (
                  <div className="text-center py-12">
                    <div className="bg-gray-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Добро пожаловать!</h3>
                    <p className="text-gray-600">Загрузите файл, чтобы начать общение с AI ассистентом</p>
                  </div>
                ) : chatHistory.length === 0 ? (
                  <div className="text-center py-12">
                    <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                      <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Готов к общению!</h3>
                    <p className="text-gray-600">Задайте вопрос о содержимом файла или выберите быстрый вопрос</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {chatHistory.map((chat, index) => (
                      <div key={index} className="space-y-3">
                        {/* Сообщение пользователя */}
                        <div className="flex justify-end">
                          <div className="bg-blue-500 text-white rounded-2xl rounded-br-md px-4 py-2 max-w-xs lg:max-w-md">
                            <p className="text-sm">{chat.question}</p>
                          </div>
                        </div>
                        
                        {/* Ответ ассистента */}
                        {chat.answer && (
                          <div className="flex justify-start">
                            <div className="bg-gray-100 rounded-2xl rounded-bl-md px-4 py-2 max-w-xs lg:max-w-md">
                              <div className="flex items-center gap-2 mb-1">
                                <div className="w-6 h-6 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center">
                                  <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                  </svg>
                                </div>
                                <span className="text-xs font-medium text-blue-600">AI Ассистент</span>
                                <span className="text-xs text-gray-500">{formatTimestamp(chat.timestamp)}</span>
                              </div>
                              <div className="text-sm text-gray-800 whitespace-pre-wrap">{chat.answer}</div>
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                    
                    {isLoading && (
                      <div className="flex justify-start">
                        <div className="bg-gray-100 rounded-2xl rounded-bl-md px-4 py-2">
                          <div className="flex items-center gap-2">
                            <div className="flex space-x-1">
                              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                              <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                            </div>
                            <span className="text-sm text-gray-600">AI думает...</span>
                          </div>
                        </div>
                      </div>
                    )}
                    <div ref={chatEndRef} />
                  </div>
                )}
              </div>

              {/* Поле ввода */}
              {selectedFile && (
                <div className="p-6 border-t bg-gray-50 rounded-b-xl">
                  <div className="flex gap-3">
                    <div className="flex-1 relative">
                      <textarea
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyDown={handleKeyPress}
                        placeholder="Напишите ваш вопрос..."
                        className="w-full p-3 pr-12 border border-gray-300 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        rows={2}
                        disabled={isLoading}
                      />
                      <div className="absolute bottom-2 right-2 text-xs text-gray-400">
                        Enter для отправки
                      </div>
                    </div>
                    <button
                      onClick={handleSendMessage}
                      disabled={!message.trim() || isLoading}
                      className="px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl hover:from-blue-600 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-105 active:scale-95"
                    >
                      {isLoading ? (
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      ) : (
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                        </svg>
                      )}
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AgenticPage 