<!-- views/HorariosHoraView.vue -->
<template>
  <div class="d-flex flex-column min-vh-100 page-bg">
    <!-- Especialidad y doctor actual -->
  <section class="py-3 rounded-3 header-band">
      <div class="container d-flex justify-content-between align-items-center">
        <button
          type="button"
          class="btn btn-nav btn-sm"
          :disabled="currentDoctorIndex === 0"
          @click="prevDoctor"
          aria-label="Doctor anterior"
        >&lt;</button>

        <div class="text-center">
          <h2 class="h6 fw-bold mb-1">{{ especialidadNombreDisplay }}</h2>
          <p class="mb-0 small text-soft">
            {{ currentDoctor?.nombre }} {{ currentDoctor?.apellido }}
          </p>
        </div>

        <button
          type="button"
          class="btn btn-nav btn-sm"
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
    <BaseModal
      v-model:open="showConfirmationModal"
      aria-label="Confirmar reserva"
      :close-on-esc="true"
      :close-on-overlay="false"
    >
      <template #header="{ close }">
        <div class="modal-title-bar">
          <h2 class="m-0 h6">Reserva de cita</h2>
          <button type="button" class="icon-btn icon-light" @click="close" aria-label="Cerrar">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
      </template>

      <div class="confirm-modal-content text-center">
        <div class="mb-2">
          <div class="d-flex align-items-start gap-2">
            <span class="bullet-icon" aria-hidden="true"><i :class="especialidadIconClass"></i></span>
            <div>
              <div class="fw-bold">{{ especialidadNombreDisplay }} - {{ currentDoctor?.nombre }} {{ currentDoctor?.apellido }}</div>
            </div>
          </div>
        </div>

        <div class="mb-2 d-flex align-items-start gap-2">
          <span class="bullet-icon" aria-hidden="true"><i class="bi bi-calendar3"></i></span>
          <div>{{ fechaFormateada }}</div>
        </div>

        <div class="mb-2 d-flex align-items-start gap-2">
          <span class="bullet-icon" aria-hidden="true"><i class="bi bi-clock"></i></span>
          <div>{{ slotSeleccionado?.horaInicio }} - {{ slotSeleccionado?.horaFin }}</div>
        </div>

        <div class="mt-3 d-flex align-items-start gap-2 text-muted small">
          <span class="bullet-icon text-danger" aria-hidden="true"><i class="bi bi-exclamation-circle"></i></span>
          <div>Recuerde llegar 10 minutos antes de su cita</div>
        </div>

        <div class="mt-3">
          <button type="button" class="btn w-100 fw-bold btn-primary-uni" @click="confirmarCita">Confirmar cita</button>
        </div>
      </div>

      <template #footer></template>
    </BaseModal>

    <!-- Botón continuar -->
    <div class="container py-4 mt-4 confirm-cta">
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
import BaseModal from "@/components/BaseModal.vue";
import { getEspecialidadIconClassById, getEspecialidadNombreById } from "@/utils/especialidades";


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
const especialidadIconClass = computed(() => getEspecialidadIconClassById(Number(especialidadId)));

// Nombre de especialidad , con preferencia por el nombre del store
const especialidadNombreDisplay = computed(() => (
  especialidadNombre && especialidadNombre !== 'Especialidad'
    ? especialidadNombre
    : getEspecialidadNombreById(Number(especialidadId))
));

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
.page-bg{ background: var(--color-surface); color: var(--color-text); }
.text-soft{ opacity:.95; }
.header-band{ background: var(--color-primary); color: var(--color-surface); }
.btn-nav{
  background: var(--color-surface);
  color: var(--color-primary);
  border: 1px solid rgba(255,255,255,.5);
}
.btn-nav:hover,
.btn-nav:focus{
  background: rgba(255,255,255,.15);
  color: var(--color-surface);
  border-color: rgba(255,255,255,.75);
}
.btn-nav:disabled{
  opacity: .6;
  color: #eee;
  background: rgba(255,255,255,.1);
}
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
/* Hover básico para slot; se puede ajustar por tema */
.btn.btn-slot:hover{ background: var(--color-surface-alt); }
.btn-slot.selected:hover{ filter: brightness(0.95); }
/* Ocupado no cambia con hover */
.btn-slot.occupied:hover{ background: var(--color-surface-alt); }
.btn-slot:focus-visible{ outline: 2px solid var(--color-primary); outline-offset: 2px; }
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

.confirm-modal-content{
  padding: 12px 16px 16px;
}
.confirm-modal-content .bullet-icon{
  width: 20px; display: inline-flex; align-items: center; justify-content: center;
}

/* Barra de título estilo mockup */
.modal-title-bar{
  background: var(--color-primary);
  color: var(--color-surface);
  padding: 10px 16px;
  border-top-left-radius: 12px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.modal-title-bar .icon-btn{
  color: var(--color-surface);
}
.icon-light{ color: var(--color-surface); }

/* Botón confirmar más redondeado */
.confirm-modal-content .btn-primary-uni{
  border-radius: 10px;
}

/* CTA spacing and centering */
.confirm-cta{ display: flex; justify-content: center; }
.confirm-cta .btn{ max-width: 520px; }

</style>
