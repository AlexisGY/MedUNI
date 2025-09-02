<script setup>
import { useAuth } from './stores/auth'
import { useRoute } from 'vue-router'
const auth = useAuth()
const route = useRoute()
</script>

<template>
  <nav v-if="route.path !== '/login'" class="navbar navbar-expand-lg" style="background:#7b0000">
    <div class="container">
      <RouterLink class="navbar-brand text-white fw-semibold" to="/">Citas UNI</RouterLink>
      <div class="collapse navbar-collapse show">
        <ul class="navbar-nav ms-auto gap-2">
          <li class="nav-item" v-if="auth.isAuth"><RouterLink class="nav-link text-white" to="/reservar">Reservar</RouterLink></li>
          <li class="nav-item" v-if="!auth.isAuth"><RouterLink class="btn btn-light btn-sm" to="/login">Ingresar</RouterLink></li>
          <li class="nav-item" v-else><button class="btn btn-outline-light btn-sm" @click="auth.logout()">Salir</button></li>
        </ul>
      </div>
    </div>
  </nav>
  <main class="container py-4"><RouterView /></main>
</template>
