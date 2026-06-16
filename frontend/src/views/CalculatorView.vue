<template>
  <div class="space-y-6">
    <!-- Header -->
    <div
      class="bg-gradient-to-r from-green-600 to-teal-600 rounded-2xl p-5 text-white"
    >
      <h2 class="text-xl font-bold flex items-center gap-2">
        <svg
          class="w-6 h-6"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        نتیجه محاسبات
      </h2>
      <p class="text-green-100 text-sm mt-1">
        محصول: {{ result.crop_name }} | رقم: {{ result.variety_name }} | مرحله:
        {{ result.stage_name }}
      </p>
    </div>

    <!-- بخش 1: تنظیمات شما -->
    <div
      class="bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl p-5 border border-gray-200"
    >
      <h3 class="font-bold text-gray-700 mb-4 flex items-center gap-2">
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
        تنظیمات شما
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white rounded-lg p-3 text-center shadow-sm">
          <svg
            class="w-6 h-6 mx-auto text-green-600 mb-1"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
            />
          </svg>
          <div class="text-xs text-gray-500">مرحله رشد</div>
          <div class="font-bold text-gray-800">{{ result.stage_name }}</div>
        </div>
        <div class="bg-white rounded-lg p-3 text-center shadow-sm">
          <svg
            class="w-6 h-6 mx-auto text-blue-600 mb-1"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M4 20h16a2 2 0 002-2V8a2 2 0 00-2-2h-7.93a2 2 0 01-1.66-.9l-.82-1.2A2 2 0 007.93 3H4a2 2 0 00-2 2v13a2 2 0 002 2z"
            />
          </svg>
          <div class="text-xs text-gray-500">حجم مخزن اصلی</div>
          <div class="font-bold text-gray-800">
            {{ formatNumber(result.tank_main_result?.tank_volume_liters || 0) }}
            <span class="text-sm font-normal">لیتر</span>
          </div>
        </div>
        <div class="bg-white rounded-lg p-3 text-center shadow-sm">
          <svg
            class="w-6 h-6 mx-auto text-amber-600 mb-1"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
            />
          </svg>
          <div class="text-xs text-gray-500">حجم مخزن کلسیم</div>
          <div class="font-bold text-gray-800">
            {{
              formatNumber(result.tank_calcium_result?.tank_volume_liters || 0)
            }}
            <span class="text-sm font-normal">لیتر</span>
          </div>
        </div>
        <div class="bg-white rounded-lg p-3 text-center shadow-sm">
          <svg
            class="w-6 h-6 mx-auto text-purple-600 mb-1"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
            />
          </svg>
          <div class="text-xs text-gray-500">حجم مخزن استوک</div>
          <div class="font-bold text-gray-800">
            {{ props.stockTankVolume || 20 }}
            <span class="text-sm font-normal">لیتر</span>
          </div>
        </div>
        <div class="bg-white rounded-lg p-3 text-center shadow-sm">
          <svg
            class="w-6 h-6 mx-auto text-indigo-600 mb-1"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <div class="text-xs text-gray-500">نسبت تزریق</div>
          <div class="font-bold text-gray-800">
            1:{{ props.injectorRatio || 200 }}
          </div>
        </div>
        <div class="bg-white rounded-lg p-3 text-center shadow-sm">
          <svg
            class="w-6 h-6 mx-auto text-gray-600 mb-1"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
          </svg>
          <div class="text-xs text-gray-500">حجم کل محلول نهایی</div>
          <div class="font-bold text-gray-800">
            {{
              (
                (result.tank_main_result?.tank_volume_liters || 0) +
                (result.tank_calcium_result?.tank_volume_liters || 0)
              ).toLocaleString()
            }}
            <span class="text-sm font-normal">لیتر</span>
          </div>
        </div>
      </div>

      <div
        class="mt-4 bg-blue-50 rounded-lg p-3 text-sm border border-blue-200"
      >
        <p class="font-medium text-blue-800 mb-1 flex items-center gap-1">
          <svg
            class="w-4 h-4"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          مفهوم نسبت تزریق 1:{{ props.injectorRatio || 200 }}
        </p>
        <p class="text-blue-700">
          به ازای هر 1 لیتر استوک، {{ (props.injectorRatio || 200) - 1 }} لیتر
          آب اضافه می‌شود تا {{ props.injectorRatio || 200 }} لیتر محلول نهایی
          بدست آید.
        </p>
      </div>
    </div>

    <!-- 🆕 بخش آب و پساب ترکیبی (نسخه 3.4.0) -->
    <div
      v-if="result.water_analysis"
      class="bg-gradient-to-r from-teal-50 to-cyan-50 rounded-xl p-5 border border-teal-200"
    >
      <h3 class="font-bold text-teal-800 mb-4 flex items-center gap-2">
        <svg
          class="w-5 h-5"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
          />
        </svg>
        💧 آنالیز آب و پساب ترکیبی
      </h3>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div class="bg-white rounded-lg p-3 text-center shadow-sm">
          <div class="text-xs text-gray-500">درصد آب</div>
          <div class="font-bold text-blue-600">
            {{ result.water_analysis.water_percent }}%
          </div>
        </div>
        <div class="bg-white rounded-lg p-3 text-center shadow-sm">
          <div class="text-xs text-gray-500">درصد پساب</div>
          <div class="font-bold text-orange-600">
            {{ result.water_analysis.wastewater_percent }}%
          </div>
        </div>
      </div>

      <!-- جدول مقادیر تامینی -->
      <div class="overflow-x-auto mb-3">
        <table class="w-full text-sm border-collapse">
          <thead>
            <tr class="bg-teal-100">
              <th class="border border-teal-200 px-2 py-1.5 text-right text-xs">
                عنصر
              </th>
              <th
                class="border border-teal-200 px-2 py-1.5 text-center text-xs"
              >
                آب
              </th>
              <th
                class="border border-teal-200 px-2 py-1.5 text-center text-xs"
              >
                پساب
              </th>
              <th
                class="border border-teal-200 px-2 py-1.5 text-center text-xs font-bold text-teal-700"
              >
                تامینی
              </th>
              <th
                class="border border-teal-200 px-2 py-1.5 text-center text-xs"
              >
                کمبود
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in waterComparisonItems"
              :key="item.element"
              class="hover:bg-teal-50/50"
            >
              <td
                class="border border-teal-200 px-2 py-1.5 font-medium text-xs"
              >
                {{ getElementName(item.element) }}
              </td>
              <td
                class="border border-teal-200 px-2 py-1.5 text-center text-xs"
              >
                {{ formatNumber(item.water) }}
              </td>
              <td
                class="border border-teal-200 px-2 py-1.5 text-center text-xs"
              >
                {{ formatNumber(item.wastewater) }}
              </td>
              <td
                class="border border-teal-200 px-2 py-1.5 text-center text-xs font-bold text-teal-700"
              >
                {{ formatNumber(item.combined) }}
              </td>
              <td
                class="border border-teal-200 px-2 py-1.5 text-center text-xs"
                :class="item.deficit > 0 ? 'text-amber-600' : 'text-green-600'"
              >
                {{
                  item.deficit > 0
                    ? "⚠️ " + formatNumber(item.deficit)
                    : "✅ " + formatNumber(Math.abs(item.deficit))
                }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div
        class="text-xs text-gray-500 bg-white/70 rounded-lg p-2 border border-teal-100"
      >
        <span class="font-medium">💡 توضیح:</span>
        مقادیر تامینی از ترکیب آب و پساب به دست آمده و از نیازهای گیاه کسر
        شده‌اند. کمبود مثبت = نیاز به تأمین توسط کود، کمبود منفی = بیش‌بود عنصر.
      </div>
    </div>

    <!-- جدول نیاز گیاه و عناصر تامین شده -->
    <div
      class="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden"
    >
      <div class="bg-gradient-to-r from-gray-600 to-gray-700 px-5 py-3">
        <h3 class="text-white font-bold flex items-center gap-2">
          <svg
            class="w-5 h-5"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
          </svg>
          مقایسه نیاز گیاه با عناصر تامین شده
        </h3>
      </div>
      <div class="p-5">
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
                <th class="border border-gray-300 px-3 py-2 text-center">
                  تامین شده (ppm)
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  وضعیت
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in nutrientComparison"
                :key="item.element"
                class="hover:bg-gray-50"
              >
                <td class="border border-gray-300 px-3 py-2 font-medium">
                  {{ getElementName(item.element) }}
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  {{ formatNumber(item.need) }}
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  {{ formatNumber(item.supplied) }}
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  <span
                    v-if="item.status === 'ok'"
                    class="text-green-600 font-medium"
                    >✓ کافی</span
                  >
                  <span
                    v-else-if="item.status === 'low'"
                    class="text-amber-600 font-medium"
                    >⚠️ کم</span
                  >
                  <span v-else class="text-red-600 font-medium"
                    >✗ بسیار کم</span
                  >
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- مخزن اصلی -->
    <div
      class="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden"
    >
      <div class="bg-gradient-to-r from-blue-600 to-indigo-600 px-5 py-3">
        <h3 class="text-white font-bold flex items-center justify-between">
          <span class="flex items-center gap-2">
            <svg
              class="w-5 h-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
              />
            </svg>
            مخزن اصلی (کودهای غیر کلسیمی)
          </span>
          <span class="text-xs bg-white/20 px-2 py-1 rounded-full">{{
            result.tank_main_result.tank_name
          }}</span>
        </h3>
      </div>

      <div class="p-5">
        <div class="overflow-x-auto mb-4">
          <table class="w-full text-sm border-collapse">
            <thead>
              <tr class="bg-gray-100">
                <th class="border border-gray-300 px-3 py-2 text-right">
                  نام کود
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  مصرف (g/L)
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  مجموع برای مخزن
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  مقدار برای استوک
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center"></th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="dose in result.tank_main_result.doses"
                :key="dose.name"
                class="hover:bg-gray-50"
              >
                <td class="border border-gray-300 px-3 py-2 font-medium">
                  {{ dose.persian_name || dose.name }}
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  {{ dose.dose_g_per_liter }} g/L
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  {{ formatNumber(dose.dose_g_for_tank) }} گرم
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  <span v-if="getStockAmount(dose) >= 1000"
                    >{{
                      (getStockAmount(dose) / 1000).toFixed(2)
                    }}
                    کیلوگرم</span
                  >
                  <span v-else-if="getStockAmount(dose) >= 1"
                    >{{ getStockAmount(dose).toFixed(0) }} گرم</span
                  >
                  <span v-else
                    >{{
                      (getStockAmount(dose) * 1000).toFixed(0)
                    }}
                    میلی‌گرم</span
                  >
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  <button
                    @click="showFertilizerDetail(dose.name)"
                    class="text-blue-600 hover:text-blue-800 transition"
                    title="مشاهده اطلاعات کامل کود"
                  >
                    <svg
                      class="w-5 h-5 inline"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <circle cx="12" cy="12" r="10" />
                      <path d="M12 16v-4M12 8h.01" />
                    </svg>
                    اطلاعات
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="grid grid-cols-2 gap-3 mb-4">
          <div class="bg-blue-50 rounded-lg p-3 text-center">
            <span class="font-bold text-blue-700">EC پیش‌بینی شده:</span>
            <span class="text-blue-700 font-bold mx-2"
              >{{ result.tank_main_result.target_ec || "---" }} mS/cm</span
            >
          </div>
          <div class="bg-blue-50 rounded-lg p-3 text-center">
            <span class="font-bold text-blue-700">pH هدف:</span>
            <span class="text-blue-700 font-bold mx-2">{{
              result.tank_main_result.target_ph || "5.8 - 6.2"
            }}</span>
          </div>
        </div>

        <div class="bg-purple-50 rounded-lg p-3 mb-3">
          <h4 class="font-medium text-purple-800 mb-2 flex items-center gap-1">
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
              />
            </svg>
            مرحله 1: ساخت استوک برای مخزن اصلی
          </h4>
          <p class="text-sm text-gray-700 mb-2">
            برای ساخت {{ props.stockTankVolume || 20 }} لیتر استوک با نسبت 1:{{
              props.injectorRatio || 200
            }}، مقادیر زیر را با دقت اندازه گیری کنید:
          </p>
          <div class="bg-white rounded-lg p-3">
            <div
              v-for="dose in result.tank_main_result.doses"
              :key="dose.name"
              class="flex justify-between items-center py-1 border-b border-gray-100 last:border-0"
            >
              <span class="text-sm font-medium">{{
                dose.persian_name || dose.name
              }}</span>
              <span class="text-sm text-gray-600">
                <span v-if="getStockAmount(dose) >= 1000"
                  >{{ (getStockAmount(dose) / 1000).toFixed(2) }} کیلوگرم</span
                >
                <span v-else-if="getStockAmount(dose) >= 1"
                  >{{ getStockAmount(dose).toFixed(0) }} گرم</span
                >
                <span v-else
                  >{{ (getStockAmount(dose) * 1000).toFixed(0) }} میلی‌گرم</span
                >
              </span>
            </div>
          </div>
        </div>

        <div class="bg-green-50 rounded-lg p-3 mb-3">
          <h4 class="font-medium text-green-800 mb-2 flex items-center gap-1">
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            مرحله 2: مصرف استوک در مخزن اصلی
          </h4>
          <div class="grid grid-cols-2 gap-3 mb-2">
            <div class="bg-white rounded-lg p-2 text-center">
              <p class="text-lg font-bold text-green-700">
                {{
                  (
                    (result.tank_main_result.tank_volume_liters || 0) /
                    (props.injectorRatio || 200)
                  ).toFixed(1)
                }}
                لیتر
              </p>
              <p class="text-xs text-gray-600">
                استوک برای مخزن
                {{
                  formatNumber(result.tank_main_result.tank_volume_liters || 0)
                }}
                لیتری
              </p>
            </div>
            <div class="bg-white rounded-lg p-2 text-center">
              <p class="text-lg font-bold text-green-700">
                {{ (1000 / (props.injectorRatio || 200)).toFixed(1) }} میلی‌لیتر
              </p>
              <p class="text-xs text-gray-600">استوک برای هر 1 لیتر آب</p>
            </div>
          </div>
        </div>

        <details class="mt-3">
          <summary
            class="cursor-pointer text-blue-600 hover:text-blue-700 font-medium text-sm inline-flex items-center gap-1"
          >
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            مشاهده دستورالعمل اختلاط مستقیم (بدون استوک)
          </summary>
          <div
            class="mt-3 p-4 bg-gray-100 rounded-lg text-sm whitespace-pre-line font-mono"
            v-html="
              formatInstructions(result.tank_main_result.mixing_instructions)
            "
          ></div>
        </details>
      </div>
    </div>

    <!-- مخزن کلسیم -->
    <div
      class="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden"
    >
      <div class="bg-gradient-to-r from-amber-600 to-orange-600 px-5 py-3">
        <h3 class="text-white font-bold flex items-center justify-between">
          <span class="flex items-center gap-2">
            <svg
              class="w-5 h-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
              />
            </svg>
            مخزن کلسیم (کودهای حاوی کلسیم)
          </span>
          <span class="text-xs bg-white/20 px-2 py-1 rounded-full">{{
            result.tank_calcium_result.tank_name
          }}</span>
        </h3>
      </div>

      <div class="p-5">
        <div class="overflow-x-auto mb-4">
          <table class="w-full text-sm border-collapse">
            <thead>
              <tr class="bg-gray-100">
                <th class="border border-gray-300 px-3 py-2 text-right">
                  نام کود
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  مصرف (g/L)
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  مجموع برای مخزن
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  مقدار برای استوک
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center"></th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="dose in result.tank_calcium_result.doses"
                :key="dose.name"
                class="hover:bg-gray-50"
              >
                <td class="border border-gray-300 px-3 py-2 font-medium">
                  {{ dose.persian_name || dose.name }}
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  {{ dose.dose_g_per_liter }} g/L
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  {{ formatNumber(dose.dose_g_for_tank) }} گرم
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  <span v-if="getStockAmount(dose) >= 1000"
                    >{{
                      (getStockAmount(dose) / 1000).toFixed(2)
                    }}
                    کیلوگرم</span
                  >
                  <span v-else-if="getStockAmount(dose) >= 1"
                    >{{ getStockAmount(dose).toFixed(0) }} گرم</span
                  >
                  <span v-else
                    >{{
                      (getStockAmount(dose) * 1000).toFixed(0)
                    }}
                    میلی‌گرم</span
                  >
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  <button
                    @click="showFertilizerDetail(dose.name)"
                    class="text-amber-600 hover:text-amber-800 transition"
                    title="مشاهده اطلاعات کامل کود"
                  >
                    <svg
                      class="w-5 h-5 inline"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <circle cx="12" cy="12" r="10" />
                      <path d="M12 16v-4M12 8h.01" />
                    </svg>
                    اطلاعات
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="grid grid-cols-2 gap-3 mb-4">
          <div class="bg-amber-50 rounded-lg p-3 text-center">
            <span class="font-bold text-amber-700">EC پیش‌بینی شده:</span>
            <span class="text-amber-700 font-bold mx-2"
              >{{ result.tank_calcium_result.target_ec || "---" }} mS/cm</span
            >
          </div>
          <div class="bg-amber-50 rounded-lg p-3 text-center">
            <span class="font-bold text-amber-700">pH هدف:</span>
            <span class="text-amber-700 font-bold mx-2">{{
              result.tank_calcium_result.target_ph || "6.0 - 6.5"
            }}</span>
          </div>
        </div>

        <div class="bg-purple-50 rounded-lg p-3 mb-3">
          <h4 class="font-medium text-purple-800 mb-2 flex items-center gap-1">
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
              />
            </svg>
            مرحله 1: ساخت استوک برای مخزن کلسیم
          </h4>
          <p class="text-sm text-gray-700 mb-2">
            برای ساخت {{ props.stockTankVolume || 20 }} لیتر استوک کلسیم با نسبت
            1:{{ props.injectorRatio || 200 }}، مقادیر زیر را با دقت اندازه گیری
            کنید:
          </p>
          <div class="bg-white rounded-lg p-3">
            <div
              v-for="dose in result.tank_calcium_result.doses"
              :key="dose.name"
              class="flex justify-between items-center py-1 border-b border-gray-100 last:border-0"
            >
              <span class="text-sm font-medium">{{
                dose.persian_name || dose.name
              }}</span>
              <span class="text-sm text-gray-600">
                <span v-if="getStockAmount(dose) >= 1000"
                  >{{ (getStockAmount(dose) / 1000).toFixed(2) }} کیلوگرم</span
                >
                <span v-else-if="getStockAmount(dose) >= 1"
                  >{{ getStockAmount(dose).toFixed(0) }} گرم</span
                >
                <span v-else
                  >{{ (getStockAmount(dose) * 1000).toFixed(0) }} میلی‌گرم</span
                >
              </span>
            </div>
          </div>
        </div>

        <div class="bg-green-50 rounded-lg p-3 mb-3">
          <h4 class="font-medium text-green-800 mb-2 flex items-center gap-1">
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            مرحله 2: مصرف استوک در مخزن کلسیم
          </h4>
          <div class="grid grid-cols-2 gap-3 mb-2">
            <div class="bg-white rounded-lg p-2 text-center">
              <p class="text-lg font-bold text-green-700">
                {{
                  (
                    (result.tank_calcium_result.tank_volume_liters || 0) /
                    (props.injectorRatio || 200)
                  ).toFixed(1)
                }}
                لیتر
              </p>
              <p class="text-xs text-gray-600">
                استوک برای مخزن
                {{
                  formatNumber(
                    result.tank_calcium_result.tank_volume_liters || 0,
                  )
                }}
                لیتری
              </p>
            </div>
            <div class="bg-white rounded-lg p-2 text-center">
              <p class="text-lg font-bold text-green-700">
                {{ (1000 / (props.injectorRatio || 200)).toFixed(1) }} میلی‌لیتر
              </p>
              <p class="text-xs text-gray-600">استوک برای هر 1 لیتر آب</p>
            </div>
          </div>
        </div>

        <div class="bg-red-50 rounded-lg p-3 mb-3">
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
            هیچگاه استوک مخزن کلسیم را با استوک مخزن اصلی قبل از ورود به مخزن
            اصلی مخلوط نکنید!
          </p>
        </div>

        <details class="mt-3">
          <summary
            class="cursor-pointer text-amber-600 hover:text-amber-700 font-medium text-sm inline-flex items-center gap-1"
          >
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            مشاهده دستورالعمل اختلاط مستقیم (بدون استوک) - مخزن کلسیم
          </summary>
          <div
            class="mt-3 p-4 bg-gray-100 rounded-lg text-sm whitespace-pre-line font-mono"
            v-html="
              formatInstructions(result.tank_calcium_result.mixing_instructions)
            "
          ></div>
        </details>
      </div>
    </div>

    <!-- نکات نگهداری و ایمنی استوک -->
    <div class="bg-yellow-50 rounded-xl p-4 border border-yellow-200">
      <h3 class="font-semibold text-yellow-800 mb-3 flex items-center gap-2">
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
        نکات نگهداری و ایمنی استوک
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
        <div class="bg-white rounded-lg p-2">
          <span class="font-bold">ماندگاری در یخچال:</span> 7 روز (دمای 4 درجه)
        </div>
        <div class="bg-white rounded-lg p-2">
          <span class="font-bold">ماندگاری در دمای محیط:</span> 3 روز (دمای زیر
          25 درجه)
        </div>
        <div class="bg-white rounded-lg p-2 col-span-2">
          <span class="font-bold">نشانه‌های خرابی:</span> رسوب سفید رنگ، تغییر
          رنگ، بوی نامطبوع، باد کردگی ظرف
        </div>
      </div>
    </div>

    <!-- مودال اطلاعات کامل کود -->
    <div
      v-if="selectedFertilizer"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      @click.self="selectedFertilizer = null"
    >
      <div
        class="bg-white rounded-2xl max-w-2xl w-full max-h-[85vh] overflow-hidden shadow-xl"
      >
        <div
          class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gradient-to-r from-green-600 to-teal-600"
        >
          <h3 class="text-lg font-semibold text-white">اطلاعات کامل کود</h3>
          <button
            @click="selectedFertilizer = null"
            class="text-white hover:text-gray-200 text-xl"
          >
            ✕
          </button>
        </div>
        <div class="p-6 overflow-y-auto max-h-[calc(85vh-70px)]">
          <div v-if="isLoadingFertilizerDetail" class="text-center py-8">
            <div
              class="inline-block w-8 h-8 border-2 border-green-500 border-t-transparent rounded-full animate-spin"
            ></div>
            <p class="mt-2 text-gray-500">در حال بارگذاری...</p>
          </div>
          <div v-else-if="fertilizerDetail" class="space-y-4">
            <div>
              <h4 class="font-bold text-gray-800 text-lg">
                {{ fertilizerDetail.persian_name || fertilizerDetail.name }}
              </h4>
              <div class="flex gap-2 mt-1">
                <span
                  class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full"
                  >{{ fertilizerDetail.brand_name }}</span
                >
                <span
                  class="text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full"
                  >{{ fertilizerDetail.fertilizer_type }}</span
                >
              </div>
            </div>

            <div class="border-t pt-3">
              <h5 class="font-semibold text-gray-700 mb-2">توضیحات</h5>
              <p class="text-sm text-gray-600 whitespace-pre-line">
                {{
                  fertilizerDetail.description ||
                  "توضیحاتی برای این کود ثبت نشده است"
                }}
              </p>
            </div>

            <div class="border-t pt-3">
              <h5 class="font-semibold text-gray-700 mb-2">ترکیبات شیمیایی</h5>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-2 text-sm">
                <div v-if="fertilizerDetail.n_percent">
                  N:
                  <span class="font-medium"
                    >{{ fertilizerDetail.n_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.p_percent">
                  P:
                  <span class="font-medium"
                    >{{ fertilizerDetail.p_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.k_percent">
                  K:
                  <span class="font-medium"
                    >{{ fertilizerDetail.k_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.ca_percent">
                  Ca:
                  <span class="font-medium"
                    >{{ fertilizerDetail.ca_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.mg_percent">
                  Mg:
                  <span class="font-medium"
                    >{{ fertilizerDetail.mg_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.s_percent">
                  S:
                  <span class="font-medium"
                    >{{ fertilizerDetail.s_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.fe_percent">
                  Fe:
                  <span class="font-medium"
                    >{{ fertilizerDetail.fe_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.zn_percent">
                  Zn:
                  <span class="font-medium"
                    >{{ fertilizerDetail.zn_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.mn_percent">
                  Mn:
                  <span class="font-medium"
                    >{{ fertilizerDetail.mn_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.cu_percent">
                  Cu:
                  <span class="font-medium"
                    >{{ fertilizerDetail.cu_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.b_percent">
                  B:
                  <span class="font-medium"
                    >{{ fertilizerDetail.b_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.mo_percent">
                  Mo:
                  <span class="font-medium"
                    >{{ fertilizerDetail.mo_percent }}%</span
                  >
                </div>
              </div>
            </div>

            <div class="border-t pt-3">
              <h5 class="font-semibold text-gray-700 mb-2">اطلاعات مصرف</h5>
              <div class="grid grid-cols-2 gap-2 text-sm">
                <div>
                  حداقل دوز:
                  <span class="font-medium"
                    >{{
                      fertilizerDetail.min_dose_g_per_liter || "نامشخص"
                    }}
                    g/L</span
                  >
                </div>
                <div>
                  حداکثر دوز:
                  <span class="font-medium"
                    >{{
                      fertilizerDetail.max_dose_g_per_liter || "نامشخص"
                    }}
                    g/L</span
                  >
                </div>
                <div v-if="fertilizerDetail.solubility_g_per_l">
                  حلالیت:
                  <span class="font-medium"
                    >{{ fertilizerDetail.solubility_g_per_l }} g/L</span
                  >
                </div>
                <div v-if="fertilizerDetail.ph_effect">
                  اثر بر pH:
                  <span class="font-medium">{{
                    fertilizerDetail.ph_effect
                  }}</span>
                </div>
              </div>
            </div>

            <div
              v-if="fertilizerDetail.registration_code"
              class="border-t pt-3"
            >
              <h5 class="font-semibold text-gray-700 mb-2">اطلاعات ثبتی</h5>
              <div class="text-sm">
                کد ثبت:
                <span class="font-mono">{{
                  fertilizerDetail.registration_code
                }}</span>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-500">
            اطلاعاتی برای این کود یافت نشد
          </div>
        </div>
      </div>
    </div>

    <!-- زمان محاسبه -->
    <div
      class="text-center text-xs text-gray-400 pt-4 border-t border-gray-100"
    >
      <svg
        class="w-4 h-4 inline ml-1"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      زمان محاسبه:
      {{ result.calculation_time_ms?.toFixed(0) || "0" }} میلی‌ثانیه
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import axios from "axios";

const props = defineProps<{
  result: any;
  stockTankVolume?: number;
  injectorRatio?: number;
}>();

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

const selectedFertilizer = ref<any>(null);
const fertilizerDetail = ref<any>(null);
const isLoadingFertilizerDetail = ref(false);
const allFertilizers = ref<any[]>([]);

const fetchAllFertilizers = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/fertilizers`);
    allFertilizers.value = response.data;
  } catch (err) {
    console.error("Error fetching fertilizers:", err);
  }
};

const showFertilizerDetail = async (fertilizerName: string) => {
  isLoadingFertilizerDetail.value = true;
  selectedFertilizer.value = { name: fertilizerName };
  fertilizerDetail.value = null;

  try {
    const found = allFertilizers.value.find(
      (f: any) => f.name === fertilizerName,
    );
    if (found) {
      fertilizerDetail.value = found;
    }
  } catch (err) {
    console.error("Error fetching fertilizer detail:", err);
  } finally {
    isLoadingFertilizerDetail.value = false;
  }
};

const getStockAmount = (dose: any) => {
  const doseGpl = dose.dose_g_per_liter || 0;
  const injectorRatio = props.injectorRatio || 200;
  const stockVolume = props.stockTankVolume || 20;
  const amountGram = doseGpl * injectorRatio * stockVolume;
  return amountGram;
};

const formatNumber = (num: number) => {
  if (!num && num !== 0) return "0";
  return new Intl.NumberFormat("fa-IR").format(Math.round(num));
};

const formatInstructions = (text: string) => {
  if (!text) return "";
  return text.replace(/\n/g, "<br>").replace(/\*/g, "•");
};

const getElementName = (element: string) => {
  const names: Record<string, string> = {
    n_no3: "نیترات (NO3)",
    p: "فسفر (P)",
    s: "گوگرد (S)",
    n_nh4: "آمونیوم (NH4)",
    k: "پتاسیم (K)",
    ca: "کلسیم (Ca)",
    mg: "منیزیم (Mg)",
    na: "سدیم (Na)",
    cl: "کلر (Cl)",
    fe: "آهن (Fe)",
    mn: "منگنز (Mn)",
    zn: "روی (Zn)",
    b: "بُر (B)",
    cu: "مس (Cu)",
    mo: "مولیبدن (Mo)",
    N: "نیتروژن (N)",
    P: "فسفر (P)",
    K: "پتاسیم (K)",
    Ca: "کلسیم (Ca)",
    Mg: "منیزیم (Mg)",
    Fe: "آهن (Fe)",
    Zn: "روی (Zn)",
    Mn: "منگنز (Mn)",
    B: "بُر (B)",
    Cu: "مس (Cu)",
    Mo: "مولیبدن (Mo)",
    Cl: "کلر (Cl)",
  };
  return names[element] || element;
};

const nutrientComparison = computed(() => {
  const elements = ["N", "P", "K", "Ca", "Mg", "Fe", "Zn", "Mn", "B"];

  const needs = props.result.custom_needs || props.result.target_needs || {};

  const suppliedMain = props.result.tank_main_result?.supplied_ppm || {};
  const suppliedCalcium = props.result.tank_calcium_result?.supplied_ppm || {};

  return elements.map((elem) => {
    const need = needs[elem] || 0;
    const supplied = (suppliedMain[elem] || 0) + (suppliedCalcium[elem] || 0);
    let status = "ok";
    if (need > 0) {
      const ratio = supplied / need;
      if (ratio < 0.7) status = "critical";
      else if (ratio < 0.9) status = "low";
      else status = "ok";
    }
    return { element: elem, need, supplied, status };
  });
});

// 🆕 آیتم‌های مقایسه آب و پساب
const waterComparisonItems = computed(() => {
  const elements = [
    "n_no3",
    "p",
    "s",
    "n_nh4",
    "k",
    "ca",
    "mg",
    "na",
    "cl",
    "fe",
    "mn",
    "zn",
    "b",
    "cu",
    "mo",
  ];

  const water = props.result.water_analysis?.combined_water || {};
  const deficit = props.result.water_analysis?.deficit || {};

  // دریافت آنالیز آب و پساب - از result نمی‌آیند، بنابراین از مقادیر نمونه استفاده می‌کنیم
  // در حالت واقعی، این داده‌ها باید از result بیایند
  const waterAnalysis = props.result.water_analysis?.water_analysis || {};
  const wastewaterAnalysis =
    props.result.water_analysis?.wastewater_analysis || {};

  return elements.map((elem) => {
    const waterVal = waterAnalysis[elem] || 0;
    const wastewaterVal = wastewaterAnalysis[elem] || 0;
    const combined = water[elem] || 0;
    const deficitVal = deficit[elem] || 0;

    return {
      element: elem,
      water: waterVal,
      wastewater: wastewaterVal,
      combined: combined,
      deficit: deficitVal,
    };
  });
});

onMounted(() => {
  fetchAllFertilizers();
});
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
  content: "📂 ";
  font-size: 14px;
}

details[open] summary::before {
  content: "📁 ";
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
    content: "📁 ";
  }

  .fixed {
    display: none !important;
  }
}
</style>
