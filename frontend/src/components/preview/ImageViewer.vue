<template>
  <div class="image-viewer">
    <el-image
      :src="src"
      fit="contain"
      :preview-src-list="[src]"
      class="responsive-image"
    >
      <template #placeholder>
        <div class="image-placeholder">
          <el-icon :size="40"><Loading /></el-icon>
          <p>加载中...</p>
        </div>
      </template>

      <template #error>
        <div class="image-error">
          <el-icon :size="40"><PictureFilled /></el-icon>
          <p>加载失败</p>
        </div>
      </template>
    </el-image>
  </div>
</template>

<script setup lang="ts">
import { Loading, PictureFilled } from '@element-plus/icons-vue'

interface Props {
  src: string
}

defineProps<Props>()
</script>

<style scoped>
.image-viewer {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  max-height: 70vh;
}

.responsive-image {
  max-width: 100%;
  max-height: 70vh;
  width: auto;
  height: auto;
}

.image-placeholder,
.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: #909399;
}

.image-placeholder p,
.image-error p {
  margin: 0;
}
</style>
