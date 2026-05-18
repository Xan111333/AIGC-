<template>
  <div class="login-page">
    <div class="particles-bg"></div>
    
    <div class="login-wrapper">
      <div class="login-info">
        <div class="logo-big animate-float">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
            <path d="M2 17l10 5 10-5"></path>
            <path d="M2 12l10 5 10-5"></path>
          </svg>
        </div>
        <h1 class="app-title">AIGC 实训平台</h1>
        <p class="app-subtitle">探索 AI 创作的无限可能</p>
        <div class="feature-list">
          <div class="feature-item">
            <div class="feature-icon text-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
              </svg>
            </div>
            <span>智能文本生成</span>
          </div>
          <div class="feature-item">
            <div class="feature-icon image-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                <polyline points="21 15 16 10 5 21"></polyline>
              </svg>
            </div>
            <span>创意图像生成</span>
          </div>
          <div class="feature-item">
            <div class="feature-icon audio-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
              </svg>
            </div>
            <span>语音合成</span>
          </div>
          <div class="feature-item">
            <div class="feature-icon video-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="23 7 16 12 23 17 23 7"></polygon>
                <rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect>
              </svg>
            </div>
            <span>视频生成</span>
          </div>
        </div>
      </div>
      
      <div class="login-card glass-card glow-border animate-slide-in-up">
        <div class="card-header">
          <div class="logo-small">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
              <path d="M2 17l10 5 10-5"></path>
              <path d="M2 12l10 5 10-5"></path>
            </svg>
          </div>
          <h2>欢迎回来</h2>
          <p>登录您的实训平台账号</p>
        </div>
        
        <el-form ref="loginForm" :model="form" class="login-form">
          <el-form-item prop="username">
            <el-input 
              v-model="form.username" 
              placeholder="请输入用户名" 
              size="large"
              class="custom-input"
            >
              <template #prefix>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input 
              v-model="form.password" 
              type="password" 
              placeholder="请输入密码" 
              size="large"
              show-password
              class="custom-input"
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </template>
            </el-input>
          </el-form-item>
          
          <div class="form-actions">
            <el-checkbox v-model="form.remember" class="custom-checkbox">记住我</el-checkbox>
            <span class="forgot-link" @click="showForgot = true">忘记密码？</span>
          </div>
          
          <el-button 
            class="login-btn gradient-btn" 
            type="primary" 
            size="large" 
            @click="handleLogin" 
            :loading="isLoading"
          >
            <svg v-if="!isLoading" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
              <polyline points="10 17 15 12 10 7"></polyline>
              <line x1="15" y1="12" x2="3" y2="12"></line>
            </svg>
            {{ isLoading ? '登录中...' : '立即登录' }}
          </el-button>
        </el-form>
        
        <div class="quick-login">
          <p class="quick-title">快速体验</p>
          <div class="quick-buttons">
            <el-button type="text" class="quick-btn" @click="quickLogin('student')">
              <span class="role-badge student">学生</span>
              <span class="role-creds">student / student123</span>
            </el-button>
            <el-button type="text" class="quick-btn" @click="quickLogin('teacher')">
              <span class="role-badge teacher">教师</span>
              <span class="role-creds">teacher / teacher123</span>
            </el-button>
            <el-button type="text" class="quick-btn" @click="quickLogin('admin')">
              <span class="role-badge admin">管理员</span>
              <span class="role-creds">admin / admin123</span>
            </el-button>
          </div>
        </div>
        
        <div class="register-link">
          <span>还没有账号？</span>
          <span class="link" @click="$router.push('/register')">立即注册</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import API from '../api'

const form = reactive({
  username: '',
  password: '',
  remember: false
})

const showForgot = ref(false)
const isLoading = ref(false)

const quickCredentials = {
  student: { username: 'student', password: 'student123' },
  teacher: { username: 'teacher', password: 'teacher123' },
  admin: { username: 'admin', password: 'admin123' }
}

const quickLogin = (role) => {
  const creds = quickCredentials[role]
  form.username = creds.username
  form.password = creds.password
}

const handleLogin = async () => {
  if (!form.username || !form.password) {
    ElMessage.error('请输入用户名和密码')
    return
  }

  isLoading.value = true

  try {
    const response = await API.login(form.username, form.password)
    
    const userResponse = await API.getCurrentUser()
    localStorage.setItem('user', JSON.stringify(userResponse))
    
    ElMessage.success('登录成功')
    
    if (form.remember) {
      localStorage.setItem('username', form.username)
    } else {
      localStorage.removeItem('username')
    }
    
    setTimeout(() => {
      if (userResponse.role === 'admin') {
        window.location.href = '/admin'
      } else if (userResponse.role === 'teacher') {
        window.location.href = '/teacher-dashboard'
      } else {
        window.location.href = '/dashboard'
      }
    }, 800)
  } catch (error) {
    ElMessage.error(error.message || '登录失败，请检查用户名和密码')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-bg);
  position: relative;
  overflow: hidden;
}

.particles-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.login-wrapper {
  display: flex;
  align-items: center;
  gap: 80px;
  max-width: 1200px;
  padding: 40px;
  position: relative;
  z-index: 1;
}

.login-info {
  flex: 1;
  max-width: 400px;
}

.logo-big {
  width: 100px;
  height: 100px;
  background: var(--gradient-primary);
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  box-shadow: var(--shadow-glow);
  margin-bottom: 24px;
}

.app-title {
  font-size: 42px;
  font-weight: 700;
  margin: 0 0 12px;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.app-subtitle {
  font-size: 18px;
  color: var(--color-text-secondary);
  margin: 0 0 40px;
}

.feature-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--color-bg-glass);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  transition: all var(--transition-normal);
}

.feature-item:hover {
  background: var(--color-bg-glass-hover);
  transform: translateX(4px);
}

.feature-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.text-icon { background: linear-gradient(135deg, #6366f1, #8b5cf6); }
.image-icon { background: linear-gradient(135deg, #f093fb, #f5576c); }
.audio-icon { background: linear-gradient(135deg, #06b6d4, #6366f1); }
.video-icon { background: linear-gradient(135deg, #4facfe, #00f2fe); }

.login-card {
  width: 420px;
  padding: 40px;
  animation-delay: 0.2s;
}

.card-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-small {
  width: 56px;
  height: 56px;
  margin: 0 auto 16px;
  background: var(--gradient-primary);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.card-header h2 {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 8px;
  color: var(--color-text-primary);
}

.card-header p {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
}

.login-form {
  margin: 0;
}

.custom-input {
  margin-bottom: 4px;
}

:deep(.custom-input .el-input__wrapper) {
  padding: 12px 16px !important;
  border-radius: var(--radius-md) !important;
}

:deep(.custom-input .el-input__inner) {
  font-size: 15px !important;
}

:deep(.custom-input .el-input__prefix) {
  color: var(--color-text-muted) !important;
  margin-right: 8px !important;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

:deep(.custom-checkbox .el-checkbox__label) {
  color: var(--color-text-secondary) !important;
  font-size: 14px;
}

.forgot-link {
  color: var(--color-primary-light);
  font-size: 14px;
  cursor: pointer;
  transition: color var(--transition-fast);
}

.forgot-link:hover {
  color: var(--color-primary);
}

.login-btn {
  width: 100%;
  height: 52px;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

:deep(.login-btn) {
  background: var(--gradient-primary) !important;
  border: none !important;
  border-radius: var(--radius-md) !important;
}

:deep(.login-btn:hover) {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4) !important;
}

.quick-login {
  margin-top: 28px;
  padding-top: 28px;
  border-top: 1px solid var(--color-border);
}

.quick-title {
  text-align: center;
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0 0 16px;
}

.quick-buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.quick-btn {
  display: flex !important;
  align-items: center;
  justify-content: flex-start;
  padding: 12px 16px !important;
  background: var(--color-bg-glass) !important;
  border-radius: var(--radius-md) !important;
  border: 1px solid var(--color-border) !important;
  transition: all var(--transition-fast) !important;
}

.quick-btn:hover {
  background: var(--color-bg-glass-hover) !important;
  border-color: rgba(99, 102, 241, 0.3) !important;
}

.role-badge {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  margin-right: 12px;
}

.role-badge.student {
  background: rgba(16, 185, 129, 0.2);
  color: #34d399;
}

.role-badge.teacher {
  background: rgba(99, 102, 241, 0.2);
  color: #818cf8;
}

.role-badge.admin {
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
}

.role-creds {
  font-size: 13px;
  color: var(--color-text-secondary);
  font-family: 'SF Mono', monospace;
}

.register-link {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.register-link .link {
  color: var(--color-primary-light);
  cursor: pointer;
  margin-left: 4px;
  transition: color var(--transition-fast);
}

.register-link .link:hover {
  color: var(--color-primary);
}

@media (max-width: 1024px) {
  .login-wrapper {
    flex-direction: column;
    gap: 40px;
    padding: 20px;
  }
  
  .login-info {
    text-align: center;
    max-width: 100%;
  }
  
  .logo-big {
    margin: 0 auto 20px;
  }
  
  .feature-list {
    grid-template-columns: repeat(2, 1fr);
    justify-items: center;
  }
  
  .login-card {
    width: 100%;
    max-width: 420px;
  }
}

@media (max-width: 640px) {
  .app-title {
    font-size: 32px;
  }
  
  .feature-list {
    grid-template-columns: 1fr;
  }
  
  .login-card {
    padding: 30px 20px;
  }
}
</style>
