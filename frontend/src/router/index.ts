import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // 检查并清除过期的认证信息
  const wasExpired = authStore.clearExpiredAuth()

  if (to.meta.requiresAuth) {
    if (!authStore.isAuthValid) {
      // 保存目标路径用于登录后重定向
      if (to.path !== '/login') {
        sessionStorage.setItem('redirectPath', to.path)
      }
      if (wasExpired) {
        ElMessage.warning('登录已过期，请重新登录')
      }
      next('/login')
      return
    }
  }

  // 如果已认证且访问登录页，重定向到首页或之前保存的路径
  if (to.path === '/login' && authStore.isAuthValid) {
    const redirectPath = sessionStorage.getItem('redirectPath') || '/'
    sessionStorage.removeItem('redirectPath')
    next(redirectPath)
    return
  }

  next()
})

export default router
