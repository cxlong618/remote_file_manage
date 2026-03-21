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
          placeholder="输入路径快速跳转"
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
            <div class="file-name">
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

        <el-table-column label="操作" width="260" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.is_dir"
              type="primary"
              size="small"
              :icon="FolderOpened"
              @click="filesStore.enterDirectory(row)"
            >
              打开
            </el-button>

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
  Delete
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
const handlePathInput = () => {
  if (pathInput.value.trim()) {
    filesStore.navigateTo(pathInput.value.trim())
    pathInput.value = ''
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
}

.file-name:hover {
  color: #409EFF;
}

:deep(.el-breadcrumb__item) {
  cursor: pointer;
}

:deep(.el-breadcrumb__item:hover .el-breadcrumb__inner) {
  color: #409EFF;
}
</style>
