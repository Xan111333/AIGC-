const BASE_URL = 'http://localhost:8000'

const API = {
  getToken() {
    return localStorage.getItem('token')
  },

  setToken(token) {
    localStorage.setItem('token', token)
  },

  removeToken() {
    localStorage.removeItem('token')
  },

  async request(url, options = {}) {
    const token = this.getToken()
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    }

    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const config = {
      url: `${BASE_URL}${url}`,
      method: options.method || 'GET',
      headers,
      body: options.body ? JSON.stringify(options.body) : null
    }

    try {
      const response = await fetch(config.url, config)
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || '请求失败')
      }

      return data
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  },

  async login(username, password) {
    const response = await fetch(`${BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || '登录失败')
    }

    if (data.access_token) {
      this.setToken(data.access_token)
    }

    return data
  },

  async getCurrentUser() {
    return this.request('/api/users/me')
  },

  async generateText(prompt, params) {
    return this.request('/api/text/generate', {
      method: 'POST',
      body: {
        prompt,
        length: params.length || 'medium',
        style: params.style || 'neutral',
        tone: params.tone || 'neutral',
        language: params.language || 'zh'
      }
    })
  },

  async generateImage(prompt, params) {
    return this.request('/api/image/generate', {
      method: 'POST',
      body: {
        prompt,
        resolution: params.resolution || '1024x1024',
        style: params.style || 'realistic',
        num_images: params.num_images || 1
      }
    })
  },

  async generateVideo(prompt, params) {
    return this.request('/api/video/generate', {
      method: 'POST',
      body: {
        prompt,
        duration: params.duration || 5,
        resolution: params.resolution || '720p',
        style: params.style || 'realistic'
      }
    })
  },

  async generateAudio(text, params) {
    return this.request('/api/audio/generate', {
      method: 'POST',
      body: {
        text,
        voice: params.voice || '女',
        speed: params.speed || 5,
        pitch: params.pitch || 5
      }
    })
  },

  async getTextHistory(skip = 0, limit = 50) {
    return this.request(`/api/text/history?skip=${skip}&limit=${limit}`)
  },

  async getImageHistory(skip = 0, limit = 50) {
    return this.request(`/api/image/history?skip=${skip}&limit=${limit}`)
  },

  async getVideoHistory(skip = 0, limit = 50) {
    return this.request(`/api/video/history?skip=${skip}&limit=${limit}`)
  },

  async getAudioHistory(skip = 0, limit = 50) {
    return this.request(`/api/audio/history?skip=${skip}&limit=${limit}`)
  },

  async createTask(task) {
    return this.request('/api/tasks', {
      method: 'POST',
      body: task
    })
  },

  async getTasks() {
    return this.request('/api/tasks')
  },

  async getTask(taskId) {
    return this.request(`/api/tasks/${taskId}`)
  },

  async updateTask(taskId, task) {
    return this.request(`/api/tasks/${taskId}`, {
      method: 'PUT',
      body: task
    })
  },

  async deleteTask(taskId) {
    return this.request(`/api/tasks/${taskId}`, {
      method: 'DELETE'
    })
  },

  async submitSubmission(submission) {
    return this.request('/api/submissions', {
      method: 'POST',
      body: submission
    })
  },

  async getMySubmissions() {
    return this.request('/api/submissions/my')
  },

  async getTaskSubmissions(taskId) {
    return this.request(`/api/tasks/${taskId}/submissions`)
  },

  async gradeSubmission(submissionId, grade) {
    return this.request(`/api/submissions/${submissionId}/grade`, {
      method: 'POST',
      body: grade
    })
  },

  async updateGrade(submissionId, grade) {
    return this.request(`/api/submissions/${submissionId}/grade`, {
      method: 'PUT',
      body: grade
    })
  },

  async exportTextToPdf(text, title = 'Generated Content') {
    const response = await fetch(`${BASE_URL}/api/export/text-to-pdf`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.getToken()}`
      },
      body: JSON.stringify({ text, title })
    })
    
    if (!response.ok) {
      throw new Error('导出失败')
    }
    
    return response.blob()
  },

  async exportTextToWord(text, title = 'Generated Content') {
    const response = await fetch(`${BASE_URL}/api/export/text-to-word`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.getToken()}`
      },
      body: JSON.stringify({ text, title })
    })
    
    if (!response.ok) {
      throw new Error('导出失败')
    }
    
    return response.blob()
  },

  async exportImagesToZip(urls) {
    const response = await fetch(`${BASE_URL}/api/export/images-to-zip`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.getToken()}`
      },
      body: JSON.stringify({ urls })
    })
    
    if (!response.ok) {
      throw new Error('导出失败')
    }
    
    return response.blob()
  },

  async createResource(resource) {
    return this.request('/api/resources', {
      method: 'POST',
      body: resource
    })
  },

  async getResources(category = null) {
    const url = category ? `/api/resources?category=${category}` : '/api/resources'
    return this.request(url)
  },

  async getResource(resourceId) {
    return this.request(`/api/resources/${resourceId}`)
  },

  async deleteResource(resourceId) {
    return this.request(`/api/resources/${resourceId}`, {
      method: 'DELETE'
    })
  },

  async getResourceCategories() {
    return this.request('/api/resources/categories')
  },

  async getStatisticsOverview() {
    return this.request('/api/statistics/overview')
  },

  async getGradeDistribution(period = 'all') {
    return this.request(`/api/statistics/grade-distribution?period=${period}`)
  },

  async getTaskCompletion() {
    return this.request('/api/statistics/task-completion')
  },

  async getModuleUsage(period = 'week') {
    return this.request(`/api/statistics/module-usage?period=${period}`)
  },

  async getStudentProgress(studentId) {
    return this.request(`/api/statistics/student-progress/${studentId}`)
  },

  async createCreationLog(module, content = null) {
    return this.request('/api/creation-logs', {
      method: 'POST',
      body: { module, content }
    })
  },

  async getAdminUsers(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    return this.request(`/api/admin/users${queryString ? '?' + queryString : ''}`)
  },

  async createAdminUser(userData) {
    return this.request('/api/admin/users', {
      method: 'POST',
      body: userData
    })
  },

  async updateAdminUser(userId, userData) {
    return this.request(`/api/admin/users/${userId}`, {
      method: 'PUT',
      body: userData
    })
  },

  async deleteAdminUser(userId) {
    return this.request(`/api/admin/users/${userId}`, {
      method: 'DELETE'
    })
  },

  async resetUserPassword(userId) {
    return this.request(`/api/admin/users/${userId}/reset-password`, {
      method: 'POST'
    })
  },

  async getSystemConfig() {
    return this.request('/api/admin/system/config')
  },

  async updateSystemConfig(configData) {
    return this.request('/api/admin/system/config', {
      method: 'PUT',
      body: configData
    })
  },

  async getAdminLogs(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    return this.request(`/api/admin/logs${queryString ? '?' + queryString : ''}`)
  },

  async getPendingContents() {
    return this.request('/api/admin/contents/pending')
  },

  async reviewContent(contentId, reviewData) {
    return this.request(`/api/admin/contents/${contentId}/review`, {
      method: 'POST',
      body: reviewData
    })
  },

  async getAdminStatistics() {
    return this.request('/api/admin/statistics')
  }
}

export default API