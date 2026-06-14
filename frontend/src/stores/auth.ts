import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin } from '@/api/auth'
import type { LoginRequest } from '@/types'

// Token 过期时间（默认24小时，与后端保持一致）
const TOKEN_EXPIRY_TIME = 24 * 60 * 60 * 1000

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  const username = ref<string>(localStorage.getItem('username') || '')
  const loading = ref(false)
  const loginTime = ref<number>(Number(localStorage.getItem('loginTime') || '0'))

  const isAuthenticated = computed(() => !!token.value)

  // 检查 token 是否过期
  const isTokenExpired = computed(() => {
    if (!loginTime.value) return false
    return Date.now() - loginTime.value > TOKEN_EXPIRY_TIME
  })

  // 检查认证状态是否有效
  const isAuthValid = computed(() => {
    return isAuthenticated.value && !isTokenExpired.value
  })

  // 登录
  const login = async (credentials: LoginRequest) => {
    loading.value = true
    try {
      const response = await apiLogin(credentials)
      token.value = response.access_token
      username.value = response.username
      loginTime.value = Date.now()

      // 持久化存储
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('username', response.username)
      localStorage.setItem('loginTime', String(loginTime.value))

      return true
    } catch (error) {
      return false
    } finally {
      loading.value = false
    }
  }

  // 登出
  const logout = () => {
    token.value = ''
    username.value = ''
    loginTime.value = 0
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('loginTime')
    // 清除重定向路径
    sessionStorage.removeItem('redirectPath')
  }

  // 清除过期认证信息
  const clearExpiredAuth = () => {
    if (isTokenExpired.value) {
      logout()
      return true
    }
    return false
  }

  return {
    token,
    username,
    loading,
    loginTime,
    isAuthenticated,
    isTokenExpired,
    isAuthValid,
    login,
    logout,
    clearExpiredAuth
  }
})
