<template>
  <div class="file-browser">
    <!-- 工具栏 -->
    <div class="toolbar">
      <div class="breadcrumb">
        <el-button
          :icon="House"
          circle
          title="根目录"
          @click="filesStore.goRoot"
        />

        <el-button
          :icon="Back"
          circle
          title="返回上级"
          :disabled="!filesStore.parentPath"
          @click="filesStore.goBack"
        />

        <el-breadcrumb separator="/">
          <el-breadcrumb-item @click="filesStore.goRoot">
            根目录
          </el-breadcrumb-item>
          <el-breadcrumb-item
            v-for="(dir, index) in pathDirs"
            :key="index"
            @click="navigateToPath(dir.path)"
          >
            {{ dir.name }}
          </el-breadcrumb-item>
        </el-breadcrumb>
      </div>

      <div class="path-input">
        <el-input
          v-model="pathInput"
          placeholder="输入路径快速跳转（支持 ~/path 或文件路径）"
          @keyup.enter="handlePathInput"
        >
          <template #append>
            <el-button :icon="Right" @click="handlePathInput" />
          </template>
        </el-input>
      </div>

      <div class="actions">
        <el-button
          type="primary"
          :icon="Upload"
          @click="showUploadDialog = true"
        >
          上传文件
        </el-button>

        <el-button
          :icon="Refresh"
          @click="refresh"
          :loading="filesStore.loading"
        >
          刷新
        </el-button>
      </div>
    </div>

    <!-- 文件列表 -->
    <div class="file-list">
      <el-table
        :data="filesStore.files"
        v-loading="filesStore.loading"
        style="width: 100%"
        @row-dblclick="handleRowDblClick"
      >
        <el-table-column prop="name" label="名称" min-width="250">
          <template #default="{ row }">
            <div class="file-name" @click="handleNameClick(row)">
              <el-icon :size="20" :color="getIconColor(row)">
                <component :is="getFileIcon(row)" />
              </el-icon>
              <span>{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="size" label="大小" width="120" align="right">
          <template #default="{ row }">
            {{ row.is_dir ? '-' : formatFileSize(row.size) }}
          </template>
        </el-table-column>

        <el-table-column prop="modified_time" label="修改时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.modified_time) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="320" fixed="right">
          <template #default="{ row }">
            <!-- 文件夹操作 -->
            <template v-if="row.is_dir">
              <el-button
                type="primary"
                size="small"
                :icon="FolderOpened"
                @click="filesStore.enterDirectory(row)"
              >
                打开
              </el-button>
              <el-button
                type="success"
                size="small"
                :icon="Download"
                @click="handleDownload(row)"
              >
                下载
              </el-button>
            </template>

            <!-- 文件操作 -->
            <template v-else>
              <el-button
                v-if="row.is_previewable"
                type="success"
                size="small"
                :icon="View"
                @click="handlePreview(row)"
              >
                预览
              </el-button>

              <el-button
                type="primary"
                size="small"
                :icon="Download"
                @click="handleDownload(row)"
              >
                下载
              </el-button>
            </template>

            <!-- 删除按钮（文件和文件夹都有） -->
            <el-button
              type="danger"
              size="small"
              :icon="Delete"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 上传对话框 -->
    <FileUpload
      v-model:visible="showUploadDialog"
      :current-path="filesStore.currentPath"
      @success="refresh"
    />

    <!-- 预览对话框 -->
    <FilePreview
      v-model:visible="showPreviewDialog"
      :file="currentPreviewFile"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  House,
  Back,
  Right,
  Upload,
  Refresh,
  FolderOpened,
  View,
  Delete,
  Download
} from '@element-plus/icons-vue'
import { useFilesStore } from '@/stores/files'
import { deleteFile } from '@/api/files'
import FileUpload from './FileUpload.vue'
import FilePreview from './FilePreview.vue'
import { formatFileSize, formatDateTime, getFileIcon } from '@/utils/format'
import type { FileInfo } from '@/types'

const filesStore = useFilesStore()
const pathInput = ref('')
const showUploadDialog = ref(false)
const showPreviewDialog = ref(false)
const currentPreviewFile = ref<FileInfo | null>(null)

// 路径目录数组（用于面包屑）
const pathDirs = computed(() => {
  if (!filesStore.currentPath || filesStore.currentPath === '/') {
    return []
  }

  const parts = filesStore.currentPath.split('/').filter(Boolean)
  let currentPath = ''

  return parts.map((part, index) => {
    currentPath += (index > 0 ? '/' : '') + part
    return {
      name: part,
      path: parts.slice(0, index + 1).join('/')
    }
  })
})

// 获取图标颜色
const getIconColor = (file: FileInfo) => {
  if (file.is_dir) return '#409EFF'
  switch (file.preview_type) {
    case 'image': return '#67C23A'
    case 'video': return '#E6A23C'
    case 'audio': return '#F56C6C'
    case 'markdown': return '#909399'
    default: return '#909399'
  }
}

// 处理路径输入
const handlePathInput = async () => {
  const inputPath = pathInput.value.trim()
  if (!inputPath) {
    return
  }

  try {
    // 显示简单提示
    ElMessage.info('正在解析路径...')

    // 处理路径输入
    const processedPath = await processPathInput(inputPath)

    if (processedPath.fileToPreview) {
      // 如果是文件路径，跳转到父目录并预览文件
      await filesStore.navigateTo(processedPath.directoryPath)

      // 延迟预览，确保文件列表已加载
      setTimeout(() => {
        const targetFile = filesStore.files.find(f => f.path === processedPath.fileToPreview)
        if (targetFile && targetFile.is_previewable) {
          handlePreview(targetFile)
          ElMessage.success('已打开文件预览')
        } else {
          ElMessage.warning('文件不支持预览或未找到')
        }
      }, 500)
    } else {
      // 如果是目录路径，直接跳转
      await filesStore.navigateTo(processedPath.directoryPath)
      ElMessage.success('已跳转到目标目录')
    }

    pathInput.value = ''
  } catch (error: any) {
    console.error('路径跳转错误:', error)
    ElMessage.error(error.response?.data?.detail || error.message || '路径跳转失败')
  }
}

/**
 * 处理路径输入，支持：
 * 1. ~ 开头 → 跳转到根目录
 * 2. 文件路径 → 跳转到父目录并预览文件
 * 3. 目录路径 → 直接跳转
 */
const processPathInput = async (inputPath: string): Promise<{
  directoryPath: string
  fileToPreview: string | null
}> => {
  let path = inputPath

  // 1. 处理 ~ 开头（跳转到根目录）
  if (path.startsWith('~')) {
    path = path.substring(1).trim()
    if (path.startsWith('/') || path.startsWith('\\')) {
      path = path.substring(1)
    }
    if (!path) {
      // 只有 ~，跳转到根目录
      return { directoryPath: '', fileToPreview: null }
    }
    // ~/xxx 形式，去掉 ~ 后继续处理
  }

  // 2. 判断是文件还是目录
  // 先尝试作为文件路径获取信息
  try {
    const { getFileInfo } = await import('@/api/files')
    const fileInfo = await getFileInfo(path)

    if (fileInfo.is_dir) {
      // 是目录，直接跳转
      return { directoryPath: path, fileToPreview: null }
    } else {
      // 是文件，跳转到父目录并预览
      const parentPath = path.includes('/') ? path.substring(0, path.lastIndexOf('/')) : ''
      return { directoryPath: parentPath, fileToPreview: path }
    }
  } catch (error: any) {
    // 如果获取文件信息失败，尝试作为目录路径处理
    return { directoryPath: path, fileToPreview: null }
  }
}

// 导航到指定路径
const navigateToPath = (path: string) => {
  filesStore.navigateTo(path)
}

// 处理双击行
const handleRowDblClick = (row: FileInfo) => {
  if (row.is_dir) {
    filesStore.enterDirectory(row)
  } else if (row.is_previewable) {
    handlePreview(row)
  }
}

// 处理名称点击
const handleNameClick = (row: FileInfo) => {
  if (row.is_dir) {
    filesStore.enterDirectory(row)
  } else if (row.is_previewable) {
    handlePreview(row)
  }
}

// 处理预览
const handlePreview = (file: FileInfo) => {
  currentPreviewFile.value = file
  showPreviewDialog.value = true
}

// 处理删除
const handleDelete = async (file: FileInfo) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除 "${file.name}" 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await deleteFile(file.path)
    ElMessage.success('删除成功')
    await filesStore.loadFiles(filesStore.currentPath)
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 处理下载
const handleDownload = async (file: FileInfo) => {
  try {
    const { downloadFile, downloadFolder } = await import('@/api/files')

    if (file.is_dir) {
      // 下载文件夹（ZIP）
      ElMessage.info('正在压缩文件夹，请稍候...')
      await downloadFolder(file.path, `${file.name}.zip`)
      ElMessage.success('下载成功')
    } else {
      // 下载文件
      await downloadFile(file.path, file.name)
      ElMessage.success('下载成功')
    }
  } catch (error: any) {
    if (error.response?.status === 413) {
      ElMessage.error('文件夹过大，无法下载')
    } else {
      ElMessage.error(error.response?.data?.detail || error.message || '下载失败')
    }
  }
}

// 刷新
const refresh = () => {
  filesStore.loadFiles(filesStore.currentPath)
}

onMounted(() => {
  filesStore.loadFiles()
})
</script>

<style scoped>
.file-browser {
  display: flex;
  flex-direction: column;
  height: 100%;
  gap: 16px;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 4px;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.path-input {
  width: 300px;
}

.actions {
  display: flex;
  gap: 8px;
}

.file-list {
  flex: 1;
  overflow: auto;
}

.file-name {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
  padding: 4px 0;
}

.file-name:hover {
  color: #409EFF;
}

.file-name:active {
  transform: scale(0.98);
}

:deep(.el-breadcrumb__item) {
  cursor: pointer;
}

:deep(.el-breadcrumb__item:hover .el-breadcrumb__inner) {
  color: #409EFF;
}
</style>
