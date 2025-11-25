/// <reference types="vite/client" />

declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// 环境变量类型声明
interface ImportMetaEnv {
  readonly VITE_AMAP_KEY: string
  readonly VITE_AMAP_SECRET: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
