<!-- components/SearchFiltro.vue -->
<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
    <input
      :placeholder="props.searchPlaceholder"
      class="border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-600"
      :value="props.search"
      @input="$emit('update:search', ($event.target as HTMLInputElement).value)"
    />

    <select
      class="border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-600"
      :value="props.filter"
      @change="$emit('update:filter', ($event.target as HTMLSelectElement).value)"
    >
      <option value="">{{ props.allLabel }}</option>
      <option v-for="opt in props.options" :key="opt.id" :value="opt[props.labelKey]">
        {{ opt[props.labelKey] }}
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

// Elimina el destructuring para mantener la reactividad de los props
</script>

<style scoped>
/* opcional */
</style>
