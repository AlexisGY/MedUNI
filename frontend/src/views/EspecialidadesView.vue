<template>
  <div class="min-h-screen bg-white flex flex-col">
    <header class="sticky top-0 z-10 bg-white/90 backdrop-blur border-b">
      <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <img src="@/assets/logo-uni.png" alt="UNI" class="h-10 w-10" />
          <h1 class="text-xl font-semibold text-gray-900">UNI</h1>
        </div>
      </div>
    </header>

    <main class="flex-1">
      <section class="max-w-3xl mx-auto px-4 py-8">
        <p class="text-center text-gray-600">
          Elige la especialidad o el doctor para reservar la cita
        </p>

        <!-- Reutilizando SearchFiltro -->
        <SearchFiltro
          class="mt-6"
          :options="especialidades"
          label-key="nombre"
          v-model:search="search"
          v-model:filter="filter"
          search-placeholder="Buscar por nombre"
          all-label="Todas las especialidades"
        />

        <!-- estados -->
        <div v-if="loading" class="mt-3 text-center text-muted">Cargando especialidades…</div>
        <div v-else-if="error" class="mt-3 text-center text-danger">{{ error }}</div>

        <!-- grid de cards -->
        <div v-else class="row g-3 mt-1">
          <div class="col-12 col-md-6" v-for="esp in especialidadesFiltradas" :key="esp.id">
            <EspecialidadCard
              :nombre="esp.nombre"
              @ver-horarios="verHorarios(esp)"
            />
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import SearchFiltro from "@/components/SearchFiltro.vue";
import EspecialidadCard from "@/components/EspecialidadCard.vue";
import { fetchEspecialidades } from "@/services/api";
import { useCitaStore } from "@/stores/reserva_cita";

const router = useRouter();
const citaStore = useCitaStore();

const especialidades = ref([]);
const search = ref("");
const filter = ref("");
const loading = ref(false);
const error = ref(null);

onMounted(async () => {
  loading.value = true;
  try {
    especialidades.value = await fetchEspecialidades();
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || "Error cargando especialidades";
  } finally {
    loading.value = false;
  }
});

const especialidadesFiltradas = computed(() => {
  const q = search.value.trim().toLowerCase();
  return especialidades.value.filter((e) => {
    const byName = e.nombre.toLowerCase().includes(q);
    const byFilter = filter.value ? e.nombre === filter.value : true;
    return byName && byFilter;
  });
});

function verHorarios(esp) {
  citaStore.setEspecialidad(esp.id);
  citaStore.setEspecialidadNombre(esp.nombre);
  router.push({ name: "disponibilidad", params: { especialidadId: esp.id } });
}
</script>
