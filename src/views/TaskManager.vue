<template>
  <AppLayout pageTitle="实训任务" pageSubtitle="教学管理 - 任务发布与作业批改">
    <div class="task-manager-content">
      <div class="content-header">
        <h2 class="page-sub-header">{{ activeNav === 'list' ? '任务列表' : '创建任务' }}</h2>
        <div class="header-actions">
          <el-button 
            v-if="activeNav === 'list'" 
            type="primary" 
            class="gradient-btn" 
            @click="activeNav = 'create'"
          >
            + 新建任务
          </el-button>
          <el-button 
            v-else 
            @click="activeNav = 'list'"
          >
            返回列表
          </el-button>
        </div>
      </div>

      <div v-if="activeNav === 'list'" class="task-list">
        <div v-if="tasks.length === 0" class="empty-state glass-card">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          <p>暂无任务</p>
          <el-button type="primary" class="gradient-btn" @click="activeNav = 'create'">创建第一个任务</el-button>
        </div>

        <div v-else class="task-cards">
          <div v-for="task in tasks" :key="task.id" class="task-card glass-card">
            <div class="card-header">
              <span class="task-type">{{ getTypeLabel(task.type) }}</span>
              <span class="task-status" :class="task.is_active ? 'active' : 'inactive'">
                {{ task.is_active ? '进行中' : '已关闭' }}
              </span>
            </div>
            <h3 class="task-title">{{ task.title }}</h3>
            <p class="task-description">{{ task.description }}</p>
            <div class="card-footer">
              <span class="teacher-name">{{ task.teacher_name }}</span>
              <span v-if="task.deadline" class="deadline">截止：{{ formatDate(task.deadline) }}</span>
            </div>
            <div class="card-actions">
              <el-button size="small" @click="editTask(task)">编辑</el-button>
              <el-button size="small" type="primary" @click="viewSubmissions(task)">查看提交</el-button>
              <el-button size="small" type="danger" @click="deleteTask(task)">删除</el-button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="task-form-container glass-card">
        <el-form ref="taskForm" :model="form" class="task-form">
          <el-form-item label="任务标题" required>
            <el-input v-model="form.title" placeholder="请输入任务标题" />
          </el-form-item>

          <el-form-item label="任务类型" required>
            <el-select v-model="form.type" placeholder="请选择任务类型" style="width: 100%;">
              <el-option label="文本生成" value="text" />
              <el-option label="图像生成" value="image" />
              <el-option label="视频生成" value="video" />
              <el-option label="音频生成" value="audio" />
            </el-select>
          </el-form-item>

          <el-form-item label="任务描述">
            <el-input v-model="form.description" type="textarea" placeholder="请输入任务描述" :rows="3" />
          </el-form-item>

          <el-form-item label="评分标准">
            <el-input v-model="form.requirements" type="textarea" placeholder="请输入评分标准和要求" :rows="4" />
          </el-form-item>

          <el-form-item label="截止时间">
            <el-date-picker
              v-model="form.deadline"
              type="datetime"
              placeholder="请选择截止时间"
              value-format="yyyy-MM-dd HH:mm"
              style="width: 100%;"
            />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" class="gradient-btn" @click="saveTask" :loading="isSaving">
              {{ isEditing ? '保存修改' : '创建任务' }}
            </el-button>
            <el-button v-if="isEditing" @click="cancelEdit">
              取消
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <el-dialog :title="`${currentTask?.title || '任务'} - 学生提交`" :visible.sync="showSubmissions" width="700px">
        <div v-if="submissions.length === 0" class="empty-state-in-dialog">
          <p>暂无学生提交</p>
        </div>
        <div v-else class="submissions-list">
          <div v-for="submission in submissions" :key="submission.id" class="submission-item">
            <div class="submission-header">
              <span class="student-name">{{ submission.student_name }}</span>
              <el-tag :type="submission.status === 'pending' ? 'warning' : 'success'" size="small">
                {{ getStatusLabel(submission.status) }}
              </el-tag>
            </div>
            <p v-if="submission.generated_content" class="submission-content">{{ submission.generated_content }}</p>
            <div v-if="submission.score !== null" class="submission-result">
              <div class="score-display">
                <span class="score-label">评分</span>
                <span class="score-value">{{ submission.score }}</span>
                <span class="score-unit">分</span>
              </div>
              <p v-if="submission.comment" class="comment">{{ submission.comment }}</p>
            </div>
            <div v-else class="grade-actions">
              <el-button type="primary" size="small" @click="openGradeModal(submission)">评分</el-button>
            </div>
          </div>
        </div>
      </el-dialog>

      <el-dialog :title="`评分 - ${gradingSubmission?.student_name}`" :visible.sync="showGradeModal" width="500px">
        <el-form :model="gradeForm" class="grade-form">
          <el-form-item label="分数" required>
            <el-input-number v-model="gradeForm.score" :min="0" :max="100" />
          </el-form-item>
          <el-form-item label="评语">
            <el-input v-model="gradeForm.comment" type="textarea" placeholder="请输入评语" :rows="3" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" class="gradient-btn" @click="submitGrade" :loading="isGrading">
              提交评分
            </el-button>
          </el-form-item>
        </el-form>
      </el-dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import API from '../api'
import AppLayout from '../components/AppLayout.vue'

const activeNav = ref('list')
const tasks = ref([])
const isSaving = ref(false)
const isEditing = ref(false)
const currentTask = ref(null)

const showSubmissions = ref(false)
const submissions = ref([])
const showGradeModal = ref(false)
const gradingSubmission = ref(null)
const isGrading = ref(false)

const form = reactive({
  title: '',
  type: 'text',
  description: '',
  requirements: '',
  deadline: ''
})

const gradeForm = reactive({
  score: null,
  comment: ''
})

const typeLabels = {
  text: '文本生成',
  image: '图像生成',
  video: '视频生成',
  audio: '音频生成'
}

const getTypeLabel = (type) => typeLabels[type] || type

const statusLabels = {
  pending: '待批改',
  completed: '已批改'
}

const getStatusLabel = (status) => statusLabels[status] || status

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

const loadTasks = async () => {
  try {
    tasks.value = await API.getTasks()
  } catch (error) {
    ElMessage.error('加载任务失败')
  }
}

const saveTask = async () => {
  if (!form.title) {
    ElMessage.error('请输入任务标题')
    return
  }

  isSaving.value = true

  try {
    const taskData = {
      title: form.title,
      type: form.type,
      description: form.description,
      requirements: form.requirements,
      deadline: form.deadline ? new Date(form.deadline).toISOString() : null
    }

    if (isEditing.value && currentTask.value) {
      await API.updateTask(currentTask.value.id, taskData)
      ElMessage.success('任务更新成功')
    } else {
      await API.createTask(taskData)
      ElMessage.success('任务创建成功')
    }

    resetForm()
    activeNav.value = 'list'
    await loadTasks()
  } catch (error) {
    ElMessage.error(error.message || '保存失败')
  } finally {
    isSaving.value = false
  }
}

const editTask = (task) => {
  isEditing.value = true
  currentTask.value = task
  form.title = task.title
  form.type = task.type
  form.description = task.description || ''
  form.requirements = task.requirements || ''
  form.deadline = task.deadline || ''
  activeNav.value = 'create'
}

const cancelEdit = () => {
  resetForm()
  isEditing.value = false
  currentTask.value = null
  activeNav.value = 'list'
}

const resetForm = () => {
  form.title = ''
  form.type = 'text'
  form.description = ''
  form.requirements = ''
  form.deadline = ''
}

const deleteTask = async (task) => {
  if (!confirm(`确定要删除任务「${task.title}」吗？`)) return

  try {
    await API.deleteTask(task.id)
    ElMessage.success('删除成功')
    await loadTasks()
  } catch (error) {
    ElMessage.error(error.message || '删除失败')
  }
}

const viewSubmissions = async (task) => {
  currentTask.value = task
  try {
    submissions.value = await API.getTaskSubmissions(task.id)
    showSubmissions.value = true
  } catch (error) {
    ElMessage.error('加载提交列表失败')
  }
}

const openGradeModal = (submission) => {
  gradingSubmission.value = submission
  gradeForm.score = submission.score || null
  gradeForm.comment = submission.comment || ''
  showGradeModal.value = true
}

const submitGrade = async () => {
  if (gradeForm.score === null) {
    ElMessage.error('请输入分数')
    return
  }

  isGrading.value = true

  try {
    await API.gradeSubmission(gradingSubmission.value.id, {
      score: gradeForm.score,
      comment: gradeForm.comment
    })
    ElMessage.success('评分成功')
    showGradeModal.value = false

    if (currentTask.value) {
      submissions.value = await API.getTaskSubmissions(currentTask.value.id)
    }
  } catch (error) {
    ElMessage.error(error.message || '评分失败')
  } finally {
    isGrading.value = false
  }
}

onMounted(() => {
  loadTasks()
})
</script>

<style scoped>
.task-manager-content {
  padding: 0;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.page-sub-header {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.gradient-btn {
  background: var(--gradient-primary);
  border: none;
  font-weight: 500;
}

.task-list {
  min-height: 400px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  color: var(--color-text-muted);
}

.empty-state svg {
  margin-bottom: 16px;
}

.empty-state p {
  margin: 8px 0;
}

.empty-state-in-dialog {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: var(--color-text-muted);
}

.task-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

.task-card {
  padding: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.task-type {
  padding: 4px 12px;
  background: rgba(99, 102, 241, 0.2);
  color: var(--color-primary-light);
  border-radius: 20px;
  font-size: 12px;
}

.task-status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
}

.task-status.active {
  background: rgba(16, 185, 129, 0.2);
  color: var(--color-success);
}

.task-status.inactive {
  background: rgba(245, 158, 11, 0.2);
  color: var(--color-warning);
}

.task-title {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.task-description {
  margin: 0 0 16px 0;
  color: var(--color-text-secondary);
  font-size: 14px;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  color: var(--color-text-muted);
  font-size: 12px;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.task-form-container {
  padding: 30px;
  max-width: 700px;
}

.task-form {
  background: transparent;
}

.submissions-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.submission-item {
  padding: 16px;
  background: var(--color-bg-glass);
  border-radius: var(--radius-md);
}

.submission-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.student-name {
  font-weight: 500;
  color: var(--color-text-primary);
}

.submission-content {
  margin: 8px 0;
  padding: 12px;
  background: var(--color-bg-main);
  border-radius: var(--radius-sm);
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.6;
}

.submission-result {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed var(--color-border);
}

.score-display {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.score-label {
  font-size: 14px;
  color: var(--color-text-muted);
}

.score-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-primary-light);
}

.score-unit {
  font-size: 14px;
  color: var(--color-text-muted);
}

.comment {
  margin: 8px 0 0 0;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.grade-actions {
  margin-top: 12px;
}

.grade-form {
  padding: 10px 0;
}
</style>
