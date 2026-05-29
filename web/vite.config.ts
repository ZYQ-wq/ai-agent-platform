import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // 将所有以 /api 开头的请求，转发到 http://127.0.0.1:8000
      '/api': {
        target: 'http://127.0.0.1:8000', 
        changeOrigin: true,
        // rewrite: (path) => path.replace(/^\/api/, '') 
        // 注意：如果你的后端接口本身就是 /api/v1/...，就不要开启上面的 rewrite
      }
    }
  }
})