<!-- Platform-v3\frontend\src\components\common\ErrorAlert.vue -->

<template>
  <div class="bg-red-50 border-r-4 border-red-500 rounded-xl p-4 mb-6 animate-fade-in">
    <div class="flex items-start gap-3">
      <div class="flex-shrink-0">
        <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <div class="flex-1">
        <h3 class="text-sm font-bold text-red-800">خطا</h3>
        <p class="text-sm text-red-700 mt-1">{{ message }}</p>
      </div>
      <button @click="$emit('close')" class="text-red-400 hover:text-red-600 transition">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  message: string
}>()

defineEmits<{
  (e: 'close'): void
}>()
</script>