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
    host: '0.0.0.0',   // modificable a quitar  Permite que escuche en todas las interfaces de red (para Docker)
    port: 5173,         // Modificable a quitar
    headers: {
      // Esta directiva permite que los scripts solo se carguen desde el mismo origen.
      // Si necesitas cargar scripts de otras fuentes, debes agregarlas aquí.
      'Content-Security-Policy': "script-src 'self' 'unsafe-inline' http://localhost:5173;",
      // Solo mientras desarrollas
    }
  }
}))