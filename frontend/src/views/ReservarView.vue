<template>
  <section class="container container-900">
    <h2 class="mb-3">Reservar cita</h2>

    <div class="row g-3 align-items-end">
      <div class="col-md-5">
        <label class="form-label">Especialidad</label>
        <select class="form-select" v-model="esp">
          <option disabled value="">Selecciona</option>
          <option v-for="e in especialidades" :key="e">{{ e }}</option>
        </select>
      </div>
      <div class="col-md-4">
        <label class="form-label">Fecha</label>
        <input class="form-control" type="date" v-model="fecha" :min="hoy" />
      </div>
      <div class="col-md-3 d-grid">
        <button class="btn btn-primary" :disabled="!esp || !fecha" @click="cargar">Ver horarios</button>
      </div>
    </div>

    <div class="mt-3">
      <div v-if="cargando" class="text-muted">Cargando…</div>
      <div v-else class="row g-2">
        <div v-for="s in horarios" :key="s.hora" class="col-6 col-md-3">
          <button class="btn w-100" :class="s.ocupado ? 'btn-outline-secondary' : 'btn-outline-primary'"
                  :disabled="s.ocupado" @click="reservar(s.hora)">
            {{ s.hora }} <span v-if="s.ocupado">(ocupado)</span>
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { listarEspecialidades, listarHorarios } from '../services/api'

const especialidades = ref([]), esp = ref(''), fecha = ref('')
const hoy = new Date().toISOString().slice(0,10)
const cargando = ref(false), horarios = ref([])

onMounted(async () => { especialidades.value = await listarEspecialidades() })
async function cargar() {
  cargando.value = true
  try { horarios.value = await listarHorarios({ especialidad: esp.value, fecha: fecha.value }) }
  finally { cargando.value = false }
}
function reservar(hora) { alert(`Reserva creada: ${esp.value} el ${fecha.value} a las ${hora}`) }
</script>

<style scoped>
.container-900{ max-width: 900px; }
</style>
