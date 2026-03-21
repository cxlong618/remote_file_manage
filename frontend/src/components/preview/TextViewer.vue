<template>
  <div class="text-viewer">
    <pre class="text-content">{{ content }}</pre>
  </div>
</template>

<script setup lang="ts">
interface Props {
  content: string
  fileName: string
}

defineProps<Props>()
</script>

<style scoped>
.text-viewer {
  width: 100%;
  height: 100%;
  overflow: auto;
  background: #f5f7fa;
  border-radius: 4px;
  padding: 16px;
}

.text-content {
  margin: 0;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
  color: #303133;
}
</style>
