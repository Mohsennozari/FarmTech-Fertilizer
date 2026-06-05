<!-- Platform-v3\frontend\src\components\common\Input.vue -->

<template>
  <div class="w-full">
    <label v-if="label" :for="id" class="block text-sm font-medium text-gray-700 mb-1.5">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <input
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :required="required"
      :step="step"
      :min="min"
      :max="max"
      class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:border-primary-500 focus:ring-1 focus:ring-primary-500 transition disabled:bg-gray-100 disabled:cursor-not-allowed"
      :class="{ 'border-red-500 focus:border-red-500': error }"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
    <p v-if="error" class="mt-1 text-xs text-red-500">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  id?: string
  label?: string
  type?: string
  modelValue: string | number | null
  placeholder?: string
  disabled?: boolean
  required?: boolean
  step?: string | number
  min?: string | number
  max?: string | number
  error?: string
}>(), {
  type: 'text',
  disabled: false,
  required: false,
  modelValue: ''
})

defineEmits<{
  (e: 'update:modelValue', value: string | number | null): void
}>()
</script>