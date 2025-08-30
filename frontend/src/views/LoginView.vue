<template>
  <section class="container" style="max-width:420px">
    <h2 class="mb-3">Iniciar sesión</h2>
    <form @submit.prevent="handleLogin" class="d-grid gap-3">
      <div>
        <label class="form-label">Codigo Estudiante</label>
        <input class="form-control" v-model.trim="username" type="text" required>
      </div>
      <div>
        <label class="form-label">Contraseña Dirce</label>
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
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../stores/auth';

const router = useRouter();
const auth = useAuth();

const username = ref(''); // Cambiado de 'email' a 'codigo'
const password = ref('');
const loading = ref(false);
const message = ref(null);

async function handleLogin() {
  loading.value = true;
  message.value = null;

  try {
    // Llama a la acción 'login' del store con el código y la contraseña
    await auth.login(username.value, password.value);
    
    // Redirige después de un login exitoso
    router.push('/home'); 

  } catch (err) {
    message.value = { 
      text: err.message || 'Error al iniciar sesión. Inténtalo de nuevo.', 
      type: 'error' 
    };
  } finally {
    loading.value = false;
  }
}
</script>
