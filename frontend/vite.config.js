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
    watch: {
      usePolling: true,
    },
    hmr: { host: 'localhost', clientPort: 5173 },
    proxy: { '/api': { target: 'http://localhost:8000', changeOrigin: true } },
    headers: {
      'Content-Security-Policy': "script-src 'self' 'unsafe-inline' http://localhost:5173;",
    }
  }
}))