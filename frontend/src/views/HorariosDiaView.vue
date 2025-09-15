<script setup>
import { useRouter } from 'vue-router'
import { reactive, computed, onMounted, watch } from "vue";
import dayjs from "dayjs";
import isoWeek from "dayjs/plugin/isoWeek";
import "dayjs/locale/es";
import { getEspecialidadImageById, getEspecialidadNombreById } from '@/utils/especialidades';

const imagenEspecialidad = computed(() => getEspecialidadImageById(state.especialidadId));
const especialidadNombreDisplay = computed(() => (
  citaStore.especialidadNombre || getEspecialidadNombreById(state.especialidadId)
));
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
  especialidadId: citaStore.especialidadId,               // ID de la especialidad (puedes cambiarlo según necesites) (MODIFICABLE)
});

// Utilidad simple para validar ID numérico positivo
function isValidId(id) {
  const n = Number(id);
  return Number.isInteger(n) && n > 0;
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

// Método para obtener los días disponibles desde el API
async function fetchAvailableDates() {
  try {
    if (!isValidId(state.especialidadId)) {
      // Aún no hay especialidad seleccionada; no llamamos al API
      return;
    }
    const data = await fetchDiasDisponibles(Number(state.especialidadId));
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

// Si el store actualiza la especialidad (p. ej., al volver atrás y elegir otra), refrescamos
watch(
  () => citaStore.especialidadId,
  (val) => {
    state.especialidadId = val;
    fetchAvailableDates();
  }
);

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
    <!-- Imagen de especialidad -->
    <div class="mb-3 d-flex justify-content-center">
      <div class="especialidad-hero">
        <div class="especialidad-hero__header">
          <span class="especialidad-hero__title">{{ especialidadNombreDisplay }}</span>
        </div>
        <img
          :src="imagenEspecialidad"
          :alt="`Imagen ${especialidadNombreDisplay}`"
          class="especialidad-hero__img"
        />
      </div>
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

    <!-- Legend -->
    <div class="d-flex align-items-center gap-3 mb-2 small" aria-hidden="true">
      <div class="d-flex align-items-center gap-2">
        <span class="legend-swatch legend-available"></span>
        <span>Disponible</span>
      </div>
      <div class="d-flex align-items-center gap-2">
        <span class="legend-swatch legend-unavailable"></span>
        <span>No disponible</span>
      </div>
      <div class="d-flex align-items-center gap-2">
        <span class="legend-swatch legend-unlisted"></span>
        <span>No listado</span>
      </div>
    </div>

    <!-- Week headers -->
    <div class="row g-1 text-center text-secondary mb-1 small">
      <div class="col" v-for="w in weekLabels" :key="w">{{ w }}</div>
    </div>

    <!-- Grid -->
    <div class="grid">
      <div v-for="d in cells" :key="d.valueOf()" class="col">
        <button
          class="w-100 border rounded-3 py-3 position-relative day-btn"
          :class="[
            isOtherMonth(d) ? 'day--other-month' : '',
            isSameDay(d, state.selected) ? 'day--selected' : '',
            isAvailable(d) === true ? 'day--available' : (isAvailable(d) === false ? 'day--unavailable' : 'day--unlisted')
          ]"
          @click="handleDayClick(d)"
          :aria-label="`Día ${d.format('D/MM/YYYY')} - ${isAvailable(d) === true ? 'Disponible' : (isAvailable(d) === false ? 'No disponible' : 'No listado')}`"
        >
          <span class="small">{{ d.date() }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .especialidad-hero{
    position: relative;
    width: min(100%, 720px);
    aspect-ratio: 16 / 5; 
    height: auto;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 2px 16px rgba(0,0,0,.08);
    background: #f5f7fa;
  }
  .especialidad-hero__img{
    width: 100%; height: 100%; object-fit: cover; display: block;
  }
  .especialidad-hero__header{
    position: absolute;
    top: 0; left: 0; right: 0;
    background: var(--color-primary);
    color: var(--color-surface);
    padding: 8px 16px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .especialidad-hero__title{
    font-weight: 700;
    font-size: 1.2rem;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: inline-block;
    max-width: 100%;
  }
  .calendar-wrapper { width: min(100%, 1100px); margin: 0 auto; }
  .grid { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: .25rem; }

  /* Legend swatches */
  .legend-swatch { width: 14px; height: 14px; border-radius: 4px; display: inline-block; border: 1px solid rgba(0,0,0,0.1); }
  .legend-available { background: #d4f1db; border-color: #7fcf97; }
  .legend-unavailable { background: #ffd9d4; border-color: #ff9e95; }
  .legend-unlisted { background: #ececec; border-color: #d6d6d6; }

  /* Day button state colors (accessible tints) */
  .day-btn { transition: background-color .15s ease, border-color .15s ease; }
  .day--available {
    background-color: #d4f1db; /* más notorio */
    color: #0f5132; /* texto oscuro legible */
    border-color: #7fcf97;
  }
  .day--available:hover { background-color: #c6ebcf; border-color: #69c788; }

  .day--unavailable {
    background-color: #ffd9d4; /* más notorio */
    color: #842029;
    border-color: #ff9e95;
  }
  .day--unavailable:hover { background-color: #ffcbc4; border-color: #ff7f73; }

  .day--unlisted {
    background-color: #ececec;
    color: #6b7280;
    border-color: #d6d6d6;
  }

  .day--other-month { opacity: .7; }

  .day--selected { border-width: 2px !important; border-color: var(--color-primary) !important; box-shadow: 0 0 0 2px rgba(13,110,253,.15) inset; }

  /* sin estado disabled para mantenerlo simple */

  @media (min-width: 768px) {
    .especialidad-hero { width: min(100%, 840px); }
  }
  @media (min-width: 992px) {
    .especialidad-hero { width: min(100%, 960px); }
  }
  @media (min-width: 1200px) {
    .especialidad-hero { width: min(100%, 1100px); }
  }
</style>