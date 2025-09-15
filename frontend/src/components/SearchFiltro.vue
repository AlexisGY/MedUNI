<!-- components/SearchFiltro.vue -->
<template>
  <div class="container search-wrap">
    <div class="text-center">
      <div class="d-flex justify-content-center align-items-center mb-2 gap-3">
        <input
          :placeholder="props.searchPlaceholder"
          class="form-control w-auto"
          :value="props.search"
          @input="$emit('update:search', ($event.target as HTMLInputElement).value)"
        />
        <select
          class="form-select w-auto"
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
</script>

<style scoped>
.search-wrap{ max-width: 900px; }
.form-control:focus, .form-select:focus {
  box-shadow: 0 0 0 0.15rem rgba(13,110,253,.25);
  outline: none;
}
</style>
