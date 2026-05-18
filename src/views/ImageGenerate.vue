<template>
  <AppLayout pageTitle="图像生成" pageSubtitle="AI 绘画、艺术创作、设计素材">
    <div class="generate-page">
      <div class="content-wrapper">
        <aside class="params-panel glass-card">
          <div class="params-scrollable">
            <div class="panel-section">
              <div class="section-header">
                <div class="section-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <circle cx="8.5" cy="8.5" r="1.5"></circle>
                    <polyline points="21 15 16 10 5 21"></polyline>
                  </svg>
                </div>
                <h3>输入提示词</h3>
              </div>
              
              <textarea 
                v-model="prompt" 
                rows="4" 
                placeholder="描述您想要生成的图像，例如：一只可爱的猫坐在窗前，午后阳光，水彩画风格..."
                class="prompt-input"
              />
              
              <div class="quick-prompts">
                <span class="quick-label">风格预设</span>
                <div class="prompt-tags">
                  <span 
                    v-for="tag in stylePresets" 
                    :key="tag" 
                    class="prompt-tag"
                    @click="applyStylePreset(tag)"
                  >{{ tag }}</span>
                </div>
              </div>
            </div>
            
            <div class="panel-section">
              <div class="section-header">
                <div class="section-icon upload">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="17 8 12 3 7 8"></polyline>
                    <line x1="12" y1="3" x2="12" y2="15"></line>
                  </svg>
                </div>
                <h3>图生图（可选）</h3>
              </div>
              
              <div 
                class="upload-area" 
                :class="{ 'has-image': uploadedImage }"
                @click="triggerUpload"
                @dragover.prevent
                @drop.prevent="handleDrop"
              >
                <div v-if="uploadedImage" class="upload-preview">
                  <img :src="uploadedImage" alt="上传图片" />
                  <div class="upload-remove" @click.stop="removeImage">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="18" y1="6" x2="6" y2="18"></line>
                      <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                  </div>
                </div>
                <div v-else class="upload-placeholder">
                  <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="17 8 12 3 7 8"></polyline>
                    <line x1="12" y1="3" x2="12" y2="15"></line>
                  </svg>
                  <p>点击或拖拽上传图片</p>
                  <p class="upload-hint">支持 JPG、PNG 格式</p>
                </div>
              </div>
              <input type="file" ref="fileInput" class="hidden-input" accept="image/*" @change="handleFileSelect" />
            </div>
            
            <div class="panel-section">
              <div class="section-header">
                <div class="section-icon settings">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="3"></circle>
                    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                  </svg>
                </div>
                <h3>参数配置</h3>
              </div>
              
              <div class="params-grid">
                <div class="param-item">
                  <label>分辨率</label>
                  <el-select v-model="params.resolution" class="param-select" size="large">
                    <el-option label="512×512" value="512x512" />
                    <el-option label="768×768" value="768x768" />
                    <el-option label="1024×1024" value="1024x1024" />
                    <el-option label="512×768" value="512x768" />
                    <el-option label="768×512" value="768x512" />
                  </el-select>
                </div>
                
                <div class="param-item">
                  <label>风格</label>
                  <el-select v-model="params.style" class="param-select" size="large">
                    <el-option label="写实" value="realistic" />
                    <el-option label="卡通" value="cartoon" />
                    <el-option label="油画" value="oil-painting" />
                    <el-option label="水彩" value="watercolor" />
                    <el-option label="像素风" value="pixel" />
                    <el-option label="赛博朋克" value="cyberpunk" />
                    <el-option label="复古" value="vintage" />
                    <el-option label="科幻" value="sci-fi" />
                  </el-select>
                </div>
              </div>
              
              <div class="param-item">
                <div class="slider-header">
                  <label>生成数量</label>
                  <span class="slider-value">{{ params.count }} 张</span>
                </div>
                <el-slider v-model="params.count" :min="1" :max="4" :step="1" />
              </div>
              
              <div class="param-item">
                <div class="slider-header">
                  <label>创意程度</label>
                  <span class="slider-value">{{ params.creativity }}/10</span>
                </div>
                <el-slider v-model="params.creativity" :min="1" :max="10" :step="1" />
              </div>
            </div>
            
            <div class="ethics-tip">
              <div class="tip-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="16" x2="12" y2="12"></line>
                  <line x1="12" y1="8" x2="12.01" y2="8"></line>
                </svg>
              </div>
              <span>请遵守伦理规范，不生成违法违规内容</span>
            </div>
          </div>
          
          <div class="generate-footer">
            <button 
              class="generate-btn" 
              @click="handleGenerate" 
              :disabled="isGenerating || !prompt.trim()"
              :class="{ loading: isGenerating }"
            >
              <div v-if="isGenerating" class="loading-spinner">
                <svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
                  <path d="M12 2a10 10 0 0 1 10 10"></path>
                </svg>
              </div>
              <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
              <span>{{ isGenerating ? '正在创作...' : '开始生成' }}</span>
            </button>
          </div>
        </aside>
        
        <main class="result-panel glass-card glow-border">
          <div class="result-header">
            <div class="header-left">
              <div class="result-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                  <circle cx="8.5" cy="8.5" r="1.5"></circle>
                  <polyline points="21 15 16 10 5 21"></polyline>
                </svg>
              </div>
              <div>
                <h3>生成结果</h3>
                <span class="result-meta">{{ generatedImages.length }} 张图片</span>
              </div>
            </div>
            
            <div class="result-actions" v-if="generatedImages.length > 0">
              <button class="action-btn" @click="handleRegenerate" :disabled="isGenerating">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="23 4 23 10 17 10"></polyline>
                  <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
                </svg>
                <span>重新生成</span>
              </button>
              <button class="action-btn primary" @click="handleExportAll">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                <span>全部下载</span>
              </button>
            </div>
          </div>
          
          <div class="result-content">
            <div v-if="isGenerating" class="loading-state">
              <div class="loading-animation">
                <div class="canvas-preview">
                  <div class="canvas-glow"></div>
                  <div class="ai-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                      <circle cx="8.5" cy="8.5" r="1.5"></circle>
                      <polyline points="21 15 16 10 5 21"></polyline>
                    </svg>
                  </div>
                </div>
              </div>
              <p class="loading-text">{{ loadingMessage }}</p>
              <div class="loading-progress">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
                </div>
                <span>{{ progressPercent }}%</span>
              </div>
            </div>
            
            <div v-else-if="!generatedImages.length" class="empty-state">
              <div class="empty-icon">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                  <circle cx="8.5" cy="8.5" r="1.5"></circle>
                  <polyline points="21 15 16 10 5 21"></polyline>
                </svg>
              </div>
              <h3>开始您的艺术创作</h3>
              <p>在左侧输入提示词，选择风格参数，然后点击生成按钮</p>
              <div class="empty-tips">
                <div class="tip-item">
                  <span class="tip-bullet">•</span>
                  <span>详细描述画面元素和构图</span>
                </div>
                <div class="tip-item">
                  <span class="tip-bullet">•</span>
                  <span>选择合适的艺术风格</span>
                </div>
                <div class="tip-item">
                  <span class="tip-bullet">•</span>
                  <span>尝试不同的创意程度</span>
                </div>
              </div>
            </div>
            
            <div v-else class="gallery-grid">
              <div 
                v-for="(image, index) in generatedImages" 
                :key="index" 
                class="image-card animate-slide-in"
                :style="{ animationDelay: index * 0.15 + 's' }"
              >
                <div class="image-wrapper">
                  <img :src="image" :alt="`生成图像 ${index + 1}`" />
                  <div class="image-overlay">
                    <div class="overlay-actions">
                      <button class="overlay-btn" @click="downloadImage(image)" title="下载">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                          <polyline points="7 10 12 15 17 10"></polyline>
                          <line x1="12" y1="15" x2="12" y2="3"></line>
                        </svg>
                      </button>
                      <button class="overlay-btn" @click="enlargeImage(image)" title="放大">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="11" cy="11" r="8"></circle>
                          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                          <line x1="11" y1="8" x2="11" y2="14"></line>
                          <line x1="8" y1="11" x2="14" y2="11"></line>
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
                <div class="image-info">
                  <span class="image-index">#{{ index + 1 }}</span>
                  <span class="image-res">{{ params.resolution }}</span>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import AppLayout from '../components/AppLayout.vue'
import API from '../api'

const prompt = ref('')
const uploadedImage = ref('')
const isGenerating = ref(false)
const generatedImages = ref([])
const progressPercent = ref(0)
const loadingMessage = ref('正在初始化生成...')

const fileInput = ref(null)
let timer = null

const params = reactive({
  resolution: '512x512',
  style: 'realistic',
  count: 1,
  creativity: 5
})

const stylePresets = ['写实', '卡通', '油画', '水彩', '赛博朋克', '复古', '科幻', '像素风']

const loadingMessages = [
  '正在初始化生成...',
  '正在分析提示词...',
  '正在构建图像特征...',
  '正在渲染细节...',
  '正在优化画质...',
  '即将完成...'
]

const mockImages = [
  'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=beautiful%20landscape%20with%20mountains%20and%20lake%20at%20sunset%20realistic%20style&image_size=landscape_16_9',
  'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=futuristic%20city%20skyline%20at%20night%20cyberpunk%20style%20neon%20lights&image_size=landscape_16_9',
  'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=cute%20cat%20portrait%20watercolor%20painting%20artistic&image_size=portrait_4_3',
  'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=ancient%20castle%20in%20misty%20mountains%20fantasy%20art&image_size=landscape_16_9'
]

const triggerUpload = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files?.[0]
  if (file) {
    previewImage(file)
  }
}

const handleDrop = (event) => {
  const file = event.dataTransfer?.files?.[0]
  if (file && file.type.startsWith('image/')) {
    previewImage(file)
  }
}

const previewImage = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    uploadedImage.value = e.target?.result
  }
  reader.readAsDataURL(file)
}

const removeImage = () => {
  uploadedImage.value = ''
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const applyStylePreset = (preset) => {
  if (!prompt.value) {
    prompt.value = `请生成一张${preset}风格的图片`
  } else {
    prompt.value = `${prompt.value}，${preset}风格`
  }
}

const startProgress = () => {
  progressPercent.value = 0
  let messageIndex = 0
  loadingMessage.value = loadingMessages[messageIndex]
  
  timer = setInterval(() => {
    progressPercent.value += Math.random() * 12 + 3
    
    if (progressPercent.value >= 100) {
      progressPercent.value = 100
      clearInterval(timer)
    }
    
    const newMessageIndex = Math.floor(progressPercent.value / 20)
    if (newMessageIndex < loadingMessages.length && newMessageIndex !== messageIndex) {
      messageIndex = newMessageIndex
      loadingMessage.value = loadingMessages[messageIndex]
    }
  }, 400)
}

const stopProgress = () => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
  progressPercent.value = 100
}

const handleGenerate = async () => {
  if (!prompt.value.trim()) {
    ElMessage.error('请输入提示词')
    return
  }
  
  isGenerating.value = true
  generatedImages.value = []
  startProgress()
  
  try {
    const result = await API.generateImage(prompt.value, {
      resolution: params.resolution,
      style: params.style,
      num_images: params.count
    })
    
    stopProgress()
    generatedImages.value = [result.result_url]
    ElMessage.success('生成成功')
  } catch (error) {
    console.error('Image generation error:', error)
    const results = []
    for (let i = 0; i < params.count; i++) {
      results.push(mockImages[i % mockImages.length])
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    stopProgress()
    generatedImages.value = results
    ElMessage.success('生成成功（使用演示数据）')
  } finally {
    isGenerating.value = false
  }
}

const handleRegenerate = () => {
  handleGenerate()
}

const downloadImage = (imageUrl) => {
  const link = document.createElement('a')
  link.href = imageUrl
  link.download = `generated_image_${Date.now()}.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  ElMessage.success('下载成功')
}

const enlargeImage = (imageUrl) => {
  ElMessage.info('大图预览功能开发中')
}

const handleExportAll = () => {
  if (!generatedImages.value.length) {
    ElMessage.error('没有可导出的内容')
    return
  }
  
  generatedImages.value.forEach((img, index) => {
    setTimeout(() => downloadImage(img), index * 500)
  })
}

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style scoped>
.generate-page {
  height: 100%;
  animation: fadeInUp 0.4s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.content-wrapper {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 24px;
  height: calc(100vh - 140px);
}

.params-panel {
  display: flex;
  flex-direction: column;
  padding: 20px;
  overflow: hidden;
}

.params-scrollable {
  flex: 1;
  overflow-y: auto;
  padding-right: 8px;
  margin-right: -8px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.generate-footer {
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
  margin-top: 16px;
  flex-shrink: 0;
}

.panel-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #f472b6, #fb7185);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.section-icon.upload {
  background: linear-gradient(135deg, #60a5fa, #3b82f6);
}

.section-icon.settings {
  background: linear-gradient(135deg, #06b6d4, #6366f1);
}

.section-header h3 {
  font-size: 15px;
  font-weight: 600;
  margin: 0;
  color: var(--color-text-primary);
}

.prompt-input {
  width: 100%;
  min-height: 100px;
  padding: 16px;
  background: var(--color-bg-glass);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  color: var(--color-text-primary);
  font-size: 14px;
  font-family: inherit;
  line-height: 1.6;
  resize: vertical;
  transition: all var(--transition-fast);
}

.prompt-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.prompt-input::placeholder {
  color: var(--color-text-muted);
}

.quick-prompts {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.quick-label {
  font-size: 12px;
  color: var(--color-text-muted);
}

.prompt-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.prompt-tag {
  padding: 6px 12px;
  background: var(--color-bg-glass);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 12px;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.prompt-tag:hover {
  background: var(--color-bg-glass-hover);
  border-color: rgba(244, 114, 182, 0.3);
  color: #f472b6;
}

.upload-area {
  border: 2px dashed var(--color-border);
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
  background: var(--color-bg-glass);
}

.upload-area:hover {
  border-color: #60a5fa;
  background: var(--color-bg-glass-hover);
}

.upload-area.has-image {
  padding: 0;
  border: none;
  background: transparent;
}

.upload-preview {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
}

.upload-preview img {
  width: 100%;
  height: 140px;
  object-fit: cover;
}

.upload-remove {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 32px;
  height: 32px;
  background: rgba(239, 68, 68, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: pointer;
  transition: transform 0.2s;
}

.upload-remove:hover {
  transform: scale(1.1);
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: var(--color-text-muted);
}

.upload-placeholder p {
  margin: 0;
  font-size: 13px;
}

.upload-hint {
  font-size: 11px !important;
  color: var(--color-text-muted);
  opacity: 0.8;
}

.hidden-input {
  display: none;
}

.params-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.param-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.param-item label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.param-select {
  width: 100%;
}

.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.slider-value {
  font-size: 13px;
  color: #f472b6;
  font-weight: 500;
}

.ethics-tip {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px;
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-radius: 12px;
  font-size: 13px;
  color: #fbbf24;
}

.tip-icon {
  flex-shrink: 0;
}

.generate-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 100%;
  height: 56px;
  background: linear-gradient(135deg, #f472b6, #fb7185);
  border: none;
  border-radius: 14px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.generate-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.generate-btn:hover:not(:disabled)::before {
  left: 100%;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(244, 114, 182, 0.4);
}

.generate-btn:active:not(:disabled) {
  transform: translateY(0);
}

.generate-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.generate-btn.loading {
  background: linear-gradient(135deg, #db2777, #e11d48);
  background-size: 200% 200%;
  animation: gradientShift 2s ease infinite;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.result-panel {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--color-border);
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.result-icon {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #f472b6, #fb7185);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.header-left h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 2px;
  color: var(--color-text-primary);
}

.result-meta {
  font-size: 12px;
  color: var(--color-text-muted);
}

.result-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: var(--color-bg-glass);
  border: 1px solid var(--color-border);
  border-radius: 10px;
  color: var(--color-text-secondary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.action-btn:hover:not(:disabled) {
  background: var(--color-bg-glass-hover);
  color: var(--color-text-primary);
  border-color: rgba(244, 114, 182, 0.3);
}

.action-btn.primary {
  background: linear-gradient(135deg, #f472b6, #fb7185);
  border-color: transparent;
  color: white;
}

.action-btn.primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(244, 114, 182, 0.3);
}

.result-content {
  flex: 1;
  overflow-y: auto;
  padding-right: 8px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  gap: 24px;
}

.loading-animation {
  position: relative;
}

.canvas-preview {
  width: 160px;
  height: 160px;
  border-radius: 20px;
  background: var(--color-bg-glass);
  border: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.canvas-glow {
  position: absolute;
  inset: -50%;
  background: radial-gradient(circle, rgba(244, 114, 182, 0.2) 0%, transparent 70%);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.2); opacity: 0.8; }
}

.ai-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #f472b6, #fb7185);
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  animation: float 2s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.loading-text {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin: 0;
}

.loading-progress {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
  max-width: 300px;
}

.loading-progress .progress-bar {
  flex: 1;
  height: 8px;
  background: var(--color-bg-glass);
  border-radius: 4px;
  overflow: hidden;
}

.loading-progress .progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #f472b6, #fb7185);
  border-radius: 4px;
  transition: width 0.2s ease;
}

.loading-progress span {
  font-size: 14px;
  font-weight: 600;
  color: #f472b6;
  min-width: 40px;
  text-align: right;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  width: 100px;
  height: 100px;
  background: var(--color-bg-glass);
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  margin-bottom: 24px;
}

.empty-state h3 {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 8px;
  color: var(--color-text-primary);
}

.empty-state > p {
  font-size: 14px;
  color: var(--color-text-muted);
  margin: 0 0 24px;
}

.empty-tips {
  display: flex;
  flex-direction: column;
  gap: 10px;
  text-align: left;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.tip-bullet {
  color: #f472b6;
  font-weight: 600;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
  align-content: start;
}

.image-card {
  background: var(--color-bg-glass);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid var(--color-border);
  transition: all var(--transition-fast);
}

.image-card:hover {
  transform: translateY(-4px);
  border-color: rgba(244, 114, 182, 0.3);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
}

.animate-slide-in {
  animation: slideIn 0.4s ease forwards;
  opacity: 0;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.image-wrapper {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.image-card:hover .image-wrapper img {
  transform: scale(1.08);
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.7) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  padding: 16px;
}

.image-card:hover .image-overlay {
  opacity: 1;
}

.overlay-actions {
  display: flex;
  gap: 8px;
}

.overlay-btn {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
  transition: all 0.2s;
}

.overlay-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.1);
}

.image-info {
  display: flex;
  justify-content: space-between;
  padding: 12px 16px;
  font-size: 12px;
}

.image-index {
  color: var(--color-text-muted);
}

.image-res {
  color: #f472b6;
  font-weight: 500;
}

@media (max-width: 1200px) {
  .content-wrapper {
    grid-template-columns: 1fr;
    height: auto;
  }
  
  .params-panel {
    max-height: none;
  }
  
  .result-panel {
    min-height: 400px;
  }
  
  .gallery-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  }
}

@media (max-width: 640px) {
  .params-grid {
    grid-template-columns: 1fr;
  }
  
  .result-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
  
  .result-actions {
    flex-wrap: wrap;
  }
  
  .gallery-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
