<!-- components/SearchFiltro.vue -->
<template>
  <div class="mx-auto max-w-[900px]">
    <div class="text-center">
      <div class="inline-flex flex-col md:flex-row items-center gap-y-3 md:gap-y-0 md:gap-x-4 mb-2">
        <input
          :placeholder="props.searchPlaceholder"
          class="w-full md:w-96 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-600"
          :value="props.search"
          @input="$emit('update:search', ($event.target as HTMLInputElement).value)"
        />
        <select
          class="border rounded-lg px-3 py-2 text-sm w-auto align-middle focus:outline-none focus:ring-2 focus:ring-red-600"
          :value="props.filter"
          @change="$emit('update:filter', ($event.target as HTMLSelectElement).value)"
        >
          <option value="">{{ props.allLabel }}</option>
          <option v-for="opt in props.options" :key="opt.id" :value="opt[props.labelKey]">
            {{ opt[props.labelKey] }}
          </option>
        </select>
      </div>
    </div>
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
