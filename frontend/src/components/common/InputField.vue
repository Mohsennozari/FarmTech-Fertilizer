<!-- Platform-v3\frontend\src\components\common\InputField.vue -->

<template>
  <div class="w-full">
    <label class="block text-xs font-medium text-gray-700 mb-1">
      <svg v-if="icon" class="w-3 h-3 inline ml-1 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path :d="icon" />
      </svg>
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    
    <input
      :type="type"
      :value="modelValue"
      @input="updateValue"
      :placeholder="placeholder"
      :step="step"
      :min="min"
      :max="max"
      class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:border-green-500 focus:ring-1 focus:ring-green-500 transition outline-none"
      :class="{ 'border-red-300 bg-red-50': error }"
    />
    
    <p v-if="helpText" class="text-[10px] text-gray-400 mt-1 flex items-start gap-1">
      <svg class="w-3 h-3 inline mt-0.5 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      {{ helpText }}
    </p>
    
    <p v-if="error" class="text-[10px] text-red-500 mt-1">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  modelValue: string | number | null
  label: string
  type?: string
  placeholder?: string
  icon?: string
  required?: boolean
  step?: string | number
  min?: string | number
  max?: string | number
  helpText?: string
  error?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number | null): void
}>()

const updateValue = (event: Event) => {
  const target = event.target as HTMLInputElement
  let value: string | number | null = target.value
  
  if (props.type === 'number') {
    value = value === '' ? null : Number(value)
  }
  
  emit('update:modelValue', value)
}
</script>