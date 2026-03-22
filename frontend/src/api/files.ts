import api from './index'
import type { FileListResponse, FileInfo } from '@/types'

export const getFileList = async (path: string = ''): Promise<FileListResponse> => {
  const response = await api.get<FileListResponse>('/files/list', {
    params: { path }
  })
  return response.data
}

export const getFileInfo = async (path: string): Promise<FileInfo> => {
  const response = await api.get<FileInfo>('/files/info', {
    params: { path }
  })
  return response.data
}

export const deleteFile = async (path: string): Promise<{ success: boolean; message: string }> => {
  const response = await api.delete('/files/', {
    params: { path }
  })
  return response.data
}

export const previewText = async (path: string): Promise<{ content: string }> => {
  const response = await api.get<{ content: string }>('/files/preview/text', {
    params: { path }
  })
  return response.data
}

export const getMediaUrl = (path: string): string => {
  return `/api/files/preview/stream?path=${encodeURIComponent(path)}`
}

export const getDownloadUrl = (path: string): string => {
  return `/api/files/download?path=${encodeURIComponent(path)}`
}

/**
 * 下载文件（使用 axios，携带认证 token）
 */
export const downloadFile = async (path: string, fileName: string) => {
  const response = await api.get('/files/download', {
    params: { path },
    responseType: 'blob' // 接收二进制数据
  })

  // 创建下载链接
  const url = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href = url
  link.download = fileName
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url) // 释放内存
}

/**
 * 下载文件夹（ZIP 压缩）
 */
export const downloadFolder = async (path: string, fileName: string) => {
  const response = await api.get('/files/download-folder', {
    params: { path },
    responseType: 'blob'
  })

  const url = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href = url
  link.download = fileName
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  window.URL.revokeObjectURL(url)
}

/**
 * 获取带 token 的媒体 URL（用于图片、视频、音频预览）
 */
export const getMediaUrlWithToken = (path: string): string => {
  const token = localStorage.getItem('token')
  const baseUrl = `/api/files/preview/stream?path=${encodeURIComponent(path)}`
  if (token) {
    return `${baseUrl}&token=${token}`
  }
  return baseUrl
}

/**
 * 获取媒体文件的 Blob URL（带认证）
 */
export const getMediaBlobUrl = async (path: string): Promise<string> => {
  const response = await api.get('/files/preview/stream', {
    params: { path },
    responseType: 'blob'
  })
  return window.URL.createObjectURL(new Blob([response.data]))
}
