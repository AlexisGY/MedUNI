import { defineStore } from 'pinia'
import * as api from '../services/api'

export const useAuth = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token'),
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    loading: false,
    error: null,
  }),
  getters: { isAuth: (s) => !!s.token },
  actions: {
    async login(username, password) {
      this.loading = true; this.error = null
      try {
        const resp = await api.login({ username, password })

        // Acepta { token, user } o { access_token, user }
        const token = resp?.token ?? resp?.access_token
        const user  = resp?.user ?? null

        if (!token) throw new Error('Respuesta de login inválida')

        this.token = token
        this.user  = user
        localStorage.setItem('token', token)
        localStorage.setItem('user', JSON.stringify(user))
        return true
      } catch (e) {
        this.error = e.message || 'Credenciales inválidas'
        return false
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // (redirige desde el componente: router.replace({ name: 'login' }))
    },
  },
})