<template>
  <el-dialog
    v-model="dialogVisible"
    title="上传文件"
    width="600px"
    @close="handleClose"
  >
    <el-upload
      ref="uploadRef"
      class="upload-demo"
      drag
      :action="uploadUrl"
      :headers="uploadHeaders"
      :on-progress="handleProgress"
      :on-success="handleSuccess"
      :on-error="handleError"
      :before-upload="beforeUpload"
      :file-list="fileList"
      multiple
      :auto-upload="false"
    >
      <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
      <div class="el-upload__text">
        将文件拖到此处，或<em>点击上传</em>
      </div>
      <template #tip>
        <div class="el-upload__tip">
          支持任意格式文件，单个文件不超过 100MB
        </div>
      </template>
    </el-upload>

    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button
        type="primary"
        :loading="uploading"
        @click="handleUpload"
      >
        {{ uploading ? '上传中...' : '开始上传' }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import type { UploadInstance, UploadProps, UploadUserFile, UploadRawFile } from 'element-plus'
import { uploadFile } from '@/api/upload'

interface Props {
  visible: boolean
  currentPath: string
}

interface Emits {
  (e: 'update:visible', value: boolean): void
  (e: 'success'): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const uploadRef = ref<UploadInstance>()
const fileList = ref<UploadUserFile[]>([])
const uploading = ref(false)

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const uploadUrl = computed(() => {
  return `/api/upload/?path=${encodeURIComponent(props.currentPath)}`
})

const uploadHeaders = computed(() => {
  const token = localStorage.getItem('token')
  return {
    Authorization: `Bearer ${token}`
  }
})

const beforeUpload = (rawFile: UploadRawFile) => {
  const maxSize = 100 * 1024 * 1024 // 100MB
  if (rawFile.size > maxSize) {
    ElMessage.error('文件大小不能超过 100MB')
    return false
  }
  return true
}

const handleProgress: UploadProps['onProgress'] = (evt) => {
  console.log('上传进度:', evt.percent)
}

const handleSuccess = (response: any) => {
  if (response.success) {
    ElMessage.success(`${response.file_name} 上传成功`)
  }
}

const handleError = (error: any) => {
  ElMessage.error('上传失败: ' + error.message)
}

const handleUpload = async () => {
  if (fileList.value.length === 0) {
    ElMessage.warning('请选择要上传的文件')
    return
  }

  uploading.value = true

  try {
    // 手动上传所有文件
    const files = uploadRef.value?.uploadFiles || []
    for (const file of files) {
      if (file.status === 'ready') {
        const rawFile = file.raw as File
        await uploadFile(rawFile, props.currentPath, (percent) => {
          file.percentage = percent
        })
      }
    }

    ElMessage.success('所有文件上传完成')
    emit('success')
    handleClose()
  } catch (error: any) {
    ElMessage.error('上传失败: ' + error.message)
  } finally {
    uploading.value = false
  }
}

const handleClose = () => {
  fileList.value = []
  uploadRef.value?.clearFiles()
  dialogVisible.value = false
}
</script>

<style scoped>
.upload-demo {
  width: 100%;
}

.el-icon--upload {
  font-size: 67px;
  color: #409EFF;
  margin: 20px 0;
}

.el-upload__text {
  font-size: 14px;
  color: #606266;
}

.el-upload__text em {
  color: #409EFF;
  font-style: normal;
}

.el-upload__tip {
  margin-top: 12px;
  font-size: 12px;
  color: #909399;
}
</style>
