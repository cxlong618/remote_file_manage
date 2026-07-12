import api from './index'
import type { UploadResponse } from '@/types'

export const uploadFile = async (
  file: File,
  path: string = '',
  onProgress?: (percent: number) => void
): Promise<UploadResponse> => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post<UploadResponse>('/upload/', formData, {
    params: { path },
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (progressEvent) => {
      if (progressEvent.total && onProgress) {
        const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(percent)
      }
    }
  })
  return response.data
}

export const uploadMultipleFiles = async (
  files: File[],
  path: string = ''
): Promise<{ success: boolean; results: any[] }> => {
  const formData = new FormData()
  files.forEach(file => {
    formData.append('files', file)
  })

  const response = await api.post('/upload/multiple', formData, {
    params: { path },
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}
