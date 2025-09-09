<script setup>
import { useRouter } from 'vue-router'
import { reactive, computed, onMounted } from "vue";
import dayjs from "dayjs";
import isoWeek from "dayjs/plugin/isoWeek";
import "dayjs/locale/es";
import uniLogo from "../assets/logo-uni.png";
import { fetchDiasDisponibles } from "@/services/api"
import { useCitaStore } from "@/stores/reserva_cita";

const citaStore = useCitaStore(); // CITA STORE

import { reservarCita } from '@/services/api'; //reservar cita

dayjs.extend(isoWeek);
dayjs.locale("es");

const today = dayjs();

const router = useRouter();

const state = reactive({
  mode: "month",                      // "week" | "month"
  cursor: today.startOf("isoweek"),  // inicio de semana (lunes)
  selected: today,
  availableDates: [],               // Aquí guardaremos las fechas disponibles
  especialidadId: citaStore.especialidad_id,               // ID de la especialidad (puedes cambiarlo según necesites) (MODIFICABLE)
});

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

// Método para obtener los días disponibles desde el API
async function fetchAvailableDates() {
  try {
    const data = await fetchDiasDisponibles(state.especialidadId);
    // Filtramos y almacenamos las fechas disponibles
    state.availableDates = data.map(item => ({
      fecha: dayjs(item.fecha),
      disponible: item.disponible
    }));
  } catch (error) {
    console.error("Error al obtener los días disponibles:", error);
  }
}

// Llamada a la API cuando el componente se monta
onMounted(() => {
  fetchAvailableDates();
});

// Función para verificar si el día está disponible
function isAvailable(d) {
  const date = dayjs(d).format("YYYY-MM-DD");
  const available = state.availableDates.find(item => item.fecha.format("YYYY-MM-DD") === date);
  return available ? available.disponible : "no listado";
}

function buildCells() {
  if (state.mode === "week") {
    const start = state.cursor.startOf("isoWeek");
    return Array.from({ length: 7 }, (_, i) => start.add(i, "day"));
  }
  const start = state.cursor.startOf("month").startOf("isoWeek");
  return Array.from({ length: 35 }, (_, i) => start.add(i, "day"));
}

const cells = computed(buildCells);

function isSameDay(a, b)   { return a.isSame(b, "day"); }
function isOtherMonth(d)   { return state.mode==="month" && !d.isSame(state.cursor, "month"); }

// Función para manejar la redirección al hacer clic en un día disponible
function handleDayClick(day) {
  if (isAvailable(day) === true) {
    // Redirige al usuario a la página de horarios para el día seleccionado
    citaStore.setFecha(day.format('YYYY-MM-DD')); // Guardamos la fecha seleccionada en el store
    router.push({ name: 'horarios', params: { selectedDate: day.format('YYYY-MM-DD') } });
  }
}   
</script>

<template>
  <div class="container-fluid py-3">
    <!-- Header -->
    <header class="d-flex align-items-center gap-3 mb-3">
      <img :src="uniLogo" alt="UNI" style="height:32px" />
      <h1 class="h5 m-0">UNI</h1>
      <button class="btn btn-outline-secondary ms-auto" aria-label="Menú">
        <i class="bi bi-list"></i>
      </button>
    </header>

    <!-- Agenda -->
    <div class="alert alert-light border mt-3 d-flex align-items-center gap-2">
      <span class="badge bg-danger">&nbsp;</span>
      No hay citas programadas
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
    <div class="grid">
      <div v-for="d in cells" :key="d.valueOf()" class="col">
        <button
          class="w-100 border rounded-3 py-3 position-relative"
          :class="{
            'bg-light text-muted': isOtherMonth(d),
            'border-2 border-primary': isSameDay(d, state.selected),
            'bg-success': isAvailable(d),     // Día disponible
            'bg-danger': !isAvailable(d),      // Día no disponible
            'bg-secondary': isAvailable(d) === 'no listado' // Día no listado en gris
          }"
          @click="handleDayClick(d)"

        >
          <span class="small">{{ d.date() }}</span>
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
  .bg-secondary {
  background-color: #f1f1f1 !important; /* Gris claro para los días no listados */
}
</style>