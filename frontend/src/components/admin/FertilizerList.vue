<!-- Platform-v3\frontend\src\components\admin\FertilizerList.vue -->

<template>
  <div class="bg-white rounded-2xl shadow-card border border-gray-100 overflow-hidden">
    <div class="px-6 py-4 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-gray-100">
      <div class="flex justify-between items-center flex-wrap gap-2">
        <div>
          <h2 class="text-lg font-semibold text-gray-800 flex items-center gap-2">
            <span class="text-xl">🧪</span>
            لیست کودهای موجود در دیتابیس
          </h2>
          <p class="text-xs text-gray-500 mt-1">تعداد کل: {{ fertilizers.length }} کود</p>
        </div>
        <div class="flex gap-2 flex-wrap">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="جستجو..." 
            class="px-3 py-1.5 text-sm border border-gray-200 rounded-lg focus:border-green-500"
          >
          <select v-model="typeFilter" class="px-3 py-1.5 text-sm border border-gray-200 rounded-lg">
            <option value="">همه انواع</option>
            <option value="NPK">NPK</option>
            <option value="تک عنصری">تک عنصری</option>
            <option value="ریزمغذی">ریزمغذی</option>
            <option value="آلی">آلی</option>
          </select>
          <button @click="fetchFertilizers" class="px-3 py-1.5 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700">
            🔄 بروزرسانی
          </button>
        </div>
      </div>
    </div>
    
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-right">نام کود</th>
            <th class="px-4 py-3 text-right">برند</th>
            <th class="px-4 py-3 text-center">نوع</th>
            <th class="px-4 py-3 text-center">فرم</th>
            <th class="px-4 py-3 text-center">N</th>
            <th class="px-4 py-3 text-center">P</th>
            <th class="px-4 py-3 text-center">K</th>
            <th class="px-4 py-3 text-center">Ca</th>
            <th class="px-4 py-3 text-center">Mg</th>
            <th class="px-4 py-3 text-center">S</th>
            <th class="px-4 py-3 text-center">ریزمغذی‌ها</th>
            <th class="px-4 py-3 text-center">حداکثر دوز</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="fert in filteredFertilizers" :key="fert.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 font-medium text-gray-800">{{ fert.name }}</td>
            <td class="px-4 py-3 text-gray-600">{{ fert.brand_name || '-' }}</td>
            <td class="px-4 py-3 text-center">
              <span :class="getTypeClass(fert.fertilizer_type)" class="px-2 py-0.5 rounded-full text-xs">
                {{ fert.fertilizer_type || '-' }}
              </span>
            </td>
            <td class="px-4 py-3 text-center">
              <span :class="fert.fertilizer_form === 'liquid' ? 'text-blue-600' : 'text-gray-600'">
                {{ fert.fertilizer_form === 'liquid' ? 'مایع' : 'پودری' }}
              </span>
            </td>
            <td class="px-4 py-3 text-center">{{ fert.n_percent || 0 }}%</td>
            <td class="px-4 py-3 text-center">{{ fert.p_percent || 0 }}%</td>
            <td class="px-4 py-3 text-center">{{ fert.k_percent || 0 }}%</td>
            <td class="px-4 py-3 text-center">{{ fert.ca_percent || 0 }}%</td>
            <td class="px-4 py-3 text-center">{{ fert.mg_percent || 0 }}%</td>
            <td class="px-4 py-3 text-center">{{ fert.s_percent || 0 }}%</td>
            <td class="px-4 py-3 text-center">
              <div class="flex flex-wrap gap-1 justify-center">
                <span v-if="fert.fe_percent > 0" class="text-xs bg-gray-100 px-1 rounded">Fe:{{ fert.fe_percent }}%</span>
                <span v-if="fert.zn_percent > 0" class="text-xs bg-gray-100 px-1 rounded">Zn:{{ fert.zn_percent }}%</span>
                <span v-if="fert.mn_percent > 0" class="text-xs bg-gray-100 px-1 rounded">Mn:{{ fert.mn_percent }}%</span>
                <span v-if="fert.cu_percent > 0" class="text-xs bg-gray-100 px-1 rounded">Cu:{{ fert.cu_percent }}%</span>
                <span v-if="fert.b_percent > 0" class="text-xs bg-gray-100 px-1 rounded">B:{{ fert.b_percent }}%</span>
                <span v-if="fert.mo_percent > 0" class="text-xs bg-gray-100 px-1 rounded">Mo:{{ fert.mo_percent }}%</span>
              </div>
            </td>
            <td class="px-4 py-3 text-center">
              <span class="text-xs">
                {{ fert.max_dose_g_per_liter ? fert.max_dose_g_per_liter + ' g/L' : '-' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div v-if="isLoading" class="p-8 text-center">
      <div class="inline-block w-6 h-6 border-2 border-green-500 border-t-transparent rounded-full animate-spin"></div>
      <p class="text-gray-500 mt-2">در حال بارگذاری...</p>
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

const filteredFertilizers = computed(() => {
  let result = fertilizers.value
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(f => f.name.toLowerCase().includes(query))
  }
  
  if (typeFilter.value) {
    result = result.filter(f => f.fertilizer_type === typeFilter.value)
  }
  
  return result
})

const getTypeClass = (type: string) => {
  switch(type) {
    case 'NPK': return 'bg-green-100 text-green-800'
    case 'تک عنصری': return 'bg-blue-100 text-blue-800'
    case 'ریزمغذی': return 'bg-purple-100 text-purple-800'
    case 'آلی': return 'bg-amber-100 text-amber-800'
    default: return 'bg-gray-100 text-gray-800'
  }
}

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

onMounted(() => {
  fetchFertilizers()
})
</script>