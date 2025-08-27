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
    async login(email, password) {
      this.loading = true; this.error = null
      try {
        const { token, user } = await api.login({ email, password })
        this.token = token; this.user = user
        localStorage.setItem('token', token)
        localStorage.setItem('user', JSON.stringify(user))
      } catch (e) {
        this.error = e.message || 'Credenciales inválidas'
        throw e
      } finally { this.loading = false }
    },
    logout() {
      this.token = null; this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },
  },
})
