<template>
  <div class="media-player">
    <video
      v-if="type === 'video' && src"
      :src="src"
      controls
      class="responsive-video"
      @loadeddata="handleLoaded"
      @error="handleError"
    >
      您的浏览器不支持视频播放
    </video>

    <audio
      v-else-if="type === 'audio' && src"
      :src="src"
      controls
      class="responsive-audio"
      @loadeddata="handleLoaded"
      @error="handleError"
    >
      您的浏览器不支持音频播放
    </audio>

    <div v-if="error" class="error-message">
      <el-icon :size="40" color="#F56C6C"><VideoPlay /></el-icon>
      <p>播放失败</p>
      <p class="error-hint">请检查文件格式是否支持</p>
    </div>

    <div v-if="!src && !error" class="loading-message">
      <el-icon :size="40" color="#409EFF"><Loading /></el-icon>
      <p>正在加载...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { VideoPlay, Loading } from '@element-plus/icons-vue'

interface Props {
  src: string
  type: 'video' | 'audio'
}

defineProps<Props>()

const error = ref(false)
const loaded = ref(false)

const handleLoaded = () => {
  loaded.value = true
  error.value = false
}

const handleError = (e: Event) => {
  console.error('媒体加载失败:', e)
  // 只有在真正无法加载时才显示错误
  const mediaElement = e.target as HTMLMediaElement
  if (mediaElement.error) {
    error.value = true
  }
}
</script>

<style scoped>
.media-player {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 300px;
  max-height: 70vh;
}

.responsive-video {
  max-width: 100%;
  max-height: 70vh;
  width: auto;
  height: auto;
}

.responsive-audio {
  width: 100%;
  max-width: 800px;
}

.error-message,
.loading-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 40px 20px;
}

.error-message {
  color: #F56C6C;
}

.loading-message {
  color: #409EFF;
}

.error-message p,
.loading-message p {
  margin: 0;
}

.error-hint {
  font-size: 14px;
  color: #909399;
  margin-top: -8px;
}
</style>
