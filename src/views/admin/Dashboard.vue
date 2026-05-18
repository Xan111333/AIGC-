<template>
  <AppLayout pageTitle="系统概览" pageSubtitle="管理后台 - 系统状态总览">
    <div class="admin-dashboard-content">
      <div class="header-info">
        <span>欢迎，{{ currentUser }}</span>
      </div>
      
      <div class="content-wrapper">
        <div class="stats-grid">
          <div class="stat-card glass-card" v-for="stat in statsCards" :key="stat.title">
            <div class="stat-icon" :class="stat.iconClass">
              <component :is="stat.icon" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-label">{{ stat.title }}</div>
            </div>
          </div>
        </div>
        
        <div class="quick-actions">
          <h3>快捷操作</h3>
          <div class="actions-grid">
            <router-link to="/admin/users" class="action-card">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="8.5" cy="7" r="4"></circle>
                <line x1="20" y1="8" x2="20" y2="14"></line>
                <line x1="23" y1="11" x2="17" y2="11"></line>
              </svg>
              <span>添加用户</span>
            </router-link>
            <router-link to="/admin/config" class="action-card">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
              <span>系统配置</span>
            </router-link>
            <router-link to="/admin/review" class="action-card">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="9" y1="15" x2="15" y2="15"></line>
              </svg>
              <span>内容审核</span>
            </router-link>
            <router-link to="/admin/logs" class="action-card">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
              </svg>
              <span>查看日志</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted, h } from 'vue'
import { ElMessage } from 'element-plus'
import API from '../../api'
import AppLayout from '../../components/AppLayout.vue'

const currentUser = ref('')

const stats = reactive({
  totalUsers: 0,
  totalStudents: 0,
  totalTeachers: 0,
  totalTasks: 0,
  pendingContents: 0
})

const statsCards = computed(() => [
  {
    title: '总用户数',
    value: stats.totalUsers,
    iconClass: 'users-icon',
    icon: () => h('svg', { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
      h('path', { d: 'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2' }),
      h('circle', { cx: 9, cy: 7, r: 4 }),
      h('path', { d: 'M23 21v-2a4 4 0 0 0-3-3.87' }),
      h('path', { d: 'M16 3.13a4 4 0 0 1 0 7.75' })
    ])
  },
  {
    title: '学生数',
    value: stats.totalStudents,
    iconClass: 'students-icon',
    icon: () => h('svg', { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
      h('path', { d: 'M22 10v6M2 10l10-5 10 5-10 5z' }),
      h('path', { d: 'M6 12v5c3 3 9 3 12 0v-5' })
    ])
  },
  {
    title: '教师数',
    value: stats.totalTeachers,
    iconClass: 'teachers-icon',
    icon: () => h('svg', { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
      h('path', { d: 'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2' }),
      h('circle', { cx: 9, cy: 7, r: 4 }),
      h('path', { d: 'M23 21v-2a4 4 0 0 0-3-3.87' }),
      h('path', { d: 'M16 3.13a4 4 0 0 1 0 7.75' })
    ])
  },
  {
    title: '待审核内容',
    value: stats.pendingContents,
    iconClass: 'pending-icon',
    icon: () => h('svg', { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': 2 }, [
      h('circle', { cx: 12, cy: 12, r: 10 }),
      h('line', { x1: 12, y1: 8, x2: 12, y2: 12 }),
      h('line', { x1: 12, y1: 16, x2: 12.01, y2: 16 })
    ])
  }
])

const loadStatistics = async () => {
  try {
    const data = await API.request('/api/admin/statistics')
    stats.totalUsers = data.total_users || 0
    stats.totalStudents = data.total_students || 0
    stats.totalTeachers = data.total_teachers || 0
    stats.pendingContents = data.pending_contents || 0
    stats.totalTasks = data.total_tasks || 0
  } catch (error) {
    console.error('Load statistics error:', error)
  }
}

const loadUser = () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  currentUser.value = user.full_name || user.username || 'Admin'
}

onMounted(() => {
  loadUser()
  loadStatistics()
})
</script>

<style scoped>
.admin-dashboard-content {
  padding: 24px;
}

.header-info {
  text-align: right;
  margin-bottom: 24px;
  font-size: 14px;
  color: #666;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.users-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.students-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.teachers-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.pending-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.quick-actions {
  margin-top: 24px;
}

.quick-actions h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #1a1a2e;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 16px;
}

.action-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px;
  background: white;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e8e8e8;
  color: #666;
  text-decoration: none;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  border-color: #10b981;
  color: #10b981;
}

.action-card svg {
  margin-bottom: 12px;
}

.action-card span {
  font-size: 14px;
  font-weight: 500;
}
</style>