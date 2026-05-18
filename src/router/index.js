import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/teacher-dashboard',
    name: 'TeacherDashboard',
    component: () => import('../views/teacher/Dashboard.vue')
  },
  {
    path: '/text-generate',
    name: 'TextGenerate',
    component: () => import('../views/TextGenerate.vue')
  },
  {
    path: '/image-generate',
    name: 'ImageGenerate',
    component: () => import('../views/ImageGenerate.vue')
  },
  {
    path: '/video-generate',
    name: 'VideoGenerate',
    component: () => import('../views/VideoGenerate.vue')
  },
  {
    path: '/audio-generate',
    name: 'AudioGenerate',
    component: () => import('../views/AudioGenerate.vue')
  },
  {
    path: '/task-manager',
    name: 'TaskManager',
    component: () => import('../views/TaskManager.vue')
  },
  {
    path: '/student-tasks',
    name: 'StudentTasks',
    component: () => import('../views/StudentTasks.vue')
  },
  {
    path: '/resource-center',
    name: 'ResourceCenter',
    component: () => import('../views/ResourceCenter.vue')
  },
  {
    path: '/my-works',
    name: 'MyWorks',
    component: () => import('../views/MyWorks.vue')
  },
  {
    path: '/student-progress',
    name: 'StudentProgress',
    component: () => import('../views/student/Progress.vue')
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/admin/Dashboard.vue')
  },
  {
    path: '/admin/users',
    name: 'AdminUserManagement',
    component: () => import('../views/admin/UserManagement.vue')
  },
  {
    path: '/admin/config',
    name: 'AdminSystemConfig',
    component: () => import('../views/admin/SystemConfig.vue')
  },
  {
    path: '/admin/review',
    name: 'AdminContentReview',
    component: () => import('../views/admin/ContentReview.vue')
  },
  {
    path: '/admin/logs',
    name: 'AdminLogViewer',
    component: () => import('../views/admin/LogViewer.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router