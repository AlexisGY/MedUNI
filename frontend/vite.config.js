import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig(() => ({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    host: true,
    port: 5173,
    strictPort: true,
    proxy: { '/api': { target: 'http://localhost:8000', changeOrigin: true } },
    watch: {
      usePolling: true,
      interval: 100
    },
    hmr: {
      host: 'localhost',   
      clientPort: 5173,   
      protocol: 'ws'     
    }
  }

}))