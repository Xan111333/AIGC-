<template>
  <AppLayout pageTitle="实训任务" pageSubtitle="完成任务，提交作业，获取反馈">
    <div class="student-tasks-content">
      <div class="filter-tabs">
        <el-radio-group v-model="activeFilter" class="filter-group">
          <el-radio-button
            v-for="tab in filterTabs"
            :key="tab.key"
            :label="tab.key"
            @change="activeFilter = tab.key"
          >
            {{ tab.label }}
          </el-radio-button>
        </el-radio-group>
      </div>

      <div v-if="filteredTasks.length === 0" class="empty-state glass-card">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
        <p>暂无{{ filterTabs.find(t => t.key === activeFilter)?.label }}</p>
      </div>

      <div v-else class="tasks-grid">
        <div
          v-for="task in filteredTasks"
          :key="task.id"
          class="task-card glass-card"
          @click="openTaskDetail(task)"
        >
          <div class="card-badge" :class="getTaskStatus(task)">
            {{ getStatusText(task) }}
          </div>
          <div class="card-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path :d="getTaskIconPath(task.type)" />
            </svg>
          </div>
          <h3 class="card-title">{{ task.title }}</h3>
          <p class="card-description">{{ task.description }}</p>
          <div class="card-meta">
            <span class="meta-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 20h5v-2a3 3 0 0 0-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 0 1 5.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 0 1 9.288 0M15 7a3 3 0 1 1-6 0 3 3 0 0 1 6 0zm6 3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zM7 10a2 2 0 1 1-4 0 2 2 0 0 1 4 0z"></path>
              </svg>
              {{ task.teacher_name }}
            </span>
            <span v-if="task.deadline" class="meta-item deadline">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              {{ formatDeadline(task.deadline) }}
            </span>
          </div>
          <div class="card-action">
            <span>查看详情</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 5l7 7-7 7"></path>
            </svg>
          </div>
        </div>
      </div>

      <el-dialog :title="`${currentTask?.title || '任务详情'}`" :visible.sync="showDetail" width="700px">
        <div v-if="currentTask" class="task-detail-content">
          <div class="detail-header">
            <el-tag size="small">{{ getTypeLabel(currentTask.type) }}</el-tag>
            <el-tag :type="getTaskStatus(currentTask) === 'pending' ? 'warning' : getTaskStatus(currentTask) === 'completed' ? 'success' : 'info'" size="small">
              {{ getStatusText(currentTask) }}
            </el-tag>
          </div>

          <h2 class="task-title">{{ currentTask.title }}</h2>
          <p class="task-description">{{ currentTask.description }}</p>

          <div class="task-section">
            <h3>评分标准</h3>
            <p>{{ currentTask.requirements || '暂无评分标准' }}</p>
          </div>

          <div class="task-section">
            <h3>任务信息</h3>
            <div class="info-grid">
              <div class="info-item">
                <span class="label">发布教师</span>
                <span class="value">{{ currentTask.teacher_name }}</span>
              </div>
              <div class="info-item">
                <span class="label">任务类型</span>
                <span class="value">{{ getTypeLabel(currentTask.type) }}</span>
              </div>
              <div class="info-item">
                <span class="label">截止时间</span>
                <span class="value" :class="{ deadline: currentTask.deadline }">{{ currentTask.deadline ? formatDate(currentTask.deadline) : '未设置' }}</span>
              </div>
              <div class="info-item">
                <span class="label">发布时间</span>
                <span class="value">{{ currentTask.created_at ? formatDate(currentTask.created_at) : '-' }}</span>
              </div>
            </div>
          </div>

          <div v-if="mySubmission" class="task-section submission-section">
            <h3>我的提交</h3>
            <div class="submission-card">
              <div class="submission-header">
                <el-tag :type="mySubmission.status === 'pending' ? 'warning' : 'success'" size="small">
                  {{ getStatusTextByStatus(mySubmission.status) }}
                </el-tag>
                <span class="submission-time">提交于 {{ formatDate(mySubmission.submitted_at) }}</span>
              </div>
              <p class="submission-content">{{ mySubmission.generated_content }}</p>
              <div v-if="mySubmission.score !== null" class="submission-result">
                <div class="score-display">
                  <span class="score-label">得分</span>
                  <span class="score-value">{{ mySubmission.score }}</span>
                  <span class="score-unit">分</span>
                </div>
                <div v-if="mySubmission.comment" class="comment-box">
                  <span class="comment-label">评语</span>
                  <p>{{ mySubmission.comment }}</p>
                </div>
              </div>
            </div>
          </div>

          <div v-else-if="canSubmit" class="task-section">
            <h3>提交作业</h3>
            <el-form :model="submitForm" class="submit-form">
              <el-form-item label="作业内容">
                <el-input
                  v-model="submitForm.content"
                  type="textarea"
                  placeholder="请输入您的作业内容或粘贴生成的作品..."
                  :rows="5"
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" class="gradient-btn" @click="submitAssignment" :loading="isSubmitting">
                  提交作业
                </el-button>
              </el-form-item>
            </el-form>
          </div>

          <div v-else class="task-section">
            <div class="no-submit-hint">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 8v4l3 3"></path>
                <circle cx="12" cy="12" r="10"></circle>
              </svg>
              <p>任务已截止，无法提交</p>
            </div>
          </div>
        </div>
      </el-dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import API from '../api'
import AppLayout from '../components/AppLayout.vue'

const tasks = ref([])
const submissions = ref([])
const activeFilter = ref('all')
const showDetail = ref(false)
const currentTask = ref(null)
const isSubmitting = ref(false)

const filterTabs = [
  { key: 'all', label: '全部任务' },
  { key: 'pending', label: '待提交' },
  { key: 'submitted', label: '已提交' },
  { key: 'completed', label: '已批改' }
]

const submitForm = reactive({
  content: ''
})

const typeLabels = {
  text: '文本生成',
  image: '图像生成',
  video: '视频生成',
  audio: '音频生成'
}

const iconPaths = {
  text: 'M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2zM14 2v6h6M16 13H8M16 17H8M10 9H9H8',
  image: 'M3 3h18v18H3zM8.5 8.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3zM21 15l-5-5L5 21',
  video: 'M23 7l-7 5 7 5V7zM1 5h15a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H1a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z',
  audio: 'M11 5l-5 4H2v6h4l5 4V5zM15.54 8.46a5 5 0 0 1 0 7.07M19.07 4.93a10 10 0 0 1 0 14.14'
}

const getTypeLabel = (type) => typeLabels[type] || type

const getTaskIconPath = (type) => {
  return iconPaths[type] || iconPaths.text
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatDeadline = (dateStr) => {
  if (!dateStr) return '未设置'
  const date = new Date(dateStr)
  const now = new Date()

  if (date < now) {
    return '已截止'
  }

  const diff = Math.floor((date - now) / (1000 * 60 * 60 * 24))

  if (diff === 0) {
    return '今天截止'
  } else if (diff === 1) {
    return '明天截止'
  } else if (diff < 7) {
    return `${diff}天后截止`
  } else {
    return date.toLocaleDateString('zh-CN')
  }
}

const getTaskStatus = (task) => {
  if (!task) return 'unknown'

  const submission = submissions.value.find(s => s.task_id === task.id)

  if (!submission) {
    const deadline = task.deadline ? new Date(task.deadline) : null
    if (deadline && deadline < new Date()) {
      return 'expired'
    }
    return 'pending'
  }

  return submission.status
}

const getStatusText = (task) => {
  const status = getTaskStatus(task)

  const statusMap = {
    pending: '待提交',
    submitted: '已提交',
    completed: '已批改',
    expired: '已过期'
  }

  return statusMap[status] || '未知'
}

const getStatusTextByStatus = (status) => {
  const statusMap = {
    pending: '待批改',
    submitted: '已提交',
    completed: '已批改'
  }
  return statusMap[status] || status
}

const filteredTasks = computed(() => {
  return tasks.value.filter(task => {
    if (activeFilter.value === 'all') return true

    const status = getTaskStatus(task)
    return status === activeFilter.value
  })
})

const mySubmission = computed(() => {
  if (!currentTask.value) return null
  return submissions.value.find(s => s.task_id === currentTask.value.id)
})

const canSubmit = computed(() => {
  if (!currentTask.value) return false

  if (mySubmission.value) return false

  const deadline = currentTask.value.deadline ? new Date(currentTask.value.deadline) : null
  return !deadline || deadline > new Date()
})

const loadTasks = async () => {
  try {
    tasks.value = await API.getTasks()
  } catch (error) {
    ElMessage.error('加载任务失败')
  }
}

const loadSubmissions = async () => {
  try {
    submissions.value = await API.getMySubmissions()
  } catch (error) {
    ElMessage.error('加载提交记录失败')
  }
}

const openTaskDetail = (task) => {
  currentTask.value = task
  showDetail.value = true
}

const submitAssignment = async () => {
  if (!submitForm.content.trim()) {
    ElMessage.error('请输入作业内容')
    return
  }

  isSubmitting.value = true

  try {
    await API.submitSubmission({
      task_id: currentTask.value.id,
      generated_content: submitForm.content
    })

    ElMessage.success('提交成功')
    submitForm.content = ''
    await loadSubmissions()
  } catch (error) {
    ElMessage.error(error.message || '提交失败')
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  loadTasks()
  loadSubmissions()
})
</script>

<style scoped>
.student-tasks-content {
  padding: 0;
}

.filter-tabs {
  margin-bottom: 24px;
}

.filter-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

:deep(.el-radio-button__inner) {
  background: var(--color-bg-glass);
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  transition: all 0.3s;
}

:deep(.el-radio-button__inner:hover) {
  background: var(--color-bg-glass-hover);
  color: var(--color-text-primary);
}

:deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: var(--gradient-primary);
  border-color: transparent;
  color: white;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px;
  color: var(--color-text-muted);
}

.empty-state svg {
  margin-bottom: 16px;
}

.empty-state p {
  margin: 0;
}

.tasks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.task-card {
  position: relative;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s;
}

.task-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: rgba(99, 102, 241, 0.3);
}

.card-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
}

.card-badge.pending {
  background: rgba(245, 158, 11, 0.2);
  color: var(--color-warning);
}

.card-badge.submitted {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}

.card-badge.completed {
  background: rgba(16, 185, 129, 0.2);
  color: var(--color-success);
}

.card-badge.expired {
  background: rgba(239, 68, 68, 0.2);
  color: var(--color-error);
}

.card-icon {
  width: 56px;
  height: 56px;
  margin-bottom: 16px;
  background: var(--color-bg-glass);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary-light);
}

.card-title {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.card-description {
  margin: 0 0 16px 0;
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--color-text-muted);
  font-size: 13px;
}

.meta-item.deadline {
  color: var(--color-warning);
}

.card-action {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16px;
  border-top: 1px solid var(--color-border);
  color: var(--color-primary-light);
  font-size: 14px;
}

.task-detail-content {
  padding: 10px 0;
}

.detail-header {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.task-title {
  margin: 0 0 12px 0;
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.task-description {
  margin: 0 0 24px 0;
  color: var(--color-text-secondary);
  font-size: 15px;
  line-height: 1.6;
}

.task-section {
  margin-bottom: 24px;
}

.task-section h3 {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  padding-bottom: 8px;
  border-bottom: 2px solid rgba(99, 102, 241, 0.2);
}

.task-section p {
  margin: 0;
  color: var(--color-text-secondary);
  line-height: 1.6;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item .label {
  font-size: 13px;
  color: var(--color-text-muted);
}

.info-item .value {
  font-size: 14px;
  color: var(--color-text-primary);
}

.info-item .value.deadline {
  color: var(--color-warning);
}

.submission-section .submission-card {
  background: var(--color-bg-glass);
  border-radius: 8px;
  padding: 16px;
}

.submission-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.submission-time {
  font-size: 12px;
  color: var(--color-text-muted);
}

.submission-content {
  margin: 0 0 16px 0;
  padding: 12px;
  background: var(--color-bg-main);
  border-radius: 6px;
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.6;
}

.submission-result {
  padding-top: 16px;
  border-top: 1px dashed var(--color-border);
}

.score-display {
  display: flex;
  align-items: baseline;
  gap: 4px;
  margin-bottom: 12px;
}

.score-label {
  font-size: 14px;
  color: var(--color-text-muted);
}

.score-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-primary-light);
}

.score-unit {
  font-size: 14px;
  color: var(--color-text-muted);
}

.comment-box {
  padding: 12px;
  background: rgba(99, 102, 241, 0.1);
  border-radius: 6px;
}

.comment-label {
  display: block;
  font-size: 12px;
  color: var(--color-primary-light);
  margin-bottom: 4px;
}

.comment-box p {
  margin: 0;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.submit-form {
  background: var(--color-bg-glass);
  border-radius: 8px;
  padding: 16px;
}

.gradient-btn {
  background: var(--gradient-primary);
  border: none;
  font-weight: 500;
}

.no-submit-hint {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  color: var(--color-text-muted);
}

.no-submit-hint svg {
  margin-bottom: 12px;
}

.no-submit-hint p {
  margin: 0;
}
</style>
