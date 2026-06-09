<!-- Platform-v3\frontend\src\views\CalculatorView.vue -->

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-100 sticky top-0 z-10 no-print">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 py-4">
        <div class="flex justify-between items-center">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-800">FarmTech</h1>
              <p class="text-xs text-gray-500">سیستم هوشمند نسخه‌دهی کود</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <div :class="['w-2 h-2 rounded-full', connectionStatus === 'connected' ? 'bg-green-500' : 'bg-red-500']"></div>
            <span class="text-xs text-gray-500">{{ connectionStatus === 'connected' ? 'متصل به سرور' : 'قطع ارتباط با سرور' }}</span>
            <button v-if="result" @click="printResult" class="px-3 py-1 text-sm text-gray-600 hover:text-green-600 border border-gray-200 rounded-lg transition">
              🖨️ پرینت
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
      <!-- Form Card -->
      <div class="bg-white rounded-2xl shadow-card border border-gray-100 overflow-hidden">
        <div class="px-6 py-5 border-b border-gray-100">
          <h2 class="text-lg font-semibold text-gray-800">اطلاعات محاسبه</h2>
          <p class="text-sm text-gray-500 mt-0.5">لطفاً اطلاعات مورد نیاز را وارد کنید</p>
        </div>

        <div class="p-6 space-y-6">
          <!-- Crop and Variety -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">🌾 محصول</label>
              <select v-model="selectedCrop" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl" disabled>
                <option value="توت‌فرنگی">توت‌فرنگی</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">🍓 رقم گیاه</label>
              <select v-model="selectedVariety" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:border-green-500 focus:ring-1 focus:ring-green-500 transition">
                <option value="">انتخاب کنید</option>
                <option value="سن اندرسا">سن اندرسا</option>
                <option value="کاماروسا">کاماروسا</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">📈 مرحله رشد</label>
              <select v-model="selectedStage" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:border-green-500 focus:ring-1 focus:ring-green-500 transition">
                <option value="">انتخاب کنید</option>
                <option value="استقرار نشاء">🌱 استقرار نشاء</option>
                <option value="ریشه‌زایی">🌿 ریشه‌زایی</option>
                <option value="رشد رویشی">🍃 رشد رویشی</option>
                <option value="گلدهی">🌸 گلدهی</option>
                <option value="میوه‌دهی">🍓 میوه‌دهی</option>
              </select>
            </div>
          </div>

          <!-- Brand Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">🏭 فیلتر برند</label>
            <select v-model="selectedBrand" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:border-green-500 focus:ring-1 focus:ring-green-500 transition">
              <option value="">همه برندها</option>
              <option value="گل سم گرگان">گل سم گرگان</option>
              <option value="رازاک شیمی">رازاک شیمی</option>
            </select>
          </div>

          <!-- Tanks -->
          <div>
            <div class="flex justify-between items-center mb-3">
              <label class="text-sm font-medium text-gray-700">🗄️ مخازن</label>
              <button @click="openTankModal" class="text-sm text-green-600 hover:text-green-700 flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                افزودن مخزن
              </button>
            </div>

            <div v-if="tanks.length === 0" class="bg-gray-50 rounded-xl p-8 text-center border border-dashed border-gray-200">
              <svg class="w-12 h-12 mx-auto text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M6 14h12M5 6h14a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2z" />
              </svg>
              <p class="text-gray-500 text-sm">هیچ مخزنی تعریف نشده است</p>
              <button @click="openTankModal" class="mt-3 text-green-600 text-sm">+ افزودن مخزن جدید</button>
            </div>

            <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              <div
                v-for="tank in tanks"
                :key="tank.id"
                @click="selectTank(tank)"
                :class="[
                  'border rounded-xl p-4 cursor-pointer transition-all',
                  selectedTank?.id === tank.id
                    ? 'border-green-500 bg-green-50 ring-2 ring-green-200'
                    : 'border-gray-200 hover:border-gray-300 hover:shadow-soft bg-white'
                ]"
              >
                <div class="flex justify-between items-start">
                  <div>
                    <h4 class="font-medium text-gray-800">{{ tank.name }}</h4>
                    <p class="text-xs text-gray-500 mt-1">{{ tank.volume_liters }} لیتر</p>
                  </div>
                  <button @click.stop="deleteTank(tank.id)" class="text-gray-400 hover:text-red-500 transition">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
                <div class="mt-2 text-xs text-gray-400">
                  <span v-if="tank.water_ec_ms_cm !== null && tank.water_ec_ms_cm !== undefined">EC: {{ tank.water_ec_ms_cm }} | </span>
                  <span v-if="tank.water_ph !== null && tank.water_ph !== undefined">pH: {{ tank.water_ph }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Water Parameters -->
          <div v-if="selectedTank" class="p-4 bg-blue-50 rounded-xl border border-blue-100">
            <h4 class="text-sm font-medium text-blue-800 mb-3 flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
              </svg>
              پارامترهای آب مخزن {{ selectedTank.name }}
            </h4>
            <p class="text-xs text-blue-600 mb-3">لطفاً مقادیر اندازه‌گیری شده با دستگاه EC و pH متر را وارد کنید</p>
            <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">EC آب (mS/cm)</label>
                <input type="number" step="0.1" min="0" max="10" v-model.number="tempWaterEc" class="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:border-blue-500" placeholder="0.8">
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">pH آب</label>
                <input type="number" step="0.1" min="0" max="14" v-model.number="tempWaterPh" class="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:border-blue-500" placeholder="7.0">
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">بیکربنات HCO₃ (ppm)</label>
                <input type="number" min="0" v-model.number="tempWaterHco3" class="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm" placeholder="0">
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">کلسیم (ppm)</label>
                <input type="number" min="0" v-model.number="tempWaterCa" class="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm" placeholder="40">
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">منیزیم (ppm)</label>
                <input type="number" min="0" v-model.number="tempWaterMg" class="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm" placeholder="15">
              </div>
            </div>
          </div>

          <!-- Calculate Button -->
          <button
            @click="calculate"
            :disabled="isLoading || !selectedVariety || !selectedStage || !selectedTank"
            class="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium py-3 rounded-xl transition-all duration-200 flex items-center justify-center gap-2"
          >
            <svg v-if="isLoading" class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            {{ isLoading ? 'در حال محاسبه...' : 'محاسبه ترکیب بهینه' }}
          </button>
        </div>
      </div>

      <!-- Errors -->
      <div v-if="validationErrors.length > 0" class="mt-6 bg-red-50 border border-red-200 rounded-xl p-4">
        <div class="flex gap-3">
          <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div class="flex-1">
            <h4 class="text-sm font-bold text-red-800">خطاهای اعتبارسنجی</h4>
            <ul class="mt-1 text-sm text-red-700 list-disc list-inside">
              <li v-for="(err, idx) in validationErrors" :key="idx">{{ err }}</li>
            </ul>
          </div>
          <button @click="validationErrors = []" class="text-red-400 hover:text-red-600">✕</button>
        </div>
      </div>

      <div v-if="errorMessage" class="mt-6 bg-red-50 border border-red-200 rounded-xl p-4">
        <div class="flex gap-3">
          <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="text-sm text-red-700">{{ errorMessage }}</p>
          <button @click="errorMessage = ''" class="mr-auto text-red-400 hover:text-red-600">✕</button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="mt-8 flex justify-center">
        <div class="bg-white rounded-xl shadow-card px-6 py-4 flex items-center gap-3">
          <div class="w-5 h-5 border-2 border-green-500 border-t-transparent rounded-full animate-spin"></div>
          <span class="text-gray-600">در حال محاسبه...</span>
        </div>
      </div>

      <!-- Results -->
      <div v-if="result" class="mt-8">
        <ResultsDisplay :result="result" />
      </div>
    </main>

    <!-- Add Tank Modal -->
    <div v-if="showTankModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" @click.self="showTankModal = false">
      <div class="bg-white rounded-2xl max-w-md w-full shadow-xl">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
          <h3 class="text-lg font-semibold text-gray-800">افزودن مخزن جدید</h3>
          <button @click="showTankModal = false" class="text-gray-400 hover:text-gray-600">✕</button>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">نام مخزن</label>
            <input v-model="newTankName" placeholder="مثال: مخزن A" class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:border-green-500">
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">حجم (لیتر)</label>
            <input type="number" min="1" v-model.number="newTankVolume" placeholder="1000" class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:border-green-500">
          </div>
          <p class="text-xs text-blue-600 mt-2">⚠️ پارامترهای EC و pH آب را بعد از انتخاب مخزن می‌توانید وارد کنید</p>
        </div>
        <div class="px-6 py-4 bg-gray-50 rounded-b-2xl flex gap-3">
          <button @click="addTank" class="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg transition">افزودن</button>
          <button @click="showTankModal = false" class="flex-1 border border-gray-200 hover:bg-gray-50 py-2 rounded-lg transition">انصراف</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import ResultsDisplay from '../components/calculator/ResultsDisplay.vue'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  timeout: 30000
})

// Connection Status
const connectionStatus = ref('checking')

// Form State
const selectedCrop = ref('توت‌فرنگی')
const selectedVariety = ref('')
const selectedStage = ref('')
const selectedBrand = ref('')

// Tanks
const tanks = ref<any[]>([])
const selectedTank = ref<any>(null)
const showTankModal = ref(false)
const isLoading = ref(false)
const result = ref<any>(null)
const errorMessage = ref('')
const validationErrors = ref<string[]>([])

// Temporary water parameters
const tempWaterEc = ref<number | null>(null)
const tempWaterPh = ref<number | null>(null)
const tempWaterHco3 = ref<number>(0)
const tempWaterCa = ref<number>(0)
const tempWaterMg = ref<number>(0)

// New tank data
const newTankName = ref('')
const newTankVolume = ref(1000)

onMounted(async () => {
  await checkConnection()
  await loadTanks()
})

const checkConnection = async () => {
  try {
    await api.get('/health')
    connectionStatus.value = 'connected'
  } catch (err) {
    connectionStatus.value = 'disconnected'
    errorMessage.value = 'خطا در اتصال به سرور. لطفاً سرور بک‌اند را بررسی کنید.'
  }
}

const loadTanks = async () => {
  try {
    const response = await api.get('/tanks')
    tanks.value = response.data
  } catch (err) {
    console.error('Error loading tanks:', err)
  }
}

const openTankModal = () => {
  newTankName.value = ''
  newTankVolume.value = 1000
  showTankModal.value = true
}

const addTank = async () => {
  validationErrors.value = []

  if (!newTankName.value || newTankName.value.trim() === '') {
    validationErrors.value.push('نام مخزن اجباری است')
    return
  }

  if (!newTankVolume.value || newTankVolume.value <= 0) {
    validationErrors.value.push('حجم مخزن باید بزرگتر از 0 باشد')
    return
  }

  try {
    const response = await api.post('/tanks', {
      name: newTankName.value,
      volume_liters: newTankVolume.value,
      water_ec_ms_cm: null,
      water_ph: null,
      water_ca_ppm: 0,
      water_mg_ppm: 0,
      water_na_ppm: 0,
      water_cl_ppm: 0,
      water_so4_ppm: 0,
      water_hco3_ppm: 0,
      water_no3_ppm: 0,
      water_fe_ppm: 0
    })
    tanks.value.push(response.data)
    showTankModal.value = false
    errorMessage.value = ''
    validationErrors.value = []
  } catch (err: any) {
    console.error('Error creating tank:', err)
    if (err.response?.data?.detail) {
      if (typeof err.response.data.detail === 'string') {
        errorMessage.value = err.response.data.detail
      } else if (Array.isArray(err.response.data.detail)) {
        validationErrors.value = err.response.data.detail.map((e: any) => `${e.loc.join('.')}: ${e.msg}`)
      } else {
        errorMessage.value = 'خطا در ایجاد مخزن'
      }
    } else {
      errorMessage.value = 'خطا در ارتباط با سرور'
    }
  }
}

const deleteTank = async (tankId: number) => {
  if (!confirm('آیا از حذف این مخزن مطمئن هستید؟')) return

  try {
    await api.delete(`/tanks/${tankId}`)
    tanks.value = tanks.value.filter(t => t.id !== tankId)
    if (selectedTank.value?.id === tankId) {
      selectedTank.value = null
      resetTempParams()
    }
    errorMessage.value = ''
  } catch (err) {
    console.error('Error deleting tank:', err)
    errorMessage.value = 'خطا در حذف مخزن'
  }
}

const selectTank = (tank: any) => {
  selectedTank.value = tank
  resetTempParams()
}

const resetTempParams = () => {
  tempWaterEc.value = null
  tempWaterPh.value = null
  tempWaterHco3.value = 0
  tempWaterCa.value = 0
  tempWaterMg.value = 0
}

const calculate = async () => {
  validationErrors.value = []

  if (!selectedVariety.value) {
    validationErrors.value.push('لطفاً رقم گیاه را انتخاب کنید')
  }
  if (!selectedStage.value) {
    validationErrors.value.push('لطفاً مرحله رشد را انتخاب کنید')
  }
  if (!selectedTank.value) {
    validationErrors.value.push('لطفاً یک مخزن را انتخاب کنید')
  }

  if (validationErrors.value.length > 0) {
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  result.value = null

  try {
    const response = await api.post('/calculate', {
      crop_name: selectedCrop.value,
      variety_name: selectedVariety.value,
      stage_name: selectedStage.value,
      brand_filter: selectedBrand.value || null,
      tank_id: selectedTank.value.id,
      tank: {
        name: selectedTank.value.name,
        volume_liters: selectedTank.value.volume_liters,
        water_ec_ms_cm: tempWaterEc.value,
        water_ph: tempWaterPh.value,
        water_hco3_ppm: tempWaterHco3.value || 0,
        water_ca_ppm: tempWaterCa.value || 0,
        water_mg_ppm: tempWaterMg.value || 0,
        water_na_ppm: 0,
        water_cl_ppm: 0,
        water_so4_ppm: 0,
        water_no3_ppm: 0,
        water_fe_ppm: 0
      }
    })
    result.value = response.data
    errorMessage.value = ''
  } catch (err: any) {
    console.error('Calculation error:', err)
    if (err.response?.data?.detail) {
      if (typeof err.response.data.detail === 'string') {
        errorMessage.value = err.response.data.detail
      } else if (Array.isArray(err.response.data.detail)) {
        validationErrors.value = err.response.data.detail.map((e: any) => `${e.loc.join('.')}: ${e.msg}`)
      } else {
        errorMessage.value = JSON.stringify(err.response.data.detail)
      }
    } else {
      errorMessage.value = 'خطا در محاسبه. لطفاً دوباره تلاش کنید.'
    }
  } finally {
    isLoading.value = false
  }
}

const printResult = () => {
  window.print()
}
</script>
