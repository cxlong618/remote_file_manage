<template>
  <el-dialog
    v-model="dialogVisible"
    :title="file?.name || '预览'"
    width="80%"
    top="5vh"
    destroy-on-close
  >
    <div class="preview-container" v-loading="loading">
      <!-- Markdown预览 -->
      <MarkdownViewer
        v-if="file?.preview_type === 'markdown' && content"
        :content="content"
      />

      <!-- 图片预览 -->
      <ImageViewer
        v-else-if="file?.preview_type === 'image'"
        :src="mediaBlobUrl"
      />

      <!-- 视频播放器 -->
      <MediaPlayer
        v-else-if="file?.preview_type === 'video'"
        :src="mediaBlobUrl"
        type="video"
      />

      <!-- 音频播放器 -->
      <MediaPlayer
        v-else-if="file?.preview_type === 'audio'"
        :src="mediaBlobUrl"
        type="audio"
      />

      <!-- 文本预览 -->
      <TextViewer
        v-else-if="file?.preview_type === 'text' && content"
        :content="content"
        :file-name="file?.name"
      />

      <!-- 不支持的类型 -->
      <div v-else-if="!loading" class="no-preview">
        <el-icon :size="60" color="#909399"><Warning /></el-icon>
        <p>该文件类型不支持预览</p>
        <el-button type="primary" @click="handleDownload">
          下载文件
        </el-button>
      </div>
    </div>

    <template #footer>
      <el-button @click="dialogVisible = false">关闭</el-button>
      <el-button
        v-if="file?.preview_type !== 'image'"
        type="primary"
        @click="handleDownload"
      >
        下载文件
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Warning } from '@element-plus/icons-vue'
import { previewText, getMediaBlobUrl, downloadFile } from '@/api/files'
import MarkdownViewer from './preview/MarkdownViewer.vue'
import ImageViewer from './preview/ImageViewer.vue'
import MediaPlayer from './preview/MediaPlayer.vue'
import TextViewer from './preview/TextViewer.vue'
import type { FileInfo } from '@/types'

interface Props {
  visible: boolean
  file: FileInfo | null
}

interface Emits {
  (e: 'update:visible', value: boolean): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const loading = ref(false)
const content = ref('')
const mediaBlobUrl = ref<string>('')

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

// 监听文件变化，加载内容
watch(() => props.file, async (newFile) => {
  // 清理旧的 Blob URL
  if (mediaBlobUrl.value) {
    window.URL.revokeObjectURL(mediaBlobUrl.value)
    mediaBlobUrl.value = ''
  }

  if (newFile && (newFile.preview_type === 'markdown' || newFile.preview_type === 'text')) {
    await loadContent()
  } else if (newFile && ['image', 'video', 'audio'].includes(newFile.preview_type || '')) {
    // 加载媒体文件的 Blob URL
    await loadMediaBlob()
  } else {
    content.value = ''
  }
})

// 加载媒体 Blob URL
const loadMediaBlob = async () => {
  if (!props.file) return

  loading.value = true
  try {
    mediaBlobUrl.value = await getMediaBlobUrl(props.file.path)
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || error.message || '加载媒体失败')
  } finally {
    loading.value = false
  }
}

// 加载文本内容
const loadContent = async () => {
  if (!props.file) return

  loading.value = true
  try {
    const response = await previewText(props.file.path)
    content.value = response.content
  } catch (error: any) {
    ElMessage.error(error.message || '加载文件失败')
    content.value = ''
  } finally {
    loading.value = false
  }
}

// 下载文件
const handleDownload = async () => {
  if (!props.file) return

  try {
    loading.value = true
    await downloadFile(props.file.path, props.file.name)
    ElMessage.success('下载成功')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || error.message || '下载失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.preview-container {
  min-height: 400px;
  max-height: 70vh;
  overflow: auto;
}

.no-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 16px;
  color: #909399;
}

.no-preview p {
  margin: 0;
  font-size: 16px;
}
</style>
