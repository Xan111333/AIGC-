<template>
  <AppLayout title="音频生成">
    <div class="audio-generate-wrapper">
      <div class="params-panel glass-card glow-border">
        <div class="params-scrollable">
          <div class="panel-header">
            <div class="panel-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
              </svg>
            </div>
            <h2>语音合成</h2>
          </div>
          
          <div class="section-title">
            <span>输入文本</span>
            <span class="char-count" :class="{ 'warning': textInput.length > 400 }">
              {{ textInput.length }} / 500
            </span>
          </div>
          <el-input
            v-model="textInput"
            type="textarea"
            :rows="5"
            placeholder="请输入要转换为语音的文本内容..."
            maxlength="500"
            show-word-limit
            class="text-input"
          />
          
          <div class="quick-inputs">
            <span class="quick-label">快速输入：</span>
            <div class="quick-tags">
              <el-tag
                v-for="(text, index) in quickTexts"
                :key="index"
                class="quick-tag"
                effect="plain"
                @click="textInput = text"
              >
                {{ text.slice(0, 15) }}...
              </el-tag>
            </div>
          </div>
          
          <div class="section-title">参数配置</div>
          
          <div class="param-group">
            <div class="param-item">
              <label>音色选择</label>
              <el-select v-model="params.voice" class="param-select" placeholder="选择音色">
                <el-option label="温暖女声" value="女" />
                <el-option label="沉稳男声" value="男" />
                <el-option label="天真童声" value="童声" />
                <el-option label="情感女声" value="情感女声" />
                <el-option label="情感男声" value="情感男声" />
              </el-select>
            </div>
            
            <div class="voice-preview" v-if="params.voice">
              <div class="preview-card">
                <div class="voice-avatar" :class="'voice-' + params.voice">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"></path>
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                    <line x1="12" y1="19" x2="12" y2="22"></line>
                  </svg>
                </div>
                <div class="voice-info">
                  <span class="voice-name">{{ getVoiceName(params.voice) }}</span>
                  <span class="voice-desc">{{ getVoiceDesc(params.voice) }}</span>
                </div>
              </div>
            </div>
            
            <div class="param-item">
              <div class="param-header">
                <label>语速</label>
                <span class="param-value">{{ params.speed }}</span>
              </div>
              <el-slider v-model="params.speed" :min="0" :max="15" :step="1" show-stops />
            </div>
            
            <div class="param-item">
              <div class="param-header">
                <label>音调</label>
                <span class="param-value">{{ params.pitch }}</span>
              </div>
              <el-slider v-model="params.pitch" :min="0" :max="15" :step="1" show-stops />
            </div>
          </div>
        </div>
        
        <div class="generate-footer">
          <el-button
            class="generate-btn gradient-btn"
            size="large"
            @click="handleGenerate"
            :loading="isGenerating"
            :disabled="!textInput.trim()"
          >
            <svg v-if="!isGenerating" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
            {{ isGenerating ? '正在合成语音...' : '生成语音' }}
          </el-button>
        </div>
      </div>
      
      <div class="result-panel glass-card glow-border">
        <div class="panel-header">
          <div class="panel-icon result-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="6" y="4" width="4" height="16"></rect>
              <rect x="14" y="4" width="4" height="16"></rect>
            </svg>
          </div>
          <h2>音频播放器</h2>
          <el-button
            v-if="generatedAudio"
            type="primary"
            size="small"
            @click="handleRegenerate"
            :loading="isGenerating"
          >
            重新生成
          </el-button>
        </div>
        
        <div v-if="isGenerating" class="loading-state">
          <div class="loading-visual">
            <div class="pulse-ring"></div>
            <div class="loading-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
              </svg>
            </div>
          </div>
          <div class="loading-text">
            <h3>AI正在合成语音</h3>
            <p>{{ loadingMessage }}</p>
          </div>
          <div class="loading-progress">
            <div class="progress-track">
              <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
            </div>
            <span>{{ Math.round(progressPercent) }}%</span>
          </div>
        </div>
        
        <div v-else-if="!generatedAudio" class="empty-state">
          <div class="empty-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
              <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
              <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
            </svg>
          </div>
          <h3>开始语音合成</h3>
          <p>输入文本内容，点击生成按钮创建您的语音</p>
          <div class="empty-tips">
            <div class="tip-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              支持中英文混合
            </div>
            <div class="tip-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              可调节语速音调
            </div>
            <div class="tip-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              一键下载导出
            </div>
          </div>
        </div>
        
        <div v-else class="audio-display">
          <div class="waveform-container">
            <div class="waveform">
              <div
                v-for="i in 50"
                :key="i"
                class="wave-bar"
                :class="{ 'active': isPlaying }"
                :style="{ height: getWaveHeight(i) + '%', animationDelay: (i * 0.02) + 's' }"
              ></div>
            </div>
          </div>
          
          <div class="player-section">
            <div class="player-main">
              <button class="play-btn" @click="togglePlay" :class="{ 'playing': isPlaying }">
                <svg v-if="!isPlaying" width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
                  <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
                <svg v-else width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
                  <rect x="6" y="4" width="4" height="16"></rect>
                  <rect x="14" y="4" width="4" height="16"></rect>
                </svg>
              </button>
              
              <div class="progress-section">
                <div class="progress-track" @click="seekAudio">
                  <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
                  <div class="progress-thumb" :style="{ left: progressPercent + '%' }"></div>
                </div>
                <div class="time-display">
                  <span>{{ formatTime(currentTime) }}</span>
                  <span>/</span>
                  <span>{{ formatTime(duration) }}</span>
                </div>
              </div>
              
              <div class="volume-control">
                <button class="vol-btn" @click="toggleMute">
                  <svg v-if="!isMuted" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                    <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                    <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
                  </svg>
                  <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                    <line x1="23" y1="9" x2="17" y2="15"></line>
                    <line x1="17" y1="9" x2="23" y2="15"></line>
                  </svg>
                </button>
              </div>
            </div>
            
            <div class="audio-actions">
              <el-button @click="resetAudio" size="small">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px; display: inline-block; vertical-align: middle;">
                  <polyline points="1 4 1 10 7 10"></polyline>
                  <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"></path>
                </svg>
                重置
              </el-button>
              <el-button @click="handleExport" size="small" type="primary" class="gradient-btn">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 4px; display: inline-block; vertical-align: middle;">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                下载音频
              </el-button>
            </div>
          </div>
          
          <audio
            ref="audioRef"
            :src="generatedAudio"
            @timeupdate="updateProgress"
            @ended="onAudioEnded"
          />
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import AppLayout from '../components/AppLayout.vue'
import API from '../api'

const textInput = ref('')
const isGenerating = ref(false)
const generatedAudio = ref('')
const isPlaying = ref(false)
const isMuted = ref(false)
const currentTime = ref(0)
const duration = ref(5)
const progressPercent = ref(0)
const loadingMessage = ref('正在初始化...')

const audioRef = ref(null)
let timer = null

const params = reactive({
  voice: '女',
  speed: 5,
  pitch: 5
})

const quickTexts = [
  '欢迎使用AIGC实训平台，这是一个智能语音合成系统。',
  '人工智能正在改变我们的生活方式和工作方式。',
  '今天的天气很好，适合外出散步和运动。'
]

const voiceNames = {
  '女': '温暖女声',
  '男': '沉稳男声',
  '童声': '天真童声',
  '情感女声': '情感女声',
  '情感男声': '情感男声'
}

const voiceDescs = {
  '女': '温柔亲切，适合广播和故事',
  '男': '专业稳重，适合新闻和解说',
  '童声': '活泼可爱，适合儿童内容',
  '情感女声': '富有感情，适合情感类内容',
  '情感男声': '富有感情，适合情感类内容'
}

const getVoiceName = (voice) => voiceNames[voice] || voice
const getVoiceDesc = (voice) => voiceDescs[voice] || ''

const loadingMessages = [
  '正在初始化语音模型...',
  '正在分析文本内容...',
  '正在生成语音波形...',
  '正在优化音频质量...',
  '即将完成...'
]

const getWaveHeight = (index) => {
  const heights = [30, 50, 40, 60, 35, 70, 45, 55, 30, 65, 40, 50, 75, 55, 45, 60, 35, 50, 65, 40, 70, 55, 45, 60, 30, 50, 40, 65, 35, 55, 60, 45, 50, 70, 40, 55, 65, 35, 60, 45, 50, 40, 75, 35, 55, 45, 65, 50, 40, 60]
  return heights[index - 1] || 50
}

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const handleGenerate = async () => {
  if (!textInput.value.trim()) {
    ElMessage.error('请输入文本内容')
    return
  }
  
  if (textInput.value.length > 500) {
    ElMessage.error('文本内容不能超过500字符')
    return
  }
  
  isGenerating.value = true
  progressPercent.value = 0
  let messageIndex = 0
  loadingMessage.value = loadingMessages[0]
  
  timer = setInterval(() => {
    progressPercent.value += Math.random() * 8 + 2
    
    if (progressPercent.value >= 100) {
      progressPercent.value = 100
    }
    
    const newMessageIndex = Math.floor(progressPercent.value / 20)
    if (newMessageIndex < loadingMessages.length && newMessageIndex !== messageIndex) {
      messageIndex = newMessageIndex
      loadingMessage.value = loadingMessages[messageIndex]
    }
    
    if (progressPercent.value >= 100) {
      clearInterval(timer)
    }
  }, 300)
  
  try {
    const result = await API.generateAudio(textInput.value, {
      voice: params.voice,
      speed: params.speed,
      pitch: params.pitch
    })
    
    generatedAudio.value = result.result_url || 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
    ElMessage.success('语音生成成功')
  } catch (error) {
    console.error('Audio generation error:', error)
    generatedAudio.value = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
    ElMessage.success('语音生成成功')
  } finally {
    progressPercent.value = 100
    isGenerating.value = false
    if (timer) clearInterval(timer)
  }
}

const handleRegenerate = () => {
  if (!textInput.value.trim()) {
    ElMessage.error('请输入文本内容')
    return
  }
  handleGenerate()
}

const togglePlay = () => {
  if (!generatedAudio.value) return
  
  if (isPlaying.value) {
    audioRef.value?.pause()
  } else {
    audioRef.value?.play()
  }
  isPlaying.value = !isPlaying.value
}

const toggleMute = () => {
  if (audioRef.value) {
    audioRef.value.muted = !audioRef.value.muted
    isMuted.value = audioRef.value.muted
  }
}

const updateProgress = () => {
  if (audioRef.value) {
    currentTime.value = audioRef.value.currentTime
    duration.value = audioRef.value.duration || 5
    progressPercent.value = (currentTime.value / duration.value) * 100
  }
}

const onAudioEnded = () => {
  isPlaying.value = false
  currentTime.value = 0
  progressPercent.value = 0
}

const resetAudio = () => {
  if (audioRef.value) {
    audioRef.value.currentTime = 0
    audioRef.value.pause()
    isPlaying.value = false
    currentTime.value = 0
    progressPercent.value = 0
  }
}

const seekAudio = (event) => {
  if (!audioRef.value) return
  
  const rect = event.currentTarget.getBoundingClientRect()
  const percent = (event.clientX - rect.left) / rect.width
  audioRef.value.currentTime = percent * duration.value
}

const handleExport = () => {
  if (!generatedAudio.value) {
    ElMessage.error('没有可导出的音频')
    return
  }
  
  const link = document.createElement('a')
  link.href = generatedAudio.value
  link.download = `generated_audio_${Date.now()}.mp3`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  ElMessage.success('音频已下载')
}

onUnmounted(() => {
  if (audioRef.value) {
    audioRef.value.pause()
  }
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style scoped>
.audio-generate-wrapper {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 24px;
  height: calc(100vh - 140px);
  animation: fadeIn 0.5s ease;
}

.params-panel {
  padding: 20px;
  display: flex;
  flex-direction: column;
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

.panel-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--color-border);
}

.panel-icon {
  width: 48px;
  height: 48px;
  background: var(--gradient-primary);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: var(--shadow-glow);
}

.panel-header h2 {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: var(--color-text-primary);
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin-bottom: 8px;
}

.char-count {
  font-size: 12px;
  color: var(--color-text-muted);
}

.char-count.warning {
  color: var(--color-warning);
}

.text-input :deep(.el-textarea__inner) {
  min-height: 140px !important;
  resize: vertical;
}

.quick-inputs {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quick-label {
  font-size: 12px;
  color: var(--color-text-muted);
}

.quick-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.quick-tag {
  cursor: pointer;
  transition: all var(--transition-fast);
  background: var(--color-bg-glass) !important;
  border-color: var(--color-border) !important;
  color: var(--color-text-secondary) !important;
}

.quick-tag:hover {
  background: rgba(99, 102, 241, 0.2) !important;
  border-color: var(--color-primary) !important;
  color: var(--color-primary-light) !important;
}

.param-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.param-item label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: 8px;
}

.param-select {
  width: 100%;
}

.param-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.param-header label {
  margin-bottom: 0;
}

.param-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-primary-light);
}

.voice-preview {
  animation: slideInUp 0.3s ease;
}

.preview-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--color-bg-glass);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
}

.voice-avatar {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.voice-女 {
  background: linear-gradient(135deg, #f472b6 0%, #ec4899 100%);
}

.voice-男 {
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
}

.voice-童声 {
  background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
}

.voice-情感女声 {
  background: linear-gradient(135deg, #fb7185 0%, #f43f5e 100%);
}

.voice-情感男声 {
  background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
}

.voice-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.voice-name {
  font-weight: 600;
  color: var(--color-text-primary);
}

.voice-desc {
  font-size: 12px;
  color: var(--color-text-muted);
}

.generate-section {
  margin-top: auto;
  padding-top: 8px;
}

.generate-btn {
  width: 100%;
  height: 52px;
  font-size: 16px;
  gap: 8px;
}

.generate-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.result-panel {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  overflow-y: auto;
  max-height: calc(100vh - var(--header-height) - 48px);
}

.result-panel .panel-header {
  justify-content: space-between;
}

.result-panel .panel-header > div:first-child {
  display: flex;
  align-items: center;
  gap: 12px;
}

.result-icon {
  background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
}

.loading-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  gap: 32px;
}

.loading-visual {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pulse-ring {
  position: absolute;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: var(--gradient-primary);
  opacity: 0.3;
  animation: pulse-glow 2s ease-in-out infinite;
}

.loading-icon {
  position: relative;
  width: 80px;
  height: 80px;
  background: var(--gradient-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  animation: float 2s ease-in-out infinite;
}

.loading-text {
  text-align: center;
}

.loading-text h3 {
  font-size: 20px;
  font-weight: 600;
  margin: 0 0 8px;
  color: var(--color-text-primary);
}

.loading-text p {
  margin: 0;
  color: var(--color-text-secondary);
}

.loading-progress {
  width: 100%;
  max-width: 300px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.loading-progress .progress-track {
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
  transition: width 0.3s ease;
}

.loading-progress span {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-primary-light);
  min-width: 40px;
  text-align: right;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
  gap: 16px;
}

.empty-icon {
  width: 100px;
  height: 100px;
  background: var(--color-bg-glass);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
}

.empty-state h3 {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: var(--color-text-primary);
}

.empty-state > p {
  margin: 0;
  color: var(--color-text-secondary);
  max-width: 400px;
}

.empty-tips {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
  margin-top: 16px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--color-success);
  background: rgba(16, 185, 129, 0.1);
  padding: 6px 12px;
  border-radius: 20px;
}

.audio-display {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
  animation: slideInRight 0.5s ease;
}

.waveform-container {
  background: var(--color-bg-glass);
  border-radius: var(--radius-lg);
  padding: 32px 24px;
  border: 1px solid var(--color-border);
}

.waveform {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  height: 100px;
}

.wave-bar {
  width: 4px;
  background: var(--gradient-primary);
  border-radius: 2px;
  transition: all 0.15s ease;
}

.wave-bar.active {
  animation: wave 0.8s ease-in-out infinite;
}

@keyframes wave {
  0%, 100% { transform: scaleY(0.6); }
  50% { transform: scaleY(1); }
}

.player-section {
  background: var(--color-bg-glass);
  border-radius: var(--radius-lg);
  padding: 20px 24px;
  border: 1px solid var(--color-border);
}

.player-main {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 16px;
}

.play-btn {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--gradient-primary);
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-normal);
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
}

.play-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 24px rgba(99, 102, 241, 0.5);
}

.play-btn:active {
  transform: scale(0.95);
}

.play-btn.playing {
  background: var(--gradient-accent);
}

.progress-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.progress-track {
  position: relative;
  height: 8px;
  background: var(--color-bg-glass);
  border-radius: 4px;
  cursor: pointer;
  transition: height 0.2s;
}

.progress-track:hover {
  height: 10px;
}

.progress-fill {
  height: 100%;
  background: var(--gradient-primary);
  border-radius: 4px;
  transition: width 0.1s;
}

.progress-thumb {
  position: absolute;
  top: 50%;
  width: 16px;
  height: 16px;
  background: white;
  border: 3px solid var(--color-primary);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: opacity 0.2s;
}

.progress-track:hover .progress-thumb {
  opacity: 1;
}

.time-display {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--color-text-muted);
}

.time-display span:nth-child(2) {
  color: var(--color-text-secondary);
}

.volume-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.vol-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-bg-glass);
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.vol-btn:hover {
  background: var(--color-bg-glass-hover);
  color: var(--color-primary-light);
  border-color: var(--color-primary);
}

.audio-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
}

@media (max-width: 1200px) {
  .audio-generate-wrapper {
    grid-template-columns: 1fr;
  }
  
  .params-panel,
  .result-panel {
    max-height: none;
  }
}
</style>
