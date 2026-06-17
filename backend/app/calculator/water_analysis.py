"""
🧪 آنالیز آب و پساب ترکیبی - نسخه 3.4.0
"""

from typing import Dict, List, Tuple, Optional

# ============================================================
# لیست کلیدهای استاندارد (با حروف کوچک)
# ============================================================

WATER_ANALYSIS_KEYS = [
    'n_no3',     # نیترات
    'p',         # فسفر
    's',         # گوگرد
    'n_nh4',     # آمونیوم
    'k',         # پتاسیم
    'ca',        # کلسیم
    'fe',        # آهن
    'mn',        # منگنز
    'zn',        # روی
    'b',         # بور
    'cu',        # مس
    'mo',        # مولیبدن
    'ec',        # هدایت الکتریکی
    'ph'         # اسیدیته
]

NUTRIENT_KEYS = [k for k in WATER_ANALYSIS_KEYS if k not in ['ec', 'ph']]


# ============================================================
# توابع اصلی
# ============================================================

def calculate_combined_water(
    water_percent: float,
    wastewater_percent: float,
    water_analysis: Dict[str, float],
    wastewater_analysis: Dict[str, float]
) -> Dict[str, float]:
    """محاسبه مقادیر ترکیبی آب و پساب"""
    combined = {}
    all_keys = set(water_analysis.keys()) | set(wastewater_analysis.keys())

    for key in all_keys:
        water_val = water_analysis.get(key, 0.0)
        waste_val = wastewater_analysis.get(key, 0.0)
        combined[key] = round((water_percent * water_val + wastewater_percent * waste_val) / 100.0, 2)

    return combined


def calculate_deficit(
    target_needs: Dict[str, float],
    combined_water: Dict[str, float]
) -> Dict[str, float]:
    """محاسبه کمبود عناصر"""
    deficit = {}
    for key, need in target_needs.items():
        water_val = combined_water.get(key, 0.0)
        deficit[key] = round(max(0.0, need - water_val), 2)
    return deficit


def get_remaining_needs(
    target_needs: Dict[str, float],
    combined_water: Dict[str, float]
) -> Dict[str, float]:
    """محاسبه نیاز باقیمانده"""
    return calculate_deficit(target_needs, combined_water)


def validate_water_percentages(water_percent: float, wastewater_percent: float) -> Tuple[bool, List[str]]:
    """اعتبارسنجی درصدها"""
    errors = []
    if water_percent < 0 or water_percent > 100:
        errors.append(f"درصد آب باید بین 0 تا 100 باشد: {water_percent}")
    if wastewater_percent < 0 or wastewater_percent > 100:
        errors.append(f"درصد پساب باید بین 0 تا 100 باشد: {wastewater_percent}")
    total = water_percent + wastewater_percent
    if abs(total - 100) > 0.01:
        errors.append(f"مجموع درصد آب و پساب باید 100 باشد: {total}")
    return len(errors) == 0, errors


def get_water_analysis_keys() -> List[str]:
    return WATER_ANALYSIS_KEYS.copy()


def normalize_analysis_keys(analysis: Dict[str, float]) -> Dict[str, float]:
    """
    نرمال‌سازی کلیدهای آنالیز (تبدیل به حروف کوچک)
    """
    result = {}
    for key, value in analysis.items():
        normalized_key = key.lower().strip()
        result[normalized_key] = value
    return result


# ============================================================
# 🆕 تابع اصلی محاسبه کامل (با خطاگیری دقیق)
# ============================================================

def calculate_complete_water_contribution(
    water_percent: float,
    wastewater_percent: float,
    water_analysis: Dict[str, float],
    wastewater_analysis: Dict[str, float],
    target_needs: Optional[Dict[str, float]] = None
) -> Dict:
    """
    محاسبه کامل ترکیب آب و پساب با گزارش خطاهای دقیق
    """
    errors = []
    warnings = []

    # 1. اعتبارسنجی درصدها
    is_valid, percent_errors = validate_water_percentages(water_percent, wastewater_percent)
    if not is_valid:
        errors.extend(percent_errors)

    # 2. نرمال‌سازی کلیدها
    water_analysis = normalize_analysis_keys(water_analysis)
    wastewater_analysis = normalize_analysis_keys(wastewater_analysis)

    # 3. بررسی وجود داده
    if not water_analysis:
        errors.append("آنالیز آب خالی است")
    if not wastewater_analysis:
        errors.append("آنالیز پساب خالی است")

    # 4. بررسی کلیدهای ناشناخته
    all_keys = set(water_analysis.keys()) | set(wastewater_analysis.keys())
    unknown_keys = [k for k in all_keys if k not in WATER_ANALYSIS_KEYS]
    if unknown_keys:
        warnings.append(f"کلیدهای ناشناخته: {unknown_keys}")

    if errors:
        return {
            "success": False,
            "errors": errors,
            "warnings": warnings,
            "combined_water": {},
            "deficit": {},
            "remaining_needs": {}
        }

    # 5. محاسبه ترکیبی
    combined_water = calculate_combined_water(
        water_percent,
        wastewater_percent,
        water_analysis,
        wastewater_analysis
    )

    result = {
        "success": True,
        "errors": [],
        "warnings": warnings,
        "combined_water": combined_water,
        "deficit": {},
        "remaining_needs": {}
    }

    # 6. محاسبه کمبود
    if target_needs:
        deficit = calculate_deficit(target_needs, combined_water)
        result["deficit"] = deficit
        result["remaining_needs"] = deficit

    return result


# ============================================================
# نمونه داده برای تست
# ============================================================

def get_sample_water_analysis() -> Dict[str, float]:
    return {
        'n_no3': 10.0, 'p': 2.0, 's': 5.0, 'n_nh4': 0.0,
        'k': 8.0, 'ca': 50.0, 'fe': 0.5, 'mn': 0.1,
        'zn': 0.05, 'b': 0.2, 'cu': 0.02, 'mo': 0.01,
        'ec': 0.4, 'ph': 7.0
    }


def get_sample_wastewater_analysis() -> Dict[str, float]:
    return {
        'n_no3': 25.0, 'p': 5.0, 's': 10.0, 'n_nh4': 2.0,
        'k': 15.0, 'ca': 80.0, 'fe': 1.0, 'mn': 0.3,
        'zn': 0.1, 'b': 0.5, 'cu': 0.05, 'mo': 0.02,
        'ec': 1.2, 'ph': 6.5
    }
