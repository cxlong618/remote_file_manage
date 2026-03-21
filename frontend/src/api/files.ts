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
