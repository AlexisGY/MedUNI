<template>
  <section class="container" style="max-width:420px">
    <h2 class="mb-3">Iniciar sesión</h2>
    <form @submit.prevent="onSubmit" class="d-grid gap-3">
      <div>
        <label class="form-label">Correo</label>
        <input class="form-control" v-model.trim="email" type="email" required>
      </div>
      <div>
        <label class="form-label">Contraseña</label>
        <input class="form-control" v-model.trim="password" type="password" required>
      </div>
      <button class="btn btn-primary" :disabled="auth.loading">
        {{ auth.loading ? 'Ingresando…' : 'Ingresar' }}
      </button>
      <p v-if="auth.error" class="text-danger m-0">{{ auth.error }}</p>
    </form>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuth()

const email = ref('')
const password = ref('')

async function onSubmit() {
  await auth.login(email.value, password.value)
  router.push(route.query.redirect || '/reservar')
}
</script>
