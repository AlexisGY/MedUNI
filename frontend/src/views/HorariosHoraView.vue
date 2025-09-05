<template>
  <div class="min-h-screen bg-white flex flex-col">
    <!-- Header -->
    <header class="flex justify-between items-center px-4 py-3 border-b">
      <div class="flex items-center space-x-2">
        <img src="@/assets/logo-uni.png" alt="UNI" class="h-10 w-10" />
        <h1 class="text-lg font-bold text-gray-800">UNI</h1>
      </div>
    </header>

    <!-- Título -->
    <div class="px-4 py-3 text-center">
      <p class="text-gray-600 text-sm">
        Médicos disponibles en la especialidad de {{ especialidad.nombre }}
      </p>
    </div>

    <!-- Lista de médicos -->
    <div v-if="loading" class="text-center text-gray-500">Cargando médicos...</div>
    <div v-else-if="error" class="text-center text-red-500">{{ error }}</div>
    <div v-else>
      <div v-if="medicos.length > 0">
        <div v-for="medico in medicos" :key="medico.id" class="border-b p-4">
          <h2 class="text-xl font-bold">{{ medico.nombre }} {{ medico.apellido }}</h2>
          <p class="text-gray-500">Especialidad: {{ especialidad.nombre }}</p>
        </div>
      </div>
      <div v-else class="text-center text-gray-500">No hay médicos disponibles para esta especialidad.</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router"; // Usado para obtener parámetros de la ruta
import { fetchMedicosPorEspecialidad } from "@/services/api";
// Usamos el route para obtener la especialidad seleccionada
const route = useRoute();
const especialidad = route.params.especialidad; // Aquí asumimos que la especialidad se pasa como un parámetro de la ruta
const medicos = ref([]);
const loading = ref(false);
const error = ref(null);

onMounted(async () => {
  if (!especialidad) {
    error.value = "No se ha seleccionado una especialidad.";
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    // Hacemos una solicitud para obtener los médicos según la especialidad
    medicos.value = await fetchMedicosPorEspecialidad(especialidad.id);
  } catch (e) {
    error.value = "Error al cargar los médicos.";
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* Estilos personalizados */
select {
  font-size: 14px;
}

button {
  cursor: pointer;
}

.text-center {
  text-align: center;
}

.text-sm {
  font-size: 0.875rem;
}

.text-gray-500 {
  color: #6b7280;
}

.w-full {
  width: 100%;
}

.bg-white {
  background-color: #ffffff;
}

.border {
  border: 1px solid #ddd;
}

.rounded-lg {
  border-radius: 8px;
}

.px-4, .py-3 {
  padding: 0.75rem;
}

.focus\:outline-none:focus {
  outline: none;
}

.focus\:ring-2:focus {
  box-shadow: 0 0 0 2px rgba(248, 113, 113, 0.5);
}
</style>