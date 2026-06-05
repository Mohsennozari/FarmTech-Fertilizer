<!-- Platform-v3\frontend\src\components\common\Button.vue -->

<template>
  <button
    :type="type"
    :disabled="disabled"
    :class="[
      'inline-flex items-center justify-center gap-2 font-medium rounded-xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2',
      variant === 'primary' && 'bg-primary-600 hover:bg-primary-700 text-white focus:ring-primary-500',
      variant === 'secondary' && 'bg-gray-100 hover:bg-gray-200 text-gray-700 focus:ring-gray-400',
      variant === 'danger' && 'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500',
      variant === 'outline' && 'border border-gray-300 bg-white hover:bg-gray-50 text-gray-700 focus:ring-primary-500',
      size === 'sm' && 'px-3 py-1.5 text-sm',
      size === 'md' && 'px-4 py-2 text-sm',
      size === 'lg' && 'px-6 py-3 text-base',
      disabled && 'opacity-50 cursor-not-allowed'
    ]"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  type?: 'button' | 'submit' | 'reset'
  variant?: 'primary' | 'secondary' | 'danger' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
}>(), {
  type: 'button',
  variant: 'primary',
  size: 'md',
  disabled: false
})

defineEmits<{
  (e: 'click'): void
}>()
</script>