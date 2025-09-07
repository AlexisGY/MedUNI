<template>
  <div
    class="card shadow-sm"
    style="background-color: var(--color-surface); border-color: var(--color-border);"
  >
    <div class="card-body d-flex justify-content-between align-items-center">
      <h6 class="card-title mb-0 fw-semibold" style="color: var(--color-text);">
        {{ nombre }}
      </h6>
      <button
        type="button"
        class="btn btn-sm btn-primary-uni"
        @click="$emit('ver-horarios')"
      >
        Ver horarios
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({ nombre: { type: String, required: true } });
</script>
