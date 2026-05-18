<template>
  <AppLayout pageTitle="学习进度" pageSubtitle="查看您的学习数据和成绩">
    <div class="progress-content">
      <div class="stats-row">
        <div class="stat-card glass-card">
          <div class="stat-icon task-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ progress.completed_tasks }}/{{ progress.total_tasks }}</div>
            <div class="stat-label">完成任务</div>
          </div>
        </div>

        <div class="stat-card glass-card">
          <div class="stat-icon score-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ progress.average_score || 0 }}</div>
            <div class="stat-label">平均分</div>
          </div>
        </div>

        <div class="stat-card glass-card">
          <div class="stat-icon submission-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ progress.total_submissions || 0 }}</div>
            <div class="stat-label">作业提交</div>
          </div>
        </div>

        <div class="stat-card glass-card">
          <div class="stat-icon rate-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="20" x2="12" y2="10"></line>
              <line x1="18" y1="20" x2="18" y2="4"></line>
              <line x1="6" y1="20" x2="6" y2="16"></line>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ progress.completion_rate || 0 }}%</div>
            <div class="stat-label">完成率</div>
          </div>
        </div>
      </div>

      <div class="charts-row">
        <div class="chart-card glass-card">
          <h3>各模块练习次数</h3>
          <div ref="radarChartRef" class="chart-container"></div>
        </div>

        <div class="chart-card glass-card">
          <h3>模块使用分布</h3>
          <div ref="pieChartRef" class="chart-container"></div>
        </div>
      </div>

      <div class="progress-section glass-card">
        <h3>我的作业</h3>
        <el-table :data="submissions" stripe style="width: 100%;">
          <el-table-column prop="task_title" label="任务" width="250" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.status === 'pending' ? 'warning' : 'success'" size="small">
                {{ row.status === 'pending' ? '待批改' : '已完成' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="score" label="成绩" width="100">
            <template #default="{ row }">
              <span v-if="row.score">{{ row.score }}分</span>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column prop="comment" label="评语" />
          <el-table-column prop="submitted_at" label="提交时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.submitted_at) }}
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import API from '../../api'
import AppLayout from '../../components/AppLayout.vue'

const progress = ref({
  completed_tasks: 0,
  total_tasks: 0,
  completion_rate: 0,
  average_score: 0,
  total_submissions: 0,
  module_usage: {
    text: 0,
    image: 0,
    video: 0,
    audio: 0
  }
})

const submissions = ref([])
const radarChartRef = ref(null)
const pieChartRef = ref(null)

let radarChart = null
let pieChart = null

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

const loadProgress = async () => {
  try {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    const studentId = user.id || 3

    const data = await API.getStudentProgress(studentId)
    progress.value = data
  } catch (error) {
    console.error('Load progress error:', error)
    progress.value = {
      completed_tasks: 3,
      total_tasks: 5,
      completion_rate: 60,
      average_score: 85.5,
      total_submissions: 8,
      module_usage: {
        text: 15,
        image: 10,
        video: 5,
        audio: 3
      }
    }
  }
}

const loadSubmissions = async () => {
  try {
    const data = await API.request('/api/submissions/my')
    submissions.value = data
  } catch (error) {
    console.error('Load submissions error:', error)
    submissions.value = [
      {
        id: 1,
        task_title: '文本生成任务',
        status: 'completed',
        score: 88,
        comment: '表现优秀',
        submitted_at: '2024-01-15T10:30:00'
      },
      {
        id: 2,
        task_title: '图像生成任务',
        status: 'pending',
        score: null,
        comment: null,
        submitted_at: '2024-01-18T14:20:00'
      }
    ]
  }
}

const initRadarChart = () => {
  if (!radarChartRef.value) return

  if (!radarChart) {
    radarChart = echarts.init(radarChartRef.value)
  }

  const usage = progress.value.module_usage || { text: 0, image: 0, video: 0, audio: 0 }

  const option = {
    tooltip: {},
    radar: {
      indicator: [
        { name: '文本生成', max: 50 },
        { name: '图像生成', max: 50 },
        { name: '视频生成', max: 50 },
        { name: '音频生成', max: 50 }
      ],
      shape: 'polygon',
      splitNumber: 5,
      axisName: {
        color: '#94a3b8'
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(99, 102, 241, 0.2)'
        }
      },
      splitArea: {
        show: true,
        areaStyle: {
          color: [
            'rgba(99, 102, 241, 0.03)',
            'rgba(99, 102, 241, 0.06)',
            'rgba(99, 102, 241, 0.09)',
            'rgba(99, 102, 241, 0.12)',
            'rgba(99, 102, 241, 0.15)'
          ]
        }
      }
    },
    series: [{
      type: 'radar',
      data: [{
        value: [usage.text || 0, usage.image || 0, usage.video || 0, usage.audio || 0],
        name: '练习次数',
        areaStyle: {
          color: 'rgba(99, 102, 241, 0.5)'
        },
        lineStyle: {
          color: '#818cf8',
          width: 2
        },
        itemStyle: {
          color: '#818cf8'
        }
      }]
    }]
  }

  radarChart.setOption(option)
}

const initPieChart = () => {
  if (!pieChartRef.value) return

  if (!pieChart) {
    pieChart = echarts.init(pieChartRef.value)
  }

  const usage = progress.value.module_usage || { text: 0, image: 0, video: 0, audio: 0 }

  const chartData = [
    { value: usage.text || 0, name: '文本生成' },
    { value: usage.image || 0, name: '图像生成' },
    { value: usage.video || 0, name: '视频生成' },
    { value: usage.audio || 0, name: '音频生成' }
  ]

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}次 ({d}%)',
      backgroundColor: 'rgba(15, 15, 35, 0.9)',
      borderColor: 'rgba(255, 255, 255, 0.1)',
      textStyle: {
        color: '#f1f5f9'
      }
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      textStyle: {
        color: '#94a3b8'
      }
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#1a1a3e',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}: {c}次',
        color: '#f1f5f9'
      },
      data: chartData,
      color: ['#6366f1', '#f093fb', '#f5576c', '#4facfe']
    }]
  }

  pieChart.setOption(option)
}

const handleResize = () => {
  radarChart?.resize()
  pieChart?.resize()
}

onMounted(() => {
  loadProgress()
  loadSubmissions()

  setTimeout(() => {
    initRadarChart()
    initPieChart()
  }, 500)

  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  radarChart?.dispose()
  pieChart?.dispose()
})
</script>

<style scoped>
.progress-content {
  padding: 0;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.task-icon {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.score-icon {
  background: rgba(236, 72, 153, 0.2);
  color: #f472b6;
}

.submission-icon {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.rate-icon {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.stat-label {
  font-size: 14px;
  color: var(--color-text-muted);
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.chart-card {
  padding: 24px;
}

.chart-card h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.chart-container {
  height: 300px;
}

.progress-section {
  padding: 24px;
}

.progress-section h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

:deep(.el-table) {
  --el-table-bg-color: transparent;
  --el-table-tr-bg-color: transparent;
  --el-table-header-bg-color: rgba(99, 102, 241, 0.1);
  --el-table-border-color: rgba(255, 255, 255, 0.05);
  --el-table-text-color: var(--color-text-primary);
  --el-table-header-text-color: var(--color-text-primary);
}

:deep(.el-table th.el-table__cell) {
  background: rgba(99, 102, 241, 0.1) !important;
}

:deep(.el-table td.el-table__cell) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

:deep(.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell) {
  background: rgba(255, 255, 255, 0.02);
}
</style>
