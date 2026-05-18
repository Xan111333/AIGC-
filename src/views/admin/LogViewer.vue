<template>
  <AppLayout pageTitle="操作日志" pageSubtitle="管理后台 - 查看系统操作记录">
    <div class="log-viewer-content">
      <div class="header-actions">
        <div class="filter-bar">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索操作..."
            prefix-icon="Search"
            class="search-input"
            @keyup.enter="handleSearch"
          />
          <el-select v-model="filterUser" placeholder="筛选用户" class="filter-select" clearable @change="handleSearch">
            <el-option label="全部" value="" />
            <el-option v-for="user in users" :key="user.id" :label="user.username" :value="user.id" />
          </el-select>
          <el-button icon="Refresh" @click="handleRefresh">刷新</el-button>
        </div>
        <el-button icon="Download" type="primary" @click="handleExportLogs">导出日志</el-button>
      </div>
      
      <div class="table-container glass-card">
        <el-table :data="logs" v-loading="loading" stripe>
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="user_name" label="用户" width="150" />
          <el-table-column prop="action" label="操作" width="200">
            <template #default="{ row }">
              <el-tag type="primary">{{ row.action || '未知操作' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="details" label="详情" min-width="300">
            <template #default="{ row }">
              <div class="log-details">{{ row.details || '-' }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="ip_address" label="IP地址" width="150" />
          <el-table-column prop="created_at" label="时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
        </el-table>
        
        <div v-if="logs.length === 0 && !loading" class="empty-state">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
          <p>暂无操作日志</p>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import API from '../../api'
import AppLayout from '../../components/AppLayout.vue'

const logs = ref([])
const users = ref([])
const loading = ref(false)
const searchKeyword = ref('')
const filterUser = ref('')

const loadLogs = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (filterUser.value) {
      params.append('user_id', filterUser.value)
    }
    
    const data = await API.request(`/api/admin/logs?${params}`)
    logs.value = data
  } catch (error) {
    console.error('Load logs error:', error)
    logs.value = []
  } finally {
    loading.value = false
  }
}

const loadUsers = async () => {
  try {
    const data = await API.request('/api/admin/users')
    users.value = data
  } catch (error) {
    console.error('Load users error:', error)
    users.value = []
  }
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

const handleSearch = () => {
  loadLogs()
}

const handleRefresh = () => {
  loadLogs()
}

const handleExportLogs = () => {
  const csvContent = [
    ['ID', '用户', '操作', '详情', 'IP地址', '时间'],
    ...logs.value.map(log => [
      log.id,
      log.user_name,
      log.action || '未知操作',
      log.details || '-',
      log.ip_address || '-',
      formatDate(log.created_at)
    ])
  ].map(row => row.join(',')).join('\n')
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `logs_${Date.now()}.csv`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
  
  ElMessage.success('日志导出成功')
}

onMounted(() => {
  loadLogs()
  loadUsers()
})
</script>

<style scoped>
.log-viewer-content {
  padding: 24px;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-bar {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.search-input {
  width: 300px;
}

.filter-select {
  width: 200px;
}

.table-container {
  padding: 24px;
}

.log-details {
  max-height: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  color: var(--color-text-muted);
}

.empty-state svg {
  margin-bottom: 16px;
}
</style>
