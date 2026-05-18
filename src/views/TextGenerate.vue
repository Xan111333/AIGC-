<template>
  <AppLayout pageTitle="文本生成" pageSubtitle="智能文章、文案撰写、创意写作">
    <div class="generate-page">
      <div class="content-wrapper">
        <aside class="params-panel glass-card">
          <div class="params-scrollable">
            <div class="panel-section">
              <div class="section-header">
                <div class="section-icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                  </svg>
                </div>
                <h3>输入提示词</h3>
              </div>
              
              <textarea 
                v-model="prompt" 
                rows="5" 
                placeholder="描述您想要生成的内容，例如：写一篇关于人工智能未来发展的科技文章..."
                class="prompt-input"
              />
              
              <div class="quick-prompts">
                <span class="quick-label">快速输入</span>
                <div class="prompt-tags">
                  <span 
                    v-for="tag in quickTags" 
                    :key="tag" 
                    class="prompt-tag"
                    @click="applyQuickPrompt(tag)"
                  >{{ tag }}</span>
                </div>
              </div>
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
                  <label>生成长度</label>
                  <el-select v-model="params.length" class="param-select" size="large">
                    <el-option label="短（100字以内）" value="short" />
                    <el-option label="中（100-500字）" value="medium" />
                    <el-option label="长（500-1000字）" value="long" />
                    <el-option label="超长（1000字以上）" value="extra-long" />
                  </el-select>
                </div>
                
                <div class="param-item">
                  <label>内容风格</label>
                  <el-select v-model="params.style" class="param-select" size="large">
                    <el-option label="正式" value="formal" />
                    <el-option label="轻松" value="casual" />
                    <el-option label="幽默" value="humorous" />
                    <el-option label="学术" value="academic" />
                    <el-option label="创意" value="creative" />
                    <el-option label="简洁" value="concise" />
                  </el-select>
                </div>
                
                <div class="param-item">
                  <label>语气</label>
                  <el-select v-model="params.tone" class="param-select" size="large">
                    <el-option label="中立" value="neutral" />
                    <el-option label="友好" value="friendly" />
                    <el-option label="专业" value="professional" />
                    <el-option label="热情" value="enthusiastic" />
                    <el-option label="严肃" value="serious" />
                  </el-select>
                </div>
                
                <div class="param-item">
                  <label>语言</label>
                  <el-select v-model="params.language" class="param-select" size="large">
                    <el-option label="中文" value="chinese" />
                    <el-option label="英文" value="english" />
                    <el-option label="中英混合" value="mixed" />
                  </el-select>
                </div>
              </div>
              
              <div class="param-item full-width">
                <div class="slider-header">
                  <label>生成数量</label>
                  <span class="slider-value">{{ params.count }} 篇</span>
                </div>
                <el-slider v-model="params.count" :min="1" :max="5" :step="1" />
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
              <span>{{ isGenerating ? '正在生成...' : '开始生成' }}</span>
            </button>
          </div>
        </aside>
        
        <main class="result-panel glass-card glow-border">
          <div class="result-header">
            <div class="header-left">
              <div class="result-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                </svg>
              </div>
              <div>
                <h3>生成结果</h3>
                <span class="result-meta">{{ generatedText.length }} 条结果</span>
              </div>
            </div>
            
            <div class="result-actions" v-if="generatedText.length > 0">
              <button class="action-btn" @click="handleRegenerate" :disabled="isGenerating">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="23 4 23 10 17 10"></polyline>
                  <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
                </svg>
                <span>重新生成</span>
              </button>
              <button class="action-btn" @click="handleCopy">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
                <span>复制</span>
              </button>
              <button class="action-btn primary" @click="handleExport">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                <span>导出</span>
              </button>
            </div>
          </div>
          
          <div class="result-content">
            <div v-if="isGenerating" class="loading-state">
              <div class="loading-animation">
                <div class="pulse-ring"></div>
                <div class="ai-icon">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                    <path d="M2 17l10 5 10-5"></path>
                    <path d="M2 12l10 5 10-5"></path>
                  </svg>
                </div>
              </div>
              <p class="loading-text">AI 正在为您创作中...</p>
              <div class="loading-progress">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
                </div>
                <span>{{ progressPercent }}%</span>
              </div>
            </div>
            
            <div v-else-if="!generatedText.length" class="empty-state">
              <div class="empty-icon">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                  <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
              </div>
              <h3>开始您的创作之旅</h3>
              <p>在左侧输入提示词，配置参数，然后点击生成按钮</p>
              <div class="empty-tips">
                <div class="tip-item">
                  <span class="tip-bullet">•</span>
                  <span>详细描述您想要的内容</span>
                </div>
                <div class="tip-item">
                  <span class="tip-bullet">•</span>
                  <span>调整风格和语气参数</span>
                </div>
                <div class="tip-item">
                  <span class="tip-bullet">•</span>
                  <span>点击生成按钮开始创作</span>
                </div>
              </div>
            </div>
            
            <div v-else class="results-list">
              <div 
                v-for="(text, index) in generatedText" 
                :key="index" 
                class="result-item animate-slide-in"
                :style="{ animationDelay: index * 0.1 + 's' }"
              >
                <div class="result-item-header">
                  <div class="result-number">{{ index + 1 }}</div>
                  <div class="result-tags">
                    <span class="tag">{{ getStyleLabel(params.style) }}</span>
                    <span class="tag">{{ getToneLabel(params.tone) }}</span>
                  </div>
                </div>
                <div class="result-item-body">{{ text }}</div>
                <div class="result-item-actions">
                  <button class="mini-btn" @click="copyItem(text)">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                    复制
                  </button>
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
const isGenerating = ref(false)
const generatedText = ref([])
const progressPercent = ref(0)
let progressInterval = null

const params = reactive({
  length: 'medium',
  style: 'formal',
  tone: 'neutral',
  language: 'chinese',
  count: 1
})

const quickTags = ['科技文章', '产品介绍', '创意故事', '营销文案', '学习总结', '邮件模板']

const styleLabels = {
  formal: '正式',
  casual: '轻松',
  humorous: '幽默',
  academic: '学术',
  creative: '创意',
  concise: '简洁'
}

const toneLabels = {
  neutral: '中立',
  friendly: '友好',
  professional: '专业',
  enthusiastic: '热情',
  serious: '严肃'
}

const mockResults = [
  '人工智能技术正在深刻改变我们的生活方式。从智能家居到自动驾驶，AI已经渗透到各个领域。随着技术的不断进步，人工智能将在更多方面发挥重要作用，为人类创造更加美好的未来。在医疗领域，AI辅助诊断系统能够帮助医生更准确地识别疾病；在教育领域，个性化学习平台为每个学生提供量身定制的学习方案。',
  '机器学习是人工智能的核心技术之一。通过大量数据的训练，机器可以自动学习并提升性能。深度学习作为机器学习的重要分支，已经在图像识别、自然语言处理等领域取得了突破性进展。这些技术的发展使得计算机能够理解复杂的模式，做出智能决策，为各行各业带来革命性的变化。',
  '自然语言处理技术让计算机能够理解和生成人类语言。这项技术的发展使得智能助手、机器翻译等应用成为可能。未来，自然语言处理将继续发展，实现更加自然的人机交互。我们已经看到了诸如智能客服、语音识别、文本摘要等应用的广泛使用，而这只是开始。'
]

const getStyleLabel = (style) => styleLabels[style] || style
const getToneLabel = (tone) => toneLabels[tone] || tone

const applyQuickPrompt = (tag) => {
  const prompts = {
    '科技文章': '写一篇关于人工智能在日常生活中的应用的科技文章',
    '产品介绍': '写一份新产品发布的产品介绍文案，突出产品特点和用户价值',
    '创意故事': '写一个关于未来城市的科幻短篇故事开头',
    '营销文案': '写一份吸引用户点击的社交媒体营销文案',
    '学习总结': '写一份关于本周学习内容的总结报告',
    '邮件模板': '写一封正式的商务合作邀请函邮件模板'
  }
  prompt.value = prompts[tag] || tag
}

const startProgress = () => {
  progressPercent.value = 0
  progressInterval = setInterval(() => {
    if (progressPercent.value < 90) {
      progressPercent.value += Math.random() * 10
    }
    if (progressPercent.value > 90) {
      progressPercent.value = 90
    }
  }, 200)
}

const stopProgress = () => {
  if (progressInterval) {
    clearInterval(progressInterval)
    progressInterval = null
  }
  progressPercent.value = 100
}

const handleGenerate = async () => {
  if (!prompt.value.trim()) {
    ElMessage.error('请输入提示词')
    return
  }
  
  isGenerating.value = true
  generatedText.value = []
  startProgress()
  
  try {
    const result = await API.generateText(prompt.value, {
      length: params.length,
      style: params.style,
      tone: params.tone,
      language: params.language === 'chinese' ? 'zh' : 'en'
    })
    
    stopProgress()
    generatedText.value = [result.result_url]
    ElMessage.success('生成成功')
  } catch (error) {
    console.error('Text generation error:', error)
    const results = []
    for (let i = 0; i < params.count; i++) {
      results.push(mockResults[i % mockResults.length])
    }
    
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    stopProgress()
    generatedText.value = results
    ElMessage.success('生成成功（使用演示数据）')
  } finally {
    isGenerating.value = false
  }
}

const handleRegenerate = () => {
  handleGenerate()
}

const handleCopy = () => {
  if (!generatedText.value.length) return
  
  const text = generatedText.value.join('\n\n---\n\n')
  navigator.clipboard.writeText(text).then(() => {
    ElMessage.success('已复制到剪贴板')
  })
}

const copyItem = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    ElMessage.success('已复制到剪贴板')
  })
}

const handleExport = () => {
  if (!generatedText.value.length) {
    ElMessage.error('没有可导出的内容')
    return
  }
  
  const text = generatedText.value.join('\n\n---\n\n')
  const blob = new Blob([text], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'generated_text.txt'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
  
  ElMessage.success('导出成功')
}

onUnmounted(() => {
  stopProgress()
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
  background: var(--gradient-primary);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
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
  min-height: 120px;
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
  border-color: rgba(99, 102, 241, 0.3);
  color: var(--color-primary-light);
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

.param-item.full-width {
  grid-column: 1 / -1;
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
  color: var(--color-primary-light);
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
  background: var(--gradient-primary);
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
  box-shadow: 0 12px 32px rgba(99, 102, 241, 0.4);
}

.generate-btn:active:not(:disabled) {
  transform: translateY(0);
}

.generate-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.generate-btn.loading {
  background: linear-gradient(135deg, #4f46e5, #7c3aed);
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
  background: var(--gradient-primary);
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
  border-color: rgba(99, 102, 241, 0.3);
}

.action-btn.primary {
  background: var(--gradient-primary);
  border-color: transparent;
  color: white;
}

.action-btn.primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
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
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pulse-ring {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid transparent;
  border-top-color: var(--color-primary);
  animation: pulse 2s ease-in-out infinite;
}

.pulse-ring::before {
  content: '';
  position: absolute;
  inset: 8px;
  border-radius: 50%;
  border: 2px solid transparent;
  border-top-color: var(--color-secondary);
  animation: pulse 2s ease-in-out infinite 0.3s;
}

@keyframes pulse {
  0% { transform: rotate(0deg); opacity: 1; }
  100% { transform: rotate(360deg); opacity: 0.5; }
}

.ai-icon {
  width: 60px;
  height: 60px;
  background: var(--gradient-primary);
  border-radius: 20px;
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
  background: var(--gradient-primary);
  border-radius: 4px;
  transition: width 0.2s ease;
}

.loading-progress span {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-primary-light);
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
  color: var(--color-primary-light);
  font-weight: 600;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.result-item {
  background: var(--color-bg-glass);
  border-radius: 16px;
  padding: 20px;
  border: 1px solid var(--color-border);
  transition: all var(--transition-fast);
}

.result-item:hover {
  background: var(--color-bg-glass-hover);
  border-color: rgba(99, 102, 241, 0.3);
}

.animate-slide-in {
  animation: slideIn 0.4s ease forwards;
  opacity: 0;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.result-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.result-number {
  width: 32px;
  height: 32px;
  background: var(--gradient-primary);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: white;
}

.result-tags {
  display: flex;
  gap: 8px;
}

.tag {
  padding: 4px 10px;
  background: rgba(99, 102, 241, 0.15);
  border-radius: 8px;
  font-size: 12px;
  color: var(--color-primary-light);
  font-weight: 500;
}

.result-item-body {
  font-size: 14px;
  line-height: 1.8;
  color: var(--color-text-secondary);
  white-space: pre-wrap;
}

.result-item-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}

.mini-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  color: var(--color-text-secondary);
  font-size: 12px;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.mini-btn:hover {
  background: var(--color-bg-glass-hover);
  color: var(--color-primary-light);
  border-color: rgba(99, 102, 241, 0.3);
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
}
</style>
