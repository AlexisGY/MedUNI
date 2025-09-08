<!-- src/components/CitaCard.vue -->
<template>
  <div>
    <h5 class="mb-3">Mis citas reservadas</h5>
    <div v-if="citas.length === 0" class="alert alert-secondary">No tienes citas registradas.</div>
    <ul class="list-group">
      <li v-for="cita in citas" :key="cita.cita_id"
          class="list-group-item list-group-item-action"
          @click="seleccionarCita(cita)">
        <div class="fw-bold">{{ cita.fecha }} - {{ cita.hora }}</div>
        <div>{{ cita.especialidad_nombre }} con Dr. {{ cita.medico_nombre }}</div>
      </li>
    </ul>

    <!-- Detalles -->
    <div v-if="citaSeleccionada" class="card mt-4">
      <div class="card-body">
        <h5 class="card-title">Detalle de la cita</h5>
        <p><strong>Especialidad:</strong> {{ citaSeleccionada.especialidad_nombre }}</p>
        <p><strong>Médico:</strong> {{ citaSeleccionada.medico_nombre }}</p>
        <p><strong>Fecha:</strong> {{ citaSeleccionada.fecha }}</p>
        <p><strong>Hora:</strong> {{ citaSeleccionada.hora }}</p>
        <p><strong>Estado:</strong> {{ citaSeleccionada.estado }}</p>
        <button class="btn btn-outline-secondary" @click="citaSeleccionada = null">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  citas: {
    type: Array,
    required: true
  }
})

const citaSeleccionada = ref(null)

function seleccionarCita(cita) {
  citaSeleccionada.value = cita
}
</script>