<template>
  <AppLayout pageTitle="系统配置" pageSubtitle="管理后台 - API配置与系统参数设置">
    <div class="system-config-content">
      <div class="config-section glass-card">
        <h3 class="section-title">API Key 状态</h3>
        <div class="api-status-grid single">
          <div class="api-status-card primary">
            <div class="api-icon zhipu">
              <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                <path d="M2 17l10 5 10-5"></path>
                <path d="M2 12l10 5 10-5"></path>
              </svg>
            </div>
            <div class="api-info">
              <div class="api-name">智谱 AI API <span class="primary-badge">主用</span></div>
              <div class="api-desc">文本生成 · 图像生成 · 语音合成</div>
              <div class="api-status">
                <span class="status-dot" :class="config.api_key_status?.zhipu ? 'active' : 'inactive'"></span>
                {{ config.api_key_status?.zhipu ? '已配置（模型已就绪）' : '未配置' }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="config-section glass-card">
        <h3 class="section-title">速率限制配置</h3>
        <el-form :model="rateLimitForm" label-width="180px" class="config-form">
          <el-form-item label="文本生成 (次/小时)">
            <el-input-number v-model="rateLimitForm.text_per_hour" :min="1" :max="1000" />
          </el-form-item>
          <el-form-item label="图像生成 (次/小时)">
            <el-input-number v-model="rateLimitForm.image_per_hour" :min="1" :max="1000" />
          </el-form-item>
          <el-form-item label="视频生成 (次/小时)">
            <el-input-number v-model="rateLimitForm.video_per_hour" :min="1" :max="1000" />
          </el-form-item>
          <el-form-item label="音频生成 (次/小时)">
            <el-input-number v-model="rateLimitForm.audio_per_hour" :min="1" :max="1000" />
          </el-form-item>
        </el-form>
      </div>
      
      <div class="config-section glass-card">
        <h3 class="section-title">文件限制配置</h3>
        <el-form :model="fileLimitForm" label-width="180px" class="config-form">
          <el-form-item label="最大文件大小 (MB)">
            <el-input-number v-model="fileLimitForm.max_file_size_mb" :min="1" :max="100" />
          </el-form-item>
          <el-form-item label="允许的文件类型">
            <el-checkbox-group v-model="fileLimitForm.allowed_extensions">
              <el-checkbox label=".txt">TXT</el-checkbox>
              <el-checkbox label=".pdf">PDF</el-checkbox>
              <el-checkbox label=".docx">DOCX</el-checkbox>
              <el-checkbox label=".png">PNG</el-checkbox>
              <el-checkbox label=".jpg">JPG</el-checkbox>
              <el-checkbox label=".mp4">MP4</el-checkbox>
              <el-checkbox label=".mp3">MP3</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </el-form>
      </div>
      
      <div class="config-actions">
        <el-button type="primary" class="action-btn-primary" @click="handleSaveConfig">
          保存配置
        </el-button>
        <el-button @click="handleResetConfig">重置</el-button>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import API from '../../api'
import AppLayout from '../../components/AppLayout.vue'

const config = ref({})
const rateLimitForm = reactive({
  text_per_hour: 100,
  image_per_hour: 50,
  video_per_hour: 20,
  audio_per_hour: 20
})

const fileLimitForm = reactive({
  max_file_size_mb: 10,
  allowed_extensions: ['.txt', '.pdf', '.docx', '.png', '.jpg', '.mp4', '.mp3']
})

const loadConfig = async () => {
  try {
    const data = await API.request('/api/admin/system/config')
    config.value = data
    
    if (data.rate_limit) {
      Object.assign(rateLimitForm, data.rate_limit)
    }
    if (data.file_limit) {
      Object.assign(fileLimitForm, data.file_limit)
    }
  } catch (error) {
    console.error('Load config error:', error)
  }
}

const handleSaveConfig = async () => {
  try {
    await API.request('/api/admin/system/config', {
      method: 'PUT',
      body: {
        rate_limit: rateLimitForm,
        file_limit: fileLimitForm
      }
    })
    
    ElMessage.success('配置保存成功')
  } catch (error) {
    console.error('Save config error:', error)
    ElMessage.error('保存失败')
  }
}

const handleResetConfig = () => {
  loadConfig()
}

onMounted(() => {
  loadConfig()
})
</script>

<style scoped>
.system-config-content {
  padding: 24px;
  max-width: 1000px;
}

.config-section {
  padding: 28px;
  margin-bottom: 24px;
}

.section-title {
  margin: 0 0 24px 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.api-status-grid {
  display: grid;
  gap: 20px;
}

.api-status-grid.single {
  max-width: 600px;
}

.api-status-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 28px;
  border: 2px solid var(--color-border);
  border-radius: 16px;
  transition: all 0.3s;
}

.api-status-card:hover {
  border-color: var(--color-primary);
}

.api-status-card.primary {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
  border-color: rgba(99, 102, 241, 0.3);
}

.api-status-card.primary:hover {
  border-color: var(--color-primary);
}

.api-icon {
  width: 72px;
  height: 72px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.api-icon.zhipu {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
}

.api-info {
  flex: 1;
}

.api-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.primary-badge {
  font-size: 12px;
  font-weight: 500;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  padding: 3px 10px;
  border-radius: 12px;
}

.api-desc {
  font-size: 14px;
  color: var(--color-text-muted);
  margin-bottom: 8px;
}

.api-status {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  color: var(--color-text-secondary);
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.status-dot.active {
  background: #52c41a;
  box-shadow: 0 0 8px rgba(82, 196, 26, 0.5);
}

.status-dot.inactive {
  background: #ff4d4f;
  box-shadow: 0 0 8px rgba(255, 77, 79, 0.5);
}

.config-form {
  max-width: 600px;
}

.config-actions {
  display: flex;
  gap: 16px;
  justify-content: flex-end;
}

.action-btn-primary {
  padding: 10px 28px;
  font-weight: 500;
}
</style>
