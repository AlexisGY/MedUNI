<template>
  <div class="card shadow-sm w-100 card-surface">
    <div class="card-body d-flex align-items-center">
      <div class="icon-badge me-3" aria-hidden="true">
    <i :class="iconClass" aria-hidden="true"></i>
      </div>

      <div class="flex-grow-1">
        <h6 class="card-title mb-0 fw-semibold card-title-text">
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
import { computed } from 'vue';

const props = defineProps({
  nombre: { type: String, required: true },
  especialidadId: { type: Number, required: true }
});

// Mapa fijo por ID .
const ICONS_BY_ID = {
  1: 'bi bi-scissors',                 // Cirugía General
  2: 'bi bi-heart-pulse-fill',         // Cardiología
  3: 'bi bi-gender-female',            // Ginecología
  4: 'bi bi-gender-male',              // Urología
  5: 'bi bi-eye-fill',                 // Oftalmología
  6: 'bi bi-capsule',                  // Endocrinología
  7: 'bi bi-chat-square-heart-fill',   // Psicología 
  8: 'bi bi-ear-fill',                 // Otorrinolaringología
  9: 'bi bi-emoji-laughing-fill',      // Odontología 
 10: 'bi bi-person-hearts',            // Psiquiatría (temporal)
 11: 'bi bi-flask-fill',               // Laboratorio Clínico
 12: 'bi bi-lungs-fill',               // Neumología 
 13: 'bi bi-hospital-fill',            // Medicina Interna/Familia/General 
 14: 'bi bi-fork-knife',               // Nutrición
 15: 'bi bi-soundwave'                 // Ecografía
};

const iconClass = computed(() => {
  return ICONS_BY_ID[props.especialidadId] || 'bi bi-hospital-fill';
});
</script>

<style scoped>
.card-surface{ background-color: var(--color-surface); border-color: var(--color-border); }
.card-title-text{ color: var(--color-text); text-overflow: ellipsis; overflow: hidden; white-space: nowrap; }
.icon-badge {
  width: 44px;
  height: 44px;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #eef2f6;
  color: #2c3e50;
  flex: 0 0 auto;
}
.icon-badge > i {
  font-size: 20px;
  line-height: 1;
}
</style>

