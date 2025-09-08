<!-- views/HorariosHoraView.vue -->
<template>
  <div class="d-flex flex-column min-vh-100" style="background: var(--color-surface); color: var(--color-text);">
    <!-- Header -->
    <header class="border-bottom" style="background: var(--color-surface);">
      <div class="container py-2 d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center gap-2">
          <img src="@/assets/logo-uni.png" alt="UNI" style="height:40px;width:40px;" />
          <h1 class="fs-5 fw-semibold mb-0">UNI</h1>
        </div>
        <button type="button" class="btn btn-sm btn-outline-secondary">☰</button>
      </div>
    </header>

    <!-- Especialidad y doctor actual -->
    <section class="py-3" style="background: var(--color-primary); color: var(--color-surface);">
      <div class="container d-flex justify-content-between align-items-center">
        <button
          type="button"
          class="btn btn-light btn-sm"
          :disabled="currentDoctorIndex === 0"
          @click="prevDoctor"
          aria-label="Doctor anterior"
        >&lt;</button>

        <div class="text-center">
          <h2 class="h6 fw-bold mb-1">{{ especialidadNombre }}</h2>
          <p class="mb-0 small" style="opacity:.95;">
            {{ currentDoctor?.nombre }} {{ currentDoctor?.apellido }}
          </p>
        </div>

        <button
          type="button"
          class="btn btn-light btn-sm"
          :disabled="currentDoctorIndex === medicos.length - 1"
          @click="nextDoctor"
          aria-label="Siguiente doctor"
        >&gt;</button>
      </div>
    </section>

    <!-- Día seleccionado -->
    <div class="container text-center py-3">
      <p class="mb-0 text-muted small">{{ fechaFormateada }}</p>
    </div>

    <!-- Leyenda -->
    <div class="container mb-2">
      <div class="d-flex justify-content-center gap-4 small">
        <div class="d-flex align-items-center gap-1">
          <span class="legend-dot border"></span><span>Disponible</span>
        </div>
        <div class="d-flex align-items-center gap-1">
          <span class="legend-dot selected"></span><span>Seleccionado</span>
        </div>
        <div class="d-flex align-items-center gap-1">
          <span class="legend-dot occupied"></span><span>Ocupado</span>
        </div>
      </div>
    </div>

    <!-- Lista de horarios -->
    <div class="grid grid-cols-3 gap-3 px-4">
      <button
        v-for="slot in horarios"
        :key="slot.hora"
        @click="seleccionarHorario(slot)"
        :class="[
          'py-2 rounded-lg border text-sm font-medium',
          slot.estado === 'disponible' ? 'bg-white text-gray-700 hover:bg-gray-100' : '',
          slot.estado === 'ocupado' ? 'bg-gray-300 text-gray-500 cursor-not-allowed' : '',
          slotSeleccionado?.hora === slot.hora ? 'bg-red-700 text-white' : ''
        ]"
        :disabled="slot.estado === 'ocupado'"
      >
        {{ slot.hora }}
      </button>
    </div>

    <!-- Botón continuar -->
    <div class="container py-4 mt-auto">
      <button
        type="button"
        class="btn w-100 fw-bold btn-primary-uni"
        :disabled="!slotSeleccionado"
        @click="continuar"
      >
        Continuar
      </button>
    </div>
  </div>
</template>

<!-- SCRIPT-->
<script setup>
import { ref, computed, onMounted } from "vue";
import { fetchMedicosPorEspecialidad, fetchHorariosPorMedico } from "@/services/api";
import { useCitaStore } from "@/stores/reserva_cita";
import { reservarCita } from "@/services/api"; // Reservar cita

const citaStore = useCitaStore();
const especialidadNombre = citaStore.especialidad_nombre || "Especialidad";
const especialidadId = citaStore.especialidad_id;

const medicos = ref([]);
const currentDoctorIndex = ref(0);
const horarios = ref([]);
const slotSeleccionado = ref(null);

const fecha = citaStore.fecha; // se asume que viene del flujo anterior
const fechaAFormato = fecha ? new Date(fecha) : new Date();

const currentDoctor = computed(() => medicos.value[currentDoctorIndex.value]);

const fechaFormateada = computed(() =>
  fechaAFormato.toLocaleDateString("es-PE", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  })
);

onMounted(async () => {
  if (!especialidadId) return;
  medicos.value = await fetchMedicosPorEspecialidad(especialidadId);
  if (medicos.value.length > 0) {
    await cargarHorarios();
  }
});

function normalizarSlot(s) {
  const hora_inicio = s.hora_inicio ?? s.hora ?? '';
  const hora_fin = s.hora_fin ?? null;

  let disponibilidad = s.disponibilidad;
  if (typeof disponibilidad !== 'boolean') {
    if (typeof s.estado === 'string') {
      disponibilidad = s.estado.toLowerCase() === 'disponible';
    } else if (s.estado === true || s.estado === false) {
      disponibilidad = s.estado;
    } else {
      disponibilidad = true;
    }
  }

  return {
    ...s,
    hora_inicio,
    hora_fin,
    disponibilidad,
  };
}

// CARGAR HORARIOS
async function cargarHorarios() {
  if (!currentDoctor.value) return;
  const raw = await fetchHorariosPorMedico(fecha, currentDoctor.value.id);

  // 👇 Esto te mostrará en la consola del navegador qué datos exactos manda tu backend
  console.log('Ejemplo de slot desde API:', raw?.[0]);

  // 👇 Normalizamos para que siempre tengas hora_inicio, hora_fin y disponibilidad
  horarios.value = raw.map(normalizarSlot);

  slotSeleccionado.value = null;
}

// CARGAR HORARIOS SEGUN EL DOCTOR POSTERIOR
function prevDoctor() {
  if (currentDoctorIndex.value > 0) {
    currentDoctorIndex.value--;
    cargarHorarios();
  }
}

// CARGAR HORARIOS SEGUN EL DOCTOR POSTERIOR
function nextDoctor() {
  if (currentDoctorIndex.value < medicos.value.length - 1) {
    currentDoctorIndex.value++;
    cargarHorarios();
  }
}

function seleccionarHorario(slot) {
  if (slot.disponibilidad === true) {
    slotSeleccionado.value = slot;
  }
}

function continuar() {
  alert(
    `Cita reservada con Dr. ${currentDoctor.value.nombre} ${currentDoctor.value.apellido} a las ${slotSeleccionado.value.hora}`
  );
}
</script>

<style scoped>
/* Botón institucional usando tu paleta */
.btn-primary-uni{
  background: var(--color-primary);
  color: var(--color-surface);
  border: none;
}
.btn-primary-uni:disabled{
  background: var(--color-border);
  color: #888;
}
.btn-primary-uni:hover,
.btn-primary-uni:focus{
  filter: brightness(0.92);
  color: var(--color-surface);
}

/* Slots */
.btn-slot{
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  color: var(--color-text);
  font-weight: 500;
}
.btn-slot:hover{ background: var(--color-surface-alt); }
.btn-slot.occupied{
  background: var(--color-surface-alt);
  color: #9aa0a6;
  cursor: not-allowed;
}
.btn-slot.selected{
  background: var(--color-primary);
  color: var(--color-surface);
  border-color: var(--color-primary);
}

/* Leyenda */
.legend-dot{
  display:inline-block;
  width: .75rem; height: .75rem;
  border-radius: 999px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
}
.legend-dot.selected{ background: var(--color-primary); border-color: var(--color-primary); }
.legend-dot.occupied{ background: var(--color-surface-alt); }
</style>
