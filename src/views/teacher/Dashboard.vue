<template>
  <AppLayout pageTitle="数据统计" pageSubtitle="教师工作台 - 查看学生学习数据">
    <div class="teacher-dashboard">
      <div class="header-actions">
        <el-select v-model="timePeriod" @change="handlePeriodChange" style="width: 150px;">
          <el-option label="本周" value="week" />
          <el-option label="本月" value="month" />
          <el-option label="本学期" value="all" />
        </el-select>
        <el-button icon="Download" type="primary" @click="handleExportReport">导出报表</el-button>
      </div>
      
      <div class="content-wrapper">
        <div class="stats-row">
          <div class="stat-card glass-card">
            <div class="stat-icon students-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ overview.total_students }}</div>
              <div class="stat-label">学生总数</div>
            </div>
          </div>
          
          <div class="stat-card glass-card">
            <div class="stat-icon tasks-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ overview.total_tasks }}</div>
              <div class="stat-label">任务总数</div>
            </div>
          </div>
          
          <div class="stat-card glass-card">
            <div class="stat-icon submission-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
              </svg>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ overview.submission_rate }}%</div>
              <div class="stat-label">提交率</div>
            </div>
          </div>
          
          <div class="stat-card glass-card">
            <div class="stat-icon score-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
              </svg>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ overview.average_score }}</div>
              <div class="stat-label">平均分</div>
            </div>
          </div>
        </div>
        
        <div class="charts-row">
          <div class="chart-card glass-card">
            <h3>成绩分布</h3>
            <div ref="gradeChartRef" class="chart-container"></div>
          </div>
          
          <div class="chart-card glass-card">
            <h3>任务完成率</h3>
            <div ref="taskChartRef" class="chart-container"></div>
          </div>
        </div>
        
        <div class="charts-row">
          <div class="chart-card wide glass-card">
            <h3>模块使用频次</h3>
            <div ref="moduleChartRef" class="chart-container"></div>
          </div>
        </div>
        
        <div class="recent-section">
          <h3>最近提交</h3>
          <el-table :data="recentSubmissions" stripe style="width: 100%">
            <el-table-column prop="student_name" label="学生" width="120" />
            <el-table-column prop="task_title" label="任务" width="200" />
            <el-table-column prop="submitted_at" label="提交时间" width="180">
              <template #default="{ row }">
                {{ formatDate(row.submitted_at) }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'pending' ? 'warning' : 'success'" size="small">
                  {{ row.status === 'pending' ? '待批改' : '已完成' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" fixed="right" width="120">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="handleGrade(row)">批改</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
      
      <el-dialog title="批改作业" :visible.sync="gradeDialogVisible" width="500px">
        <el-form :model="gradeForm" label-width="80px">
          <el-form-item label="学生">
            <el-input v-model="gradeForm.studentName" disabled />
          </el-form-item>
          <el-form-item label="任务">
            <el-input v-model="gradeForm.taskTitle" disabled />
          </el-form-item>
          <el-form-item label="成绩">
            <el-input-number v-model="gradeForm.score" :min="0" :max="100" />
          </el-form-item>
          <el-form-item label="评语">
            <el-input v-model="gradeForm.comment" type="textarea" :rows="4" placeholder="请输入评语" />
          </el-form-item>
        </el-form>
        <div slot="footer">
          <el-button @click="gradeDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitGrade">提交</el-button>
        </div>
      </el-dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import API from '../../api'
import AppLayout from '../../components/AppLayout.vue'

const timePeriod = ref('week')
const overview = ref({
  total_students: 0,
  total_tasks: 0,
  total_submissions: 0,
  submission_rate: 0,
  average_score: 0,
  pending_grades: 0,
  recent_submissions: []
})

const recentSubmissions = ref([])
const gradeChartRef = ref(null)
const taskChartRef = ref(null)
const moduleChartRef = ref(null)

let gradeChart = null
let taskChart = null
let moduleChart = null

const gradeDialogVisible = ref(false)
const gradeForm = reactive({
  id: null,
  studentName: '',
  taskTitle: '',
  score: 0,
  comment: ''
})

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

const loadOverview = async () => {
  try {
    const data = await API.request('/api/statistics/overview')
    overview.value = data
    recentSubmissions.value = data.recent_submissions || []
  } catch (error) {
    console.error('Load overview error:', error)
    overview.value = {
      total_students: 5,
      total_tasks: 3,
      total_submissions: 12,
      submission_rate: 80,
      average_score: 85.5,
      pending_grades: 3,
      recent_submissions: []
    }
  }
}

const loadGradeDistribution = async () => {
  try {
    const data = await API.request('/api/statistics/grade-distribution')
    initGradeChart(data)
  } catch (error) {
    console.error('Load grade distribution error:', error)
    initGradeChart({
      "0-59": 2,
      "60-69": 5,
      "70-79": 8,
      "80-89": 10,
      "90-100": 5
    })
  }
}

const loadTaskCompletion = async () => {
  try {
    const data = await API.request('/api/statistics/task-completion')
    initTaskChart(data)
  } catch (error) {
    console.error('Load task completion error:', error)
    initTaskChart([
      { title: '文本生成任务', completion_rate: 85 },
      { title: '图像生成任务', completion_rate: 70 },
      { title: '综合实训任务', completion_rate: 60 }
    ])
  }
}

const loadModuleUsage = async () => {
  try {
    const data = await API.request(`/api/statistics/module-usage?period=${timePeriod.value}`)
    initModuleChart(data)
  } catch (error) {
    console.error('Load module usage error:', error)
    initModuleChart({
      text: 45,
      image: 32,
      video: 18,
      audio: 12
    })
  }
}

const initGradeChart = (data) => {
  if (!gradeChartRef.value) return
  
  if (!gradeChart) {
    gradeChart = echarts.init(gradeChartRef.value)
  }
  
  const option = {
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: Object.keys(data),
      axisLabel: { rotate: 0 }
    },
    yAxis: { type: 'value', name: '人数' },
    series: [{
      type: 'bar',
      data: Object.values(data),
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#667eea' },
          { offset: 1, color: '#764ba2' }
        ])
      },
      barRadius: [4, 4, 0, 0]
    }],
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true }
  }
  
  gradeChart.setOption(option)
}

const initTaskChart = (data) => {
  if (!taskChartRef.value) return
  
  if (!taskChart) {
    taskChart = echarts.init(taskChartRef.value)
  }
  
  const chartData = data.map(item => ({
    name: item.title,
    value: item.completion_rate
  }))
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}%'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}: {c}%'
      },
      data: chartData,
      color: ['#667eea', '#764ba2', '#f093fb', '#f5576c']
    }]
  }
  
  taskChart.setOption(option)
}

const initModuleChart = (data) => {
  if (!moduleChartRef.value) return
  
  if (!moduleChart) {
    moduleChart = echarts.init(moduleChartRef.value)
  }
  
  const moduleNames = {
    text: '文本生成',
    image: '图像生成',
    video: '视频生成',
    audio: '音频生成'
  }
  
  const option = {
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['文本生成', '图像生成', '视频生成', '音频生成']
    },
    yAxis: { type: 'value', name: '使用次数' },
    series: [{
      type: 'line',
      data: [data.text || 0, data.image || 0, data.video || 0, data.audio || 0],
      smooth: true,
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(102, 126, 234, 0.5)' },
          { offset: 1, color: 'rgba(102, 126, 234, 0.1)' }
        ])
      },
      lineStyle: { color: '#667eea', width: 3 },
      itemStyle: { color: '#667eea' }
    }],
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true }
  }
  
  moduleChart.setOption(option)
}

const handlePeriodChange = () => {
  loadModuleUsage()
}

const handleExportReport = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/statistics/export-report`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    
    if (!response.ok) throw new Error('Export failed')
    
    const blob = await response.blob()
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'grade_report.xlsx'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
    
    ElMessage.success('报表导出成功')
  } catch (error) {
    console.error('Export error:', error)
    ElMessage.error('报表导出失败')
  }
}

const handleGrade = (row) => {
  gradeForm.id = row.id
  gradeForm.studentName = row.student_name
  gradeForm.taskTitle = row.task_title
  gradeForm.score = row.score || 0
  gradeForm.comment = row.comment || ''
  gradeDialogVisible.value = true
}

const submitGrade = async () => {
  try {
    await API.updateGrade(gradeForm.id, {
      score: gradeForm.score,
      comment: gradeForm.comment
    })
    
    ElMessage.success('批改成功')
    gradeDialogVisible.value = false
    loadOverview()
  } catch (error) {
    console.error('Grade error:', error)
    ElMessage.error('批改失败')
  }
}

const handleResize = () => {
  gradeChart?.resize()
  taskChart?.resize()
  moduleChart?.resize()
}

onMounted(() => {
  loadOverview()
  loadGradeDistribution()
  loadTaskCompletion()
  loadModuleUsage()
  
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  gradeChart?.dispose()
  taskChart?.dispose()
  moduleChart?.dispose()
})
</script>

<style scoped>
.teacher-dashboard {
  display: flex;
  min-height: 100vh;
  background: #f5f7fa;
}

.sidebar {
  width: 220px;
  background: #1a1a2e;
  color: white;
  display: flex;
  flex-direction: column;
}

.logo {
  display: flex;
  align-items: center;
  padding: 20px;
  gap: 10px;
  font-size: 16px;
  font-weight: 600;
  border-bottom: 1px solid #2d2d44;
}

.nav-menu {
  flex: 1;
  padding: 10px;
}

:deep(.el-menu) {
  background: transparent;
  border: none;
}

:deep(.el-menu-item), :deep(.el-sub-menu__title) {
  color: rgba(255, 255, 255, 0.8);
  margin: 5px 0;
  border-radius: 8px;
}

:deep(.el-menu-item:hover), :deep(.el-sub-menu__title:hover) {
  background: rgba(102, 126, 234, 0.3);
}

:deep(.el-menu-item.active) {
  background: #667eea;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.header h1 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.content-wrapper {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.students-icon {
  background: #e8f4fd;
  color: #3b82f6;
}

.tasks-icon {
  background: #dcfce7;
  color: #22c55e;
}

.submission-icon {
  background: #fef3c7;
  color: #f59e0b;
}

.score-icon {
  background: #fce7f3;
  color: #ec4899;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a2e;
}

.stat-label {
  font-size: 14px;
  color: #999;
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.chart-card.wide {
  grid-column: span 2;
}

.chart-card h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1a1a2e;
}

.chart-container {
  height: 300px;
}

.recent-section {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.recent-section h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1a1a2e;
}
</style>