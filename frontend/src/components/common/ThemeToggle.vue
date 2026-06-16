<template>
  <button 
    @click="toggleTheme" 
    class="px-3 py-1 rounded-lg border transition-colors duration-200"
    :class="isDark ? 'bg-gray-700 border-gray-600 text-yellow-400' : 'bg-gray-100 border-gray-300 text-gray-700'"
    :title="isDark ? 'حالت روشن' : 'حالت تاریک'"
  >
    {{ isDark ? '☀️' : '🌙' }}
  </button>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isDark = ref(false)

const toggleTheme = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
})
</script>