<!-- Platform-v3\frontend\src\components\common\Select.vue -->

<template>
  <div class="w-full">
    <label v-if="label" :for="id" class="block text-sm font-medium text-gray-700 mb-1.5">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <select
      :id="id"
      :value="modelValue"
      :disabled="disabled"
      :required="required"
      class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:border-primary-500 focus:ring-1 focus:ring-primary-500 transition disabled:bg-gray-100 disabled:cursor-not-allowed"
      :class="{ 'border-red-500': error }"
      @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
    >
      <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
      <option v-for="option in options" :key="String(option.value)" :value="option.value">
        {{ option.label }}
      </option>
    </select>
    <p v-if="error" class="mt-1 text-xs text-red-500">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
interface Option {
  value: string | number
  label: string
}

withDefaults(defineProps<{
  id?: string
  label?: string
  modelValue: string | number | null
  options: Option[]
  placeholder?: string
  disabled?: boolean
  required?: boolean
  error?: string
}>(), {
  disabled: false,
  required: false,
  modelValue: ''
})

defineEmits<{
  (e: 'update:modelValue', value: string | number | null): void
}>()
</script>