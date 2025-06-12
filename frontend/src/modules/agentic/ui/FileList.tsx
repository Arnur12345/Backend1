import React, { useState } from 'react'
import { apiClient } from '../../../lib/api'
import type { FileInfo } from '../../../lib/types'

interface FileListProps {
  files: FileInfo[]
  selectedFile: string | null
  onFileSelect: (fileId: string) => void
  onFileDelete: (fileId: string) => void
}

const FileList: React.FC<FileListProps> = ({ 
  files, 
  selectedFile, 
  onFileSelect, 
  onFileDelete 
}) => {
  const [deletingFileId, setDeletingFileId] = useState<string | null>(null)

  const handleDelete = async (fileId: string) => {
    if (!confirm('Вы уверены, что хотите удалить этот файл?')) return

    setDeletingFileId(fileId)
    try {
      await apiClient.deleteFile(fileId)
      onFileDelete(fileId)
    } catch (error) {
      alert('Ошибка при удалении файла')
    } finally {
      setDeletingFileId(null)
    }
  }

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleString('ru-RU')
  }

  if (!Array.isArray(files) || files.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <p>Файлы не загружены</p>
        <p className="text-sm">Загрузите файл, чтобы начать чат с агентом</p>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Загруженные файлы</h3>
      
      {files.map((file) => (
        <div
          key={file.file_id}
          className={`border rounded-lg p-4 cursor-pointer transition-colors ${
            selectedFile === file.file_id
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-200 hover:border-gray-300'
          }`}
          onClick={() => onFileSelect(file.file_id)}
        >
          <div className="flex items-center justify-between">
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-2">
                <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span className="text-sm font-medium text-gray-900 truncate">
                  {file.filename}
                </span>
              </div>
              
              <div className="mt-1 flex items-center space-x-4 text-xs text-gray-500">
                <span>{formatFileSize(file.file_size)}</span>
                <span>{file.content_type}</span>
                <span>{formatDate(file.upload_time)}</span>
              </div>
            </div>
            
            <button
              onClick={(e) => {
                e.stopPropagation()
                handleDelete(file.file_id)
              }}
              disabled={deletingFileId === file.file_id}
              className="ml-4 text-red-600 hover:text-red-800 disabled:opacity-50"
              title="Удалить файл"
            >
              {deletingFileId === file.file_id ? (
                <svg className="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              )}
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}

export default FileList 