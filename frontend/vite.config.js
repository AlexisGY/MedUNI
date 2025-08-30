import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig(({ mode }) => ({
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
    headers: {
      // Esta directiva permite que los scripts solo se carguen desde el mismo origen.
      // Si necesitas cargar scripts de otras fuentes, debes agregarlas aquí.
      'Content-Security-Policy': "script-src 'self' 'unsafe-inline' http://localhost:5173;",
      // Solo mientras desarrollas
    }
  }
}))