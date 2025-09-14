<template>
  <Teleport to="body">
    <div v-if="open" class="modal-backdrop" @click.self="onOverlayClick">
      <div
        class="modal-container"
        ref="container"
        role="dialog"
        aria-modal="true"
        :aria-label="ariaLabel"
      >
        <div v-if="$slots.header" class="modal-header" :class="{ 'modal-header--full': headerFullBleed }">
          <slot name="header" :close="close" />
        </div>

        <div class="modal-body">
          <slot />
        </div>

        <div v-if="$slots.footer" class="modal-footer">
          <slot name="footer" :close="close" />
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'

const props = defineProps({
  open: { type: Boolean, default: false },
  closeOnEsc: { type: Boolean, default: true },
  closeOnOverlay: { type: Boolean, default: true },
  ariaLabel: { type: String, default: 'Modal' },
  headerFullBleed: { type: Boolean, default: false },
})

const emit = defineEmits(['update:open', 'close'])

const container = ref(null)

function close() {
  emit('update:open', false)
  emit('close')
}

function onOverlayClick() {
  if (props.closeOnOverlay) close()
}

function onKeydown(e) {
  if (props.closeOnEsc && e.key === 'Escape') {
    e.stopPropagation()
    close()
  }
}

function focusFirst() {
  // Intenta enfocar el primer elemento enfocable del modal
  const el = container.value
  if (!el) return
  const focusable = el.querySelector(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  )
  if (focusable) {
    focusable.focus()
  } else {
    el.setAttribute('tabindex', '-1')
    el.focus()
  }
}

watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      document.addEventListener('keydown', onKeydown)
      // Pequeño delay para asegurar que el modal esté montado
      requestAnimationFrame(() => focusFirst())
    } else {
      document.removeEventListener('keydown', onKeydown)
    }
  },
  { immediate: true }
)

onMounted(() => {
  if (props.open) {
    document.addEventListener('keydown', onKeydown)
    requestAnimationFrame(() => focusFirst())
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', onKeydown)
})
</script>

<style scoped>
.modal-backdrop{
  position: fixed; inset: 0;
  background: rgba(0,0,0,.45);
  display: grid; place-items: center;
  z-index: 1050;
}
.modal-container{
  width: min(520px, 92vw);
  background: var(--color-surface);
  color: var(--color-text);
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,.25);
  overflow: hidden;
}
.modal-header{ padding: 0; }
.modal-header{ display: block; width: 100%; }
.modal-footer{ padding: 12px 16px; }
.modal-body{ padding: 8px 16px; }

.modal-header :deep(.btn-close){
  border: none; background: transparent; font-size: 18px; line-height: 1; color: inherit;
}
.modal-header--full{ padding: 0; }
.modal-header :deep(.icon-btn){
  border: none; background: transparent; color: inherit; width: 32px; height: 32px; display: inline-flex; align-items: center; justify-content: center; font-size: 18px; line-height: 1; border-radius: 6px;
}
</style>
