<template>
  <AppLayout pageTitle="首页仪表盘" pageSubtitle="探索 AI 创作的无限可能">
    <div class="dashboard-page">
      <section class="hero-section">
        <div class="hero-content">
          <div class="hero-badge">
            <span class="badge-dot"></span>
            <span>AI 驱动的创意平台</span>
          </div>
          <h1 class="hero-title">
            <span class="gradient-text">释放创意，</span>
            <span class="gradient-text">与 AI 共舞</span>
          </h1>
          <p class="hero-desc">
            一站式 AI 生成平台，支持文本、图像、音频、视频四大模态生成能力，
            让创意不再受限。
          </p>
          <div class="hero-stats">
            <div class="stat-item">
              <span class="stat-number">4</span>
              <span class="stat-label">生成模态</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-number">99%</span>
              <span class="stat-label">生成成功率</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-number">2s</span>
              <span class="stat-label">平均响应</span>
            </div>
          </div>
        </div>
        <div class="hero-visual">
          <div class="floating-card card-1 glass-card glow-border">
            <div class="card-icon text">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
              </svg>
            </div>
            <span>智能写作</span>
          </div>
          <div class="floating-card card-2 glass-card glow-border">
            <div class="card-icon image">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                <polyline points="21 15 16 10 5 21"></polyline>
              </svg>
            </div>
            <span>图像生成</span>
          </div>
          <div class="floating-card card-3 glass-card glow-border">
            <div class="card-icon audio">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
              </svg>
            </div>
            <span>语音合成</span>
          </div>
        </div>
      </section>
      
      <section class="quick-start-section">
        <div class="section-header">
          <h2>快速开始</h2>
          <p>选择一个生成工具，立即开始创作</p>
        </div>
        <div class="quick-cards">
          <router-link to="/text-generate" class="quick-card glass-card glow-border">
            <div class="quick-icon text">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10 9 9 9 8 9"></polyline>
              </svg>
            </div>
            <div class="quick-info">
              <h3>文本生成</h3>
              <p>智能文章、文案撰写、创意写作</p>
            </div>
            <div class="quick-arrow">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </div>
          </router-link>
          
          <router-link to="/image-generate" class="quick-card glass-card glow-border">
            <div class="quick-icon image">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                <polyline points="21 15 16 10 5 21"></polyline>
              </svg>
            </div>
            <div class="quick-info">
              <h3>图像生成</h3>
              <p>AI 绘画、艺术创作、设计素材</p>
            </div>
            <div class="quick-arrow">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </div>
          </router-link>
          
          <router-link to="/video-generate" class="quick-card glass-card glow-border">
            <div class="quick-icon video">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="23 7 16 12 23 17 23 7"></polygon>
                <rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect>
              </svg>
            </div>
            <div class="quick-info">
              <h3>视频生成</h3>
              <p>创意视频、动态内容、短视频</p>
            </div>
            <div class="quick-arrow">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </div>
          </router-link>
          
          <router-link to="/audio-generate" class="quick-card glass-card glow-border">
            <div class="quick-icon audio">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
              </svg>
            </div>
            <div class="quick-info">
              <h3>音频生成</h3>
              <p>语音合成、旁白配音、音效生成</p>
            </div>
            <div class="quick-arrow">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
              </svg>
            </div>
          </router-link>
        </div>
      </section>
      
      <section class="dashboard-grid">
        <div class="grid-left">
          <div class="stats-panel glass-card">
            <div class="panel-header">
              <h3>学习进度</h3>
              <span class="update-time">实时更新</span>
            </div>
            <div class="stats-grid">
              <div class="stat-card">
                <div class="stat-circle" style="--progress: 75%">
                  <svg viewBox="0 0 36 36">
                    <path d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                      class="circle-bg"
                    />
                    <path d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                      class="circle-progress"
                      stroke-dasharray="75, 100"
                    />
                  </svg>
                  <span class="circle-text">75%</span>
                </div>
                <span class="stat-name">总体进度</span>
              </div>
              
              <div class="stat-card">
                <div class="stat-number primary">12</div>
                <span class="stat-name">已完成任务</span>
              </div>
              
              <div class="stat-card">
                <div class="stat-number warning">3</div>
                <span class="stat-name">待完成任务</span>
              </div>
            </div>
            
            <div class="progress-list">
              <div class="progress-item">
                <div class="progress-header">
                  <span>文本生成</span>
                  <span>80%</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 80%"></div>
                </div>
              </div>
              <div class="progress-item">
                <div class="progress-header">
                  <span>图像生成</span>
                  <span>70%</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 70%; background: linear-gradient(90deg, #f472b6, #fb7185)"></div>
                </div>
              </div>
              <div class="progress-item">
                <div class="progress-header">
                  <span>视频生成</span>
                  <span>60%</span>
                </div>
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 60%; background: linear-gradient(90deg, #60a5fa, #06b6d4)"></div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="tasks-panel glass-card">
            <div class="panel-header">
              <h3>待完成任务</h3>
              <router-link to="/student-tasks" class="view-all">查看全部</router-link>
            </div>
            <div class="task-list">
              <div v-for="task in pendingTasks" :key="task.id" class="task-item">
                <div class="task-status" :class="task.status"></div>
                <div class="task-info">
                  <h4>{{ task.title }}</h4>
                  <p>{{ task.type }} · 截止: {{ task.deadline }}</p>
                </div>
                <el-button size="small" class="task-btn" @click="goToTask(task.id)">开始</el-button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="grid-right">
          <div class="works-panel glass-card">
            <div class="panel-header">
              <h3>最近作品</h3>
              <router-link to="/my-works" class="view-all">查看全部</router-link>
            </div>
            <div class="works-scroll">
              <div class="works-list">
                <div v-for="work in recentWorks" :key="work.id" class="work-item">
                  <div class="work-thumb" :style="{ background: work.gradient }">
                    <component :is="getWorkIcon(work.type)" />
                  </div>
                  <div class="work-info">
                    <h4>{{ work.title }}</h4>
                    <p>{{ work.date }}</p>
                  </div>
                  <div class="work-type-tag" :class="work.type">{{ getTypeLabel(work.type) }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="tips-panel glass-card glow-border">
            <div class="tip-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 12.5A2.5 2.5 0 0 1 4.5 10h15A2.5 2.5 0 0 1 22 12.5v4.5A2.5 2.5 0 0 1 19.5 19h-15A2.5 2.5 0 0 1 2 16.5z"></path>
                <path d="M6 10V8a6 6 0 0 1 12 0v2"></path>
              </svg>
            </div>
            <div class="tip-content">
              <h4>今日提示</h4>
              <p>{{ todayTip }}</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, h } from 'vue'
import { ElMessage } from 'element-plus'
import AppLayout from '../components/AppLayout.vue'

const pendingTasks = ref([
  { id: 1, title: '文本生成基础练习', type: '文本生成', deadline: '2024-01-20', status: 'pending' },
  { id: 2, title: '创意图像设计', type: '图像生成', deadline: '2024-01-22', status: 'pending' },
  { id: 3, title: '视频剪辑实训', type: '视频生成', deadline: '2024-01-25', status: 'pending' }
])

const recentWorks = ref([
  { id: 1, title: '科技文章', type: 'text', date: '2024-01-15', gradient: 'linear-gradient(135deg, #6366f1, #8b5cf6)' },
  { id: 2, title: '风景插画', type: 'image', date: '2024-01-14', gradient: 'linear-gradient(135deg, #f472b6, #fb7185)' },
  { id: 3, title: '产品介绍', type: 'text', date: '2024-01-13', gradient: 'linear-gradient(135deg, #6366f1, #8b5cf6)' },
  { id: 4, title: '人物肖像', type: 'image', date: '2024-01-12', gradient: 'linear-gradient(135deg, #60a5fa, #06b6d4)' },
  { id: 5, title: '音频旁白', type: 'audio', date: '2024-01-11', gradient: 'linear-gradient(135deg, #34d399, #10b981)' }
])

const todayTip = ref('使用更具体的提示词可以获得更好的生成效果。尝试添加细节描述，如颜色、风格、场景等，AI 会更准确地理解您的需求。')

const getWorkIcon = (type) => {
  const icons = {
    text: h('svg', { width: '24', height: '24', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('path', { d: 'M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z' }),
      h('polyline', { points: '14 2 14 8 20 8' })
    ]),
    image: h('svg', { width: '24', height: '24', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('rect', { x: '3', y: '3', width: '18', height: '18', rx: '2', ry: '2' }),
      h('circle', { cx: '8.5', cy: '8.5', r: '1.5' }),
      h('polyline', { points: '21 15 16 10 5 21' })
    ]),
    audio: h('svg', { width: '24', height: '24', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('polygon', { points: '11 5 6 9 2 9 2 15 6 15 11 19 11 5' }),
      h('path', { d: 'M15.54 8.46a5 5 0 0 1 0 7.07' })
    ]),
    video: h('svg', { width: '24', height: '24', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, [
      h('polygon', { points: '23 7 16 12 23 17 23 7' }),
      h('rect', { x: '1', y: '5', width: '15', height: '14', rx: '2', ry: '2' })
    ])
  }
  return icons[type] || icons.text
}

const getTypeLabel = (type) => {
  const labels = {
    text: '文本',
    image: '图像',
    audio: '音频',
    video: '视频'
  }
  return labels[type] || type
}

const goToTask = (taskId) => {
  ElMessage.info('跳转到任务页面')
}
</script>

<style scoped>
.dashboard-page {
  animation: fadeInUp 0.5s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  margin-bottom: 40px;
  align-items: center;
}

.hero-content {
  animation-delay: 0.1s;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: var(--color-bg-glass);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  margin-bottom: 20px;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.badge-dot {
  width: 6px;
  height: 6px;
  background: var(--color-success);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--color-success);
}

.hero-title {
  font-size: 48px;
  font-weight: 800;
  line-height: 1.2;
  margin: 0 0 16px;
}

.gradient-text {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline;
}

.hero-desc {
  font-size: 16px;
  color: var(--color-text-secondary);
  line-height: 1.7;
  margin: 0 0 32px;
  max-width: 500px;
}

.hero-stats {
  display: flex;
  align-items: center;
  gap: 24px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 13px;
  color: var(--color-text-muted);
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: var(--color-border);
}

.hero-visual {
  position: relative;
  height: 320px;
}

.floating-card {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 20px;
  width: 140px;
  font-size: 13px;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.card-1 {
  top: 20px;
  left: 20px;
  animation: float1 4s ease-in-out infinite;
}

.card-2 {
  top: 60px;
  right: 40px;
  animation: float2 5s ease-in-out infinite;
}

.card-3 {
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  animation: float3 4.5s ease-in-out infinite;
}

@keyframes float1 {
  0%, 100% { transform: translateY(0) rotate(-2deg); }
  50% { transform: translateY(-15px) rotate(2deg); }
}

@keyframes float2 {
  0%, 100% { transform: translateY(0) rotate(2deg); }
  50% { transform: translateY(-20px) rotate(-2deg); }
}

@keyframes float3 {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(-12px); }
}

.card-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.card-icon.text { background: linear-gradient(135deg, #6366f1, #8b5cf6); }
.card-icon.image { background: linear-gradient(135deg, #f472b6, #fb7185); }
.card-icon.audio { background: linear-gradient(135deg, #06b6d4, #6366f1); }

.section-header {
  text-align: center;
  margin-bottom: 32px;
}

.section-header h2 {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 8px;
  color: var(--color-text-primary);
}

.section-header p {
  margin: 0;
  color: var(--color-text-muted);
}

.quick-start-section {
  margin-bottom: 40px;
}

.quick-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.quick-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  text-decoration: none;
  position: relative;
  overflow: hidden;
}

.quick-icon {
  width: 64px;
  height: 64px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.quick-icon.text { background: linear-gradient(135deg, #6366f1, #8b5cf6); }
.quick-icon.image { background: linear-gradient(135deg, #f472b6, #fb7185); }
.quick-icon.video { background: linear-gradient(135deg, #60a5fa, #06b6d4); }
.quick-icon.audio { background: linear-gradient(135deg, #34d399, #10b981); }

.quick-info {
  flex: 1;
}

.quick-info h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 4px;
  color: var(--color-text-primary);
}

.quick-info p {
  font-size: 13px;
  color: var(--color-text-muted);
  margin: 0;
}

.quick-arrow {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--color-bg-glass);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  transition: all var(--transition-normal);
}

.quick-card:hover .quick-arrow {
  background: var(--gradient-primary);
  color: white;
  transform: translateX(4px);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.grid-left,
.grid-right {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.panel-header h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: var(--color-text-primary);
}

.update-time {
  font-size: 12px;
  color: var(--color-text-muted);
  padding: 4px 10px;
  background: var(--color-bg-glass);
  border-radius: 12px;
}

.view-all {
  font-size: 13px;
  color: var(--color-primary-light);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.view-all:hover {
  color: var(--color-primary);
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background: var(--color-bg-glass);
  border-radius: 16px;
}

.stat-circle {
  position: relative;
  width: 64px;
  height: 64px;
}

.stat-circle svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.circle-bg {
  fill: none;
  stroke: var(--color-border);
  stroke-width: 3;
}

.circle-progress {
  fill: none;
  stroke: url(#circleGradient);
  stroke-width: 3;
  stroke-linecap: round;
  transition: stroke-dasharray 0.5s ease;
}

.stat-circle::before {
  content: '';
  position: absolute;
  inset: 3px;
  border-radius: 50%;
  background: var(--gradient-primary);
  opacity: 0.1;
}

.circle-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 14px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.stat-number {
  font-size: 28px;
  font-weight: 700;
}

.stat-number.primary { color: var(--color-primary-light); }
.stat-number.warning { color: var(--color-warning); }

.stat-name {
  font-size: 12px;
  color: var(--color-text-muted);
}

.progress-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.progress-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.progress-header span:first-child {
  color: var(--color-text-secondary);
}

.progress-header span:last-child {
  color: var(--color-primary-light);
  font-weight: 600;
}

.progress-bar {
  height: 8px;
  background: var(--color-bg-glass);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--gradient-primary);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: var(--color-bg-glass);
  border-radius: 12px;
  transition: all var(--transition-fast);
}

.task-item:hover {
  background: var(--color-bg-glass-hover);
}

.task-status {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-warning);
  box-shadow: 0 0 8px var(--color-warning);
}

.task-info {
  flex: 1;
}

.task-info h4 {
  font-size: 14px;
  font-weight: 500;
  margin: 0 0 4px;
  color: var(--color-text-primary);
}

.task-info p {
  font-size: 12px;
  color: var(--color-text-muted);
  margin: 0;
}

.task-btn {
  background: var(--gradient-primary) !important;
  border: none !important;
  color: white !important;
}

.works-scroll {
  overflow-x: auto;
  padding-bottom: 8px;
}

.works-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.work-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px;
  background: var(--color-bg-glass);
  border-radius: 12px;
  transition: all var(--transition-fast);
}

.work-item:hover {
  background: var(--color-bg-glass-hover);
}

.work-thumb {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.work-info {
  flex: 1;
}

.work-info h4 {
  font-size: 14px;
  font-weight: 500;
  margin: 0 0 4px;
  color: var(--color-text-primary);
}

.work-info p {
  font-size: 12px;
  color: var(--color-text-muted);
  margin: 0;
}

.work-type-tag {
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
}

.work-type-tag.text { background: rgba(99, 102, 241, 0.2); color: #818cf8; }
.work-type-tag.image { background: rgba(244, 114, 182, 0.2); color: #f472b6; }
.work-type-tag.audio { background: rgba(6, 182, 212, 0.2); color: #22d3ee; }
.work-type-tag.video { background: rgba(96, 165, 250, 0.2); color: #60a5fa; }

.tips-panel {
  display: flex;
  gap: 16px;
  padding: 20px;
}

.tip-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #f59e0b, #f97316);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.tip-content h4 {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 6px;
  color: var(--color-text-primary);
}

.tip-content p {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 0;
  line-height: 1.6;
}

@media (max-width: 1200px) {
  .hero-section {
    grid-template-columns: 1fr;
  }
  
  .hero-visual {
    display: none;
  }
  
  .quick-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .hero-title {
    font-size: 32px;
  }
  
  .hero-stats {
    flex-wrap: wrap;
    gap: 16px;
  }
  
  .stat-divider {
    display: none;
  }
  
  .quick-cards {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
