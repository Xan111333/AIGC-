<template>
  <AppLayout pageTitle="内容审核" pageSubtitle="管理后台 - 审核用户生成的AI内容">
    <div class="content-review-content">
      <div class="table-container glass-card">
        <el-table :data="contents" v-loading="loading" stripe>
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="type" label="类型" width="120">
            <template #default="{ row }">
              <el-tag>{{ row.type }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="content" label="内容" min-width="300">
            <template #default="{ row }">
              <div class="content-preview">{{ row.content }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="user_id" label="提交用户" width="120" />
          <el-table-column prop="status" label="状态" width="120">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" fixed="right" width="200">
            <template #default="{ row }">
              <el-button size="small" type="primary" @click="handleApprove(row)">通过</el-button>
              <el-button size="small" type="danger" @click="handleReject(row)">拒绝</el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <div v-if="contents.length === 0 && !loading" class="empty-state">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
          <p>暂无待审核内容</p>
        </div>
      </div>
      
      <el-dialog title="审核内容" :visible.sync="showReviewDialog" width="600px">
        <div v-if="selectedContent" class="review-content">
          <div class="content-detail">
            <h4>内容详情</h4>
            <p>{{ selectedContent.content }}</p>
          </div>
          <el-form :model="reviewForm" label-width="80px">
            <el-form-item label="审核结果">
              <el-radio-group v-model="reviewForm.approved">
                <el-radio :label="true">通过</el-radio>
                <el-radio :label="false">拒绝</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="审核理由">
              <el-input v-model="reviewForm.reason" type="textarea" :rows="4" placeholder="请输入审核理由" />
            </el-form-item>
          </el-form>
        </div>
        <div slot="footer">
          <el-button @click="showReviewDialog = false">取消</el-button>
          <el-button type="primary" @click="handleSubmitReview">提交</el-button>
        </div>
      </el-dialog>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import API from '../../api'
import AppLayout from '../../components/AppLayout.vue'

const contents = ref([])
const loading = ref(false)
const showReviewDialog = ref(false)
const selectedContent = ref(null)

const reviewForm = reactive({
  approved: true,
  reason: ''
})

const getStatusType = (status) => {
  const types = { pending: 'warning', approved: 'success', rejected: 'danger' }
  return types[status] || 'info'
}

const getStatusLabel = (status) => {
  const labels = { pending: '待审核', approved: '已通过', rejected: '已拒绝' }
  return labels[status] || status
}

const loadContents = async () => {
  loading.value = true
  try {
    const data = await API.request('/api/admin/contents/pending')
    contents.value = data
  } catch (error) {
    console.error('Load contents error:', error)
    contents.value = []
  } finally {
    loading.value = false
  }
}

const handleApprove = (content) => {
  selectedContent.value = content
  reviewForm.approved = true
  reviewForm.reason = ''
  showReviewDialog.value = true
}

const handleReject = (content) => {
  selectedContent.value = content
  reviewForm.approved = false
  reviewForm.reason = ''
  showReviewDialog.value = true
}

const handleSubmitReview = async () => {
  try {
    await API.request(`/api/admin/contents/${selectedContent.value.id}/review`, {
      method: 'POST',
      body: reviewForm
    })
    
    ElMessage.success('审核提交成功')
    showReviewDialog.value = false
    loadContents()
  } catch (error) {
    console.error('Submit review error:', error)
    ElMessage.error('审核提交失败')
  }
}

onMounted(() => {
  loadContents()
})
</script>

<style scoped>
.content-review-content {
  padding: 24px;
}

.table-container {
  padding: 24px;
}

.content-preview {
  max-height: 100px;
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

.review-content {
  padding: 20px;
}

.content-detail {
  background: var(--color-bg-glass);
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 20px;
}

.content-detail h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.content-detail p {
  margin: 0;
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-text-secondary);
}
</style>
