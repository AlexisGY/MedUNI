<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
import { reactive, computed} from "vue";
import { fetchUsuario, fetchCitasPorEstudiante } from '@/services/api'; // OBTENER USUARIO
import dayjs from "dayjs";
import { ref, onMounted } from 'vue';
import isoWeek from "dayjs/plugin/isoWeek";
import "dayjs/locale/es";
import uniLogo from "../assets/logo-uni.png";

import CitasCard from'@/components/CitaCard.vue' // COMPONENTE MOSTRAR CITAS

import { useCitaStore } from "@/stores/reserva_cita";
const citaStore = useCitaStore(); // CITA STORE

const citas = ref([]); // AQUI GUARDAMOS LAS CITAS

const diasReservados = ref([]); // Aquí guardaremos los días que tienen citas reservadas

// Simula una llamada asíncrona, como la carga de datos
const estudianteDatos = ref([]);
const loading = ref(false);
const error = ref(null);
onMounted(async () => {
  loading.value = true;
  try {
   const username = localStorage.getItem('user');
    estudianteDatos.value = await fetchUsuario(username);
    citaStore.setEstudiante(estudianteDatos.value.id) // Llamar al API
    // Si tu backend NO envía icono, podrías mapear un ícono por defecto aquí.
    // ejemplo: especialidades.value = especialidades.value.map(e => ({ ...e, icon: "🦷" }));

    citas.value = await fetchCitasPorEstudiante(estudianteDatos.value.id);

     diasReservados.value = citas.value.map(cita => dayjs(cita.fecha).date());
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || "Error cargando especialidades";
  } finally {
    loading.value = false;
  }
});

 // ID del estudiante logueado

dayjs.extend(isoWeek);
dayjs.locale("es");

const today = dayjs();
const state = reactive({
  mode: "month",                      // "week" | "month"
  cursor: today.startOf("isoweek"),  // inicio de semana (lunes)
  selected: today,
});
// FUNCION DEL BOTON PARA IR A LAS ESPECIALIDADES
function irEspecialidades() {
  
  router.push('/especialidades')
}

function prev()  { state.cursor = state.cursor.subtract(1, state.mode); }
function next()  { state.cursor = state.cursor.add(1, state.mode); }
function goToday(){ state.cursor = today.startOf(state.mode === "week" ? "isoWeek" : "month"); state.selected = today; }
function toggleMode() {
  state.mode = state.mode === "week" ? "month" : "week";
  state.cursor = state.mode === "week" ? state.cursor.startOf("isoWeek") : state.cursor.startOf("month");
}

const weekLabels = ["L","M","M","J","V","S","D"];

const monthTitle = computed(() => {
  const start = state.mode === "week" ? state.cursor.startOf("isoWeek") : state.cursor.startOf("month");
  const end   = state.mode === "week" ? state.cursor.endOf("isoWeek")   : state.cursor.endOf("month");
  return `${start.format("D")} – ${end.format("D")} ${end.format("MMMM")}`;
});

function buildCells() {
  if (state.mode === "week") {
    const start = state.cursor.startOf("isoWeek");
    return Array.from({ length: 7 }, (_, i) => start.add(i, "day"));
  }
  // mes completo (6 filas)
  const start = state.cursor.startOf("month").startOf("isoWeek");
  return Array.from({ length: 35 }, (_, i) => start.add(i, "day"));
}
const cells = computed(buildCells);

function isSameDay(a, b)   { return a.isSame(b, "day"); }
function isOtherMonth(d)   { return state.mode==="month" && !d.isSame(state.cursor, "month"); }
function isDayReserved(d) {
  return diasReservados.value.includes(d.date()) && d.month() === state.cursor.month(); // Verifica que el mes coincida; // Verifica si el día está en la lista de días reservados
}

function handleCancelCita(citaId) {
  citas.value = citas.value.filter(c => c.citaId !== citaId)
}
  
</script>

<template>
  <div class="container-fluid py-3">
      <!-- Saludo -->
      <div class="alert alert-info text-center py-3 mb-3">
      <span class="fw-bold">¡Bienvenido, {{estudianteDatos.nombres}} {{estudianteDatos.apellidos}}!</span>
      </div>

      <div class="mb-4">
      <!-- Lista de citas -->
        <CitasCard :citas="citas" @cancel="handleCancelCita" />
      </div>

    <!-- Controls -->
    <div class="d-flex align-items-center gap-2 mb-2">
      <button class="btn btn-light" @click="prev">‹</button>
      <button class="btn btn-outline-secondary" @click="goToday">Hoy</button>
      <span class="fw-semibold ms-2">{{ monthTitle }}</span>
      <button class="btn btn-light ms-2" @click="next">›</button>
      <button class="btn btn-outline-secondary ms-auto" @click="toggleMode">
        {{ state.mode === "week" ? "Mes" : "Semana" }}
      </button>
    </div>

    <!-- Week headers -->
    <div class="row g-1 text-center text-secondary mb-1 small">
      <div class="col" v-for="w in weekLabels" :key="w">{{ w }}</div>
    </div>

    <!-- Grid -->
    <div class="grid" >
      <div v-for="d in cells" :key="d.valueOf()" class="col">
        <button
          class="w-100 border rounded-3 py-3 position-relative"
          :class="{
            'bg-light text-muted': isOtherMonth(d),
            'border-2 border-primary': isSameDay(d, state.selected),
            'bg-gray-200': isDayReserved(d)
          }"
          @click="state.selected = d"
        >
          <span class="small">{{ d.date() }}</span>
        </button>
      </div>
    </div>

    <div class="container px-5">
        <div class="d-flex justify-content-center mt-4 mb-3">
          <button class="btn btn-primary-uni w-100 fs-4" @click="irEspecialidades">
            Reservar cita
          </button>
        </div>
    </div>

  </div>
</template>

<style scoped>
  .calendar-wrapper { width: min(100%, 1100px); margin: 0 auto; }
  .grid { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: .25rem; }
  .cell { aspect-ratio: 1 / 1; } /* mantiene celdas cuadradas en mes */
  button.border-2 { border-width: 2px !important; }


  /* Estilo para los días reservados */
  .bg-gray-200 {
    background-color: #d1d5db !important; /* Gris claro */
    color: #6b7280; /* Gris más oscuro para el texto */
  }
</style>
