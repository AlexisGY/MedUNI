<!-- components/SearchFiltro.vue -->
<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
    <input
      :placeholder="searchPlaceholder"
      class="border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-600"
      :value="search"
      @input="$emit('update:search', ($event.target as HTMLInputElement).value)"
    />

    <select
      class="border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-600"
      :value="filter"
      @change="$emit('update:filter', ($event.target as HTMLSelectElement).value)"
    >
      <option value="">{{ allLabel }}</option>
      <option v-for="opt in options" :key="opt.id" :value="opt[labelKey]">
        {{ opt[labelKey] }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">
type AnyObj = Record<string, any>;

const props = defineProps<{
  options?: AnyObj[];
  labelKey?: string;
  search?: string;
  filter?: string;
  searchPlaceholder?: string;
  allLabel?: string;
}>();

defineEmits<{
  'update:search': [value: string];
  'update:filter': [value: string];
}>();

// Defaults
const {
  options = [],
  labelKey = 'nombre',
  search = '',
  filter = '',
  searchPlaceholder = 'Buscar',
  allLabel = 'Todos',
} = props;
</script>

<style scoped>
/* opcional */
</style>
