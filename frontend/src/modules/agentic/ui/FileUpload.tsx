import React, { useState, useRef } from 'react'
import type { UploadedFile } from '../../../lib/types'

interface FileUploadProps {
  onFileUpload: (file: File) => Promise<UploadedFile>
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload }) => {
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

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
      await onFileUpload(file)
      
      // Очистка input
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Ошибка загрузки файла')
    } finally {
      setIsUploading(false)
    }
  }

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    const file = event.dataTransfer.files[0]
    if (file && fileInputRef.current) {
      const dataTransfer = new DataTransfer()
      dataTransfer.items.add(file)
      fileInputRef.current.files = dataTransfer.files
      handleFileSelect({ target: { files: dataTransfer.files } } as React.ChangeEvent<HTMLInputElement>)
    }
  }

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault()
  }

  return (
    <div className="w-full">
      <div
        className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        <input
          ref={fileInputRef}
          type="file"
          onChange={handleFileSelect}
          accept=".txt,.csv,.json,.md,.html"
          className="hidden"
          disabled={isUploading}
        />
        
        <div className="space-y-2">
          <div className="text-gray-600">
            <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
              <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          
          <div>
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              disabled={isUploading}
              className="text-blue-600 hover:text-blue-500 font-medium disabled:opacity-50"
            >
              {isUploading ? 'Загрузка...' : 'Выберите файл'}
            </button>
            <span className="text-gray-500"> или перетащите сюда</span>
          </div>
          
          <p className="text-sm text-gray-500">
            Поддерживаются: TXT, CSV, JSON, MD, HTML (до 10MB)
          </p>
        </div>
      </div>

      {error && (
        <div className="mt-2 text-sm text-red-600 bg-red-50 border border-red-200 rounded p-2">
          {error}
        </div>
      )}
    </div>
  )
}

export default FileUpload 