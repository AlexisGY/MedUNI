<template>
  <div class="min-h-screen bg-white flex flex-col">
    <!-- Header -->
    <header class="flex justify-between items-center px-4 py-3 border-b">
      <div class="flex items-center space-x-2">
        <img src="@/assets/logo-uni.png" alt="UNI" class="h-10 w-10" />
        <h1 class="text-lg font-bold text-gray-800">UNI</h1>
      </div>
      <button>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M4 6h16M4 12h16m-7 6h7" />
        </svg>
      </button>
    </header>

    <!-- Título -->
    <div class="px-4 py-3 text-center">
      <p class="text-gray-600 text-sm">
        Elige la especialidad o el doctor para reservar la cita
      </p>
    </div>

    <!-- Buscador -->
    <div class="px-4 py-3 text-center">
      <input
        v-model="search"
        type="text"
        placeholder="Nombre de la especialidad"
        class="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-500"
      />
    </div>

    <!-- Filtro Especialidad -->
    <div class="px-4 py-3 text-center">
      <select
        v-model="filter"
        class="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-500"
      >
        <option value="">Todas las especialidades</option>
        <option
          v-for="esp in especialidades"
          :key="esp.id"
          :value="esp.nombre"
        >
          {{ esp.nombre }}
        </option>
      </select>
    </div>

    <!-- Lista de especialidades (componente reutilizable) -->
    <div v-if="loading" class="text-center text-gray-500">Cargando especialidades...</div>
<div v-else-if="error" class="text-center text-red-500">{{ error }}</div>
<div v-else class="px-4 py-3 text-center">
  <EspecialidadCard
    v-for="esp in especialidadesFiltradas"
    :key="esp.id"
    :nombre="esp.nombre"
    @ver-horarios="verHorarios(esp)"
  />
</div>

    
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import EspecialidadCard from "@/components/EspecialidadCard.vue";
import { fetchEspecialidades } from "@/services/api";
import { useRouter } from "vue-router";
import { useCitaStore } from "@/stores/reserva_cita";

const citaStore = useCitaStore(); // CITA STORE

const router = useRouter();

const especialidades = ref([]);
const search = ref("");
const filter = ref("");
const loading = ref(false); // 👈 aquí declaramos loading
const error = ref(null);
// Funcion del backend : ESPECIALIDADES
onMounted(async () => {
  loading.value = true;
  try {
    especialidades.value = await fetchEspecialidades();
    // Si tu backend NO envía icono, podrías mapear un ícono por defecto aquí.
    // ejemplo: especialidades.value = especialidades.value.map(e => ({ ...e, icon: "🦷" }));
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || "Error cargando especialidades";
  } finally {
    loading.value = false;
  }
});


// Datos simulados (esto luego vendría del backend con Axios o Fetch)

// Computed para filtrar
const especialidadesFiltradas = computed(() => {
  return especialidades.value.filter((e) => {
    const byName = e.nombre
      .toLowerCase()
      .includes(search.value.toLowerCase());
    const byFilter = filter.value ? e.nombre === filter.value : true;
    return byName && byFilter;
  });
});

// Acción al presionar "Ver horarios"
function verHorarios(esp) {
// Usamos el ID de la especialidad para redirigir a la ruta de disponibilidad
  citaStore.setEspecialidad(esp.id);
  citaStore.setEspecialidadNombre(esp.nombre);
  router.push({ name: 'disponibilidad', params: { especialidadId: esp.id } });
}
</script>