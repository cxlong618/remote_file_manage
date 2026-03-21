import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { FileInfo, FileListResponse } from '@/types'
import { getFileList } from '@/api/files'

export const useFilesStore = defineStore('files', () => {
  const currentPath = ref<string>('')
  const files = ref<FileInfo[]>([])
  const parentPath = ref<string | null>(null)
  const loading = ref(false)

  // 加载文件列表
  const loadFiles = async (path: string = '') => {
    loading.value = true
    try {
      const response = await getFileList(path)
      currentPath.value = response.current_path
      files.value = response.files
      parentPath.value = response.parent_path || null
    } catch (error) {
      console.error('加载文件列表失败:', error)
    } finally {
      loading.value = false
    }
  }

  // 导航到指定路径
  const navigateTo = async (path: string) => {
    await loadFiles(path)
  }

  // 进入目录
  const enterDirectory = async (file: FileInfo) => {
    if (file.is_dir) {
      const newPath = file.path || file.name
      await loadFiles(newPath)
    }
  }

  // 返回上级目录
  const goBack = async () => {
    if (parentPath.value !== null) {
      await loadFiles(parentPath.value)
    }
  }

  // 返回根目录
  const goRoot = async () => {
    await loadFiles('')
  }

  return {
    currentPath,
    files,
    parentPath,
    loading,
    loadFiles,
    navigateTo,
    enterDirectory,
    goBack,
    goRoot
  }
})
