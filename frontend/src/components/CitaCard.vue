<!-- src/components/CitaCard.vue -->
<template>
  <section>
    <header class="d-flex align-items-center justify-content-between mb-3">
      <h5 class="mb-0">Mis citas reservadas</h5>
      <div v-if="loading" class="text-muted small">Cargando…</div>
    </header>

    <!-- vacío -->
    <div v-if="!loading && citas.length === 0" class="alert alert-secondary py-2">
      No tienes citas registradas.
    </div>

    <!-- listado -->
    <ul
      v-else
      class="list-group"
      aria-label="Listado de citas"
    >
      <li
        v-for="c in citas"
        :key="c.cita_id"
        class="list-group-item list-group-item-action d-flex align-items-center gap-3"
        role="button"
        tabindex="0"
        @click="onSelect(c)"
        @keydown.enter.prevent="onSelect(c)"
        @keydown.space.prevent="onSelect(c)"
      >
        <div class="flex-grow-1">
          <div class="fw-semibold">
            {{ formatFecha(c.fecha) }} · {{ formatHora(c.hora) }}
          </div>
          <div class="text-muted small">
            {{ c.especialidad_nombre }} • {{ c.medico_nombre }}
          </div>
        </div>
        <span class="badge" :class="estadoBadgeClass(c.estado)">
          {{ capitalizar(c.estado) }}
        </span>
      </li>
    </ul>

    <!-- detalle -->
    <div v-if="citaSeleccionada" class="card mt-4">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-start">
          <h5 class="card-title mb-2">Detalle de la cita</h5>
          <span class="badge" :class="estadoBadgeClass(citaSeleccionada.estado)">
            {{ capitalizar(citaSeleccionada.estado) }}
          </span>
        </div>

        <dl class="row mb-3">
          <dt class="col-4 col-sm-3">Especialidad</dt>
          <dd class="col-8 col-sm-9">{{ citaSeleccionada.especialidad_nombre }}</dd>

          <dt class="col-4 col-sm-3">Médico</dt>
          <dd class="col-8 col-sm-9">{{ citaSeleccionada.medico_nombre }}</dd>

          <dt class="col-4 col-sm-3">Fecha</dt>
          <dd class="col-8 col-sm-9">{{ formatFecha(citaSeleccionada.fecha) }}</dd>

          <dt class="col-4 col-sm-3">Hora</dt>
          <dd class="col-8 col-sm-9">{{ formatHora(citaSeleccionada.hora) }}</dd>
        </dl>

        <div class="d-flex gap-2">
          <button class="btn btn-outline-secondary" @click="citaSeleccionada = null">
            Cerrar
          </button>
          <button
            class="btn btn-outline-danger"
            v-if="citaSeleccionada.estado !== 'cancelada'"
            @click="$emit('cancel', citaSeleccionada)"
          >
            Cancelar
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  citas: { type: Array, required: true },
  loading: { type: Boolean, default: false },
  locale: { type: String, default: 'es-PE' },
  timeZone: { type: String, default: 'America/Lima' }
})

const emit = defineEmits(['select', 'cancel'])

const citaSeleccionada = ref(null)

function onSelect(cita) {
  citaSeleccionada.value = cita
}

function formatFecha(fechaStr) {
  // acepta "YYYY-MM-DD" o Date-like
  const d = typeof fechaStr === 'string' ? new Date(`${fechaStr}T00:00:00`) : new Date(fechaStr)
  return new Intl.DateTimeFormat(props.locale, {
    weekday: 'long', day: '2-digit', month: 'long', year: 'numeric',
    timeZone: props.timeZone
  }).format(d)
}

function formatHora(horaStr) {
  // "HH:MM" o "HH:MM:SS"
  const [h, m] = horaStr.split(':').map(Number)
  const d = new Date()
  d.setHours(h ?? 0, m ?? 0, 0, 0)
  return new Intl.DateTimeFormat(props.locale, {
    hour: '2-digit', minute: '2-digit', hour12: false,
    timeZone: props.timeZone
  }).format(d)
}

function capitalizar(s) {
  if (!s) return ''
  return s.charAt(0).toUpperCase() + s.slice(1)
}

function estadoBadgeClass(estado) {
  switch ((estado || '').toLowerCase().trim()) {
    case 'confirmada': return 'badge badge-primary-uni'
    case 'pendiente':  return 'badge badge-warning-uni'
    case 'cancelada':  return 'badge badge-danger-uni'
    default:           return 'badge badge-secondary'
  }
}
</script>
