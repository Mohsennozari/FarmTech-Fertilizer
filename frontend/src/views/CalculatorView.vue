<!-- frontend/src/views/CalculatorView.vue -->

<template>
  <div class="min-h-screen bg-[var(--bg-primary)]">
    <!-- Header -->
    <header
      class="bg-[var(--bg-card)] border-b border-gray-100 sticky top-0 z-10 no-print"
    >
      <div class="max-w-6xl mx-auto px-4 sm:px-6 py-4">
        <div class="flex justify-between items-center">
          <div class="flex items-center gap-3">
            <div
              class="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center"
            >
              <svg
                class="w-5 h-5 text-white"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
                />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-800">FarmTech</h1>
              <p class="text-xs text-gray-500">
                سیستم هوشمند نسخه‌دهی کود - دو مخزن
              </p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <div
              :class="[
                'w-2 h-2 rounded-full',
                connectionStatus === 'connected'
                  ? 'bg-green-500'
                  : 'bg-red-500',
              ]"
            ></div>
            <span class="text-xs text-gray-500">{{
              connectionStatus === "connected"
                ? "متصل به سرور"
                : "قطع ارتباط با سرور"
            }}</span>
            <button
              @click="showFertilizerList = !showFertilizerList"
              class="px-3 py-1 text-sm text-gray-600 hover:text-green-600 border border-gray-200 rounded-lg transition"
            >
              <svg
                class="w-4 h-4 inline ml-1"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              لیست کودها
            </button>
            <button
              v-if="result"
              @click="printResult"
              class="px-3 py-1 text-sm text-gray-600 hover:text-green-600 border border-gray-200 rounded-lg transition"
            >
              <svg
                class="w-4 h-4 inline ml-1"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"
                />
              </svg>
              پرینت
            </button>
            <ThemeToggle />
          </div>
        </div>
      </div>
    </header>

    <!-- Modal لیست کودها -->
    <div
      v-if="showFertilizerList"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      @click.self="showFertilizerList = false"
    >
      <div
        class="bg-[var(--bg-card)] rounded-2xl max-w-4xl w-full max-h-[80vh] overflow-hidden shadow-xl"
      >
        <div
          class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gradient-to-r from-green-600 to-teal-600"
        >
          <h3 class="text-lg font-semibold text-white">
            📋 لیست کودهای موجود در دیتابیس
          </h3>
          <button
            @click="showFertilizerList = false"
            class="text-white hover:text-gray-200 text-xl"
          >
            ✕
          </button>
        </div>
        <div class="p-6 overflow-y-auto max-h-[calc(80vh-120px)]">
          <div v-if="isLoadingFertilizers" class="text-center py-8">
            <div
              class="inline-block w-8 h-8 border-2 border-green-500 border-t-transparent rounded-full animate-spin"
            ></div>
            <p class="mt-2 text-gray-500">در حال بارگذاری...</p>
          </div>
          <div
            v-else-if="fertilizers.length === 0"
            class="text-center py-8 text-gray-500"
          >
            هیچ کودی در دیتابیس یافت نشد
          </div>
          <div v-else class="space-y-3">
            <div
              v-for="fert in fertilizers"
              :key="fert.id"
              class="border border-gray-200 rounded-xl p-4 hover:shadow-md transition"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center gap-2 flex-wrap">
                    <h4 class="font-bold text-gray-800">
                      {{ fert.persian_name || fert.name }}
                    </h4>
                    <span
                      class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full"
                      >{{ fert.brand_name }}</span
                    >
                    <span
                      class="text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full"
                      >{{ fert.fertilizer_type }}</span
                    >
                  </div>
                  <div
                    class="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2 text-xs text-gray-500"
                  >
                    <span v-if="fert.n_percent">N: {{ fert.n_percent }}%</span>
                    <span v-if="fert.p_percent">P: {{ fert.p_percent }}%</span>
                    <span v-if="fert.k_percent">K: {{ fert.k_percent }}%</span>
                    <span v-if="fert.ca_percent"
                      >Ca: {{ fert.ca_percent }}%</span
                    >
                    <span v-if="fert.mg_percent"
                      >Mg: {{ fert.mg_percent }}%</span
                    >
                    <span v-if="fert.fe_percent"
                      >Fe: {{ fert.fe_percent }}%</span
                    >
                    <span v-if="fert.zn_percent"
                      >Zn: {{ fert.zn_percent }}%</span
                    >
                    <span v-if="fert.s_percent">S: {{ fert.s_percent }}%</span>
                  </div>
                  <p class="text-xs text-gray-400 mt-2">
                    {{ getFertilizerDescription(fert.name) }}
                  </p>
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
      <div
        class="bg-[var(--bg-card)] rounded-2xl shadow-card border border-gray-100 overflow-hidden"
      >
        <div class="px-6 py-5 border-b border-gray-100">
          <h2 class="text-lg font-semibold text-gray-800">اطلاعات محاسبه</h2>
          <p class="text-sm text-gray-500 mt-0.5">
            لطفاً اطلاعات مورد نیاز را وارد کنید
          </p>
        </div>

        <div class="p-6 space-y-6">
          <!-- Crop and Variety and Cultivation Type -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                <svg
                  class="w-4 h-4 inline ml-1 text-gray-500"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
                  />
                </svg>
                محصول
              </label>
              <select
                v-model="selectedCrop"
                class="w-full px-3 py-2.5 bg-[var(--bg-primary)] border border-gray-200 rounded-xl"
                disabled
              >
                <option value="توت‌فرنگی">توت‌فرنگی</option>
              </select>
              <p class="text-xs text-gray-400 mt-1">
                محصول انتخابی - توت فرنگی
              </p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                <svg
                  class="w-4 h-4 inline ml-1 text-gray-500"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2zM12 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z"
                  />
                  <path
                    d="M20 12c0-4.418-3.582-8-8-8s-8 3.582-8 8 3.582 8 8 8 8-3.582 8-8z"
                  />
                </svg>
                رقم گیاه
              </label>
              <select
                v-model="selectedVariety"
                class="w-full px-3 py-2.5 bg-[var(--bg-primary)] border border-gray-200 rounded-xl focus:border-green-500 focus:ring-1 focus:ring-green-500 transition"
              >
                <option value="">انتخاب کنید</option>
                <option value="سن اندرسا">سن اندرسا</option>
                <option value="کاماروسا">کاماروسا</option>
              </select>
              <p class="text-xs text-gray-400 mt-1">
                رقم مورد نظر خود را انتخاب کنید
              </p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                <svg
                  class="w-4 h-4 inline ml-1 text-gray-500"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
                مرحله رشد
              </label>
              <select
                v-model="selectedStage"
                @change="onStageChange"
                class="w-full px-3 py-2.5 bg-[var(--bg-primary)] border border-gray-200 rounded-xl focus:border-green-500 focus:ring-1 focus:ring-green-500 transition"
              >
                <option value="">انتخاب کنید</option>
                <option value="استقرار نشاء">استقرار نشاء</option>
                <option value="ریشه‌زایی">ریشه‌زایی</option>
                <option value="رشد رویشی">رشد رویشی</option>
                <option value="گلدهی">گلدهی</option>
                <option value="میوه‌دهی">میوه‌دهی</option>
              </select>
              <p class="text-xs text-gray-400 mt-1">
                مرحله رشدی گیاه را انتخاب کنید
              </p>
            </div>
          </div>

          <!-- Cultivation Type -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">
              <svg
                class="w-4 h-4 inline ml-1 text-gray-500"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              بستر کشت
            </label>
            <select
              v-model="cultivationType"
              class="w-full px-3 py-2.5 bg-[var(--bg-primary)] border border-gray-200 rounded-xl"
              disabled
            >
              <option value="هیدروپونیک">هیدروپونیک</option>
            </select>
            <p class="text-xs text-gray-400 mt-1">
              بستر کشت انتخابی - هیدروپونیک
            </p>
          </div>

          <!-- Brand Filter - Multi Select -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">
              <svg
                class="w-4 h-4 inline ml-1 text-gray-500"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2v16z" />
              </svg>
              فیلتر برند (اختیاری - چندگانه)
            </label>

            <div class="relative">
              <button
                @click="brandDropdownOpen = !brandDropdownOpen"
                type="button"
                class="w-full px-3 py-2.5 bg-[var(--bg-primary)] border border-gray-200 rounded-xl text-right flex justify-between items-center focus:border-green-500 focus:ring-1 focus:ring-green-500 transition"
              >
                <span class="text-gray-700">
                  {{
                    selectedBrands.length === 0
                      ? "همه برندها"
                      : selectedBrands.length + " برند انتخاب شده"
                  }}
                </span>
                <svg
                  class="w-4 h-4 text-gray-500"
                  :class="{ 'rotate-180': brandDropdownOpen }"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <div
                v-if="brandDropdownOpen"
                class="absolute z-20 mt-1 w-full bg-[var(--bg-card)] border border-gray-200 rounded-xl shadow-lg max-h-60 overflow-y-auto"
              >
                <div class="p-2">
                  <label
                    class="flex items-center gap-2 p-2 hover:bg-[var(--bg-primary)] rounded-lg cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      v-model="selectAllBrands"
                      @change="toggleAllBrands"
                      class="w-4 h-4 text-green-600 rounded"
                    />
                    <span class="text-sm font-medium text-gray-700"
                      >انتخاب همه برندها</span
                    >
                  </label>
                  <div class="border-t my-2"></div>
                  <div
                    v-for="brand in allBrandsList"
                    :key="brand"
                    class="flex items-center gap-2 p-2 hover:bg-[var(--bg-primary)] rounded-lg cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      v-model="selectedBrands"
                      :value="brand"
                      class="w-4 h-4 text-green-600 rounded"
                    />
                    <span class="text-sm text-gray-700">{{ brand }}</span>
                  </div>
                </div>
              </div>
            </div>
            <p class="text-xs text-gray-400 mt-1">
              می‌توانید یک یا چند برند را انتخاب کنید. در صورت عدم انتخاب، همه
              برندها در نظر گرفته می‌شوند.
            </p>
          </div>

          <!-- ============================================================ -->
          <!-- 🆕 بخش عناصر هدف ۱۶ گانه -->
          <!-- ============================================================ -->
          <TargetElementsTable
            :target-elements="targetElements16"
            :final-solution="finalSolution16"
            @update:targets="(targets) => { targetElements16 = targets; }"
          />

          <!-- ============================================================ -->
          <!-- 🆕 بخش آنالیز آب و پساب ترکیبی -->
          <!-- ============================================================ -->
          <div class="border border-blue-200 rounded-xl overflow-hidden">
            <div class="bg-blue-50 px-4 py-3 border-b border-blue-200">
              <div class="flex items-center gap-2">
                <svg
                  class="w-5 h-5 text-blue-600"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
                  />
                </svg>
                <h3 class="font-semibold text-blue-800">
                  💧 آنالیز آب و پساب ترکیبی
                </h3>
              </div>
              <p class="text-xs text-blue-600 mt-1">
                مقادیر آب تامینی خود را به صورت درصد وارد کنید
              </p>
            </div>
            <div class="p-4">
              <!-- درصد آب و پساب -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <InputField
                  v-model.number="waterPercent"
                  label="درصد آب تامینی"
                  type="number"
                  placeholder="80"
                  icon="M3 10h18M3 14h18M5 18h14M5 6h14"
                  :step="1"
                  :min="0"
                  :max="100"
                  help-text="مثال: 80% آب و 20% پساب"
                />
                <InputField
                  v-model.number="wastewaterPercent"
                  label="درصد پساب تامینی"
                  type="number"
                  placeholder="20"
                  icon="M3 10h18M3 14h18M5 18h14M5 6h14"
                  :step="1"
                  :min="0"
                  :max="100"
                  help-text="مجموع درصدها باید 100 باشد"
                />
              </div>

              <!-- هشدار مجموع درصد -->
              <div
                v-if="Math.abs(waterPercent + wastewaterPercent - 100) > 0.01"
                class="bg-red-50 border border-red-200 rounded-lg p-3 mb-4"
              >
                <p class="text-sm text-red-700 flex items-center gap-2">
                  <svg
                    class="w-5 h-5"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <path
                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                    />
                  </svg>
                  ⚠️ مجموع درصد آب و پساب باید 100 باشد. مقدار فعلی:
                  {{ waterPercent + wastewaterPercent }}%
                </p>
              </div>

              <!-- جدول آنالیز آب -->
              <div
                class="border border-green-200 rounded-lg overflow-hidden mb-4"
              >
                <div class="bg-green-50 px-3 py-2 border-b border-green-200">
                  <h4 class="text-sm font-semibold text-green-800">
                    📊 آنالیز آب
                  </h4>
                </div>
                <div class="p-3 overflow-x-auto">
                  <table class="w-full text-sm border-collapse">
                    <thead>
                      <tr class="bg-gray-100">
                        <th class="border border-gray-300 px-2 py-1 text-right">
                          عنصر
                        </th>
                        <th
                          class="border border-gray-300 px-2 py-1 text-center"
                        >
                          مقدار (ppm)
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="(value, key) in waterAnalysis"
                        :key="key"
                        class="hover:bg-[var(--bg-primary)]"
                      >
                        <td
                          class="border border-gray-300 px-2 py-1 font-medium text-gray-700"
                        >
                          {{ getElementDisplayName(key) }}
                        </td>
                        <td
                          class="border border-gray-300 px-2 py-1 text-center"
                        >
                          <input
                            type="number"
                            v-model.number="waterAnalysis[key]"
                            class="w-24 px-2 py-1 text-center border border-gray-300 rounded focus:border-green-500 focus:ring-1 focus:ring-green-500 bg-[var(--bg-primary)] text-[var(--text-primary)]"
                            step="0.1"
                            min="0"
                          />
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- جدول آنالیز پساب -->
              <div class="border border-amber-200 rounded-lg overflow-hidden">
                <div class="bg-amber-50 px-3 py-2 border-b border-amber-200">
                  <h4 class="text-sm font-semibold text-amber-800">
                    📊 آنالیز پساب
                  </h4>
                </div>
                <div class="p-3 overflow-x-auto">
                  <table class="w-full text-sm border-collapse">
                    <thead>
                      <tr class="bg-gray-100">
                        <th class="border border-gray-300 px-2 py-1 text-right">
                          عنصر
                        </th>
                        <th
                          class="border border-gray-300 px-2 py-1 text-center"
                        >
                          مقدار (ppm)
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="(value, key) in wastewaterAnalysis"
                        :key="key"
                        class="hover:bg-[var(--bg-primary)]"
                      >
                        <td
                          class="border border-gray-300 px-2 py-1 font-medium text-gray-700"
                        >
                          {{ getElementDisplayName(key) }}
                        </td>
                        <td
                          class="border border-gray-300 px-2 py-1 text-center"
                        >
                          <input
                            type="number"
                            v-model.number="wastewaterAnalysis[key]"
                            class="w-24 px-2 py-1 text-center border border-gray-300 rounded focus:border-amber-500 focus:ring-1 focus:ring-amber-500 bg-[var(--bg-primary)] text-[var(--text-primary)]"
                            step="0.1"
                            min="0"
                          />
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- نمایش مقادیر ترکیبی (پیش‌نمایش) -->
              <div
                v-if="hasWaterData"
                class="mt-4 bg-purple-50 border border-purple-200 rounded-lg p-3"
              >
                <h4 class="text-sm font-semibold text-purple-800 mb-2">
                  🔬 مقادیر ترکیبی آب و پساب
                </h4>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
                  <div
                    v-for="(value, key) in combinedWaterPreview"
                    :key="key"
                    class="bg-white rounded px-2 py-1"
                  >
                    <span class="font-medium"
                      >{{ getElementDisplayName(key) }}:</span
                    >
                    <span class="text-gray-700"
                      >{{ value.toFixed(1) }} ppm</span
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- ============================================================ -->
          <!-- تنظیمات پیشرفته: ویرایش دستی نیازهای گیاه -->
          <!-- ============================================================ -->
          <div class="border border-gray-300 rounded-xl overflow-hidden">
            <button
              @click="advancedSettingsOpen = !advancedSettingsOpen"
              type="button"
              class="w-full px-4 py-3 bg-gray-100 hover:bg-gray-200 transition flex justify-between items-center text-right"
            >
              <div class="flex items-center gap-2">
                <svg
                  class="w-5 h-5 text-gray-600"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                  />
                  <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span class="font-medium text-gray-700"
                  >⚙️ تنظیمات پیشرفته - ویرایش دستی نیازهای گیاه</span
                >
              </div>
              <svg
                class="w-5 h-5 text-gray-500 transition-transform"
                :class="{ 'rotate-180': advancedSettingsOpen }"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <div
              v-if="advancedSettingsOpen"
              class="p-5 border-t border-gray-200"
            >
              <p class="text-sm text-amber-600 mb-4 flex items-center gap-2">
                <svg
                  class="w-5 h-5"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                ⚠️ توجه: تغییر این مقادیر فقط برای محاسبه فعلی اعمال می‌شود و در
                دیتابیس ذخیره نمی‌شود.
              </p>

              <div class="overflow-x-auto">
                <table class="w-full text-sm border-collapse">
                  <thead>
                    <tr class="bg-gray-100">
                      <th class="border border-gray-300 px-3 py-2 text-right">
                        عنصر
                      </th>
                      <th class="border border-gray-300 px-3 py-2 text-center">
                        نیاز گیاه (ppm)
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="nutrient in editableNutrients"
                      :key="nutrient.element"
                      class="hover:bg-[var(--bg-primary)]"
                    >
                      <td class="border border-gray-300 px-3 py-2 font-medium">
                        {{ nutrient.name }} ({{ nutrient.element }})
                      </td>
                      <td class="border border-gray-300 px-3 py-2 text-center">
                        <input
                          type="number"
                          v-model.number="nutrient.value"
                          class="w-24 px-2 py-1 text-center border border-gray-300 rounded focus:border-green-500 focus:ring-1 focus:ring-green-500 bg-[var(--bg-primary)] text-[var(--text-primary)]"
                          step="1"
                          min="0"
                        />
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <button
                @click="resetNutrientsToDefault"
                type="button"
                class="mt-4 text-sm text-blue-600 hover:text-blue-800 transition flex items-center gap-1"
              >
                <svg
                  class="w-4 h-4"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
                بازنشانی به مقادیر پیش‌فرض مرحله رشد
              </button>
            </div>
          </div>

          <!-- ============================================================ -->
          <!-- بخش آب (منبع مشترک) -->
          <!-- ============================================================ -->
          <div class="border border-green-200 rounded-xl overflow-hidden">
            <div class="bg-green-50 px-4 py-3 border-b border-green-200">
              <div class="flex items-center gap-2">
                <svg
                  class="w-5 h-5 text-green-600"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
                  />
                </svg>
                <h3 class="font-semibold text-green-800">
                  اطلاعات آب (منبع مشترک)
                </h3>
              </div>
              <p class="text-xs text-green-600 mt-1">
                اطلاعات کیفیت آب - این مقادیر برای هر دو مخزن یکسان خواهد بود
              </p>
            </div>
            <div class="p-4">
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <InputField
                  v-model.number="waterSource.water_ec_ms_cm"
                  label="EC آب (mS/cm)"
                  type="number"
                  placeholder="0.4"
                  icon="M13 10V3L4 14h7v7l9-11h-7z"
                  :step="0.1"
                  :min="0"
                  help-text="بازه ایده‌آل: 0.2 - 0.8 mS/cm"
                />
                <InputField
                  v-model.number="waterSource.water_ph"
                  label="pH آب"
                  type="number"
                  placeholder="7.0"
                  icon="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 6.34l-1.41-1.41M17.66 6.34l1.41-1.41"
                  :step="0.1"
                  :min="0"
                  :max="14"
                  help-text="بازه ایده‌آل: 6.0 - 7.0"
                />
                <InputField
                  v-model.number="waterSource.water_ca_ppm"
                  label="کلسیم آب (ppm)"
                  type="number"
                  placeholder="50"
                  icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2zM12 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z"
                  :step="1"
                  :min="0"
                  help-text="بازه ایده‌آل: 40 - 80 ppm"
                />
                <InputField
                  v-model.number="waterSource.water_mg_ppm"
                  label="منیزیم آب (ppm)"
                  type="number"
                  placeholder="20"
                  icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2zM12 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z"
                  :step="1"
                  :min="0"
                  help-text="بازه ایده‌آل: 15 - 30 ppm"
                />
                <InputField
                  v-model.number="waterSource.water_hco3_ppm"
                  label="بیکربنات (ppm)"
                  type="number"
                  placeholder="0"
                  icon="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  :step="1"
                  :min="0"
                  help-text="بازه ایده‌آل: 0 - 100 ppm"
                />
                <InputField
                  v-model.number="waterSource.water_cl_ppm"
                  label="کلر آب (ppm)"
                  type="number"
                  placeholder="0"
                  icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z"
                  :step="1"
                  :min="0"
                  help-text="بازه ایده‌آل: 0 - 50 ppm"
                />
              </div>
            </div>
          </div>

          <!-- ============================================================ -->
          <!-- مخزن اصلی -->
          <!-- ============================================================ -->
          <div class="border border-blue-200 rounded-xl overflow-hidden">
            <div class="bg-blue-50 px-4 py-3 border-b border-blue-200">
              <div class="flex items-center gap-2">
                <svg
                  class="w-5 h-5 text-blue-600"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
                  />
                </svg>
                <h3 class="font-semibold text-blue-800">
                  مخزن اصلی (کودهای غیر کلسیمی)
                </h3>
              </div>
              <p class="text-xs text-blue-600 mt-1">
                این مخزن برای کودهای NPK، سولفات‌ها و ریز مغذی‌ها استفاده می‌شود
              </p>
            </div>
            <div class="p-4">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
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
                  help-text="حجم مخزن بر حسب لیتر"
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
                <svg
                  class="w-5 h-5 text-amber-600"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
                  />
                </svg>
                <h3 class="font-semibold text-amber-800">
                  مخزن کلسیم (کودهای حاوی کلسیم)
                </h3>
              </div>
              <p class="text-xs text-amber-600 mt-1">
                این مخزن فقط برای کودهای حاوی کلسیم مانند نیترات کلسیم و کلات
                آهن استفاده می‌شود
              </p>
            </div>
            <div class="p-4">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
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
                  help-text="حجم مخزن بر حسب لیتر"
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
                <svg
                  class="w-5 h-5 text-purple-600"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
                  />
                </svg>
                <h3 class="font-semibold text-purple-800">
                  تنظیمات سیستم استوک (محلول مادر)
                </h3>
              </div>
              <p class="text-xs text-purple-600 mt-1">
                این تنظیمات برای محاسبه مقدار کود مورد نیاز برای ساخت استوک
                استفاده می‌شود
              </p>
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
              <div
                class="mt-3 text-xs text-gray-500 bg-[var(--bg-primary)] rounded-lg p-2"
              >
                <span class="font-medium">💡 مفهوم نسبت تزریق:</span>
                <span>
                  به ازای هر 1 لیتر استوک، {{ injectorRatio - 1 }} لیتر آب اضافه
                  می‌شود تا {{ injectorRatio }} لیتر محلول نهایی بدست آید.</span
                >
              </div>
            </div>
          </div>

          <!-- Calculate Button -->
          <button
            @click="calculateDualTank"
            :disabled="isLoading || !selectedVariety || !selectedStage"
            class="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium py-3 rounded-xl transition-all duration-200 flex items-center justify-center gap-2"
          >
            <svg
              v-if="isLoading"
              class="w-5 h-5 animate-spin"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            <svg
              v-else
              class="w-5 h-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
            {{ isLoading ? "در حال محاسبه..." : "محاسبه ترکیب بهینه دو مخزن" }}
          </button>
        </div>
      </div>

      <!-- Errors -->
      <div
        v-if="validationErrors.length > 0"
        class="mt-6 bg-red-50 border border-red-200 rounded-xl p-4"
      >
        <div class="flex gap-3">
          <svg
            class="w-5 h-5 text-red-500"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <div class="flex-1">
            <h4 class="text-sm font-bold text-red-800">خطاهای اعتبارسنجی</h4>
            <ul class="mt-1 text-sm text-red-700 list-disc list-inside">
              <li v-for="(err, idx) in validationErrors" :key="idx">
                {{ err }}
              </li>
            </ul>
          </div>
          <button
            @click="validationErrors = []"
            class="text-red-400 hover:text-red-600"
          >
            ✕
          </button>
        </div>
      </div>

      <div
        v-if="errorMessage"
        class="mt-6 bg-red-50 border border-red-200 rounded-xl p-4"
      >
        <div class="flex gap-3">
          <svg
            class="w-5 h-5 text-red-500"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <p class="text-sm text-red-700">{{ errorMessage }}</p>
          <button
            @click="errorMessage = ''"
            class="mr-auto text-red-400 hover:text-red-600"
          >
            ✕
          </button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="mt-8 flex justify-center">
        <div
          class="bg-[var(--bg-card)] rounded-xl shadow-card px-6 py-4 flex items-center gap-3"
        >
          <div
            class="w-5 h-5 border-2 border-green-500 border-t-transparent rounded-full animate-spin"
          ></div>
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
import { ref, reactive, computed, onMounted, toRaw } from "vue";
import axios from "axios";
import ResultsDisplay from "../components/calculator/ResultsDisplay.vue";
import InputField from "../components/common/InputField.vue";
import ThemeToggle from "../components/common/ThemeToggle.vue";
import TargetElementsTable from "../components/calculator/TargetElementsTable.vue";

// ============================================================
// Constants
// ============================================================

const API_BASE_URL = "/api/v1";

// ============================================================
// State - Connection & UI
// ============================================================

const connectionStatus = ref("checking");
const selectedCrop = ref("توت‌فرنگی");
const cultivationType = ref("هیدروپونیک");
const selectedVariety = ref("");
const selectedStage = ref("");
const isLoading = ref(false);
const isLoadingFertilizers = ref(false);
const result = ref<any>(null);
const errorMessage = ref("");
const validationErrors = ref<string[]>([]);
const showFertilizerList = ref(false);
const fertilizers = ref<any[]>([]);

// ============================================================
// 🆕 State - Target Elements 16
// ============================================================

const targetElements16 = ref<Record<string, number>>({});
const finalSolution16 = ref<Record<string, number>>({});

// ============================================================
// State - Stock System
// ============================================================

const stockTankVolume = ref(20);
const injectorRatio = ref(200);

// ============================================================
// State - Advanced Settings (Custom Nutrient Needs)
// ============================================================

const advancedSettingsOpen = ref(false);

const editableNutrients = ref([
  { element: "N", name: "نیتروژن", value: 0 },
  { element: "P", name: "فسفر", value: 0 },
  { element: "K", name: "پتاسیم", value: 0 },
  { element: "Ca", name: "کلسیم", value: 0 },
  { element: "Mg", name: "منیزیم", value: 0 },
  { element: "S", name: "گوگرد", value: 0 },
  { element: "Fe", name: "آهن", value: 0 },
  { element: "Zn", name: "روی", value: 0 },
  { element: "Mn", name: "منگنز", value: 0 },
  { element: "Cu", name: "مس", value: 0 },
  { element: "B", name: "بُر", value: 0 },
  { element: "Mo", name: "مولیبدن", value: 0 },
  { element: "Cl", name: "کلر", value: 0 },
]);

let defaultNutrientValues: Record<string, number> = {};

// ============================================================
// State - Brand Filter
// ============================================================

const brandDropdownOpen = ref(false);
const allBrandsList = ref<string[]>([
  "گل سم گرگان",
  "رازاک شیمی",
  "گرین استار",
  "زاگرا استار",
  "اطلس",
  "ردسا",
]);
const selectedBrands = ref<string[]>([]);
const selectAllBrands = ref(false);

// ============================================================
// 🆕 State - Water & Wastewater Analysis
// ============================================================

const waterPercent = ref(80);
const wastewaterPercent = ref(20);

const waterAnalysis = reactive<Record<string, number>>({
  n_no3: 10,
  p: 2,
  s: 5,
  n_nh4: 0,
  k: 8,
  ca: 50,
  fe: 0.5,
  mn: 0.1,
  zn: 0.05,
  b: 0.2,
  cu: 0.02,
  mo: 0.01,
  ec: 0.4,
  ph: 7.0,
});

const wastewaterAnalysis = reactive<Record<string, number>>({
  n_no3: 25,
  p: 5,
  s: 10,
  n_nh4: 2,
  k: 15,
  ca: 80,
  fe: 1.0,
  mn: 0.3,
  zn: 0.1,
  b: 0.5,
  cu: 0.05,
  mo: 0.02,
  ec: 1.2,
  ph: 6.5,
});

// ============================================================
// Computed - Combined Water Preview
// ============================================================

const hasWaterData = computed(() => {
  return (
    Object.values(waterAnalysis).some((v) => v > 0) ||
    Object.values(wastewaterAnalysis).some((v) => v > 0)
  );
});

const combinedWaterPreview = computed(() => {
  const result: Record<string, number> = {};
  const keys = Object.keys(waterAnalysis);

  for (const key of keys) {
    const waterVal = waterAnalysis[key] || 0;
    const wasteVal = wastewaterAnalysis[key] || 0;
    result[key] =
      (waterPercent.value * waterVal + wastewaterPercent.value * wasteVal) /
      100;
  }

  return result;
});

// ============================================================
// State - Water Source (Common)
// ============================================================

const waterSource = reactive({
  water_ec_ms_cm: 0.4,
  water_ph: 7.0,
  water_ca_ppm: 50,
  water_mg_ppm: 20,
  water_hco3_ppm: 0,
  water_cl_ppm: 0,
  water_na_ppm: 0,
  water_so4_ppm: 0,
  water_no3_ppm: 0,
  water_fe_ppm: 0,
});

// ============================================================
// State - Tanks
// ============================================================

const tankMain = reactive({
  name: "مخزن اصلی",
  tank_type: "main",
  volume_liters: 100,
});

const tankCalcium = reactive({
  name: "مخزن کلسیم",
  tank_type: "calcium",
  volume_liters: 100,
});

// ============================================================
// Helper Functions
// ============================================================

const getElementDisplayName = (key: string) => {
  const names: Record<string, string> = {
    n_no3: "N-NO₃ (نیترات)",
    p: "P (فسفر)",
    s: "S (گوگرد)",
    n_nh4: "N-NH₄ (آمونیوم)",
    k: "K (پتاسیم)",
    ca: "Ca (کلسیم)",
    fe: "Fe (آهن)",
    mn: "Mn (منگنز)",
    zn: "Zn (روی)",
    b: "B (بور)",
    cu: "Cu (مس)",
    mo: "Mo (مولیبدن)",
    ec: "EC (هدایت الکتریکی)",
    ph: "pH (اسیدیته)",
  };
  return names[key] || key;
};

const getFertilizerDescription = (name: string) => {
  const descriptions: Record<string, string> = {
    "نیترات کلسیم":
      "منبع کلسیم و نیتروژن - برای رشد ساختار گیاه و جلوگیری از پوسیدگی گلگاه",
    "سولفات منیزیم":
      "منبع منیزیم و گوگرد - برای تولید کلروفیل و فعالسازی آنزیم‌ها",
    "سولفات پتاسیم": "منبع پتاسیم و گوگرد - برای کیفیت میوه و مقاومت به تنش",
    "کلات آهن": "منبع آهن - برای جلوگیری از زردی برگ‌ها (کلروز)",
    "فرتی‌گل 20-20-20":
      "کود کامل NPK متعادل - مناسب برای رشد عمومی و مراحل اولیه",
    "فرتی‌گل 36-12-12":
      "کود NPK با پتاسیم بالا - مناسب برای میوه‌دهی و افزایش کیفیت",
    "فرتی‌گل 10-50-10": "کود NPK با فسفر بالا - مناسب برای ریشه‌زایی و گلدهی",
    "فرتی‌گل 30-5-15": "کود NPK با نیتروژن بالا - مناسب برای رشد رویشی",
    "یونی کمپلکس پودری": "کود کامل ریز مغذی‌ها - برای تامین عناصر کم مصرف",
    "NPK 20-20-20 گرین استار": "کود NPK متعادل - مناسب برای رشد عمومی",
    "NPK 12-12-36 گرین استار": "کود NPK با پتاسیم بالا - مناسب برای میوه‌دهی",
    "NPK 10-52-10 زاگرا استار": "کود NPK با فسفر بالا - مناسب برای ریشه‌زایی",
    "کلرید پتاسیم": "منبع پتاسیم و کلر - برای تغذیه عمومی (در آب با کلر پایین)",
  };
  return descriptions[name] || "کود مغذی برای تامین عناصر مورد نیاز گیاه";
};

// ============================================================
// Nutrient Needs Functions
// ============================================================

const fetchNutrientNeeds = async (stageName: string) => {
  if (!stageName) return;

  try {
    console.log(`📤 Fetching nutrient needs for stage: ${stageName}`);
    const response = await axios.get(`${API_BASE_URL}/growth-stages`);
    console.log('✅ Growth stages response:', response.data);

    const stages = response.data;
    const stage = stages.find((s: any) => s.name === stageName);

    if (stage && stage.nutrient_needs) {
      const needs = stage.nutrient_needs;

      for (const nutrient of editableNutrients.value) {
        const value = needs[nutrient.element] || 0;
        nutrient.value = value;
        defaultNutrientValues[nutrient.element] = value;
      }
      console.log('✅ Nutrient needs loaded:', needs);
    }
  } catch (err: any) {
    console.error('❌ Error fetching nutrient needs:', err.message);
  }
};

const resetNutrientsToDefault = () => {
  for (const nutrient of editableNutrients.value) {
    nutrient.value = defaultNutrientValues[nutrient.element] || 0;
  }
};

const getCustomNutrientNeeds = () => {
  const needs: Record<string, number> = {};
  for (const nutrient of editableNutrients.value) {
    needs[nutrient.element] = nutrient.value;
  }
  return needs;
};

const onStageChange = () => {
  if (selectedStage.value) {
    fetchNutrientNeeds(selectedStage.value);
  }
};

// ============================================================
// Brand Functions
// ============================================================

const toggleAllBrands = () => {
  if (selectAllBrands.value) {
    selectedBrands.value = [...allBrandsList.value];
  } else {
    selectedBrands.value = [];
  }
};

// ============================================================
// Fertilizer Functions
// ============================================================

const fetchFertilizers = async () => {
  isLoadingFertilizers.value = true;
  try {
    console.log('📤 Fetching fertilizers...');
    const response = await axios.get(`${API_BASE_URL}/fertilizers`);
    fertilizers.value = response.data;
    console.log('✅ Fertilizers loaded:', fertilizers.value.length);
  } catch (err: any) {
    console.error('❌ Error fetching fertilizers:', err.message);
  } finally {
    isLoadingFertilizers.value = false;
  }
};

// ============================================================
// Connection Check
// ============================================================

const checkConnection = async () => {
  console.log('🔍 Checking connection to backend...');
  console.log(`📍 API_BASE_URL: ${API_BASE_URL}`);

  try {
    const response = await axios.get(`${API_BASE_URL}/health`);
    console.log('✅ Health check response:', response.data);

    if (response.data && response.data.status === "ok") {
      connectionStatus.value = "connected";
      console.log('✅ Connected to server successfully');
      await fetchFertilizers();
    } else {
      connectionStatus.value = "disconnected";
      errorMessage.value = "خطا در اتصال به سرور";
      console.error('❌ Invalid health response:', response.data);
    }
  } catch (err: any) {
    console.error('❌ Connection error:', err.message);
    connectionStatus.value = "disconnected";
    errorMessage.value = 'خطا در اتصال به سرور. لطفاً سرور بک‌اند را بررسی کنید.';
  }
};

// ============================================================
// 🆕 Main Calculation Function
// ============================================================

const calculateDualTank = async () => {
  validationErrors.value = [];

  if (!selectedVariety.value) {
    validationErrors.value.push("لطفاً رقم گیاه را انتخاب کنید");
  }
  if (!selectedStage.value) {
    validationErrors.value.push("لطفاً مرحله رشد را انتخاب کنید");
  }

  const mainVolume = Number(tankMain.volume_liters);
  if (isNaN(mainVolume) || mainVolume <= 0) {
    validationErrors.value.push(
      "حجم مخزن اصلی معتبر نیست (باید عدد مثبت باشد)",
    );
  }

  const calciumVolume = Number(tankCalcium.volume_liters);
  if (isNaN(calciumVolume) || calciumVolume <= 0) {
    validationErrors.value.push(
      "حجم مخزن کلسیم معتبر نیست (باید عدد مثبت باشد)",
    );
  }

  const totalPercent = waterPercent.value + wastewaterPercent.value;
  if (Math.abs(totalPercent - 100) > 0.01) {
    validationErrors.value.push(
      `مجموع درصد آب و پساب باید 100 باشد. مقدار فعلی: ${totalPercent}%`,
    );
  }

  if (validationErrors.value.length > 0) {
    return;
  }

  isLoading.value = true;
  errorMessage.value = "";
  result.value = null;

  try {
    const rawWaterSource = toRaw(waterSource);
    const rawTankMain = toRaw(tankMain);
    const rawTankCalcium = toRaw(tankCalcium);
    const rawWaterAnalysis = toRaw(waterAnalysis);
    const rawWastewaterAnalysis = toRaw(wastewaterAnalysis);
    const rawCustomNutrientNeeds = getCustomNutrientNeeds();

    const payload = {
      crop_name: selectedCrop.value,
      variety_name: selectedVariety.value,
      stage_name: selectedStage.value,
      brand_filter:
        selectedBrands.value.length > 0 ? selectedBrands.value : null,
      custom_nutrient_needs: rawCustomNutrientNeeds,

      // 🆕 عناصر هدف ۱۶ گانه
      target_elements_16: Object.keys(targetElements16.value).length > 0
        ? { ...targetElements16.value }
        : null,

      tank_main: {
        name: rawTankMain.name,
        tank_type: rawTankMain.tank_type,
        volume_liters: mainVolume,
        water_ec_ms_cm: rawWaterSource.water_ec_ms_cm,
        water_ph: rawWaterSource.water_ph,
        water_ca_ppm: rawWaterSource.water_ca_ppm,
        water_mg_ppm: rawWaterSource.water_mg_ppm,
        water_hco3_ppm: rawWaterSource.water_hco3_ppm,
        water_cl_ppm: rawWaterSource.water_cl_ppm,
        water_na_ppm: rawWaterSource.water_na_ppm,
        water_so4_ppm: rawWaterSource.water_so4_ppm,
        water_no3_ppm: rawWaterSource.water_no3_ppm,
        water_fe_ppm: rawWaterSource.water_fe_ppm,
      },
      tank_calcium: {
        name: rawTankCalcium.name,
        tank_type: rawTankCalcium.tank_type,
        volume_liters: calciumVolume,
        water_ec_ms_cm: rawWaterSource.water_ec_ms_cm,
        water_ph: rawWaterSource.water_ph,
        water_ca_ppm: rawWaterSource.water_ca_ppm,
        water_mg_ppm: rawWaterSource.water_mg_ppm,
        water_hco3_ppm: rawWaterSource.water_hco3_ppm,
        water_cl_ppm: rawWaterSource.water_cl_ppm,
        water_na_ppm: rawWaterSource.water_na_ppm,
        water_so4_ppm: rawWaterSource.water_so4_ppm,
        water_no3_ppm: rawWaterSource.water_no3_ppm,
        water_fe_ppm: rawWaterSource.water_fe_ppm,
      },
      stock_tank_volume_liters: stockTankVolume.value,
      injector_ratio: injectorRatio.value,
      water_percent: waterPercent.value,
      wastewater_percent: wastewaterPercent.value,
      water_analysis: rawWaterAnalysis,
      wastewater_analysis: rawWastewaterAnalysis,
    };

    console.log('📤 Sending request to:', `${API_BASE_URL}/calculate-dual-tank`);
    console.log('📤 Payload:', payload);

    const response = await axios.post(
      `${API_BASE_URL}/calculate-dual-tank`,
      payload,
    );

    console.log('📥 Response status:', response.status);
    console.log('📥 Response data:', response.data);

    if (response.data.success) {
      result.value = response.data;

      if (response.data.final_solution_ppm) {
        finalSolution16.value = response.data.final_solution_ppm;
      }

      console.log('✅ Calculation successful');
    } else {
      errorMessage.value = response.data.error_message || "خطا در محاسبه";
      console.error('❌ Calculation failed:', response.data.error_message);
    }
  } catch (err: any) {
    console.error('❌ Calculation error:', err);

    if (err.code === 'ERR_NETWORK') {
      errorMessage.value = 'خطا در اتصال به سرور. لطفاً سرور بک‌اند را بررسی کنید.';
    } else if (err.response?.data?.detail) {
      if (typeof err.response.data.detail === "string") {
        errorMessage.value = err.response.data.detail;
      } else if (Array.isArray(err.response.data.detail)) {
        validationErrors.value = err.response.data.detail.map((e: any) => {
          if (e.msg === "Input should be a valid number") {
            return "لطفاً مقدار معتبر برای حجم مخزن وارد کنید";
          }
          return e.msg;
        });
      } else {
        errorMessage.value = JSON.stringify(err.response.data.detail);
      }
    } else {
      errorMessage.value = "خطا در محاسبه. لطفاً دوباره تلاش کنید.";
    }
  } finally {
    isLoading.value = false;
  }
};

// ============================================================
// Print Function
// ============================================================

const printResult = () => {
  window.print();
};

// ============================================================
// Lifecycle Hooks
// ============================================================

onMounted(() => {
  console.log('🚀 CalculatorView mounted');
  console.log(`📍 API_BASE_URL: ${API_BASE_URL}`);
  checkConnection();
});
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
