<template>
  <div class="markdown-viewer" v-html="renderedHtml"></div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'

interface Props {
  content: string
}

const props = defineProps<Props>()

// 配置marked
marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value
      } catch (err) {}
    }
    return hljs.highlightAuto(code).value
  },
  breaks: true,
  gfm: true
})

const renderedHtml = computed(() => {
  return marked(props.content)
})
</script>

<style scoped>
.markdown-viewer {
  padding: 16px;
  background: #1e1e1e;
  border-radius: 4px;
  color: #d4d4d4;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
  overflow: auto;
}

.markdown-viewer :deep(h1),
.markdown-viewer :deep(h2),
.markdown-viewer :deep(h3),
.markdown-viewer :deep(h4),
.markdown-viewer :deep(h5),
.markdown-viewer :deep(h6) {
  color: #fff;
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
}

.markdown-viewer :deep(h1) {
  font-size: 2em;
  border-bottom: 1px solid #3e3e3e;
  padding-bottom: 8px;
}

.markdown-viewer :deep(h2) {
  font-size: 1.5em;
  border-bottom: 1px solid #3e3e3e;
  padding-bottom: 8px;
}

.markdown-viewer :deep(p) {
  margin: 16px 0;
}

.markdown-viewer :deep(code) {
  background: #2d2d2d;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}

.markdown-viewer :deep(pre) {
  background: #2d2d2d;
  padding: 16px;
  border-radius: 4px;
  overflow-x: auto;
  margin: 16px 0;
}

.markdown-viewer :deep(pre code) {
  background: transparent;
  padding: 0;
}

.markdown-viewer :deep(blockquote) {
  border-left: 4px solid #4CAF50;
  padding-left: 16px;
  margin: 16px 0;
  color: #9cdcfe;
}

.markdown-viewer :deep(ul),
.markdown-viewer :deep(ol) {
  margin: 16px 0;
  padding-left: 32px;
}

.markdown-viewer :deep(li) {
  margin: 8px 0;
}

.markdown-viewer :deep(a) {
  color: #4CAF50;
  text-decoration: none;
}

.markdown-viewer :deep(a:hover) {
  text-decoration: underline;
}

.markdown-viewer :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 16px 0;
}

.markdown-viewer :deep(th),
.markdown-viewer :deep(td) {
  border: 1px solid #3e3e3e;
  padding: 8px 12px;
  text-align: left;
}

.markdown-viewer :deep(th) {
  background: #2d2d2d;
  font-weight: 600;
}

.markdown-viewer :deep(img) {
  max-width: 100%;
  height: auto;
}
</style>
