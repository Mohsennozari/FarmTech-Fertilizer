<!-- Platform-v3\frontend\src\components\admin\FertilizerList.vue -->

<template>
  <div class="bg-white rounded-2xl shadow-card border border-gray-100 overflow-hidden">
    <!-- Header -->
    <div class="px-6 py-4 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-gray-100">
      <div class="flex justify-between items-center flex-wrap gap-2">
        <div>
          <div class="flex items-center gap-2">
            <svg class="w-6 h-6 text-green-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 7h-4.18A3 3 0 0016 5.18V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v1.18A3 3 0 008.18 7H4a2 2 0 00-2 2v4a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z" />
              <path d="M12 12v4m0 0l-2-2m2 2l2-2" />
              <path d="M4 15v4a2 2 0 002 2h12a2 2 0 002-2v-4" />
            </svg>
            <h2 class="text-lg font-semibold text-gray-800">📋 لیست کودهای موجود در دیتابیس</h2>
          </div>
          <p class="text-xs text-gray-500 mt-1">
            تعداد کل: <span class="font-bold text-green-600">{{ fertilizers.length }}</span> کود
            <span v-if="filteredFertilizers.length !== fertilizers.length" class="mr-2">
              | نمایش: <span class="font-bold text-blue-600">{{ filteredFertilizers.length }}</span> کود
            </span>
          </p>
        </div>
        <div class="flex gap-2 flex-wrap">
          <div class="relative">
            <svg class="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="جستجو..." 
              class="pr-9 pl-3 py-1.5 text-sm border border-gray-200 rounded-lg focus:border-green-500 w-48"
            >
          </div>
          <select v-model="typeFilter" class="px-3 py-1.5 text-sm border border-gray-200 rounded-lg focus:border-green-500">
            <option value="">همه انواع</option>
            <option value="NPK">NPK (کودهای کامل)</option>
            <option value="تک عنصری">تک عنصری</option>
            <option value="ریزمغذی">ریزمغذی</option>
            <option value="محرک رشد">محرک رشد</option>
          </select>
          <select v-model="brandFilter" class="px-3 py-1.5 text-sm border border-gray-200 rounded-lg focus:border-green-500">
            <option value="">همه برندها</option>
            <option v-for="brand in uniqueBrands" :key="brand" :value="brand">{{ brand }}</option>
          </select>
          <button @click="fetchFertilizers" class="px-3 py-1.5 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 transition flex items-center gap-1">
            <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            بروزرسانی
          </button>
        </div>
      </div>
    </div>
    
    <!-- آمار خلاصه -->
    <div class="px-6 py-3 bg-gray-50 border-b border-gray-100 flex flex-wrap gap-4 text-sm">
      <div class="flex items-center gap-2">
        <span class="w-3 h-3 rounded-full bg-green-500"></span>
        <span>NPK: <span class="font-bold">{{ getCountByType('NPK') }}</span></span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-3 h-3 rounded-full bg-blue-500"></span>
        <span>تک عنصری: <span class="font-bold">{{ getCountByType('تک عنصری') }}</span></span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-3 h-3 rounded-full bg-purple-500"></span>
        <span>ریزمغذی: <span class="font-bold">{{ getCountByType('ریزمغذی') }}</span></span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-3 h-3 rounded-full bg-amber-500"></span>
        <span>محرک رشد: <span class="font-bold">{{ getCountByType('محرک رشد') }}</span></span>
      </div>
    </div>
    
    <!-- جدول اصلی -->
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-right">نام کود</th>
            <th class="px-4 py-3 text-right">برند</th>
            <th class="px-4 py-3 text-center">نوع</th>
            <th class="px-4 py-3 text-center">فرم</th>
            <th class="px-4 py-3 text-center bg-green-50">N</th>
            <th class="px-4 py-3 text-center bg-green-50">P</th>
            <th class="px-4 py-3 text-center bg-green-50">K</th>
            <th class="px-4 py-3 text-center bg-blue-50">Ca</th>
            <th class="px-4 py-3 text-center bg-blue-50">Mg</th>
            <th class="px-4 py-3 text-center bg-blue-50">S</th>
            <th class="px-4 py-3 text-center">ریزمغذی‌ها</th>
            <th class="px-4 py-3 text-center">دوز مجاز</th>
            <th class="px-4 py-3 text-center">حلالیت</th>
            <th class="px-4 py-3 text-center">pH اثر</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="fert in filteredFertilizers" :key="fert.id" class="hover:bg-gray-50 transition cursor-pointer" @click="showDetail(fert)">
            <td class="px-4 py-3 font-medium text-gray-800">
              <div class="flex items-center gap-2">
                <span class="text-lg">{{ getFertilizerIcon(fert.fertilizer_type) }}</span>
                <span>{{ fert.name }}</span>
              </div>
              <div class="text-xs text-gray-400 mt-0.5">{{ fert.chemical_formula || 'فرمول نامشخص' }}</div>
            </td>
            <td class="px-4 py-3">
              <span class="text-gray-600">{{ fert.brand_name || '-' }}</span>
            </td>
            <td class="px-4 py-3 text-center">
              <span :class="getTypeClass(fert.fertilizer_type)" class="px-2 py-0.5 rounded-full text-xs">
                {{ getTypePersian(fert.fertilizer_type) }}
              </span>
            </td>
            <td class="px-4 py-3 text-center">
              <span :class="fert.fertilizer_form === 'liquid' ? 'text-blue-600' : 'text-gray-600'">
                {{ fert.fertilizer_form === 'liquid' ? 'مایع' : 'پودری' }}
              </span>
            </td>
            <td class="px-4 py-3 text-center font-mono">
              <span :class="getNutrientClass(fert.n_percent, 15)">{{ formatPercent(fert.n_percent) }}</span>
            </td>
            <td class="px-4 py-3 text-center font-mono">
              <span :class="getNutrientClass(fert.p_percent, 15)">{{ formatPercent(fert.p_percent) }}</span>
            </td>
            <td class="px-4 py-3 text-center font-mono">
              <span :class="getNutrientClass(fert.k_percent, 20)">{{ formatPercent(fert.k_percent) }}</span>
            </td>
            <td class="px-4 py-3 text-center font-mono">
              <span :class="getNutrientClass(fert.ca_percent, 10)">{{ formatPercent(fert.ca_percent) }}</span>
            </td>
            <td class="px-4 py-3 text-center font-mono">
              <span :class="getNutrientClass(fert.mg_percent, 5)">{{ formatPercent(fert.mg_percent) }}</span>
            </td>
            <td class="px-4 py-3 text-center font-mono">
              <span :class="getNutrientClass(fert.s_percent, 10)">{{ formatPercent(fert.s_percent) }}</span>
            </td>
            <td class="px-4 py-3 text-center">
              <div class="flex flex-wrap gap-1 justify-center">
                <span v-if="fert.fe_percent > 0" class="text-xs bg-gray-100 px-1.5 py-0.5 rounded-full" title="آهن">
                  Fe: {{ fert.fe_percent }}%
                </span>
                <span v-if="fert.zn_percent > 0" class="text-xs bg-gray-100 px-1.5 py-0.5 rounded-full" title="روی">
                  Zn: {{ fert.zn_percent }}%
                </span>
                <span v-if="fert.mn_percent > 0" class="text-xs bg-gray-100 px-1.5 py-0.5 rounded-full" title="منگنز">
                  Mn: {{ fert.mn_percent }}%
                </span>
                <span v-if="fert.cu_percent > 0" class="text-xs bg-gray-100 px-1.5 py-0.5 rounded-full" title="مس">
                  Cu: {{ fert.cu_percent }}%
                </span>
                <span v-if="fert.b_percent > 0" class="text-xs bg-gray-100 px-1.5 py-0.5 rounded-full" title="بُر">
                  B: {{ fert.b_percent }}%
                </span>
                <span v-if="fert.mo_percent > 0" class="text-xs bg-gray-100 px-1.5 py-0.5 rounded-full" title="مولیبدن">
                  Mo: {{ fert.mo_percent }}%
                </span>
                <span v-if="!hasMicros(fert)" class="text-xs text-gray-400">-</span>
              </div>
            </td>
            <td class="px-4 py-3 text-center">
              <div class="text-xs">
                <span class="font-mono">{{ fert.max_dose_g_per_liter ? fert.max_dose_g_per_liter + ' g/L' : '-' }}</span>
                <span v-if="fert.min_dose_g_per_liter" class="text-gray-400 block text-[10px]">
                  min: {{ fert.min_dose_g_per_liter }} g/L
                </span>
              </div>
            </td>
            <td class="px-4 py-3 text-center">
              <span class="text-xs font-mono">
                {{ fert.solubility_g_per_l ? fert.solubility_g_per_l + ' g/L' : '-' }}
              </span>
              <span v-if="fert.solubility_g_per_l && fert.solubility_g_per_l < 200" class="block text-[10px] text-amber-600">
                ⚠️ حلالیت محدود
              </span>
            </td>
            <td class="px-4 py-3 text-center">
              <span :class="getPhEffectClass(fert.ph_effect)" class="text-xs px-2 py-0.5 rounded-full">
                {{ getPhEffectPersian(fert.ph_effect) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- لودینگ -->
    <div v-if="isLoading" class="p-8 text-center">
      <div class="inline-block w-6 h-6 border-2 border-green-500 border-t-transparent rounded-full animate-spin"></div>
      <p class="text-gray-500 mt-2">در حال بارگذاری...</p>
    </div>
    
    <!-- بدون داده -->
    <div v-if="!isLoading && filteredFertilizers.length === 0" class="p-8 text-center">
      <svg class="w-16 h-16 mx-auto text-gray-300 mb-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M20 12H4M12 4v16" />
      </svg>
      <p class="text-gray-500">هیچ کودی یافت نشد</p>
    </div>
  </div>
  
  <!-- مودال جزئیات کود -->
  <div v-if="selectedFertilizer" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" @click.self="selectedFertilizer = null">
    <div class="bg-white rounded-2xl max-w-2xl w-full max-h-[85vh] overflow-hidden shadow-xl">
      <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gradient-to-r from-green-600 to-teal-600">
        <h3 class="text-lg font-semibold text-white flex items-center gap-2">
          <span class="text-xl">{{ getFertilizerIcon(selectedFertilizer.fertilizer_type) }}</span>
          {{ selectedFertilizer.name }}
        </h3>
        <button @click="selectedFertilizer = null" class="text-white hover:text-gray-200 text-xl">✕</button>
      </div>
      <div class="p-6 overflow-y-auto max-h-[calc(85vh-120px)] space-y-4">
        <!-- اطلاعات پایه -->
        <div class="grid grid-cols-2 gap-4">
          <div class="bg-gray-50 rounded-lg p-3">
            <div class="text-xs text-gray-500">برند</div>
            <div class="font-medium">{{ selectedFertilizer.brand_name || '-' }}</div>
          </div>
          <div class="bg-gray-50 rounded-lg p-3">
            <div class="text-xs text-gray-500">نوع کود</div>
            <div class="font-medium">{{ getTypePersian(selectedFertilizer.fertilizer_type) }}</div>
          </div>
          <div class="bg-gray-50 rounded-lg p-3">
            <div class="text-xs text-gray-500">فرم ظاهری</div>
            <div class="font-medium">{{ selectedFertilizer.fertilizer_form === 'liquid' ? 'مایع' : 'پودری' }}</div>
          </div>
          <div class="bg-gray-50 rounded-lg p-3">
            <div class="text-xs text-gray-500">فرمول شیمیایی</div>
            <div class="font-mono text-sm">{{ selectedFertilizer.chemical_formula || '-' }}</div>
          </div>
        </div>
        
        <!-- ترکیبات عناصر -->
        <div>
          <h4 class="font-semibold text-gray-800 mb-3 flex items-center gap-2">
            <svg class="w-5 h-5 text-green-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            ترکیبات عناصر (درصد وزنی)
          </h4>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
            <div class="bg-green-50 rounded-lg p-2 text-center">
              <div class="text-xs text-gray-500">نیتروژن (N)</div>
              <div class="font-bold text-green-700">{{ formatPercent(selectedFertilizer.n_percent) }}</div>
            </div>
            <div class="bg-green-50 rounded-lg p-2 text-center">
              <div class="text-xs text-gray-500">فسفر (P)</div>
              <div class="font-bold text-green-700">{{ formatPercent(selectedFertilizer.p_percent) }}</div>
            </div>
            <div class="bg-green-50 rounded-lg p-2 text-center">
              <div class="text-xs text-gray-500">پتاسیم (K)</div>
              <div class="font-bold text-green-700">{{ formatPercent(selectedFertilizer.k_percent) }}</div>
            </div>
            <div class="bg-blue-50 rounded-lg p-2 text-center">
              <div class="text-xs text-gray-500">کلسیم (Ca)</div>
              <div class="font-bold text-blue-700">{{ formatPercent(selectedFertilizer.ca_percent) }}</div>
            </div>
            <div class="bg-blue-50 rounded-lg p-2 text-center">
              <div class="text-xs text-gray-500">منیزیم (Mg)</div>
              <div class="font-bold text-blue-700">{{ formatPercent(selectedFertilizer.mg_percent) }}</div>
            </div>
            <div class="bg-blue-50 rounded-lg p-2 text-center">
              <div class="text-xs text-gray-500">گوگرد (S)</div>
              <div class="font-bold text-blue-700">{{ formatPercent(selectedFertilizer.s_percent) }}</div>
            </div>
          </div>
        </div>
        
        <!-- ریز مغذی‌ها -->
        <div v-if="hasMicros(selectedFertilizer)">
          <h4 class="font-semibold text-gray-800 mb-3 flex items-center gap-2">
            <svg class="w-5 h-5 text-purple-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 7h-4.18A3 3 0 0016 5.18V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v1.18A3 3 0 008.18 7H4a2 2 0 00-2 2v4a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z" />
            </svg>
            عناصر ریزمغذی
          </h4>
          <div class="flex flex-wrap gap-2">
            <span v-if="selectedFertilizer.fe_percent > 0" class="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm">آهن (Fe): {{ selectedFertilizer.fe_percent }}%</span>
            <span v-if="selectedFertilizer.zn_percent > 0" class="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm">روی (Zn): {{ selectedFertilizer.zn_percent }}%</span>
            <span v-if="selectedFertilizer.mn_percent > 0" class="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm">منگنز (Mn): {{ selectedFertilizer.mn_percent }}%</span>
            <span v-if="selectedFertilizer.cu_percent > 0" class="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm">مس (Cu): {{ selectedFertilizer.cu_percent }}%</span>
            <span v-if="selectedFertilizer.b_percent > 0" class="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm">بُر (B): {{ selectedFertilizer.b_percent }}%</span>
            <span v-if="selectedFertilizer.mo_percent > 0" class="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm">مولیبدن (Mo): {{ selectedFertilizer.mo_percent }}%</span>
          </div>
        </div>
        
        <!-- خواص فیزیکی و شیمیایی -->
        <div>
          <h4 class="font-semibold text-gray-800 mb-3 flex items-center gap-2">
            <svg class="w-5 h-5 text-amber-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
            خواص فیزیکی و شیمیایی
          </h4>
          <div class="grid grid-cols-2 gap-3">
            <div class="bg-amber-50 rounded-lg p-2">
              <div class="text-xs text-gray-500">حداکثر دوز مصرف</div>
              <div class="font-medium">{{ selectedFertilizer.max_dose_g_per_liter || '-' }} گرم در لیتر</div>
            </div>
            <div class="bg-amber-50 rounded-lg p-2">
              <div class="text-xs text-gray-500">حداقل دوز مصرف</div>
              <div class="font-medium">{{ selectedFertilizer.min_dose_g_per_liter || '-' }} گرم در لیتر</div>
            </div>
            <div class="bg-amber-50 rounded-lg p-2">
              <div class="text-xs text-gray-500">حلالیت در آب</div>
              <div class="font-medium">{{ selectedFertilizer.solubility_g_per_l || '-' }} گرم در لیتر</div>
              <div v-if="selectedFertilizer.solubility_g_per_l && selectedFertilizer.solubility_g_per_l < 200" class="text-xs text-amber-600 mt-1">⚠️ حلالیت محدود - محلول مادر غلیظ نسازید</div>
            </div>
            <div class="bg-amber-50 rounded-lg p-2">
              <div class="text-xs text-gray-500">اثر بر pH</div>
              <div class="font-medium">{{ getPhEffectPersian(selectedFertilizer.ph_effect) }}</div>
            </div>
          </div>
        </div>
        
        <!-- توضیحات -->
        <div v-if="selectedFertilizer.description" class="bg-gray-50 rounded-lg p-3">
          <div class="text-xs text-gray-500 mb-1">📝 توضیحات</div>
          <div class="text-sm whitespace-pre-line">{{ selectedFertilizer.description }}</div>
        </div>
        
        <!-- یادداشت‌ها -->
        <div v-if="selectedFertilizer.notes" class="bg-gray-50 rounded-lg p-3">
          <div class="text-xs text-gray-500 mb-1">📌 یادداشت‌ها</div>
          <div class="text-sm">{{ selectedFertilizer.notes }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  timeout: 30000
})

const fertilizers = ref<any[]>([])
const isLoading = ref(false)
const searchQuery = ref('')
const typeFilter = ref('')
const brandFilter = ref('')
const selectedFertilizer = ref<any>(null)

// برندهای یکتا
const uniqueBrands = computed(() => {
  const brands = new Set(fertilizers.value.map(f => f.brand_name).filter(Boolean))
  return Array.from(brands)
})

// فیلتر شده
const filteredFertilizers = computed(() => {
  let result = fertilizers.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(f => 
      f.name.toLowerCase().includes(query) || 
      (f.brand_name && f.brand_name.toLowerCase().includes(query))
    )
  }
  
  if (typeFilter.value) {
    result = result.filter(f => f.fertilizer_type === typeFilter.value)
  }
  
  if (brandFilter.value) {
    result = result.filter(f => f.brand_name === brandFilter.value)
  }
  
  return result
})

// آمار بر اساس نوع
const getCountByType = (type: string) => {
  return fertilizers.value.filter(f => f.fertilizer_type === type).length
}

// بررسی وجود ریز مغذی‌ها
const hasMicros = (fert: any) => {
  return fert.fe_percent > 0 || fert.zn_percent > 0 || fert.mn_percent > 0 || 
         fert.cu_percent > 0 || fert.b_percent > 0 || fert.mo_percent > 0
}

// فرمت درصد
const formatPercent = (value: number) => {
  if (!value && value !== 0) return '-'
  return value.toFixed(1) + '%'
}

// کلاس رنگی برای عناصر
const getNutrientClass = (value: number, threshold: number) => {
  if (!value || value === 0) return 'text-gray-400'
  if (value >= threshold) return 'text-green-600 font-bold'
  if (value >= threshold / 2) return 'text-blue-600'
  return 'text-gray-600'
}

// کلاس رنگی برای نوع کود
const getTypeClass = (type: string) => {
  switch(type) {
    case 'NPK': return 'bg-green-100 text-green-800'
    case 'تک عنصری': return 'bg-blue-100 text-blue-800'
    case 'ریزمغذی': return 'bg-purple-100 text-purple-800'
    case 'محرک رشد': return 'bg-amber-100 text-amber-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

// نام فارسی نوع کود
const getTypePersian = (type: string) => {
  switch(type) {
    case 'NPK': return 'NPK'
    case 'تک عنصری': return 'تک عنصری'
    case 'ریزمغذی': return 'ریزمغذی'
    case 'محرک رشد': return 'محرک رشد'
    default: return type || 'متفرقه'
  }
}

// آیکون برای نوع کود
const getFertilizerIcon = (type: string) => {
  switch(type) {
    case 'NPK': return '🧪'
    case 'تک عنصری': return '🔬'
    case 'ریزمغذی': return '✨'
    case 'محرک رشد': return '🌱'
    default: return '💊'
  }
}

// اثر بر pH
const getPhEffectPersian = (effect: string) => {
  switch(effect) {
    case 'اسیدی': return '🔻 اسیدی (کاهش pH)'
    case 'اسیدی ملایم': return '📉 اسیدی ملایم'
    case 'بازی ملایم': return '📈 بازی ملایم'
    case 'بازی': return '🔺 بازی (افزایش pH)'
    default: return '⚖️ خنثی'
  }
}

// کلاس اثر pH
const getPhEffectClass = (effect: string) => {
  switch(effect) {
    case 'اسیدی': return 'bg-red-100 text-red-800'
    case 'اسیدی ملایم': return 'bg-orange-100 text-orange-800'
    case 'بازی ملایم': return 'bg-blue-100 text-blue-800'
    case 'بازی': return 'bg-indigo-100 text-indigo-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

// دریافت کودها از API
const fetchFertilizers = async () => {
  isLoading.value = true
  try {
    const response = await api.get('/fertilizers')
    fertilizers.value = response.data
  } catch (err) {
    console.error('Error fetching fertilizers:', err)
  } finally {
    isLoading.value = false
  }
}

// نمایش جزئیات
const showDetail = (fert: any) => {
  selectedFertilizer.value = fert
}

onMounted(() => {
  fetchFertilizers()
})
</script>

<style scoped>
table {
  min-width: 1200px;
}

tr {
  transition: background-color 0.2s;
}
</style>