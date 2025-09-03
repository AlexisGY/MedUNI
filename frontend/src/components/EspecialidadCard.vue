<template>
  <div class="flex items-center justify-between border rounded-lg px-4 py-3 shadow-sm">
    <div class="flex items-center space-x-3">
      <span class="font-semibold text-gray-700">{{ nombre }}</span>
    </div>
    <button
      @click="$emit('ver-horarios')"
      class="bg-red-700 text-white px-3 py-1 rounded-lg text-sm"
    >
      Ver horarios
    </button>
  </div>
</template>

<script setup>
defineProps({
  nombre: String,
});
</script>