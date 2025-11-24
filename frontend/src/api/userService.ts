import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加认证token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 用户相关API
export const userService = {
  // 注册
  register: async (username: string, email: string, password: string) => {
    return await api.post('/users/register', null, {
      params: { username, email, password }
    })
  },
  
  // 登录
  login: async (email: string, password: string) => {
    const formData = new FormData()
    formData.append('username', email) // OAuth2PasswordRequestForm使用username字段
    formData.append('password', password)
    
    return await api.post('/users/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  
  // 获取当前用户信息
  getCurrentUser: async () => {
    return await api.get('/users/me')
  },
  
  // 更新用户名
  updateUsername: async (newUsername: string) => {
    return await api.put('/users/update-username', null, {
      params: { new_username: newUsername }
    })
  },
  
  // 更新密码
  updatePassword: async (oldPassword: string, newPassword: string) => {
    return await api.put('/users/update-password', null, {
      params: { old_password: oldPassword, new_password: newPassword }
    })
  },
  
  // 退出登录
  logout: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }
}