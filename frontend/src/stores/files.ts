import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { FileInfo, FileListResponse } from '@/types'
import { getFileList } from '@/api/files'

export const useFilesStore = defineStore('files', () => {
  const currentPath = ref<string>('')
  const files = ref<FileInfo[]>([])
  const parentPath = ref<string | null>(null)
  const loading = ref(false)

  // 批量选择状态
  const selectedFiles = ref<FileInfo[]>([])
  const selectAll = ref(false)
  const isIndeterminate = ref(false)

  // 计算属性：是否有可下载的文件被选中
  const hasDownloadableItems = computed(() => {
    return selectedFiles.value.length > 0
  })

  // 计算属性：全选状态
  const allSelected = computed(() => {
    return files.value.length > 0 && selectedFiles.value.length === files.value.length
  })

  // 加载文件列表
  const loadFiles = async (path: string = '') => {
    loading.value = true
    try {
      const response = await getFileList(path)
      currentPath.value = response.current_path
      files.value = response.files
      parentPath.value = response.parent_path || null
      // 清空选择状态
      clearSelection()
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

  // 处理选择变化
  const handleSelectionChange = (selection: FileInfo[]) => {
    selectedFiles.value = selection
    // 更新全选状态
    selectAll.value = selection.length > 0 && selection.length === files.value.length
    isIndeterminate.value = selection.length > 0 && selection.length < files.value.length
  }

  // 全选/取消全选
  const toggleSelectAll = () => {
    if (selectAll.value) {
      // 取消全选
      clearSelection()
    } else {
      // 全选
      selectedFiles.value = [...files.value]
      selectAll.value = true
      isIndeterminate.value = false
    }
  }

  // 清空选择
  const clearSelection = () => {
    selectedFiles.value = []
    selectAll.value = false
    isIndeterminate.value = false
  }

  return {
    currentPath,
    files,
    parentPath,
    loading,
    selectedFiles,
    selectAll,
    isIndeterminate,
    hasDownloadableItems,
    allSelected,
    loadFiles,
    navigateTo,
    enterDirectory,
    goBack,
    goRoot,
    handleSelectionChange,
    toggleSelectAll,
    clearSelection
  }
})
