<!-- Platform-v3\frontend\src\components\calculator\ResultsDisplay.vue -->

<template>
  <div class="space-y-6 print-friendly">
    <!-- Header Info -->
    <div class="bg-white rounded-xl shadow-card border border-gray-100 p-5">
      <div class="flex flex-wrap justify-between gap-4">
        <div>
          <p class="text-xs text-gray-500 mb-1">تاریخ محاسبه</p>
          <p class="text-sm font-medium text-gray-800">{{ formatDate(result.created_at) }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 mb-1">مرحله رشد</p>
          <p class="text-sm font-medium text-gray-800">{{ result.stage_name }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 mb-1">رقم</p>
          <p class="text-sm font-medium text-gray-800">{{ result.variety_name }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 mb-1">مخزن</p>
          <p class="text-sm font-medium text-gray-800">{{ result.tank_name }} ({{ result.tank_volume_liters }} L)</p>
        </div>
      </div>
    </div>
    
    <!-- Warnings -->
    <div v-if="result.warnings && result.warnings.length > 0" class="bg-amber-50 border border-amber-200 rounded-xl p-5">
      <div class="flex gap-3">
        <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div class="flex-1">
          <h3 class="font-semibold text-amber-800 mb-2">هشدارها</h3>
          <div v-for="(warn, idx) in result.warnings" :key="idx" class="text-sm text-amber-700 mb-2">
            <span class="font-medium">{{ warn.fertilizers?.join(' + ') || '' }}</span>
            <span> - {{ warn.description }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Doses Table -->
    <div class="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden">
      <div class="px-5 py-4 border-b border-gray-100 bg-gray-50">
        <h3 class="font-semibold text-gray-800 flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          دستور تهیه محلول
        </h3>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">نام کود</th>
              <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">دوز (g/L)</th>
              <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">برای مخزن (g)</th>
              <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">استوک 200x (g/L)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="dose in result.doses" :key="dose.id" class="hover:bg-gray-50 transition">
              <td class="px-4 py-3 text-sm text-gray-800">{{ dose.name }}</td>
              <td class="px-4 py-3 text-sm text-center font-mono font-medium text-primary-600">{{ dose.dose_g_per_liter }}</td>
              <td class="px-4 py-3 text-sm text-center text-gray-600">{{ dose.dose_g_for_tank }}</td>
              <td class="px-4 py-3 text-sm text-center text-gray-600">{{ dose.stock_200x_g_per_liter }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Nutrient Comparison -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white rounded-xl shadow-card border border-gray-100 p-5">
        <h4 class="font-semibold text-gray-800 mb-3 flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          نیاز گیاه (ppm)
        </h4>
        <div class="space-y-2">
          <div v-for="(val, key) in result.target_needs_ppm" :key="key" class="flex justify-between items-center text-sm border-b border-gray-100 pb-1.5">
            <span class="text-gray-600">{{ getElementName(String(key)) }}</span>
            <span class="font-medium text-gray-800">{{ val }}</span>
          </div>
        </div>
      </div>
      
      <div class="bg-white rounded-xl shadow-card border border-gray-100 p-5">
        <h4 class="font-semibold text-gray-800 mb-3 flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          تامین شده (ppm)
        </h4>
        <div class="space-y-2">
          <div v-for="(val, key) in result.calculated_supply_ppm" :key="key" class="flex justify-between items-center text-sm border-b border-gray-100 pb-1.5">
            <span class="text-gray-600">{{ getElementName(String(key)) }}</span>
            <span class="font-medium text-primary-600">{{ val }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- EC & pH Targets -->
    <div class="bg-white rounded-xl shadow-card border border-gray-100 p-5 flex flex-col sm:flex-row justify-between items-center gap-4">
      <div class="text-center sm:text-right">
        <p class="text-xs text-gray-500 mb-1">محدوده EC هدف</p>
        <p class="text-xl font-semibold text-gray-800">
          {{ result.ec_ph_targets?.ec_min || 0 }} - {{ result.ec_ph_targets?.ec_max || 0 }} <span class="text-sm font-normal text-gray-500">mS/cm</span>
        </p>
      </div>
      <div class="w-px h-8 bg-gray-200 hidden sm:block"></div>
      <div class="text-center sm:text-right">
        <p class="text-xs text-gray-500 mb-1">محدوده pH هدف</p>
        <p class="text-xl font-semibold text-gray-800">
          {{ result.ec_ph_targets?.ph_min || 0 }} - {{ result.ec_ph_targets?.ph_max || 0 }}
        </p>
      </div>
    </div>
    
    <!-- Mixing Instructions -->
    <div class="bg-white rounded-xl shadow-card border border-gray-100 p-5">
      <h4 class="font-semibold text-gray-800 mb-3 flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        دستورالعمل اختلاط
      </h4>
      <div class="text-sm text-gray-600 whitespace-pre-line font-mono text-xs bg-gray-50 p-4 rounded-lg">
        {{ result.mixing_instructions }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  result: any
}>()

const getElementName = (key: string): string => {
  const names: Record<string, string> = {
    N: 'نیتروژن',
    P: 'فسفر',
    K: 'پتاسیم',
    Ca: 'کلسیم',
    Mg: 'منیزیم',
    S: 'گوگرد',
    Fe: 'آهن',
    Zn: 'روی',
    Mn: 'منگنز',
    Cu: 'مس',
    B: 'بور',
    Mo: 'مولیبدن',
    Cl: 'کلر'
  }
  return names[key] || key
}

const formatDate = (dateStr: string): string => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('fa-IR') + ' - ' + date.toLocaleTimeString('fa-IR')
}
</script>