<!-- Platform-v3\frontend\src\components\calculator\ResultsDisplay.vue -->

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-gradient-to-r from-green-600 to-teal-600 rounded-2xl p-5 text-white">
      <h2 class="text-xl font-bold flex items-center gap-2">
        <svg class="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        نتیجه محاسبات
      </h2>
      <p class="text-green-100 text-sm mt-1">محصول: {{ result.crop_name }} | رقم: {{ result.variety_name }} | مرحله: {{ result.stage_name }}</p>
    </div>

    <!-- هشدارها -->
    <div v-if="result.combined_warnings && result.combined_warnings.length > 0" class="bg-red-50 border border-red-200 rounded-xl p-4">
      <div class="flex items-start gap-3">
        <svg class="w-5 h-5 text-red-500 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div>
          <h4 class="font-bold text-red-800">هشدارهای مهم</h4>
          <ul class="list-disc list-inside text-sm text-red-700 mt-1">
            <li v-for="(w, idx) in result.combined_warnings" :key="idx">{{ w }}</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- جدول نیاز گیاه و عناصر تامین شده -->
    <!-- ============================================================ -->
    <div class="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden">
      <div class="bg-gradient-to-r from-gray-600 to-gray-700 px-5 py-3">
        <h3 class="text-white font-bold flex items-center gap-2">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          مقایسه نیاز گیاه با عناصر تامین شده
        </h3>
      </div>
      <div class="p-5">
        <div class="overflow-x-auto">
          <table class="w-full text-sm border-collapse">
            <thead>
              <tr class="bg-gray-100">
                <th class="border border-gray-300 px-3 py-2 text-right">عنصر</th>
                <th class="border border-gray-300 px-3 py-2 text-center">نیاز گیاه (ppm)</th>
                <th class="border border-gray-300 px-3 py-2 text-center">تامین شده (ppm)</th>
                <th class="border border-gray-300 px-3 py-2 text-center">وضعیت</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in nutrientComparison" :key="item.element" class="hover:bg-gray-50">
                <td class="border border-gray-300 px-3 py-2 font-medium">{{ getElementName(item.element) }}</td>
                <td class="border border-gray-300 px-3 py-2 text-center">{{ formatNumber(item.need) }}</td>
                <td class="border border-gray-300 px-3 py-2 text-center">{{ formatNumber(item.supplied) }}</td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  <span v-if="item.status === 'ok'" class="text-green-600">
                    <svg class="w-5 h-5 inline" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M5 13l4 4L19 7" />
                    </svg>
                  </span>
                  <span v-else-if="item.status === 'low'" class="text-amber-600">
                    <svg class="w-5 h-5 inline" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                  </span>
                  <span v-else class="text-red-600">
                    <svg class="w-5 h-5 inline" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- مخزن اصلی -->
    <!-- ============================================================ -->
    <div class="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden">
      <div class="bg-gradient-to-r from-blue-600 to-indigo-600 px-5 py-3">
        <h3 class="text-white font-bold flex items-center justify-between">
          <span class="flex items-center gap-2">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
            مخزن اصلی (کودهای غیر کلسیمی)
          </span>
          <span class="text-xs bg-white/20 px-2 py-1 rounded-full">{{ result.tank_main_result.tank_name }}</span>
        </h3>
      </div>
      
      <div class="p-5">
        <!-- جدول دوزها -->
        <div class="overflow-x-auto mb-4">
          <table class="w-full text-sm border-collapse">
            <thead>
              <tr class="bg-gray-100">
                <th class="border border-gray-300 px-3 py-2 text-right">نام کود</th>
                <th class="border border-gray-300 px-3 py-2 text-center">مصرف (g/L)</th>
                <th class="border border-gray-300 px-3 py-2 text-center">مجموع برای مخزن</th>
                <th class="border border-gray-300 px-3 py-2 text-center">محلول مادر 200x</th>
                <th class="border border-gray-300 px-3 py-2 text-center">توضیحات</th>
               </tr>
            </thead>
            <tbody>
              <tr v-for="dose in result.tank_main_result.doses" :key="dose.name" class="hover:bg-gray-50">
                <td class="border border-gray-300 px-3 py-2 font-medium">{{ dose.persian_name || dose.name }}</td>
                <td class="border border-gray-300 px-3 py-2 text-center">{{ dose.dose_g_per_liter }} g/L</td>
                <td class="border border-gray-300 px-3 py-2 text-center">{{ formatNumber(dose.dose_g_for_tank) }} گرم</td>
                <td class="border border-gray-300 px-3 py-2 text-center">{{ dose.stock_200x_g_per_liter ? dose.stock_200x_g_per_liter + ' g/L' : '---' }}</td>
                <td class="border border-gray-300 px-3 py-2 text-xs text-gray-500">{{ getFertilizerDescription(dose.name) }}</td>
               </tr>
            </tbody>
           </table>
        </div>

        <!-- EC و pH -->
        <div class="grid grid-cols-2 gap-3 mb-4">
          <div class="bg-blue-50 rounded-lg p-3 text-center">
            <span class="font-bold text-blue-700">📊 EC پیش‌بینی شده:</span>
            <span class="text-blue-700 font-bold mx-2">{{ result.tank_main_result.target_ec || '---' }} mS/cm</span>
            <span class="text-xs text-gray-500">(هدف: 1.2 - 2.0)</span>
          </div>
          <div class="bg-blue-50 rounded-lg p-3 text-center">
            <span class="font-bold text-blue-700">🧪 pH هدف:</span>
            <span class="text-blue-700 font-bold mx-2">{{ result.tank_main_result.target_ph || '5.8 - 6.2' }}</span>
          </div>
        </div>

        <!-- دستورالعمل اختلاط -->
        <details class="mt-3">
          <summary class="cursor-pointer text-blue-600 hover:text-blue-700 font-medium text-sm inline-flex items-center gap-1">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            مشاهده دستورالعمل اختلاط مخزن اصلی
          </summary>
          <div class="mt-3 p-4 bg-gray-100 rounded-lg text-sm whitespace-pre-line font-mono" v-html="formatInstructions(result.tank_main_result.mixing_instructions)"></div>
        </details>

        <!-- هشدارها -->
        <div v-if="result.tank_main_result.warnings && result.tank_main_result.warnings.length > 0" class="mt-4">
          <div v-for="(w, idx) in result.tank_main_result.warnings" :key="idx" class="text-xs text-amber-600 bg-amber-50 p-2 rounded-lg mb-1 flex items-start gap-2">
            <svg class="w-4 h-4 flex-shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            {{ w }}
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- مخزن کلسیم -->
    <!-- ============================================================ -->
    <div class="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden">
      <div class="bg-gradient-to-r from-amber-600 to-orange-600 px-5 py-3">
        <h3 class="text-white font-bold flex items-center justify-between">
          <span class="flex items-center gap-2">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
            مخزن کلسیم (کودهای حاوی کلسیم)
          </span>
          <span class="text-xs bg-white/20 px-2 py-1 rounded-full">{{ result.tank_calcium_result.tank_name }}</span>
        </h3>
      </div>
      
      <div class="p-5">
        <!-- جدول دوزها -->
        <div class="overflow-x-auto mb-4">
          <table class="w-full text-sm border-collapse">
            <thead>
              <tr class="bg-gray-100">
                <th class="border border-gray-300 px-3 py-2 text-right">نام کود</th>
                <th class="border border-gray-300 px-3 py-2 text-center">مصرف (g/L)</th>
                <th class="border border-gray-300 px-3 py-2 text-center">مجموع برای مخزن</th>
                <th class="border border-gray-300 px-3 py-2 text-center">محلول مادر 200x</th>
                <th class="border border-gray-300 px-3 py-2 text-center">توضیحات</th>
               </tr>
            </thead>
            <tbody>
              <tr v-for="dose in result.tank_calcium_result.doses" :key="dose.name" class="hover:bg-gray-50">
                <td class="border border-gray-300 px-3 py-2 font-medium">{{ dose.persian_name || dose.name }}</td>
                <td class="border border-gray-300 px-3 py-2 text-center">{{ dose.dose_g_per_liter }} g/L</td>
                <td class="border border-gray-300 px-3 py-2 text-center">{{ formatNumber(dose.dose_g_for_tank) }} گرم</td>
                <td class="border border-gray-300 px-3 py-2 text-center">{{ dose.stock_200x_g_per_liter ? dose.stock_200x_g_per_liter + ' g/L' : '---' }}</td>
                <td class="border border-gray-300 px-3 py-2 text-xs text-gray-500">{{ getFertilizerDescription(dose.name) }}</td>
               </tr>
            </tbody>
           </table>
        </div>

        <!-- EC و pH -->
        <div class="grid grid-cols-2 gap-3 mb-4">
          <div class="bg-amber-50 rounded-lg p-3 text-center">
            <span class="font-bold text-amber-700">📊 EC پیش‌بینی شده:</span>
            <span class="text-amber-700 font-bold mx-2">{{ result.tank_calcium_result.target_ec || '---' }} mS/cm</span>
            <span class="text-xs text-gray-500">(هدف: 1.2 - 2.0)</span>
          </div>
          <div class="bg-amber-50 rounded-lg p-3 text-center">
            <span class="font-bold text-amber-700">🧪 pH هدف:</span>
            <span class="text-amber-700 font-bold mx-2">{{ result.tank_calcium_result.target_ph || '6.0 - 6.5' }}</span>
          </div>
        </div>

        <!-- دستورالعمل اختلاط -->
        <details class="mt-3">
          <summary class="cursor-pointer text-amber-600 hover:text-amber-700 font-medium text-sm inline-flex items-center gap-1">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            مشاهده دستورالعمل اختلاط مخزن کلسیم
          </summary>
          <div class="mt-3 p-4 bg-gray-100 rounded-lg text-sm whitespace-pre-line font-mono" v-html="formatInstructions(result.tank_calcium_result.mixing_instructions)"></div>
        </details>

        <!-- هشدارها -->
        <div v-if="result.tank_calcium_result.warnings && result.tank_calcium_result.warnings.length > 0" class="mt-4">
          <div v-for="(w, idx) in result.tank_calcium_result.warnings" :key="idx" class="text-xs text-amber-600 bg-amber-50 p-2 rounded-lg mb-1 flex items-start gap-2">
            <svg class="w-4 h-4 flex-shrink-0 mt-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            {{ w }}
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================ -->
    <!-- دستورالعمل کلی -->
    <!-- ============================================================ -->
    <div class="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden">
      <div class="bg-gradient-to-r from-green-600 to-teal-600 px-5 py-3">
        <h3 class="text-white font-bold flex items-center gap-2">
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          دستورالعمل کلی استفاده از دو مخزن
        </h3>
      </div>
      <div class="p-5">
        <details open>
          <summary class="cursor-pointer text-green-600 hover:text-green-700 font-medium text-sm inline-flex items-center gap-1">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            نمایش دستورالعمل کامل
          </summary>
          <div class="mt-3 p-4 bg-green-50 rounded-lg text-sm whitespace-pre-line font-mono" v-html="formatInstructions(result.general_mixing_instructions)"></div>
        </details>
      </div>
    </div>

    <!-- زمان محاسبه -->
    <div class="text-center text-xs text-gray-400 pt-4 border-t border-gray-100">
      <svg class="w-4 h-4 inline ml-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      زمان محاسبه: {{ result.calculation_time_ms?.toFixed(0) || '0' }} میلی‌ثانیه
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  result: any
}>()

const formatNumber = (num: number) => {
  if (!num && num !== 0) return '0'
  return new Intl.NumberFormat('fa-IR').format(Math.round(num))
}

const formatInstructions = (text: string) => {
  if (!text) return ''
  return text.replace(/\n/g, '<br>').replace(/\*/g, '•')
}

const getElementName = (element: string) => {
  const names: Record<string, string> = {
    'N': 'نیتروژن (N)',
    'P': 'فسفر (P)',
    'K': 'پتاسیم (K)',
    'Ca': 'کلسیم (Ca)',
    'Mg': 'منیزیم (Mg)',
    'S': 'گوگرد (S)',
    'Fe': 'آهن (Fe)',
    'Zn': 'روی (Zn)',
    'Mn': 'منگنز (Mn)',
    'Cu': 'مس (Cu)',
    'B': 'بُر (B)',
    'Mo': 'مولیبدن (Mo)',
    'Cl': 'کلر (Cl)'
  }
  return names[element] || element
}

const getFertilizerDescription = (name: string) => {
  const descriptions: Record<string, string> = {
    'نیترات کلسیم': 'منبع کلسیم و نیتروژن - برای رشد ساختار گیاه',
    'سولفات منیزیم': 'منبع منیزیم و گوگرد - برای کلروفیل و آنزیم‌ها',
    'سولفات پتاسیم': 'منبع پتاسیم و گوگرد - برای کیفیت میوه',
    'کلات آهن': 'منبع آهن - برای جلوگیری از زردی برگ',
    'فرتی‌گل 20-20-20': 'کود کامل NPK - مناسب برای رشد عمومی',
    'فرتی‌گل 36-12-12': 'کود NPK با پتاسیم بالا - مناسب برای میوه‌دهی',
    'فرتی‌گل 10-50-10': 'کود NPK با فسفر بالا - مناسب برای ریشه‌زایی و گلدهی',
    'فرتی‌گل 30-5-15': 'کود NPK با نیتروژن بالا - مناسب برای رشد رویشی',
    'یونی کمپلکس پودری': 'کود کامل ریز مغذی‌ها - برای تامین عناصر کم مصرف'
  }
  return descriptions[name] || 'کود مغذی برای تامین عناصر مورد نیاز گیاه'
}

// محاسبه مقایسه عناصر
const nutrientComparison = computed(() => {
  const elements = ['N', 'P', 'K', 'Ca', 'Mg', 'Fe', 'Zn', 'Mn', 'B']
  const needs = props.result.target_needs || {}
  const suppliedMain = props.result.tank_main_result?.supplied_ppm || {}
  const suppliedCalcium = props.result.tank_calcium_result?.supplied_ppm || {}
  
  return elements.map(elem => {
    const need = needs[elem] || 0
    const supplied = (suppliedMain[elem] || 0) + (suppliedCalcium[elem] || 0)
    let status = 'ok'
    if (need > 0) {
      const ratio = supplied / need
      if (ratio < 0.7) status = 'critical'
      else if (ratio < 0.9) status = 'low'
      else status = 'ok'
    }
    return { element: elem, need, supplied, status }
  })
})
</script>

<style scoped>
details summary {
  list-style: none;
  cursor: pointer;
}

details summary::-webkit-details-marker {
  display: none;
}

details summary::before {
  content: '📂 ';
  font-size: 14px;
}

details[open] summary::before {
  content: '📁 ';
}

@media print {
  .bg-white {
    break-inside: avoid;
    page-break-inside: avoid;
  }
  
  details {
    display: block !important;
  }
  
  details summary {
    display: block !important;
  }
  
  details[open] summary::before {
    content: '📁 ';
  }
}
</style>