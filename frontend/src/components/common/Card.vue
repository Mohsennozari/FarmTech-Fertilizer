<!-- Platform-v3\frontend\src\components\common\Card.vue -->

<template>
  <div class="bg-white rounded-2xl shadow-card border border-gray-100 overflow-hidden">
    <div v-if="$slots.header" class="px-6 py-4 border-b border-gray-100 bg-gray-50">
      <slot name="header" />
    </div>
    <div class="p-6">
      <slot />
    </div>
    <div v-if="$slots.footer" class="px-6 py-4 bg-gray-50 border-t border-gray-100">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
// No props needed for this simple card component
</script>