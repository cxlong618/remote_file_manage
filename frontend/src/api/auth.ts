import api from './index'
import type { LoginRequest, LoginResponse, UserInfo } from '@/types'

// OAuth2密码表单格式
export const login = async (data: LoginRequest): Promise<LoginResponse> => {
  const formData = new FormData()
  formData.append('username', data.username)
  formData.append('password', data.password)

  const response = await api.post<LoginResponse>('/auth/login', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return response.data
}

export const getCurrentUser = async (): Promise<UserInfo> => {
  const response = await api.get<UserInfo>('/auth/me')
  return response.data
}
