<template>
  <AppLayout pageTitle="我的作品" pageSubtitle="管理和导出您的 AI 创作">
    <div class="my-works-content">
      <div class="header-actions">
        <el-select v-model="activeType" class="type-select" style="width: 150px;">
          <el-option label="全部" value="all" />
          <el-option label="文本" value="text" />
          <el-option label="图像" value="image" />
          <el-option label="视频" value="video" />
          <el-option label="音频" value="audio" />
        </el-select>
        <el-button
          type="primary"
          class="gradient-btn"
          @click="handleBatchExport"
          :disabled="selectedWorks.length === 0"
        >
          批量导出
        </el-button>
      </div>

      <div class="stats-row">
        <div class="stat-card glass-card">
          <div class="stat-icon text-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.text }}</div>
            <div class="stat-label">文本作品</div>
          </div>
        </div>
        <div class="stat-card glass-card">
          <div class="stat-icon image-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <circle cx="8.5" cy="8.5" r="1.5"></circle>
              <polyline points="21 15 16 10 5 21"></polyline>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.image }}</div>
            <div class="stat-label">图像作品</div>
          </div>
        </div>
        <div class="stat-card glass-card">
          <div class="stat-icon video-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="23 7 16 12 23 17 23 7"></polygon>
              <rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.video }}</div>
            <div class="stat-label">视频作品</div>
          </div>
        </div>
        <div class="stat-card glass-card">
          <div class="stat-icon audio-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
              <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
              <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.audio }}</div>
            <div class="stat-label">音频作品</div>
          </div>
        </div>
      </div>

      <div class="works-header">
        <div class="select-all">
          <el-checkbox
            v-model="selectAll"
            @change="handleSelectAll"
            :disabled="filteredWorks.length === 0"
          >全选</el-checkbox>
          <span v-if="filteredWorks.length > 0">已选 {{ selectedWorks.length }} 件</span>
        </div>
      </div>

      <div v-if="filteredWorks.length === 0" class="empty-state glass-card">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
          <polyline points="22 4 12 14.01 9 11.01"></polyline>
        </svg>
        <p>暂无作品</p>
        <p class="empty-hint">使用生成工具创建您的第一个作品</p>
      </div>

      <div v-else class="works-list">
        <div
          v-for="work in filteredWorks"
          :key="work.id"
          class="work-card glass-card"
        >
          <div class="work-checkbox">
            <el-checkbox
            v-model="selectedWorks"
            :label="work.id"
          ></el-checkbox>
          </div>

          <div class="work-preview">
            <div v-if="work.type === 'text'" class="text-preview">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
              </svg>
              <span class="preview-label">文本</span>
            </div>
            <div v-else-if="work.type === 'image'" class="image-preview">
              <img :src="work.url" :alt="work.title" />
            </div>
            <div v-else-if="work.type === 'video'" class="video-preview">
              <img :src="work.thumbnail || work.url" :alt="work.title" />
              <div class="play-overlay">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor" stroke="white" stroke-width="0">
                  <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
              </div>
            </div>
            <div v-else-if="work.type === 'audio'" class="audio-preview">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
              </svg>
              <span class="preview-label">音频</span>
            </div>
          </div>

          <div class="work-info">
            <h3 class="work-title">{{ work.title }}</h3>
            <p class="work-desc">{{ work.description }}</p>
            <div class="work-meta">
              <span class="work-type">{{ getTypeLabel(work.type) }}</span>
              <span class="work-date">{{ formatDate(work.created_at) }}</span>
            </div>
          </div>

          <div class="work-actions">
            <el-button size="small" @click="previewWork(work)">预览</el-button>
            <el-button size="small" type="primary" @click="downloadWork(work)">下载</el-button>
            <el-button size="small" type="danger" @click="deleteWork(work.id)">删除</el-button>
          </div>
        </div>
      </div>

      <el-dialog :title="previewWorkData?.title || '作品预览'" :visible.sync="showPreviewModal" width="700px">
        <div v-if="previewWorkData" class="preview-content">
          <div v-if="previewWorkData.type === 'text'" class="text-content">
            <pre>{{ previewWorkData.content }}</pre>
          </div>
          <div v-else-if="previewWorkData.type === 'image'" class="image-content">
            <img :src="previewWorkData.url" :alt="previewWorkData.title" />
          </div>
          <div v-else-if="previewWorkData.type === 'video'" class="video-content">
            <video :src="previewWorkData.url" controls class="preview-video">
              您的浏览器不支持视频播放
            </video>
          </div>
          <div v-else-if="previewWorkData.type === 'audio'" class="audio-content">
            <audio :src="previewWorkData.url" controls class="preview-audio">
              您的浏览器不支持音频播放
            </audio>
          </div>
          <div class="preview-actions">
            <el-button type="primary" class="gradient-btn" @click="downloadWork(previewWorkData)">下载作品</el-button>
          </div>
        </div>
      </el-dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import AppLayout from '../components/AppLayout.vue'

const works = ref([])
const activeType = ref('all')
const selectAll = ref(false)
const selectedWorks = ref([])
const showPreviewModal = ref(false)
const previewWorkData = ref(null)

const typeLabels = {
  text: '文本',
  image: '图像',
  video: '视频',
  audio: '音频'
}

const mockWorks = [
  {
    id: 1,
    title: 'AI技术发展趋势分析',
    description: '分析人工智能技术的最新发展趋势和未来展望',
    type: 'text',
    content: '人工智能技术正在深刻改变我们的生活方式。从智能家居到自动驾驶，AI已经渗透到各个领域。随着大语言模型的发展，自然语言处理能力得到了显著提升，使得智能助手能够理解和生成更加自然的语言。未来，人工智能将在更多方面发挥重要作用，为人类创造更加美好的未来。',
    url: '',
    thumbnail: '',
    created_at: '2024-01-15T10:30:00'
  },
  {
    id: 2,
    title: '风景摄影作品',
    description: '使用AI生成的美丽风景图片',
    type: 'image',
    content: '',
    url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=beautiful%20landscape%20with%20mountains%20and%20lake%20at%20sunset%20realistic&image_size=landscape_16_9',
    thumbnail: '',
    created_at: '2024-01-16T14:20:00'
  },
  {
    id: 3,
    title: '城市夜景',
    description: '赛博朋克风格的城市夜景',
    type: 'image',
    content: '',
    url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=futuristic%20city%20skyline%20at%20night%20cyberpunk%20style&image_size=landscape_16_9',
    thumbnail: '',
    created_at: '2024-01-17T09:45:00'
  },
  {
    id: 4,
    title: '产品介绍视频',
    description: 'AI生成的产品宣传视频',
    type: 'video',
    content: '',
    url: '',
    thumbnail: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=product%20video%20thumbnail%20modern%20tech&image_size=landscape_16_9',
    created_at: '2024-01-18T16:00:00'
  },
  {
    id: 5,
    title: '背景音乐',
    description: 'AI生成的舒缓背景音乐',
    type: 'audio',
    content: '',
    url: '',
    thumbnail: '',
    created_at: '2024-01-19T11:30:00'
  }
]

const stats = computed(() => ({
  text: works.value.filter(w => w.type === 'text').length,
  image: works.value.filter(w => w.type === 'image').length,
  video: works.value.filter(w => w.type === 'video').length,
  audio: works.value.filter(w => w.type === 'audio').length
}))

const filteredWorks = computed(() => {
  if (activeType.value === 'all') {
    return works.value
  }
  return works.value.filter(w => w.type === activeType.value)
})

const getTypeLabel = (type) => typeLabels[type] || type

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const loadWorks = () => {
  works.value = mockWorks
}

const handleSelectAll = (val) => {
  if (val) {
    selectedWorks.value = filteredWorks.value.map(w => w.id)
  } else {
    selectedWorks.value = []
  }
}

const previewWork = (work) => {
  previewWorkData.value = work
  showPreviewModal.value = true
}

const downloadWork = (work) => {
  if (work.type === 'text') {
    const blob = new Blob([work.content], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${work.title}.txt`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
    ElMessage.success('下载成功')
  } else if (work.type === 'image' && work.url) {
    const link = document.createElement('a')
    link.href = work.url
    link.download = `${work.title}.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    ElMessage.success('下载成功')
  } else {
    ElMessage.info('该作品暂无法下载')
  }
}

const deleteWork = (workId) => {
  const index = works.value.findIndex(w => w.id === workId)
  if (index !== -1) {
    works.value.splice(index, 1)
    const selectedIndex = selectedWorks.value.indexOf(workId)
    if (selectedIndex !== -1) {
      selectedWorks.value.splice(selectedIndex, 1)
    }
    ElMessage.success('删除成功')
  }
}

const handleBatchExport = () => {
  if (selectedWorks.value.length === 0) {
    ElMessage.error('请选择要导出的作品')
    return
  }

  const selectedData = works.value.filter(w => selectedWorks.value.includes(w.id))

  selectedData.forEach(work => {
    downloadWork(work)
  })

  ElMessage.success(`已导出 ${selectedData.length} 件作品`)
  selectedWorks.value = []
  selectAll.value = false
}

onMounted(() => {
  loadWorks()
})
</script>

<style scoped>
.my-works-content {
  padding: 0;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.type-select {
  width: 150px;
}

.gradient-btn {
  background: var(--gradient-primary);
  border: none;
  font-weight: 500;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.text-icon {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}

.image-icon {
  background: rgba(236, 72, 153, 0.2);
  color: #f472b6;
}

.video-icon {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.audio-icon {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.stat-label {
  font-size: 14px;
  color: var(--color-text-muted);
}

.works-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.select-all {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--color-text-secondary);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  color: var(--color-text-muted);
}

.empty-state svg {
  margin-bottom: 16px;
}

.empty-state p {
  margin: 0 0 8px 0;
}

.empty-hint {
  font-size: 14px;
}

.works-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.work-card {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s;
}

.work-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: rgba(99, 102, 241, 0.3);
}

.work-preview {
  width: 100px;
  height: 100px;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
}

.text-preview,
.audio-preview {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-glass);
  color: var(--color-text-muted);
}

.text-preview svg,
.audio-preview svg {
  width: 40px;
  height: 40px;
}

.preview-label {
  font-size: 12px;
  margin-top: 4px;
}

.image-preview img,
.video-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-preview {
  position: relative;
}

.play-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 40px;
  height: 40px;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.work-info {
  flex: 1;
  min-width: 0;
}

.work-title {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.work-desc {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: var(--color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.work-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: var(--color-text-muted);
}

.work-type {
  background: var(--color-bg-glass);
  padding: 2px 8px;
  border-radius: 4px;
}

.work-actions {
  display: flex;
  gap: 8px;
}

.preview-content {
  padding: 10px 0;
}

.text-content pre {
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 400px;
  overflow-y: auto;
  padding: 16px;
  background: var(--color-bg-main);
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-text-secondary);
}

.image-content img {
  max-width: 100%;
  max-height: 400px;
  object-fit: contain;
  border-radius: 8px;
}

.video-content,
.audio-content {
  display: flex;
  justify-content: center;
}

.preview-video {
  width: 100%;
  max-height: 400px;
  border-radius: 8px;
}

.preview-audio {
  width: 100%;
}

.preview-actions {
  margin-top: 20px;
  text-align: right;
}
</style>
