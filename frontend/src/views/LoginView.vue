<template>
  <main class="auth">
    <section class="auth-card">
      <div class="brand-row">
        <img :src="logo" alt="UNI" class="brand" />
        <h1>Centro Médico UNI</h1>
      </div>

  <form class="auth-form" @submit.prevent="submit" novalidate>
        <label for="username">Código de estudiante</label>
        <input
          id="username"
          v-model="username"
          type="text"
          inputmode="numeric"
          placeholder="2025xxxxx"
          class="auth-input"
          autocomplete="username"
        />

        <label for="password">Contraseña</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="••••••"
          class="auth-input"
          autocomplete="current-password"
        />

        <a href="#" class="auth-forgot">Olvidé mi contraseña</a>
        <button type="submit" class="auth-btn" :disabled="loading">
          <span v-if="!loading">Acceder</span>
          <span v-else>Accediendo...</span>
        </button>
        <div v-if="errorMessage" class="auth-alert" role="alert">{{ errorMessage }}</div>
      </form>
    </section>
  </main>
</template>


<script setup>
import logo from "@/assets/logo-uni.png";
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../stores/auth';

const router = useRouter();
const auth = useAuth();

const username = ref(''); 
const password = ref('');
const loading = ref(false);
const errorMessage = ref(null);

async function submit() {
  loading.value = true;
  errorMessage.value = null;

  try {
  await auth.login(username.value, password.value);
    router.push('/calendario'); 

  } catch (err) {
  errorMessage.value = err.message || 'Credenciales inválidas';
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.auth{
  min-height:100svh; display:grid; place-items:center;
  padding:clamp(16px,4vw,32px); background:#f6f7f9;
}

.auth-card{
  width:clamp(320px, 90vw, 560px);
  background:#fff; border-radius:16px;
  box-shadow:0 8px 30px rgba(16,24,40,.08);
  padding:clamp(16px,3.5vw,28px);
}

.brand-row{ display:flex; align-items:center; gap:12px; margin-bottom:clamp(12px,2.5vw,18px); }
.brand{ width:clamp(40px,6vw,56px); height:auto; }
h1{ margin:0; color:#1f2328; font-size:clamp(1.15rem,1rem + 1vw,1.7rem); }

.auth-form{ display:grid; gap:10px; }


label{ color:#5f6b7a; font-size:clamp(.9rem,.85rem + .3vw,1rem); }
.auth-input{
  width:100%; box-sizing:border-box;
  padding:clamp(12px,1.8vw,16px);
  border:1px solid #e4e7ec; border-radius:12px;
  background:#f3f4f6; font-size:clamp(.95rem,.9rem + .3vw,1.05rem);
  outline:none; transition:border-color .2s, box-shadow .2s, background .2s;
}
.auth-input:focus{
  background:#fff; border-color:#7a0000;
  box-shadow:0 0 0 4px rgba(122,0,0,.18);
}

.auth-forgot{ margin:4px 0 6px; color:#7a0000; text-decoration:none; font-size:.95rem; }
.auth-forgot:hover{ text-decoration:underline; }

.auth-btn{
  width:100%; padding:clamp(12px,1.8vw,16px);
  border:0; border-radius:12px; background:#7a0000; color:#fff;
  font-weight:700; font-size:clamp(1rem,.95rem + .35vw,1.1rem); cursor:pointer;
}
.auth-btn:hover{ filter:brightness(.95); }
.auth-btn:disabled{ opacity:.7; cursor:not-allowed; }
.auth-alert{ margin-top:10px; padding:12px; border-radius:10px; background:#fee2e2; color:#7a0a0a; font-size:.9rem; border:1px solid #f8b4b4; }
</style>