<!-- views/HorariosHoraView.vue -->
<template>
  <div class="d-flex flex-column min-vh-100" style="background: var(--color-surface); color: var(--color-text);">
    <!-- Especialidad y doctor actual -->
    <section class="py-3 rounded-3" style="background: var(--color-primary); color: var(--color-surface);">
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
    <div class="container text-center py-3 ">
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

        <!-- Lista de horarios (responsive, limpio y accesible) -->
    <div class="container">
      <div v-if="horarios.length" class="row row-cols-2 row-cols-md-3 row-cols-lg-4 g-2 g-md-4">
        <div class="col" v-for="slot in horarios" :key="slot.horaInicio">
          <button
            type="button"
            class="btn w-100 btn-slot"
            :class="{
              occupied: slot.disponibilidad === false,
              selected: slotSeleccionado?.horaInicio === slot.horaInicio
            }"
            :disabled="slot.disponibilidad === false"
            @click="seleccionarHorario(slot)"
            :aria-pressed="slotSeleccionado?.horaInicio === slot.horaInicio"
            :title="slot.disponibilidad === false ? 'Ocupado' : 'Disponible'"
          >
            <span class="fw-medium">{{ slot.horaInicio }}</span>
            <span v-if="slot.horaFin"> – {{ slot.horaFin }}</span>
          </button>
        </div>
      </div>

      <!-- Estado vacío -->
      <div v-else class="text-center text-muted py-5 small">
        No hay horarios para este día.
      </div>
    </div>

    <!-- Modal de confirmación -->
    <div v-if="showConfirmationModal" class="modal-backdrop">
      <div class="modal-container">
        <div class="modal-header">
          <h3>Reserva de cita</h3>
          <button class="btn-close" @click="closeConfirmationModal">✖</button>
        </div>
        <div class="modal-body">
          <p><strong>Especialidad:</strong> {{ especialidadNombre }}</p>
          <p><strong>Médico:</strong> {{ currentDoctor?.nombre }} {{ currentDoctor?.apellido }}</p>
          <p><strong>Fecha:</strong> {{ fechaFormateada }}</p>
          <p><strong>Hora:</strong> {{ slotSeleccionado?.horaInicio }} - {{ slotSeleccionado?.horaFin }}</p>
          <p><strong>Recuerde llegar 10 minutos antes de su cita.</strong></p>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeConfirmationModal">Cancelar</button>
          <button class="btn btn-primary" @click="confirmarCita">Confirmar cita</button>
        </div>
      </div>
    </div>

    <!-- Botón continuar -->
    <div class="container py-4 mt-auto">
      <button
        type="button"
        class="btn w-100 fw-bold btn-primary-uni"
        :disabled="!slotSeleccionado"
        @click="mostrarModalConfirmacion"
      >
        Continuar
      </button>
    </div>
  </div>
</template>

<!-- SCRIPT-->
<script setup>
import { ref, computed, onMounted } from "vue";
import { fetchMedicosPorEspecialidad, fetchHorariosPorMedico, reservarCita } from "@/services/api";
import { useCitaStore } from "@/stores/reserva_cita";
import { useRoute, useRouter } from "vue-router";


const route = useRoute();
const citaStore = useCitaStore();

const especialidadNombre = citaStore.especialidadNombre || "Especialidad";
const especialidadId = citaStore.especialidadId;
const router = useRouter();

const medicos = ref([]);
const currentDoctorIndex = ref(0);
const horarios = ref([]);
const slotSeleccionado = ref(null);

const fechaStr = route.params.selectedDate || citaStore.fecha || new Date().toISOString().slice(0, 10);
const fechaAFormato = fechaStr ? new Date(`${fechaStr}T00:00:00`) : new Date();
const showConfirmationModal = ref(false);

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
  const horaInicio = s.horaInicio ?? s.hora ?? '';
  const horaFin = s.horaFin ?? null;

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
    horaInicio,
    horaFin,
    disponibilidad,
  };
}

// CARGAR HORARIOS
async function cargarHorarios() {
  if (!currentDoctor.value) return;
  const raw = await fetchHorariosPorMedico(fechaStr, currentDoctor.value.id);

  console.log('Ejemplo de slot desde API:', raw?.[0]);

  horarios.value = raw.map(normalizarSlot);

  slotSeleccionado.value = null;
}

// CARGAR HORARIOS SEGUN EL DOCTOR ANTERIOR
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

// Modal de confirmación
function mostrarModalConfirmacion() {
  showConfirmationModal.value = true; // Muestra el modal de confirmación
}
// Cerrar modal de confirmación
function closeConfirmationModal() {
  showConfirmationModal.value = false; // Cierra el modal de confirmación
}


async function confirmarCita() {

  const citaData = {
    estudianteId: Number(citaStore.estudianteId),
    medicoId: Number(currentDoctor.value.id),
    especialidadId: Number(especialidadId),
    fecha: fechaStr,
    hora: slotSeleccionado.value.horaInicio,   
    estado: citaStore.estado ?? "pendiente",
  };


  try {
    await reservarCita(citaData);
    closeConfirmationModal();
    router.push("/calendario");
  } catch (error) {
    console.error("Error reservando la cita:", error);
    alert("Hubo un error al reservar la cita. Inténtalo de nuevo.");
  }
}

</script>

<style scoped>
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

/* Modal */
.modal-backdrop{
  position: fixed; inset: 0;
  background: rgba(0,0,0,.45);
  display: grid; place-items: center;
  z-index: 1050;
}
.modal-container{
  width: min(520px, 92vw);
  background: var(--color-surface);
  color: var(--color-text);
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,.25);
  overflow: hidden;
}
.modal-header, .modal-footer{ padding: 12px 16px; }
.modal-body{ padding: 8px 16px; }
.btn-close{
  border: none; background: transparent; font-size: 18px; line-height: 1;
}

</style>
