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

    <!-- Tanks (A and B) -->
    <div v-for="tank in result.tanks" :key="tank.name" class="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden">
      <div class="px-5 py-4 border-b" :class="tank.name.includes('کلسیم') ? 'bg-blue-50 border-blue-100' : 'bg-green-50 border-green-100'">
        <h3 class="font-semibold flex items-center gap-2" :class="tank.name.includes('کلسیم') ? 'text-blue-800' : 'text-green-800'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
          </svg>
          {{ tank.name }}
        </h3>
        <p v-if="tank.description" class="text-xs mt-1" :class="tank.name.includes('کلسیم') ? 'text-blue-600' : 'text-green-600'">
          {{ tank.description }}
        </p>
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
            <tr v-for="dose in tank.doses" :key="dose.id" class="hover:bg-gray-50 transition">
              <td class="px-4 py-3 text-sm text-gray-800">
                {{ dose.name }}
                <span v-if="dose.brand_name" class="text-xs text-gray-400 block">{{ dose.brand_name }}</span>
              </td>
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

    <!-- Predicted EC -->
    <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl shadow-card border border-blue-100 p-5">
      <h4 class="font-semibold text-gray-800 mb-3 flex items-center gap-2">
        <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        پیش‌بینی EC نهایی
      </h4>
      <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
        <div class="text-center">
          <p class="text-sm text-gray-500 mb-1">EC محاسبه شده</p>
          <p class="text-3xl font-bold" :class="(result.predicted_ec || 0) > (result.ec_ph_targets?.ec_max || 2) ? 'text-red-600' : 'text-green-600'">
            {{ result.predicted_ec || 0 }} <span class="text-sm font-normal text-gray-500">mS/cm</span>
          </p>
        </div>
        <div class="w-px h-12 bg-gray-200 hidden sm:block"></div>
        <div class="text-center">
          <p class="text-sm text-gray-500 mb-1">EC آب پایه</p>
          <p class="text-xl font-semibold text-gray-800">{{ result.water_ec_ms_cm || 0 }} mS/cm</p>
        </div>
        <div class="w-px h-12 bg-gray-200 hidden sm:block"></div>
        <div class="text-center">
          <p class="text-sm text-gray-500 mb-1">افزایش ناشی از کودها</p>
          <p class="text-xl font-semibold text-gray-800">{{ ((result.predicted_ec || 0) - (result.water_ec_ms_cm || 0)).toFixed(2) }} mS/cm</p>
        </div>
      </div>
      <div v-if="result.ec_warning" class="mt-4 p-3 bg-amber-50 rounded-lg border border-amber-200">
        <p class="text-sm text-amber-700 flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          {{ result.ec_warning }}
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
      <div class="text-gray-600 whitespace-pre-line font-mono text-xs bg-gray-50 p-4 rounded-lg">
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
