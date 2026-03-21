<template>
  <div class="media-player">
    <video
      v-if="type === 'video'"
      :src="src"
      controls
      style="width: 100%; height: auto"
      @error="handleError"
    >
      您的浏览器不支持视频播放
    </video>

    <audio
      v-else-if="type === 'audio'"
      :src="src"
      controls
      style="width: 100%"
      @error="handleError"
    >
      您的浏览器不支持音频播放
    </audio>

    <div v-if="error" class="error-message">
      <el-icon :size="40" color="#F56C6C"><VideoPlay /></el-icon>
      <p>播放失败</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { VideoPlay } from '@element-plus/icons-vue'

interface Props {
  src: string
  type: 'video' | 'audio'
}

defineProps<Props>()

const error = ref(false)

const handleError = () => {
  error.value = true
}
</script>

<style scoped>
.media-player {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.error-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: #F56C6C;
}

.error-message p {
  margin: 0;
}
</style>
