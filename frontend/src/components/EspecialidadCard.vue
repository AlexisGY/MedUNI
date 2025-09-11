<template>
  <div
    class="card shadow-sm w-100"
    style="background-color: var(--color-surface); border-color: var(--color-border);"
  >
    <div class="card-body d-flex align-items-center">
      <div class="flex-grow-1">
        <h6 class="card-title mb-0 fw-semibold" 
          style="color: var(--color-text); text-overflow: ellipsis;">
          {{ nombre }}
        </h6>
      </div>
      <button
        type="button"
        class="btn btn-sm btn-primary-uni ms-3"
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
