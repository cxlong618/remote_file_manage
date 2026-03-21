// 文件信息接口
export interface FileInfo {
  name: string
  path: string
  is_dir: boolean
  size: number
  modified_time: string
  preview_type?: string
  is_previewable: boolean
}

// 文件列表响应
export interface FileListResponse {
  current_path: string
  files: FileInfo[]
  parent_path?: string
}

// 登录请求
export interface LoginRequest {
  username: string
  password: string
}

// 登录响应
export interface LoginResponse {
  access_token: string
  token_type: string
  username: string
}

// 用户信息
export interface UserInfo {
  username: string
  is_authenticated: boolean
}

// 上传响应
export interface UploadResponse {
  success: boolean
  message: string
  file_path: string
  file_name: string
  file_size: number
}

// API响应基础类型
export interface ApiResponse<T = any> {
  data: T
  message?: string
  success?: boolean
}
