import { createApp } from 'vue'
import App from './App.vue'
import 'element-plus/dist/index.css'
import router from './router'
import { createPinia } from 'pinia'
import { useAuthStore } from './store/auth'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)

// 恢复登录状态
const authStore = useAuthStore()
authStore.restoreAuthState()

app.use(router)

// 确保在恢复登录状态后再挂载应用
app.mount('#app')
