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
        :src="mediaUrl"
      />

      <!-- 视频播放器 -->
      <MediaPlayer
        v-else-if="file?.preview_type === 'video'"
        :src="mediaUrl"
        type="video"
      />

      <!-- 音频播放器 -->
      <MediaPlayer
        v-else-if="file?.preview_type === 'audio'"
        :src="mediaUrl"
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
import { previewText, getMediaUrl, getDownloadUrl } from '@/api/files'
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

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const mediaUrl = computed(() => {
  if (!props.file) return ''
  return getMediaUrl(props.file.path)
})

// 监听文件变化，加载内容
watch(() => props.file, async (newFile) => {
  if (newFile && (newFile.preview_type === 'markdown' || newFile.preview_type === 'text')) {
    await loadContent()
  } else {
    content.value = ''
  }
})

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
const handleDownload = () => {
  if (!props.file) return

  const url = getDownloadUrl(props.file.path)
  const link = document.createElement('a')
  link.href = url
  link.download = props.file.name
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
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
