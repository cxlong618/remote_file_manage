/**
 * 格式化文件大小
 */
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

/**
 * 格式化日期时间
 */
export const formatDateTime = (dateString: string): string => {
  const date = new Date(dateString)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}`
}

/**
 * 获取文件图标
 */
export const getFileIcon = (file: { is_dir: boolean; name: string; preview_type?: string }): string => {
  if (file.is_dir) {
    return 'Folder'
  }

  const ext = file.name.split('.').pop()?.toLowerCase()

  switch (file.preview_type) {
    case 'image':
      return 'Picture'
    case 'video':
      return 'VideoCamera'
    case 'audio':
      return 'Headset'
    case 'markdown':
      return 'Document'
    case 'text':
      return 'DocumentCopy'
    default:
      // 根据扩展名返回图标
      switch (ext) {
        case 'pdf':
          return 'Reading'
        case 'zip':
        case 'rar':
        case '7z':
          return 'Box'
        case 'js':
        case 'ts':
        case 'py':
        case 'java':
          return 'Code'
        default:
          return 'Document'
      }
  }
}

/**
 * 判断是否为图片文件
 */
export const isImageFile = (file: { name: string; preview_type?: string }): boolean => {
  return file.preview_type === 'image'
}

/**
 * 判断是否为视频文件
 */
export const isVideoFile = (file: { name: string; preview_type?: string }): boolean => {
  return file.preview_type === 'video'
}

/**
 * 判断是否为音频文件
 */
export const isAudioFile = (file: { name: string; preview_type?: string }): boolean => {
  return file.preview_type === 'audio'
}

/**
 * 判断是否为Markdown文件
 */
export const isMarkdownFile = (file: { name: string; preview_type?: string }): boolean => {
  return file.preview_type === 'markdown'
}

/**
 * 判断是否为文本文件
 */
export const isTextFile = (file: { name: string; preview_type?: string }): boolean => {
  return file.preview_type === 'text' || file.preview_type === 'markdown'
}
