import axios from 'axios';
import { useAuthStore } from '../store/auth';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8080/api',
  timeout: 10000,
});

// 请求拦截器 - 添加认证信息
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    if (authStore.isLoggedIn && authStore.userId) {
      // 在实际项目中，这里应该添加JWT token到请求头
      // config.headers.Authorization = `Bearer ${token}`;
      console.log('当前登录用户:', authStore.userId);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// TypeScript类型定义
export interface UserSimple {
  id: number;
  username: string;
  email: string;
}

export interface BillItem {
  id: number;
  ledger_id: number;
  type: string;
  amount: number;
  payer_id: number;
  payer_name: string;
  participants: UserSimple[];
  description?: string;
  occurred_at: string;
}

export interface Ledger {
  id: number;
  title: string;
  creator_id: number;
  travel_plan_id?: number;
  created_at: string;
  updated_at: string;
  member_count: number;
  total_amount: number;
}

export interface LedgerDetail extends Ledger {
  members: UserSimple[];
  bill_items: BillItem[];
}

// 请求类型定义
export interface LedgerCreateRequest {
  title: string;
  travel_plan_id?: number;
}

export interface LedgerUpdateRequest {
  title?: string;
  travel_plan_id?: number;
}

export interface LedgerMemberRequest {
  user_id: number;
}

export interface BillItemCreateRequest {
  type: string;
  amount: number;
  payer_id: number;
  participant_ids: number[];
  description?: string;
  occurred_at?: string;
}

export interface BillItemUpdateRequest {
  type?: string;
  amount?: number;
  payer_id?: number;
  participant_ids?: number[];
  description?: string;
  occurred_at?: string;
}

// API响应类型
export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  ledger?: Ledger;
  bill_item?: BillItem;
}

// 账单类型选项
export const BILL_TYPES = [
  { value: 'hotel', label: '住宿', color: '#FF6B6B' },
  { value: 'meal', label: '餐饮', color: '#4ECDC4' },
  { value: 'transport', label: '交通', color: '#45B7D1' },
  { value: 'ticket', label: '门票', color: '#96CEB4' },
  { value: 'other', label: '其他', color: '#FFEAA7' }
];

// 格式化金额（分转元）
export const formatAmount = (amount: number): string => {
  return (amount / 100).toFixed(2);
};

// 格式化日期
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// 账本相关API
export const createLedger = async (data: LedgerCreateRequest): Promise<ApiResponse> => {
  const response = await api.post('/ledgers/', data);
  return response.data;
};

export const getMyLedgers = async (): Promise<ApiResponse<Ledger[]>> => {
  const response = await api.get('/ledgers/my-ledgers');
  return response.data;
};

export const getLedgerDetail = async (ledgerId: number): Promise<ApiResponse<LedgerDetail>> => {
  const response = await api.get(`/ledgers/${ledgerId}`);
  return response.data;
};

export const updateLedger = async (ledgerId: number, data: LedgerUpdateRequest): Promise<ApiResponse> => {
  const response = await api.put(`/ledgers/${ledgerId}`, data);
  return response.data;
};

export const deleteLedger = async (ledgerId: number): Promise<ApiResponse> => {
  const response = await api.delete(`/ledgers/${ledgerId}`);
  return response.data;
};

export const addMemberToLedger = async (ledgerId: number, data: LedgerMemberRequest): Promise<ApiResponse> => {
  const response = await api.post(`/ledgers/${ledgerId}/members`, data);
  return response.data;
};

export const removeMemberFromLedger = async (ledgerId: number, userId: number): Promise<ApiResponse> => {
  const response = await api.delete(`/ledgers/${ledgerId}/members/${userId}`);
  return response.data;
};

// 账单相关API
export const createBillItem = async (ledgerId: number, data: BillItemCreateRequest): Promise<ApiResponse> => {
  const response = await api.post(`/ledgers/${ledgerId}/bill-items`, data);
  return response.data;
};

export const updateBillItem = async (billItemId: number, data: BillItemUpdateRequest): Promise<ApiResponse> => {
  const response = await api.put(`/ledgers/bill-items/${billItemId}`, data);
  return response.data;
};

export const deleteBillItem = async (billItemId: number): Promise<ApiResponse> => {
  const response = await api.delete(`/ledgers/bill-items/${billItemId}`);
  return response.data;
};
