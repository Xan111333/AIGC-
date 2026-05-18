<template>
  <AppLayout pageTitle="学习资源" pageSubtitle="探索 AI 学习内容，提升创作技能">
    <div class="resource-center-content">
      <div class="header-actions">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索资源..."
          prefix-icon="Search"
          class="search-input"
          style="width: 300px;"
          @keyup.enter="handleSearch"
        />
        <el-button
          v-if="isTeacher"
          type="primary"
          class="gradient-btn"
          @click="showUploadModal = true"
        >上传资源</el-button>
      </div>

      <div class="category-tabs">
        <el-tabs v-model="activeCategory" @tab-click="handleCategoryChange">
          <el-tab-pane label="全部" name="all"></el-tab-pane>
          <el-tab-pane v-for="cat in categories" :key="cat.id" :label="cat.name" :name="cat.id"></el-tab-pane>
        </el-tabs>
      </div>

      <div v-if="resources.length === 0" class="empty-state glass-card">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
        <p>暂无学习资源</p>
        <p v-if="isTeacher" class="empty-hint">点击上方按钮上传资源</p>
      </div>

      <div v-else class="resource-grid">
        <div
          v-for="resource in resources"
          :key="resource.id"
          class="resource-card glass-card"
          @click="showResourceDetail(resource)"
        >
          <div class="resource-cover">
            <img :src="resource.cover_url" :alt="resource.title" />
            <div class="category-badge">{{ resource.category_name }}</div>
          </div>
          <div class="resource-info">
            <h3 class="resource-title">{{ resource.title }}</h3>
            <p class="resource-desc">{{ resource.description }}</p>
            <div class="resource-meta">
              <span class="uploader">{{ resource.uploader_name }}</span>
              <span class="views">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
                </svg>
                {{ resource.view_count }}
              </span>
            </div>
          </div>
          <div class="resource-actions">
            <el-button v-if="resource.file_url" size="small" @click.stop="downloadResource(resource)">下载</el-button>
            <el-button size="small" type="primary" @click.stop="showResourceDetail(resource)">查看</el-button>
            <el-button
              v-if="isTeacher"
              size="small"
              type="danger"
              @click.stop="deleteResource(resource.id)"
            >删除</el-button>
          </div>
        </div>
      </div>

      <el-dialog title="资源详情" :visible.sync="showDetailModal" width="600px">
        <div v-if="selectedResource" class="resource-detail">
          <img :src="selectedResource.cover_url" :alt="selectedResource.title" class="detail-cover" />
          <h2>{{ selectedResource.title }}</h2>
          <div class="detail-meta">
            <el-tag size="small">{{ selectedResource.category_name }}</el-tag>
            <span>上传者: {{ selectedResource.uploader_name }}</span>
            <span>浏览量: {{ selectedResource.view_count }}</span>
          </div>
          <p class="detail-desc">{{ selectedResource.description }}</p>
          <div class="detail-actions">
            <el-button v-if="selectedResource.file_url" type="primary" class="gradient-btn" @click="downloadResource(selectedResource)">下载资源</el-button>
          </div>
        </div>
      </el-dialog>

      <el-dialog title="上传资源" :visible.sync="showUploadModal" width="500px">
        <el-form :model="uploadForm" label-width="100px">
          <el-form-item label="资源标题">
            <el-input v-model="uploadForm.title" placeholder="请输入资源标题" />
          </el-form-item>
          <el-form-item label="资源描述">
            <el-input v-model="uploadForm.description" type="textarea" placeholder="请输入资源描述" :rows="3" />
          </el-form-item>
          <el-form-item label="资源分类">
            <el-select v-model="uploadForm.category" style="width: 100%;">
              <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="资源链接">
            <el-input v-model="uploadForm.file_url" placeholder="请输入资源文件链接" />
          </el-form-item>
          <el-form-item label="封面链接">
            <el-input v-model="uploadForm.cover_url" placeholder="请输入封面图片链接（可选）" />
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="showUploadModal = false">取消</el-button>
          <el-button type="primary" class="gradient-btn" @click="handleUpload">上传</el-button>
        </div>
      </el-dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import API from '../api'
import AppLayout from '../components/AppLayout.vue'

const resources = ref([])
const categories = ref([])
const activeCategory = ref('all')
const searchKeyword = ref('')
const showDetailModal = ref(false)
const showUploadModal = ref(false)
const selectedResource = ref(null)
const isTeacher = ref(false)

const uploadForm = reactive({
  title: '',
  description: '',
  category: 'document',
  file_url: '',
  cover_url: ''
})

const mockResources = [
  {
    id: 1,
    title: 'AIGC文本生成入门教程',
    description: '从零开始学习AIGC文本生成技术，包括提示词设计、参数调优、应用场景等内容。',
    category: 'tutorial',
    category_name: '教程',
    file_url: '',
    cover_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=AI%20text%20generation%20tutorial%20cover&image_size=landscape_16_9',
    uploader_id: 1,
    uploader_name: '张老师',
    view_count: 156,
    created_at: '2024-01-15T10:00:00'
  },
  {
    id: 2,
    title: '图像生成实战案例集',
    description: '包含10个经典图像生成案例，涵盖风格迁移、超分辨率、图像修复等技术。',
    category: 'case',
    category_name: '案例',
    file_url: '',
    cover_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=AI%20image%20generation%20case%20study&image_size=landscape_16_9',
    uploader_id: 1,
    uploader_name: '李老师',
    view_count: 89,
    created_at: '2024-01-18T14:30:00'
  },
  {
    id: 3,
    title: 'AIGC技术白皮书',
    description: '全面介绍AIGC技术原理、发展趋势和应用前景的权威文档。',
    category: 'document',
    category_name: '文档',
    file_url: '',
    cover_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=technical%20whitepaper%20AI%20technology&image_size=landscape_16_9',
    uploader_id: 2,
    uploader_name: '王教授',
    view_count: 234,
    created_at: '2024-01-20T09:00:00'
  },
  {
    id: 4,
    title: '视频生成技术详解',
    description: '深入讲解AI视频生成技术原理，包含多个实战演示视频。',
    category: 'video',
    category_name: '视频',
    file_url: '',
    cover_url: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=AI%20video%20generation%20technology&image_size=landscape_16_9',
    uploader_id: 1,
    uploader_name: '张老师',
    view_count: 178,
    created_at: '2024-01-22T16:00:00'
  }
]

const loadResources = async () => {
  try {
    const result = await API.getResources(activeCategory.value === 'all' ? null : activeCategory.value)
    resources.value = result
  } catch (error) {
    console.error('Load resources error:', error)
    resources.value = mockResources.filter(r => activeCategory.value === 'all' || r.category === activeCategory.value)
  }
}

const loadCategories = async () => {
  try {
    const result = await API.getResourceCategories()
    categories.value = result
  } catch (error) {
    console.error('Load categories error:', error)
    categories.value = [
      { id: 'tutorial', name: '教程' },
      { id: 'case', name: '案例' },
      { id: 'document', name: '文档' },
      { id: 'video', name: '视频' }
    ]
  }
}

const checkRole = () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  isTeacher.value = user.role === 'teacher' || user.role === 'admin'
}

const handleSearch = () => {
  if (!searchKeyword.value.trim()) {
    loadResources()
    return
  }

  const keyword = searchKeyword.value.toLowerCase()
  resources.value = mockResources.filter(r =>
    r.title.toLowerCase().includes(keyword) ||
    r.description.toLowerCase().includes(keyword)
  )
}

const handleCategoryChange = () => {
  loadResources()
}

const showResourceDetail = async (resource) => {
  try {
    selectedResource.value = await API.getResource(resource.id)
  } catch (error) {
    selectedResource.value = resource
  }
  showDetailModal.value = true
}

const downloadResource = (resource) => {
  if (resource.file_url) {
    const link = document.createElement('a')
    link.href = resource.file_url
    link.download = resource.title
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    ElMessage.success('下载成功')
  } else {
    ElMessage.info('该资源暂无下载链接')
  }
}

const handleUpload = async () => {
  if (!uploadForm.title.trim()) {
    ElMessage.error('请输入资源标题')
    return
  }

  try {
    await API.createResource({
      title: uploadForm.title,
      description: uploadForm.description,
      category: uploadForm.category,
      file_url: uploadForm.file_url || undefined,
      cover_url: uploadForm.cover_url || undefined
    })

    ElMessage.success('上传成功')
    showUploadModal.value = false
    uploadForm.title = ''
    uploadForm.description = ''
    uploadForm.category = 'document'
    uploadForm.file_url = ''
    uploadForm.cover_url = ''
    loadResources()
  } catch (error) {
    ElMessage.error('上传失败')
  }
}

const deleteResource = async (resourceId) => {
  try {
    await API.deleteResource(resourceId)
    ElMessage.success('删除成功')
    loadResources()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  checkRole()
  loadCategories()
  loadResources()
})
</script>

<style scoped>
.resource-center-content {
  padding: 0;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 16px;
}

.search-input {
  width: 300px;
}

.gradient-btn {
  background: var(--gradient-primary);
  border: none;
  font-weight: 500;
}

.category-tabs {
  margin-bottom: 24px;
}

:deep(.el-tabs__item) {
  color: var(--color-text-secondary) !important;
}

:deep(.el-tabs__item.is-active) {
  color: var(--color-primary-light) !important;
}

:deep(.el-tabs__active-bar) {
  background: var(--gradient-primary) !important;
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

.resource-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.resource-card {
  overflow: hidden;
  transition: all 0.3s;
  cursor: pointer;
}

.resource-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: rgba(99, 102, 241, 0.3);
}

.resource-cover {
  position: relative;
  height: 180px;
  overflow: hidden;
  margin: -24px -24px 16px;
}

.resource-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.category-badge {
  position: absolute;
  top: 16px;
  left: 16px;
  background: rgba(15, 15, 35, 0.8);
  backdrop-filter: blur(10px);
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.resource-info {
  margin-bottom: 16px;
}

.resource-title {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.resource-desc {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.resource-meta {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: var(--color-text-muted);
}

.views {
  display: flex;
  align-items: center;
  gap: 4px;
}

.resource-actions {
  display: flex;
  gap: 8px;
}

.resource-detail {
  padding: 10px 0;
}

.detail-cover {
  width: 100%;
  height: 250px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 16px;
}

.resource-detail h2 {
  margin: 0 0 16px 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.detail-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  font-size: 14px;
  color: var(--color-text-muted);
  align-items: center;
}

.detail-desc {
  line-height: 1.8;
  color: var(--color-text-secondary);
  margin-bottom: 20px;
}

.detail-actions {
  margin-top: 20px;
}

.dialog-footer {
  text-align: right;
}
</style>
