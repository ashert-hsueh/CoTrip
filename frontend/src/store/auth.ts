import { defineStore } from 'pinia';

interface AuthState {
  isLoggedIn: boolean;
  userId?: number;
  username?: string;
  accessToken?: string;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    isLoggedIn: false,
    userId: undefined,
    username: undefined,
    accessToken: undefined,
  }),

  actions: {
    login(userId: number, username: string, accessToken: string) {
      this.isLoggedIn = true;
      this.userId = userId;
      this.username = username;
      this.accessToken = accessToken;
      // 将登录状态保存到localStorage
      localStorage.setItem('auth', JSON.stringify({
        isLoggedIn: true,
        userId,
        username,
        accessToken,
      }));
    },

    logout() {
      this.isLoggedIn = false;
      this.userId = undefined;
      this.username = undefined;
      this.accessToken = undefined;
      // 清除localStorage中的登录状态
      localStorage.removeItem('auth');
      localStorage.removeItem('userInfo');
    },

    // 从localStorage中恢复登录状态
    restoreAuthState() {
      const authState = localStorage.getItem('auth');
      if (authState) {
        const { isLoggedIn, userId, username, accessToken } = JSON.parse(authState);
        this.isLoggedIn = isLoggedIn;
        this.userId = userId;
        this.username = username;
        this.accessToken = accessToken;
      }
    },
  },
});
