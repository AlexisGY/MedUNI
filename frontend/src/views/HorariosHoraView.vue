<template>
  <div class="min-h-screen bg-white flex flex-col">
    <!-- Header -->
    <header class="flex justify-between items-center px-4 py-3 border-b">
      <div class="flex items-center space-x-2">
        <img src="@/assets/logo-uni.png" alt="UNI" class="h-10 w-10" />
        <h1 class="text-lg font-bold text-gray-800">UNI</h1>
      </div>
      <button class="text-gray-700">☰</button>
    </header>

    <!-- Especialidad y doctor actual -->
    <div class="px-4 py-3 flex justify-between items-center bg-red-700 text-black">
      <button @click="prevDoctor" :disabled="currentDoctorIndex === 0" class="px-2">&lt;</button>
      <div class="text-center">
        <h2 class="font-bold">{{ especialidadNombre }}</h2>
        <p>{{ currentDoctor?.nombre }} {{ currentDoctor?.apellido }}</p>
      </div>
      <button @click="nextDoctor" :disabled="currentDoctorIndex === medicos.length - 1" class="px-2">&gt;</button>
    </div>

    <!-- Día seleccionado -->
    <div class="px-4 py-3 text-center">
      <p class="text-sm text-gray-600">{{ fechaFormateada }}</p>
    </div>

    <!-- Leyenda -->
    <div class="flex justify-center space-x-4 mb-4">
      <div class="flex items-center space-x-1 text-sm">
        <span class="w-3 h-3 rounded-full border"></span>
        <span>Disponible</span>
      </div>
      <div class="flex items-center space-x-1 text-sm">
        <span class="w-3 h-3 rounded-full bg-red-700"></span>
        <span>Seleccionado</span>
      </div>
      <div class="flex items-center space-x-1 text-sm">
        <span class="w-3 h-3 rounded-full bg-gray-300"></span>
        <span>Ocupado</span>
      </div>
    </div>

    <!-- Lista de horarios (RECORDAR QUE EN EL BACKEND LOS ATRIBUTOS SON HORA_INICIO, HORA_FINAL, DISPONIBILIDAD)-->
    <div class="grid grid-cols-3 gap-3 px-4">
      <button
        v-for="slot in horarios"
        :key="slot.hora_inicio"
        @click="seleccionarHorario(slot)"
        :class="[
          'py-2 rounded-lg border text-sm font-medium',
          slot.disponibilidad === true ? 'bg-white text-gray-700 hover:bg-gray-100' : '',
          slot.disponibilidad === false ? 'bg-gray-300 text-gray-500 cursor-not-allowed' : '',
          slotSeleccionado?.hora_inicio === slot.hora_inicio ? 'bg-red-700 text-white' : ''
        ]"
        :disabled="slot.disponibilidad === false"
      >
        {{ slot.hora_inicio }} - {{ slot.hora_fin }}
      </button>
    </div>

    <!-- Botón continuar -->
    <div class="px-4 py-6">
      <button
        class="w-full py-3 bg-red-700 text-white rounded-lg font-bold disabled:bg-gray-300"
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
import { fetchMedicosPorEspecialidad } from "@/services/api"
import { fetchHorariosPorMedico } from "@/services/api";
import { useCitaStore } from "@/stores/reserva_cita";
import { reservarCita } from "@/services/api"; // Reservar cita

// Store con la especialidad seleccionada
const citaStore = useCitaStore();
const especialidadNombre = citaStore.especialidad_nombre || "Especialidad";
const especialidadId = citaStore.especialidad_id;

const medicos = ref([]);
const currentDoctorIndex = ref(0);
const horarios = ref([]);
const slotSeleccionado = ref(null);
const fecha = citaStore.fecha
const fechaAFormato = new Date(fecha);
 // puedes cambiar dinámicamente la fecha

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
// CARGAR HORARIOS
async function cargarHorarios() {
  if (!currentDoctor.value) return;
  horarios.value = await fetchHorariosPorMedico(fecha, currentDoctor.value.id);
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
  citaStore.setHora(slotSeleccionado.value.hora_inicio)
  citaStore.setMedico(currentDoctor.value.id)
  // Datos de la cita a reservar
  const citaData = {    
    estudiante_id: citaStore.estudiante_id, // ID del estudiante logueado
    medico_id: currentDoctor.value.id,
    especialidad_id: especialidadId,
    fecha: fecha,
    hora: slotSeleccionado.value.hora_inicio,
    estado : citaStore.estado
  };
  reservarCita(citaData)
    .then(() => {
        alert(`Cita reservada con Dr. ${currentDoctor.value.nombre} ${currentDoctor.value.apellido} a las ${slotSeleccionado.value.hora_inicio}`);
    })
    .catch((error) => {
      console.error("Error reservando la cita:", error);
      alert("Hubo un error al reservar la cita. Por favor, inténtalo de nuevo.");
    });
}

</script>