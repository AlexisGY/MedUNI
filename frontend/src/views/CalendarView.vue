<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
import { reactive, computed } from "vue";
import { fetchUsuario } from '@/services/api'; // OBTENER USUARIO
import dayjs from "dayjs";
import { ref, onMounted } from 'vue';
import isoWeek from "dayjs/plugin/isoWeek";
import "dayjs/locale/es";
import uniLogo from "../assets/logo-uni.png";

import { useCitaStore } from "@/stores/reserva_cita";
const citaStore = useCitaStore(); // CITA STORE

// Simula una llamada asíncrona, como la carga de datos
const estudianteDatos = ref([]);
const loading = ref(false); // 👈 aquí declaramos loading
const error = ref(null);
onMounted(async () => {
  loading.value = true;
  try {
   const username = localStorage.getItem('user');
    estudianteDatos.value = await fetchUsuario(username);
    citaStore.setEstudiante(estudianteDatos.value.id) // Llamar al API
    // Si tu backend NO envía icono, podrías mapear un ícono por defecto aquí.
    // ejemplo: especialidades.value = especialidades.value.map(e => ({ ...e, icon: "🦷" }));
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || "Error cargando especialidades";
  } finally {
    loading.value = false;
  }
});

console.log(estudianteDatos)
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
// FUNCION DEL BOTON PARA IR A LAS ESPECIALIDADES

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
  return Array.from({ length: 42 }, (_, i) => start.add(i, "day"));
}
const cells = computed(buildCells);

function isSameDay(a, b)   { return a.isSame(b, "day"); }
function isOtherMonth(d)   { return state.mode==="month" && !d.isSame(state.cursor, "month"); }
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
    
     <!-- Saludo -->
    <div class="alert alert-info text-center py-3 mb-3">
    <span class="fw-bold">¡Bienvenido, {{estudianteDatos.nombres}} {{estudianteDatos.apellidos}}!</span>
    </div>

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
    <div class="grid" >
      <div v-for="d in cells" :key="d.valueOf()" class="col">
        <button
          class="w-100 border rounded-3 py-3 position-relative"
          :class="{
            'bg-light text-muted': isOtherMonth(d),
            'border-2 border-primary': isSameDay(d, state.selected)
          }"
          @click="state.selected = d"
        >
          <span class="small">{{ d.date() }}</span>
        </button>
      </div>
    </div>


    <button class="btn btn-danger 0 mb-3"
    @click="irEspecialidades">Reservar cita</button>
  </div>
</template>

<style scoped>
  .calendar-wrapper { width: min(100%, 1100px); margin: 0 auto; }
  .grid { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: .25rem; }
  .cell { aspect-ratio: 1 / 1; } /* mantiene celdas cuadradas en mes */
  button.border-2 { border-width: 2px !important; }
</style>
