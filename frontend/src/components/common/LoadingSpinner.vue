<!-- Platform-v3\frontend\src\components\common\LoadingSpinner.vue -->

<template>
  <div class="flex flex-col items-center justify-center py-12">
    <div class="relative">
      <svg class="w-16 h-16 animate-spin" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="#10b981" stroke-width="4"></circle>
        <path class="opacity-75" fill="#10b981" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
    <p class="mt-4 text-gray-600 font-medium">{{ text || 'در حال محاسبه...' }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  text?: string
}>()
</script>