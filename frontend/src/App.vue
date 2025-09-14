<script setup>
import { useAuth } from './stores/auth'
import { useRoute, useRouter } from 'vue-router'
const auth = useAuth()
const route = useRoute()
const router = useRouter()
import logoBlanco from "@/assets/logo-uni-blanco.png";
const onLogout = async () => {
  await auth.logout()
  router.replace({ name: 'login' })
}
</script>

<template>
  <nav v-if="route.path !== '/login'" class="navbar navbar-expand-lg" style="background:#7b0000">
    <div class="container">
      <RouterLink class="navbar-brand text-white fw-semibold d-flex align-items-center gap-2" to="/">
        <img :src="logoBlanco" alt="UNI" style="height:48px;width:auto;" />
        MedUNI
      </RouterLink>
      <div class="collapse navbar-collapse show">
        <ul class="navbar-nav ms-auto gap-2">
          <li class="nav-item" v-if="!auth.isAuth"><RouterLink class="btn btn-light btn-sm" to="/login">Ingresar</RouterLink></li>
          <li class="nav-item" v-else><button class="btn btn-outline-light btn-sm" @click="onLogout">Salir</button></li>
        </ul>
      </div>
    </div>
  </nav>
  <main class="container py-4"><RouterView /></main>
</template>
