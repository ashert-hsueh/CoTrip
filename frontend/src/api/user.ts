import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
});

// 请求拦截器 - 添加认证信息
api.interceptors.request.use(
  (config) => {
    // 从localStorage中获取token（避免在模块加载时直接使用Pinia store）
    const authState = localStorage.getItem('auth');
    if (authState) {
      const { accessToken } = JSON.parse(authState);
      if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 用户注册请求
interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

// 用户登录请求
interface LoginRequest {
  email: string;
  password: string;
}

// 更新用户名请求
interface UpdateUsernameRequest {
  user_id: number;
  new_username: string;
}

// 更新密码请求
interface UpdatePasswordRequest {
  user_id: number;
  old_password: string;
  new_password: string;
}

// API响应类型
interface ApiResponse {
  success: boolean;
  message: string;
  user_id?: number;
  username?: string;
  access_token?: string;
  email?: string;
}

// 用户注册
export const registerUser = async (data: RegisterRequest): Promise<ApiResponse> => {
  const response = await api.post('/users/register', data);
  return response.data;
};

// 用户登录
export const loginUser = async (data: LoginRequest): Promise<ApiResponse> => {
  const response = await api.post('/users/login', data);
  // Save user info to localStorage if login is successful
  if (response.data.success) {
    localStorage.setItem(
      'userInfo',
      JSON.stringify({
        userId: response.data.user_id,
        username: response.data.username,
        email: response.data.email || data.email,
      })
    );
  }
  return response.data;
};

// 更新用户名
export const updateUsername = async (data: UpdateUsernameRequest): Promise<ApiResponse> => {
  const response = await api.put('/users/update-username', data);
  return response.data;
};

// 更新密码
export const updatePassword = async (data: UpdatePasswordRequest): Promise<ApiResponse> => {
  const response = await api.put('/users/update-password', data);
  return response.data;
};
