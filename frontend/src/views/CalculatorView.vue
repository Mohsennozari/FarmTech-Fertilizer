<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-100 sticky top-0 z-10 no-print">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 py-4">
        <div class="flex justify-between items-center">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-800">FarmTech</h1>
              <p class="text-xs text-gray-500">سیستم هوشمند نسخه‌دهی کود - دو مخزن</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <div :class="['w-2 h-2 rounded-full', connectionStatus === 'connected' ? 'bg-green-500' : 'bg-red-500']"></div>
            <span class="text-xs text-gray-500">{{ connectionStatus === 'connected' ? 'متصل به سرور' : 'قطع ارتباط با سرور' }}</span>
            <button @click="showFertilizerList = !showFertilizerList" class="px-3 py-1 text-sm text-gray-600 hover:text-green-600 border border-gray-200 rounded-lg transition">
              <svg class="w-4 h-4 inline ml-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              لیست کودها
            </button>
            <button v-if="result" @click="printResult" class="px-3 py-1 text-sm text-gray-600 hover:text-green-600 border border-gray-200 rounded-lg transition">
              <svg class="w-4 h-4 inline ml-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              پرینت
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Modal لیست کودها -->
    <div v-if="showFertilizerList" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" @click.self="showFertilizerList = false">
      <div class="bg-white rounded-2xl max-w-4xl w-full max-h-[80vh] overflow-hidden shadow-xl">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gradient-to-r from-green-600 to-teal-600">
          <h3 class="text-lg font-semibold text-white">📋 لیست کودهای موجود در دیتابیس</h3>
          <button @click="showFertilizerList = false" class="text-white hover:text-gray-200 text-xl">✕</button>
        </div>
        <div class="p-6 overflow-y-auto max-h-[calc(80vh-120px)]">
          <div v-if="isLoadingFertilizers" class="text-center py-8">
            <div class="inline-block w-8 h-8 border-2 border-green-500 border-t-transparent rounded-full animate-spin"></div>
            <p class="mt-2 text-gray-500">در حال بارگذاری...</p>
          </div>
          <div v-else-if="fertilizers.length === 0" class="text-center py-8 text-gray-500">
            هیچ کودی در دیتابیس یافت نشد
          </div>
          <div v-else class="space-y-3">
            <div v-for="fert in fertilizers" :key="fert.id" class="border border-gray-200 rounded-xl p-4 hover:shadow-md transition">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center gap-2 flex-wrap">
                    <h4 class="font-bold text-gray-800">{{ fert.persian_name || fert.name }}</h4>
                    <span class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">{{ fert.brand_name }}</span>
                    <span class="text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full">{{ fert.fertilizer_type }}</span>
                  </div>
                  <div class="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2 text-xs text-gray-500">
                    <span v-if="fert.n_percent">N: {{ fert.n_percent }}%</span>
                    <span v-if="fert.p_percent">P: {{ fert.p_percent }}%</span>
                    <span v-if="fert.k_percent">K: {{ fert.k_percent }}%</span>
                    <span v-if="fert.ca_percent">Ca: {{ fert.ca_percent }}%</span>
                    <span v-if="fert.mg_percent">Mg: {{ fert.mg_percent }}%</span>
                    <span v-if="fert.fe_percent">Fe: {{ fert.fe_percent }}%</span>
                    <span v-if="fert.zn_percent">Zn: {{ fert.zn_percent }}%</span>
                    <span v-if="fert.s_percent">S: {{ fert.s_percent }}%</span>
                  </div>
                  <p class="text-xs text-gray-400 mt-2">{{ getFertilizerDescription(fert.name) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

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
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                <svg class="w-4 h-4 inline ml-1 text-gray-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                </svg>
                محصول
              </label>
              <select v-model="selectedCrop" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl" disabled>
                <option value="توت‌فرنگی">توت‌فرنگی</option>
              </select>
              <p class="text-xs text-gray-400 mt-1">محصول انتخابی - توت فرنگی</p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                <svg class="w-4 h-4 inline ml-1 text-gray-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2zM12 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z" />
                  <path d="M20 12c0-4.418-3.582-8-8-8s-8 3.582-8 8 3.582 8 8 8 8-3.582 8-8z" />
                </svg>
                رقم گیاه
              </label>
              <select v-model="selectedVariety" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:border-green-500 focus:ring-1 focus:ring-green-500 transition">
                <option value="">انتخاب کنید</option>
                <option value="سن اندرسا">سن اندرسا</option>
                <option value="کاماروسا">کاماروسا</option>
              </select>
              <p class="text-xs text-gray-400 mt-1">رقم مورد نظر خود را انتخاب کنید</p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                <svg class="w-4 h-4 inline ml-1 text-gray-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
                مرحله رشد
              </label>
              <select v-model="selectedStage" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:border-green-500 focus:ring-1 focus:ring-green-500 transition">
                <option value="">انتخاب کنید</option>
                <option value="استقرار نشاء">استقرار نشاء</option>
                <option value="ریشه‌زایی">ریشه‌زایی</option>
                <option value="رشد رویشی">رشد رویشی</option>
                <option value="گلدهی">گلدهی</option>
                <option value="میوه‌دهی">میوه‌دهی</option>
              </select>
              <p class="text-xs text-gray-400 mt-1">مرحله رشدی گیاه را انتخاب کنید</p>
            </div>
          </div>

          <!-- Brand Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">
              <svg class="w-4 h-4 inline ml-1 text-gray-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2v16z" />
              </svg>
              فیلتر برند (اختیاری)
            </label>
            <select v-model="selectedBrand" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:border-green-500 focus:ring-1 focus:ring-green-500 transition">
              <option value="">همه برندها</option>
              <option value="گل سم گرگان">گل سم گرگان</option>
              <option value="رازاک شیمی">رازاک شیمی</option>
              <option value="گرین استار">گرین استار</option>
              <option value="زاگرا استار">زاگرا استار</option>
              <option value="اطلس">اطلس</option>
              <option value="ردسا">ردسا</option>
            </select>
            <p class="text-xs text-gray-400 mt-1">در صورت تمایل می‌توانید برند خاصی را فیلتر کنید</p>
          </div>

          <!-- ============================================================ -->
          <!-- مخزن اصلی -->
          <!-- ============================================================ -->
          <div class="border border-blue-200 rounded-xl overflow-hidden">
            <div class="bg-blue-50 px-4 py-3 border-b border-blue-200">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-blue-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
                <h3 class="font-semibold text-blue-800">مخزن اصلی (کودهای غیر کلسیمی)</h3>
              </div>
              <p class="text-xs text-blue-600 mt-1">این مخزن برای کودهای NPK، سولفات‌ها و ریز مغذی‌ها استفاده می‌شود</p>
            </div>
            <div class="p-4">
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <InputField
                  v-model="tankMain.name"
                  label="نام مخزن"
                  placeholder="مثال: مخزن اصلی"
                  icon="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
                  :required="true"
                />
                <InputField
                  v-model.number="tankMain.volume_liters"
                  label="حجم مخزن (لیتر)"
                  type="number"
                  placeholder="100"
                  icon="M4 20h16a2 2 0 002-2V8a2 2 0 00-2-2h-7.93a2 2 0 01-1.66-.9l-.82-1.2A2 2 0 007.93 3H4a2 2 0 00-2 2v13a2 2 0 002 2z"
                  :step="1"
                  :min="1"
                  :required="true"
                  help-text="حجم مخزن بر حسب لیتر - مقدار پیش‌فرض 100 لیتر"
                />
                <InputField
                  v-model.number="tankMain.water_ec_ms_cm"
                  label="EC آب (mS/cm)"
                  type="number"
                  placeholder="اختیاری"
                  icon="M13 10V3L4 14h7v7l9-11h-7z"
                  :step="0.1"
                  :min="0"
                  help-text="مقدار EC آب پایه - اختیاری"
                />
                <InputField
                  v-model.number="tankMain.water_ph"
                  label="pH آب"
                  type="number"
                  placeholder="اختیاری"
                  icon="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 6.34l-1.41-1.41M17.66 6.34l1.41-1.41"
                  :step="0.1"
                  :min="0"
                  :max="14"
                  help-text="pH آب پایه - اختیاری"
                />
                <InputField
                  v-model.number="tankMain.water_ca_ppm"
                  label="کلسیم آب (ppm)"
                  type="number"
                  placeholder="اختیاری"
                  icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2zM12 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z"
                  :step="1"
                  :min="0"
                  help-text="مقدار کلسیم موجود در آب - اختیاری"
                />
                <InputField
                  v-model.number="tankMain.water_mg_ppm"
                  label="منیزیم آب (ppm)"
                  type="number"
                  placeholder="اختیاری"
                  icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2zM12 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z"
                  :step="1"
                  :min="0"
                  help-text="مقدار منیزیم موجود در آب - اختیاری"
                />
                <InputField
                  v-model.number="tankMain.water_hco3_ppm"
                  label="بیکربنات (ppm)"
                  type="number"
                  placeholder="اختیاری"
                  icon="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  :step="1"
                  :min="0"
                  help-text="بیکربنات آب - اختیاری"
                />
                <InputField
                  v-model.number="tankMain.water_cl_ppm"
                  label="کلر آب (ppm)"
                  type="number"
                  placeholder="اختیاری"
                  icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z"
                  :step="1"
                  :min="0"
                  help-text="کلر آب - اختیاری"
                />
              </div>
            </div>
          </div>

          <!-- ============================================================ -->
          <!-- مخزن کلسیم -->
          <!-- ============================================================ -->
          <div class="border border-amber-200 rounded-xl overflow-hidden">
            <div class="bg-amber-50 px-4 py-3 border-b border-amber-200">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-amber-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
                <h3 class="font-semibold text-amber-800">مخزن کلسیم (کودهای حاوی کلسیم)</h3>
              </div>
              <p class="text-xs text-amber-600 mt-1">این مخزن فقط برای کودهای حاوی کلسیم مانند نیترات کلسیم و کلات آهن استفاده می‌شود</p>
            </div>
            <div class="p-4">
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <InputField
                  v-model="tankCalcium.name"
                  label="نام مخزن"
                  placeholder="مثال: مخزن کلسیم"
                  icon="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
                  :required="true"
                />
                <InputField
                  v-model.number="tankCalcium.volume_liters"
                  label="حجم مخزن (لیتر)"
                  type="number"
                  placeholder="100"
                  icon="M4 20h16a2 2 0 002-2V8a2 2 0 00-2-2h-7.93a2 2 0 01-1.66-.9l-.82-1.2A2 2 0 007.93 3H4a2 2 0 00-2 2v13a2 2 0 002 2z"
                  :step="1"
                  :min="1"
                  :required="true"
                  help-text="حجم مخزن بر حسب لیتر - مقدار پیش‌فرض 100 لیتر"
                />
                <InputField
                  v-model.number="tankCalcium.water_ec_ms_cm"
                  label="EC آب (mS/cm)"
                  type="number"
                  placeholder="اختیاری"
                  icon="M13 10V3L4 14h7v7l9-11h-7z"
                  :step="0.1"
                  :min="0"
                  help-text="مقدار EC آب پایه - اختیاری"
                />
                <InputField
                  v-model.number="tankCalcium.water_ph"
                  label="pH آب"
                  type="number"
                  placeholder="اختیاری"
                  icon="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 6.34l-1.41-1.41M17.66 6.34l1.41-1.41"
                  :step="0.1"
                  :min="0"
                  :max="14"
                  help-text="pH آب پایه - اختیاری"
                />
                <InputField
                  v-model.number="tankCalcium.water_ca_ppm"
                  label="کلسیم آب (ppm)"
                  type="number"
                  placeholder="اختیاری"
                  icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2zM12 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z"
                  :step="1"
                  :min="0"
                  help-text="مقدار کلسیم موجود در آب - اختیاری"
                />
                <InputField
                  v-model.number="tankCalcium.water_mg_ppm"
                  label="منیزیم آب (ppm)"
                  type="number"
                  placeholder="اختیاری"
                  icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2zM12 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z"
                  :step="1"
                  :min="0"
                  help-text="مقدار منیزیم موجود در آب - اختیاری"
                />
                <InputField
                  v-model.number="tankCalcium.water_hco3_ppm"
                  label="بیکربنات (ppm)"
                  type="number"
                  placeholder="اختیاری"
                  icon="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  :step="1"
                  :min="0"
                  help-text="بیکربنات آب - اختیاری"
                />
                <InputField
                  v-model.number="tankCalcium.water_cl_ppm"
                  label="کلر آب (ppm)"
                  type="number"
                  placeholder="اختیاری"
                  icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z"
                  :step="1"
                  :min="0"
                  help-text="کلر آب - اختیاری"
                />
              </div>
            </div>
          </div>

          <!-- ============================================================ -->
          <!-- تنظیمات سیستم استوک -->
          <!-- ============================================================ -->
          <div class="border border-purple-200 rounded-xl overflow-hidden">
            <div class="bg-purple-50 px-4 py-3 border-b border-purple-200">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-purple-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
                <h3 class="font-semibold text-purple-800">تنظیمات سیستم استوک (محلول مادر)</h3>
              </div>
              <p class="text-xs text-purple-600 mt-1">این تنظیمات برای محاسبه مقدار کود مورد نیاز برای ساخت استوک استفاده می‌شود</p>
            </div>
            <div class="p-4">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <InputField
                  v-model.number="stockTankVolume"
                  label="حجم مخزن استوک (لیتر)"
                  type="number"
                  placeholder="20"
                  icon="M4 20h16a2 2 0 002-2V8a2 2 0 00-2-2h-7.93a2 2 0 01-1.66-.9l-.82-1.2A2 2 0 007.93 3H4a2 2 0 00-2 2v13a2 2 0 002 2z"
                  :step="1"
                  :min="1"
                  :max="500"
                  help-text="ظرفی که محلول استوک در آن ساخته می‌شود - پیش‌فرض 20 لیتر"
                />
                <InputField
                  v-model.number="injectorRatio"
                  label="نسبت تزریق (1 : X)"
                  type="number"
                  placeholder="200"
                  icon="M13 10V3L4 14h7v7l9-11h-7z"
                  :step="10"
                  :min="50"
                  :max="1000"
                  help-text="مثال: 200 یعنی 1 لیتر استوک + 199 لیتر آب = 200 لیتر محلول نهایی"
                />
              </div>
              <div class="mt-3 text-xs text-gray-500 bg-gray-50 rounded-lg p-2">
                <span class="font-medium">💡 مفهوم نسبت تزریق:</span>
                <span> به ازای هر 1 لیتر استوک، {{ injectorRatio - 1 }} لیتر آب اضافه می‌شود تا {{ injectorRatio }} لیتر محلول نهایی بدست آید.</span>
              </div>
            </div>
          </div>

          <!-- Calculate Button -->
          <button
            @click="calculateDualTank"
            :disabled="isLoading || !selectedVariety || !selectedStage"
            class="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium py-3 rounded-xl transition-all duration-200 flex items-center justify-center gap-2"
          >
            <svg v-if="isLoading" class="w-5 h-5 animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            {{ isLoading ? 'در حال محاسبه...' : 'محاسبه ترکیب بهینه دو مخزن' }}
          </button>
        </div>
      </div>

      <!-- Errors -->
      <div v-if="validationErrors.length > 0" class="mt-6 bg-red-50 border border-red-200 rounded-xl p-4">
        <div class="flex gap-3">
          <svg class="w-5 h-5 text-red-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
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
          <svg class="w-5 h-5 text-red-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
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
        <ResultsDisplay 
          :result="result" 
          :stock-tank-volume="stockTankVolume"
          :injector-ratio="injectorRatio"
        />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import ResultsDisplay from '../components/calculator/ResultsDisplay.vue'
import InputField from '../components/common/InputField.vue'

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'

const connectionStatus = ref('checking')
const selectedCrop = ref('توت‌فرنگی')
const selectedVariety = ref('')
const selectedStage = ref('')
const selectedBrand = ref('')
const isLoading = ref(false)
const isLoadingFertilizers = ref(false)
const result = ref<any>(null)
const errorMessage = ref('')
const validationErrors = ref<string[]>([])
const showFertilizerList = ref(false)
const fertilizers = ref<any[]>([])

// ============================================================
// فیلدهای جدید سیستم استوک
// ============================================================
const stockTankVolume = ref(20)
const injectorRatio = ref(200)

// مخزن اصلی
const tankMain = ref({
  name: 'مخزن اصلی',
  tank_type: 'main',
  volume_liters: 100,
  water_ec_ms_cm: null as number | null,
  water_ph: null as number | null,
  water_ca_ppm: null as number | null,
  water_mg_ppm: null as number | null,
  water_hco3_ppm: null as number | null,
  water_cl_ppm: null as number | null,
  water_na_ppm: 0,
  water_so4_ppm: 0,
  water_no3_ppm: 0,
  water_fe_ppm: 0
})

// مخزن کلسیم
const tankCalcium = ref({
  name: 'مخزن کلسیم',
  tank_type: 'calcium',
  volume_liters: 100,
  water_ec_ms_cm: null as number | null,
  water_ph: null as number | null,
  water_ca_ppm: null as number | null,
  water_mg_ppm: null as number | null,
  water_hco3_ppm: null as number | null,
  water_cl_ppm: null as number | null,
  water_na_ppm: 0,
  water_so4_ppm: 0,
  water_no3_ppm: 0,
  water_fe_ppm: 0
})

const getFertilizerDescription = (name: string) => {
  const descriptions: Record<string, string> = {
    'نیترات کلسیم': 'منبع کلسیم و نیتروژن - برای رشد ساختار گیاه و جلوگیری از پوسیدگی گلگاه',
    'سولفات منیزیم': 'منبع منیزیم و گوگرد - برای تولید کلروفیل و فعالسازی آنزیم‌ها',
    'سولفات پتاسیم': 'منبع پتاسیم و گوگرد - برای کیفیت میوه و مقاومت به تنش',
    'کلات آهن': 'منبع آهن - برای جلوگیری از زردی برگ‌ها (کلروز)',
    'فرتی‌گل 20-20-20': 'کود کامل NPK متعادل - مناسب برای رشد عمومی و مراحل اولیه',
    'فرتی‌گل 36-12-12': 'کود NPK با پتاسیم بالا - مناسب برای میوه‌دهی و افزایش کیفیت',
    'فرتی‌گل 10-50-10': 'کود NPK با فسفر بالا - مناسب برای ریشه‌زایی و گلدهی',
    'فرتی‌گل 30-5-15': 'کود NPK با نیتروژن بالا - مناسب برای رشد رویشی',
    'یونی کمپلکس پودری': 'کود کامل ریز مغذی‌ها - برای تامین عناصر کم مصرف',
    'NPK 20-20-20 گرین استار': 'کود NPK متعادل - مناسب برای رشد عمومی',
    'NPK 12-12-36 گرین استار': 'کود NPK با پتاسیم بالا - مناسب برای میوه‌دهی',
    'NPK 10-52-10 زاگرا استار': 'کود NPK با فسفر بالا - مناسب برای ریشه‌زایی',
    'کلرید پتاسیم': 'منبع پتاسیم و کلر - برای تغذیه عمومی (در آب با کلر پایین)'
  }
  return descriptions[name] || 'کود مغذی برای تامین عناصر مورد نیاز گیاه'
}

const fetchFertilizers = async () => {
  isLoadingFertilizers.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/fertilizers`)
    fertilizers.value = response.data
  } catch (err) {
    console.error('Error fetching fertilizers:', err)
  } finally {
    isLoadingFertilizers.value = false
  }
}

const checkConnection = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`)
    if (response.data && response.data.status === 'ok') {
      connectionStatus.value = 'connected'
      console.log('Connected to server')
      await fetchFertilizers()
    } else {
      connectionStatus.value = 'disconnected'
      errorMessage.value = 'خطا در اتصال به سرور'
    }
  } catch (err: any) {
    console.error('Connection error:', err.message)
    connectionStatus.value = 'disconnected'
    errorMessage.value = 'خطا در اتصال به سرور. لطفاً سرور بک‌اند را بررسی کنید.'
  }
}

const calculateDualTank = async () => {
  validationErrors.value = []

  if (!selectedVariety.value) {
    validationErrors.value.push('لطفاً رقم گیاه را انتخاب کنید')
  }
  if (!selectedStage.value) {
    validationErrors.value.push('لطفاً مرحله رشد را انتخاب کنید')
  }
  
  // اعتبارسنجی حجم مخزن اصلی
  const mainVolume = Number(tankMain.value.volume_liters)
  if (isNaN(mainVolume) || mainVolume <= 0) {
    validationErrors.value.push('حجم مخزن اصلی معتبر نیست (باید عدد مثبت باشد)')
  }
  
  // اعتبارسنجی حجم مخزن کلسیم
  const calciumVolume = Number(tankCalcium.value.volume_liters)
  if (isNaN(calciumVolume) || calciumVolume <= 0) {
    validationErrors.value.push('حجم مخزن کلسیم معتبر نیست (باید عدد مثبت باشد)')
  }

  if (validationErrors.value.length > 0) {
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  result.value = null

  try {
    const payload = {
      crop_name: selectedCrop.value,
      variety_name: selectedVariety.value,
      stage_name: selectedStage.value,
      brand_filter: selectedBrand.value || null,
      tank_main: {
        name: tankMain.value.name,
        tank_type: tankMain.value.tank_type,
        volume_liters: mainVolume,
        water_ec_ms_cm: tankMain.value.water_ec_ms_cm,
        water_ph: tankMain.value.water_ph,
        water_ca_ppm: tankMain.value.water_ca_ppm || 0,
        water_mg_ppm: tankMain.value.water_mg_ppm || 0,
        water_hco3_ppm: tankMain.value.water_hco3_ppm || 0,
        water_cl_ppm: tankMain.value.water_cl_ppm || 0,
        water_na_ppm: tankMain.value.water_na_ppm || 0,
        water_so4_ppm: tankMain.value.water_so4_ppm || 0,
        water_no3_ppm: tankMain.value.water_no3_ppm || 0,
        water_fe_ppm: tankMain.value.water_fe_ppm || 0
      },
      tank_calcium: {
        name: tankCalcium.value.name,
        tank_type: tankCalcium.value.tank_type,
        volume_liters: calciumVolume,
        water_ec_ms_cm: tankCalcium.value.water_ec_ms_cm,
        water_ph: tankCalcium.value.water_ph,
        water_ca_ppm: tankCalcium.value.water_ca_ppm || 0,
        water_mg_ppm: tankCalcium.value.water_mg_ppm || 0,
        water_hco3_ppm: tankCalcium.value.water_hco3_ppm || 0,
        water_cl_ppm: tankCalcium.value.water_cl_ppm || 0,
        water_na_ppm: tankCalcium.value.water_na_ppm || 0,
        water_so4_ppm: tankCalcium.value.water_so4_ppm || 0,
        water_no3_ppm: tankCalcium.value.water_no3_ppm || 0,
        water_fe_ppm: tankCalcium.value.water_fe_ppm || 0
      },
      stock_tank_volume_liters: stockTankVolume.value,
      injector_ratio: injectorRatio.value
    }
    
    console.log('Sending request:', payload)
    const response = await axios.post(`${API_BASE_URL}/calculate-dual-tank`, payload)
    
    if (response.data.success) {
      result.value = response.data
      console.log('Calculation successful')
    } else {
      errorMessage.value = response.data.error_message || 'خطا در محاسبه'
    }
  } catch (err: any) {
    console.error('Calculation error:', err)
    if (err.response?.data?.detail) {
      if (typeof err.response.data.detail === 'string') {
        errorMessage.value = err.response.data.detail
      } else if (Array.isArray(err.response.data.detail)) {
        validationErrors.value = err.response.data.detail.map((e: any) => {
          if (e.msg === 'Input should be a valid number') {
            return 'لطفاً مقدار معتبر برای حجم مخزن وارد کنید'
          }
          return e.msg
        })
      } else {
        errorMessage.value = JSON.stringify(err.response.data.detail)
      }
    } else if (err.message === 'Network Error') {
      errorMessage.value = 'خطا در اتصال به سرور. لطفاً از اجرای سرور بک‌اند اطمینان حاصل کنید.'
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

onMounted(() => {
  checkConnection()
})
</script>

<style scoped>
@media print {
  .no-print {
    display: none !important;
  }
  
  header {
    display: none !important;
  }
  
  button {
    display: none !important;
  }
}
</style>