import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// 防止重复跳转的标志
let isRedirectingToLogin = false

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 清除认证信息并跳转到登录页
function clearAuthAndRedirect() {
  if (isRedirectingToLogin) return

  isRedirectingToLogin = true
  localStorage.removeItem('token')
  localStorage.removeItem('username')

  // 保存当前路由路径，登录后可以返回
  const currentPath = router.currentRoute.value.path
  if (currentPath !== '/login') {
    sessionStorage.setItem('redirectPath', currentPath)
  }

  ElMessage.warning('登录已过期，请重新登录')
  router.push('/login').finally(() => {
    // 延迟重置标志，确保多个并发请求都能被处理
    setTimeout(() => {
      isRedirectingToLogin = false
    }, 500)
  })
}

// 请求拦截器 - 添加token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          clearAuthAndRedirect()
          break
        case 403:
          ElMessage.error('没有权限访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器错误')
          break
        default:
          ElMessage.error(error.response.data?.detail || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络错误，请检查连接')
    } else {
      ElMessage.error('请求配置错误')
    }
    return Promise.reject(error)
  }
)

export default api
