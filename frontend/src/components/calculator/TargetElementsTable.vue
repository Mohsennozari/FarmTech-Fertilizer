<template>
  <div class="border border-blue-200 rounded-xl overflow-hidden">
    <!-- Header -->
    <div class="bg-blue-50 px-4 py-3 border-b border-blue-200">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <svg class="w-5 h-5 text-blue-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <h3 class="font-semibold text-blue-800">🎯 عناصر هدف ۱۶ گانه</h3>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs text-blue-600">واحد پیش‌فرض:</span>
          <select v-model="unit" class="text-xs px-2 py-1 border border-blue-300 rounded-lg bg-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500">
            <option value="ppm">PPM/L</option>
            <option value="meq">MEQ/L</option>
            <option value="mmol">MMOLS/L</option>
          </select>
        </div>
      </div>
      <p class="text-xs text-blue-600 mt-1">
        مقادیر هدف مورد نظر خود را برای هر عنصر وارد کنید
      </p>
    </div>

    <!-- جدول عناصر -->
    <div class="p-4 overflow-x-auto">
      <table class="w-full text-sm border-collapse">
        <thead>
          <tr class="bg-gray-100">
            <th class="border border-gray-300 px-2 py-2 text-right min-w-[80px]">عنصر</th>
            <th v-for="elem in ELEMENTS_16" :key="elem" class="border border-gray-300 px-2 py-2 text-center min-w-[70px]">
              {{ elem }}
            </th>
          </tr>
        </thead>
        <tbody>
          <!-- ردیف: مقدار هدف (ورودی کاربر) -->
          <tr class="hover:bg-[var(--bg-primary)]">
            <td class="border border-gray-300 px-2 py-2 font-medium text-gray-700 bg-gray-50 text-sm">
              هدف
            </td>
            <td v-for="elem in ELEMENTS_16" :key="`target-${elem}`" class="border border-gray-300 px-1 py-1 text-center">
              <input
                type="number"
                :value="getTargetValue(elem)"
                @input="updateTarget(elem, ($event.target as HTMLInputElement).value)"
                class="w-full min-w-[60px] px-1 py-1 text-center border border-gray-200 rounded focus:border-blue-500 focus:ring-1 focus:ring-blue-500 bg-[var(--bg-primary)] text-[var(--text-primary)] text-sm"
                step="0.01"
                min="0"
                placeholder="۰"
              />
            </td>
          </tr>

          <!-- ردیف: محلول نهایی (محاسبه شده) -->
          <tr class="hover:bg-[var(--bg-primary)]">
            <td class="border border-gray-300 px-2 py-2 font-medium text-gray-700 bg-gray-50 text-sm">
              محلول نهایی
            </td>
            <td v-for="elem in ELEMENTS_16" :key="`final-${elem}`" class="border border-gray-300 px-2 py-2 text-center text-sm font-mono">
              {{ getFinalValue(elem) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- دکمه اعمال -->
    <div class="px-4 py-3 bg-gray-50 border-t border-gray-200 flex justify-end">
      <button
        @click="applyTargets"
        class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm transition flex items-center gap-2"
      >
        <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M5 13l4 4L19 7" />
        </svg>
        اعمال عناصر هدف
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';

// ============================================================
// Constants
// ============================================================

const ELEMENTS_16 = [
  'N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl',
  'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'
] as const;

// ============================================================
// Props & Emits
// ============================================================

const props = defineProps<{
  targetElements?: Record<string, number>;
  finalSolution?: Record<string, number>;
}>();

const emit = defineEmits<{
  (e: 'update:targets', targets: Record<string, number>): void;
}>();

// ============================================================
// State
// ============================================================

const unit = ref('ppm');

// مقادیر هدف محلی
const localTargets = ref<Record<string, number>>({});

// مقداردهی اولیه
watch(() => props.targetElements, (newVal) => {
  if (newVal) {
    localTargets.value = { ...newVal };
  }
}, { immediate: true });

// ============================================================
// Functions
// ============================================================

const getTargetValue = (elem: string): string => {
  const val = localTargets.value[elem];
  return val !== undefined && val !== null ? String(val) : '';
};

const updateTarget = (elem: string, value: string) => {
  const num = parseFloat(value);
  if (!isNaN(num) && num >= 0) {
    localTargets.value[elem] = num;
  } else if (value === '') {
    delete localTargets.value[elem];
  }
};

const getFinalValue = (elem: string): string => {
  const val = props.finalSolution?.[elem];
  if (val !== undefined && val !== null && val > 0) {
    return val.toFixed(2);
  }
  return '—';
};

const applyTargets = () => {
  emit('update:targets', { ...localTargets.value });
};
</script>
