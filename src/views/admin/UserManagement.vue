<template>
  <AppLayout pageTitle="用户管理" pageSubtitle="管理后台 - 用户账号与权限管理">
    <div class="user-management-content">
      <div class="header-actions">
        <div class="filter-bar">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索用户名或姓名..."
            prefix-icon="Search"
            class="search-input"
            @keyup.enter="handleSearch"
          />
          <el-select v-model="filterRole" placeholder="筛选角色" class="filter-select" @change="handleSearch">
            <el-option label="全部" value="" />
            <el-option label="学生" value="student" />
            <el-option label="教师" value="teacher" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </div>
        <el-button type="primary" class="action-btn-primary" icon="Plus" @click="showAddDialog = true">
          添加用户
        </el-button>
      </div>
      
      <div class="table-container glass-card">
        <el-table :data="users" v-loading="loading" stripe>
          <el-table-column prop="id" label="ID" width="80" />
          <el-table-column prop="username" label="用户名" width="150" />
          <el-table-column prop="full_name" label="姓名" width="150">
            <template #default="{ row }">
              {{ row.full_name || '-' }}
            </template>
          </el-table-column>
          <el-table-column prop="email" label="邮箱" width="200" />
          <el-table-column prop="role" label="角色" width="120">
            <template #default="{ row }">
              <el-tag :type="getRoleType(row.role)" size="small">
                {{ getRoleLabel(row.role) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="is_active" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.is_active === false ? 'danger' : 'success'" size="small">
                {{ row.is_active === false ? '已禁用' : '正常' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="注册时间" width="180">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" fixed="right" width="280">
            <template #default="{ row }">
              <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
              <el-button size="small" type="warning" @click="handleResetPassword(row)">重置密码</el-button>
              <el-button 
                size="small" 
                :type="row.is_active === false ? 'success' : 'danger'" 
                @click="handleToggleStatus(row)"
              >
                {{ row.is_active === false ? '启用' : '禁用' }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="handlePageChange"
          class="pagination"
        />
      </div>
      
      <el-dialog title="添加用户" :visible.sync="showAddDialog" width="500px">
        <el-form :model="userForm" label-width="80px">
          <el-form-item label="用户名" required>
            <el-input v-model="userForm.username" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="姓名">
            <el-input v-model="userForm.full_name" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="邮箱" required>
            <el-input v-model="userForm.email" placeholder="请输入邮箱" />
          </el-form-item>
          <el-form-item label="密码" required>
            <el-input v-model="userForm.password" type="password" placeholder="请输入密码" />
          </el-form-item>
          <el-form-item label="角色" required>
            <el-select v-model="userForm.role" style="width: 100%;">
              <el-option label="学生" value="student" />
              <el-option label="教师" value="teacher" />
              <el-option label="管理员" value="admin" />
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer">
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="handleAddUser">确定</el-button>
        </div>
      </el-dialog>
      
      <el-dialog title="编辑用户" :visible.sync="showEditDialog" width="500px">
        <el-form :model="editForm" label-width="80px">
          <el-form-item label="用户名">
            <el-input v-model="editForm.username" disabled />
          </el-form-item>
          <el-form-item label="姓名">
            <el-input v-model="editForm.full_name" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input v-model="editForm.email" placeholder="请输入邮箱" />
          </el-form-item>
          <el-form-item label="角色">
            <el-select v-model="editForm.role" style="width: 100%;">
              <el-option label="学生" value="student" />
              <el-option label="教师" value="teacher" />
              <el-option label="管理员" value="admin" />
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer">
          <el-button @click="showEditDialog = false">取消</el-button>
          <el-button type="primary" @click="handleUpdateUser">确定</el-button>
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

const users = ref([])
const loading = ref(false)
const searchKeyword = ref('')
const filterRole = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const showAddDialog = ref(false)
const showEditDialog = ref(false)

const userForm = reactive({
  username: '',
  email: '',
  password: '',
  role: 'student',
  full_name: ''
})

const editForm = reactive({
  id: null,
  username: '',
  email: '',
  role: 'student',
  full_name: ''
})

const getRoleType = (role) => {
  const types = { student: 'primary', teacher: 'success', admin: 'warning' }
  return types[role] || 'info'
}

const getRoleLabel = (role) => {
  const labels = { student: '学生', teacher: '教师', admin: '管理员' }
  return labels[role] || role
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

const loadUsers = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams({
      skip: ((currentPage.value - 1) * pageSize.value).toString(),
      limit: pageSize.value.toString()
    })
    
    if (filterRole.value) {
      params.append('role', filterRole.value)
    }
    if (searchKeyword.value) {
      params.append('search', searchKeyword.value)
    }
    
    const data = await API.request(`/api/admin/users?${params}`)
    users.value = data
    total.value = data.length
  } catch (error) {
    console.error('Load users error:', error)
    users.value = []
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadUsers()
}

const handlePageChange = () => {
  loadUsers()
}

const handleAddUser = async () => {
  try {
    await API.request('/api/admin/users', {
      method: 'POST',
      body: userForm
    })
    
    ElMessage.success('用户创建成功')
    showAddDialog.value = false
    Object.keys(userForm).forEach(key => userForm[key] = '')
    userForm.role = 'student'
    loadUsers()
  } catch (error) {
    console.error('Create user error:', error)
    ElMessage.error('创建失败：' + (error.message || '未知错误'))
  }
}

const handleEdit = (user) => {
  editForm.id = user.id
  editForm.username = user.username
  editForm.email = user.email
  editForm.role = user.role
  editForm.full_name = user.full_name
  showEditDialog.value = true
}

const handleUpdateUser = async () => {
  try {
    await API.request(`/api/admin/users/${editForm.id}`, {
      method: 'PUT',
      body: {
        email: editForm.email,
        role: editForm.role,
        full_name: editForm.full_name
      }
    })
    
    ElMessage.success('用户更新成功')
    showEditDialog.value = false
    loadUsers()
  } catch (error) {
    console.error('Update user error:', error)
    ElMessage.error('更新失败')
  }
}

const handleResetPassword = async (user) => {
  try {
    const result = await API.request(`/api/admin/users/${user.id}/reset-password`, {
      method: 'POST'
    })
    
    ElMessage.success('密码已重置为：' + (result.message || 'password123'))
  } catch (error) {
    console.error('Reset password error:', error)
    ElMessage.error('重置失败')
  }
}

const handleToggleStatus = async (user) => {
  try {
    if (user.is_active === false) {
      await API.request(`/api/admin/users/${user.id}`, {
        method: 'PUT',
        body: { is_active: true }
      })
      ElMessage.success('用户已启用')
    } else {
      await API.request(`/api/admin/users/${user.id}`, {
        method: 'DELETE'
      })
      ElMessage.success('用户已禁用')
    }
    loadUsers()
  } catch (error) {
    console.error('Toggle status error:', error)
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.user-management-content {
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
  width: 150px;
}

.action-btn-primary {
  padding: 10px 20px;
  font-weight: 500;
}

.table-container {
  padding: 24px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}
</style>
