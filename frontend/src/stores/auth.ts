import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin } from '@/api/auth'
import type { LoginRequest } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string>(localStorage.getItem('token') || '')
  const username = ref<string>(localStorage.getItem('username') || '')
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value)

  // 登录
  const login = async (credentials: LoginRequest) => {
    loading.value = true
    try {
      const response = await apiLogin(credentials)
      token.value = response.access_token
      username.value = response.username

      // 持久化存储
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('username', response.username)

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
    localStorage.removeItem('token')
    localStorage.removeItem('username')
  }

  return {
    token,
    username,
    loading,
    isAuthenticated,
    login,
    logout
  }
})
