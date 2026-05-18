<template>
  <div class="register-page">
    <div class="particles-bg"></div>
    
    <div class="register-wrapper">
      <div class="register-info">
        <div class="logo-big animate-float">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
            <path d="M2 17l10 5 10-5"></path>
            <path d="M2 12l10 5 10-5"></path>
          </svg>
        </div>
        <h1 class="app-title">加入 AIGC 实训平台</h1>
        <p class="app-subtitle">开启您的 AI 创作学习之旅</p>
        
        <div class="benefits-list">
          <div class="benefit-item">
            <div class="benefit-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
            <div class="benefit-content">
              <h4>免费体验</h4>
              <p>四大 AI 生成工具免费试用</p>
            </div>
          </div>
          <div class="benefit-item">
            <div class="benefit-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
            </div>
            <div class="benefit-content">
              <h4>学习跟踪</h4>
              <p>记录您的学习进度和成就</p>
            </div>
          </div>
          <div class="benefit-item">
            <div class="benefit-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="8" r="7"></circle>
                <polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline>
              </svg>
            </div>
            <div class="benefit-content">
              <h4>社区支持</h4>
              <p>与其他学习者交流分享</p>
            </div>
          </div>
        </div>
      </div>
      
      <div class="register-card glass-card glow-border animate-slide-in-up">
        <div class="card-header">
          <div class="logo-small">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
              <path d="M2 17l10 5 10-5"></path>
              <path d="M2 12l10 5 10-5"></path>
            </svg>
          </div>
          <h2>创建账号</h2>
          <p>只需几步即可开始您的 AI 之旅</p>
        </div>
        
        <el-form ref="registerForm" :model="form" class="register-form">
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
          
          <el-form-item prop="email">
            <el-input 
              v-model="form.email" 
              placeholder="请输入邮箱地址" 
              size="large"
              class="custom-input"
            >
              <template #prefix>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                  <polyline points="22,6 12,13 2,6"></polyline>
                </svg>
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input 
              v-model="form.password" 
              type="password" 
              placeholder="请输入密码（至少6位）" 
              size="large"
              show-password
              class="custom-input"
            >
              <template #prefix>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item prop="confirmPassword">
            <el-input 
              v-model="form.confirmPassword" 
              type="password" 
              placeholder="请再次输入密码" 
              size="large"
              show-password
              class="custom-input"
            >
              <template #prefix>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                </svg>
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item prop="role">
            <el-select v-model="form.role" placeholder="请选择您的身份" size="large" class="custom-select">
              <template #prefix>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="9" cy="7" r="4"></circle>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
              </template>
              <el-option label="学生" value="student">
                <div class="option-item">
                  <span class="option-icon student">🎓</span>
                  <div class="option-info">
                    <span class="option-label">学生</span>
                    <span class="option-desc">学习课程、完成实训任务</span>
                  </div>
                </div>
              </el-option>
              <el-option label="教师" value="teacher">
                <div class="option-item">
                  <span class="option-icon teacher">👨‍🏫</span>
                  <div class="option-info">
                    <span class="option-label">教师</span>
                    <span class="option-desc">管理课程、指导学生学习</span>
                  </div>
                </div>
              </el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item prop="agreed">
            <el-checkbox v-model="form.agreed" class="custom-checkbox">
              我已阅读并同意
              <span class="agreement-link">《用户协议》</span>
              和
              <span class="agreement-link">《隐私政策》</span>
            </el-checkbox>
          </el-form-item>
          
          <el-button 
            class="register-btn gradient-btn" 
            type="primary" 
            size="large" 
            @click="handleRegister" 
            :loading="isLoading"
          >
            <svg v-if="!isLoading" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            {{ isLoading ? '注册中...' : '立即注册' }}
          </el-button>
        </el-form>
        
        <div class="login-link">
          <span>已有账号？</span>
          <span class="link" @click="$router.push('/')">立即登录</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  role: 'student',
  agreed: false
})

const isLoading = ref(false)

const handleRegister = async () => {
  if (!form.username) {
    ElMessage.error('请输入用户名')
    return
  }
  
  if (!form.email) {
    ElMessage.error('请输入邮箱地址')
    return
  }
  
  if (!form.password) {
    ElMessage.error('请输入密码')
    return
  }
  
  if (form.password.length < 6) {
    ElMessage.error('密码至少需要6位')
    return
  }
  
  if (form.password !== form.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  
  if (!form.agreed) {
    ElMessage.error('请同意用户协议和隐私政策')
    return
  }
  
  isLoading.value = true
  
  try {
    const response = await fetch('http://localhost:8000/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: form.username,
        email: form.email,
        password: form.password,
        full_name: form.username
      })
    })
    
    const data = await response.json()
    
    if (!response.ok) {
      throw new Error(data.detail || '注册失败')
    }
    
    ElMessage.success('注册成功，请登录')
    
    setTimeout(() => {
      window.location.href = '/'
    }, 1000)
  } catch (error) {
    ElMessage.error(error.message || '注册失败，请稍后重试')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.register-page {
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

.register-wrapper {
  display: flex;
  align-items: center;
  gap: 80px;
  max-width: 1200px;
  padding: 40px;
  position: relative;
  z-index: 1;
}

.register-info {
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
  font-size: 38px;
  font-weight: 700;
  margin: 0 0 12px;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.app-subtitle {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin: 0 0 32px;
}

.benefits-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  background: var(--color-bg-glass);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  transition: all var(--transition-normal);
}

.benefit-item:hover {
  background: var(--color-bg-glass-hover);
  transform: translateX(4px);
}

.benefit-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary-light);
  flex-shrink: 0;
}

.benefit-content h4 {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 2px;
  color: var(--color-text-primary);
}

.benefit-content p {
  font-size: 12px;
  margin: 0;
  color: var(--color-text-muted);
}

.register-card {
  width: 440px;
  padding: 36px;
  animation-delay: 0.2s;
}

.card-header {
  text-align: center;
  margin-bottom: 28px;
}

.logo-small {
  width: 48px;
  height: 48px;
  margin: 0 auto 12px;
  background: var(--gradient-primary);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.card-header h2 {
  font-size: 22px;
  font-weight: 600;
  margin: 0 0 6px;
  color: var(--color-text-primary);
}

.card-header p {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 0;
}

.register-form {
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

.custom-select {
  width: 100%;
}

:deep(.custom-select .el-select__wrapper) {
  padding: 12px 16px !important;
  border-radius: var(--radius-md) !important;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.option-icon {
  font-size: 24px;
}

.option-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.option-label {
  font-weight: 500;
  color: var(--color-text-primary);
}

.option-desc {
  font-size: 12px;
  color: var(--color-text-muted);
}

:deep(.custom-checkbox .el-checkbox__label) {
  color: var(--color-text-secondary) !important;
  font-size: 13px;
}

.agreement-link {
  color: var(--color-primary-light);
  cursor: pointer;
  transition: color var(--transition-fast);
}

.agreement-link:hover {
  color: var(--color-primary);
  text-decoration: underline;
}

.register-btn {
  width: 100%;
  height: 52px;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 8px;
}

:deep(.register-btn) {
  background: var(--gradient-primary) !important;
  border: none !important;
  border-radius: var(--radius-md) !important;
}

:deep(.register-btn:hover) {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4) !important;
}

.login-link {
  text-align: center;
  margin-top: 24px;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.login-link .link {
  color: var(--color-primary-light);
  cursor: pointer;
  margin-left: 4px;
  transition: color var(--transition-fast);
}

.login-link .link:hover {
  color: var(--color-primary);
}

@media (max-width: 1024px) {
  .register-wrapper {
    flex-direction: column;
    gap: 40px;
    padding: 20px;
  }
  
  .register-info {
    text-align: center;
    max-width: 100%;
  }
  
  .logo-big {
    margin: 0 auto 20px;
  }
  
  .benefits-list {
    align-items: center;
  }
  
  .benefit-item {
    max-width: 350px;
    width: 100%;
  }
  
  .register-card {
    width: 100%;
    max-width: 440px;
  }
}

@media (max-width: 640px) {
  .app-title {
    font-size: 28px;
  }
  
  .register-card {
    padding: 28px 20px;
  }
}
</style>
