<template>
  <div class="d-flex flex-column min-vh-100 bg-white">

    <main class="flex-grow-1">
      <section class="container py-4">
        <p class="text-center text-muted">
          Elige la especialidad o el doctor para reservar la cita
        </p>

        <SearchFiltro
          class="mt-3"
          :options="especialidades"
          label-key="nombre"
          v-model:search="search"
          v-model:filter="filter"
          search-placeholder="Buscar por nombre..."
          all-label="Todas las especialidades"
        />

        <div v-if="loading" class="mt-3 text-center text-muted">Cargando especialidades…</div>
        <div v-else-if="error" class="mt-3 text-center text-danger">{{ error }}</div>

        <div v-else class="row g-4 mt-1">
          <div class="col-12 col-sm-6 col-md-6 col-lg-4" v-for="esp in especialidadesFiltradas" :key="esp.id">
            <EspecialidadCard
              :nombre="esp.nombre"
              :especialidadId="esp.id"
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
    // Si no hay búsqueda, muestra todas; si hay, filtra por nombre
    const byName = !q || e.nombre.toLowerCase().includes(q);
    // Si el filtro está vacío o es 'Todas las especialidades', muestra todas; si no, filtra por nombre exacto
    const byFilter = !filter.value || filter.value === "Todas las especialidades" || e.nombre === filter.value;
    return byName && byFilter;
  });
});

function verHorarios(esp) {
  citaStore.setEspecialidad(esp.id);
  citaStore.setEspecialidadNombre(esp.nombre);
  router.push({ name: "disponibilidad", params: { especialidadId: esp.id } });
}
</script>
