import { defineStore } from 'pinia';

interface AuthState {
  isLoggedIn: boolean;
  userId?: number;
  username?: string;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    isLoggedIn: false,
    userId: undefined,
    username: undefined,
  }),

  actions: {
    login(userId: number, username: string) {
      this.isLoggedIn = true;
      this.userId = userId;
      this.username = username;
      // 将登录状态保存到localStorage
      localStorage.setItem('auth', JSON.stringify({
        isLoggedIn: true,
        userId,
        username,
      }));
    },

    logout() {
      this.isLoggedIn = false;
      this.userId = undefined;
      this.username = undefined;
      // 清除localStorage中的登录状态
      localStorage.removeItem('auth');
    },

    // 从localStorage中恢复登录状态
    restoreAuthState() {
      const authState = localStorage.getItem('auth');
      if (authState) {
        const { isLoggedIn, userId, username } = JSON.parse(authState);
        this.isLoggedIn = isLoggedIn;
        this.userId = userId;
        this.username = username;
      }
    },
  },
});
