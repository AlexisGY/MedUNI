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
    async login(username, password) { // Cambiado de 'email' a 'codigo'
      this.loading = true; this.error = null
      try {
        // Envia el 'codigo' y 'password' a la API
        const { token, user } = await api.login({ username, password })
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