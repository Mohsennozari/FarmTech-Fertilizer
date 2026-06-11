from typing import List, Dict, Tuple, Optional
from .core import SUPPORTED_ELEMENTS, calculate_element_ppm
import numpy as np

# ============================================================
# توابع کمکی برای ترکیب چند کود NPK (مرحله 1)
# ============================================================

def is_npk_fertilizer(fertilizer) -> bool:
    """تشخیص اینکه آیا کود NPK است یا خیر"""
    fert_type = (fertilizer.fertilizer_type or "").upper()
    if fert_type == 'NPK' or 'NPK' in fert_type:
        return True

    has_n = (fertilizer.n_percent or 0) > 0
    has_p = (fertilizer.p_percent or 0) > 0
    has_k = (fertilizer.k_percent or 0) > 0

    return has_n and has_p and has_k


def generate_combinations(fertilizers, max_fertilizers=3):
    """تولید تمام ترکیب‌های ممکن از 1 تا max_fertilizers کود"""
    from itertools import combinations

    all_combinations = []
    for r in range(1, min(max_fertilizers, len(fertilizers)) + 1):
        for combo in combinations(fertilizers, r):
            all_combinations.append(list(combo))

    return all_combinations


def brute_force_optimization(fertilizers, needs, bounds, steps=10):
    """
    جستجوی شبکه‌ای برای ترکیب‌های کوچک (2-3 کود).

    برای 3 کود تعداد گام‌ها مستقل از حالت 2 کود تنظیم می‌شود
    تا دقت کافی حفظ شود.
    """
    best_doses = None
    best_error = float('inf')

    n = len(fertilizers)

    if n == 2:
        (min1, max1), (min2, max2) = bounds

        for i in range(steps + 1):
            dose1 = min1 + (max1 - min1) * i / steps
            for j in range(steps + 1):
                dose2 = min2 + (max2 - min2) * j / steps

                n_val = (dose1 * (fertilizers[0].n_percent or 0) +
                         dose2 * (fertilizers[1].n_percent or 0)) * 10
                p_val = (dose1 * (fertilizers[0].p_percent or 0) +
                         dose2 * (fertilizers[1].p_percent or 0)) * 10
                k_val = (dose1 * (fertilizers[0].k_percent or 0) +
                         dose2 * (fertilizers[1].k_percent or 0)) * 10

                error = ((needs.get('N', 0) - n_val) ** 2 +
                         (needs.get('P', 0) - p_val) ** 2 +
                         (needs.get('K', 0) - k_val) ** 2)

                if error < best_error:
                    best_error = error
                    best_doses = [dose1, dose2]

    elif n == 3:
        (min1, max1), (min2, max2), (min3, max3) = bounds

        # از تعداد گام مستقل استفاده می‌کنیم (نه نصف steps)
        # تا دقت قابل قبول داشته باشیم
        steps_3d = steps

        for i in range(steps_3d + 1):
            dose1 = min1 + (max1 - min1) * i / steps_3d
            for j in range(steps_3d + 1):
                dose2 = min2 + (max2 - min2) * j / steps_3d
                for k_idx in range(steps_3d + 1):
                    dose3 = min3 + (max3 - min3) * k_idx / steps_3d

                    n_val = (dose1 * (fertilizers[0].n_percent or 0) +
                             dose2 * (fertilizers[1].n_percent or 0) +
                             dose3 * (fertilizers[2].n_percent or 0)) * 10
                    p_val = (dose1 * (fertilizers[0].p_percent or 0) +
                             dose2 * (fertilizers[1].p_percent or 0) +
                             dose3 * (fertilizers[2].p_percent or 0)) * 10
                    k_val = (dose1 * (fertilizers[0].k_percent or 0) +
                             dose2 * (fertilizers[1].k_percent or 0) +
                             dose3 * (fertilizers[2].k_percent or 0)) * 10

                    error = ((needs.get('N', 0) - n_val) ** 2 +
                             (needs.get('P', 0) - p_val) ** 2 +
                             (needs.get('K', 0) - k_val) ** 2)

                    if error < best_error:
                        best_error = error
                        best_doses = [dose1, dose2, dose3]

    return best_doses, best_error


def build_combination_result(fertilizers, doses, needs):
    """ساخت خروجی استاندارد از ترکیب بهینه"""
    result_doses = []
    total_supply = {'N': 0.0, 'P': 0.0, 'K': 0.0}

    for fert, dose in zip(fertilizers, doses):
        if dose <= 0.01:
            continue

        result_doses.append({
            "id": fert.id,
            "name": fert.name,
            "brand_name": fert.brand_name,
            "dose_g_per_liter": round(dose, 3),
            "chemical_formula": fert.chemical_formula,
            "layer": "macro",
            "combination_order": len(result_doses) + 1
        })

        total_supply['N'] += dose * (fert.n_percent or 0) * 10
        total_supply['P'] += dose * (fert.p_percent or 0) * 10
        total_supply['K'] += dose * (fert.k_percent or 0) * 10

    total_supply = {k: round(v, 1) for k, v in total_supply.items()}

    return result_doses, total_supply


# ============================================================
# توابع بررسی حلالیت (مرحله 2)
# ============================================================

# ضریب حساسیت دمایی واقعی (Δحلالیت به ازای هر درجه سانتیگراد، نسبی)
# منبع: داده‌های تجربی کودهای رایج در هیدروپونیک
_SOLUBILITY_TEMP_COEFFICIENTS = {
    'calcium_nitrate':    0.010,   # حساسیت متوسط به دما
    'potassium_sulfate':  0.003,   # حساسیت پایین
    'magnesium_sulfate':  0.007,   # حساسیت متوسط
    'mkp':                0.005,   # حساسیت متوسط
    'potassium_nitrate':  0.013,   # حساسیت نسبتاً بالا
    'ammonium_nitrate':   0.020,   # حساسیت بالا
    'default':            0.005,
}

_DEFAULT_SOLUBILITY = {
    'calcium_nitrate':    1200,
    'potassium_sulfate':  120,
    'magnesium_sulfate':  350,
    'mkp':                230,
    'potassium_nitrate':  320,
    'ammonium_nitrate':   2000,
    'default':            400,
}


def _identify_fertilizer_key(fertilizer) -> str:
    """تشخیص کلید داخلی کود برای جداول پیش‌فرض"""
    name = (fertilizer.name or "").lower()
    if 'calcium' in name or 'نیترات کلسیم' in name:
        return 'calcium_nitrate'
    if 'potassium sulfate' in name or 'سولفات پتاسیم' in name:
        return 'potassium_sulfate'
    if 'magnesium sulfate' in name or 'سولفات منیزیم' in name:
        return 'magnesium_sulfate'
    if 'mkp' in name or 'monopotassium' in name:
        return 'mkp'
    if 'potassium nitrate' in name or 'نیترات پتاسیم' in name:
        return 'potassium_nitrate'
    if 'ammonium nitrate' in name or 'نیترات آمونیوم' in name:
        return 'ammonium_nitrate'
    return 'default'


def get_solubility_limit(fertilizer, temperature_c: float = 20.0) -> float:
    """
    برگرداندن حد حلالیت کود بر حسب g/L در دمای مشخص.

    اصلاح: هر نوع کود ضریب دمایی مخصوص خود را دارد
    (به جای یک ضریب ثابت ۰.۰۰۵ برای همه).
    """
    if hasattr(fertilizer, 'solubility_g_per_l') and fertilizer.solubility_g_per_l:
        base_solubility = fertilizer.solubility_g_per_l
    else:
        key = _identify_fertilizer_key(fertilizer)
        base_solubility = _DEFAULT_SOLUBILITY[key]

    if temperature_c != 20.0:
        key = _identify_fertilizer_key(fertilizer)
        coef = _SOLUBILITY_TEMP_COEFFICIENTS[key]
        temp_factor = 1 + (temperature_c - 20.0) * coef
        base_solubility = base_solubility * temp_factor

    return base_solubility


def check_solubility(fertilizer, proposed_dose: float, temperature_c: float = 20.0) -> Tuple[bool, float, str]:
    """بررسی اینکه دوز پیشنهادی از حد حلالیت تجاوز نمی‌کند"""
    solubility_limit = get_solubility_limit(fertilizer, temperature_c)

    if proposed_dose <= solubility_limit:
        return True, proposed_dose, ""

    max_safe_dose = solubility_limit * 0.95

    warning = (
        f"⚠️ دوز پیشنهادی {proposed_dose:.2f} g/L برای {fertilizer.name} "
        f"بیشتر از حد حلالیت ({solubility_limit:.0f} g/L) است. "
        f"حداکثر دوز قابل استفاده: {max_safe_dose:.2f} g/L"
    )

    return False, max_safe_dose, warning


def enforce_solubility_limit(doses: List[Dict], fertilizers: List, temperature_c: float = 20.0) -> Tuple[List[Dict], List[Dict]]:
    """اعمال محدودیت حلالیت روی لیست دوزها"""
    adjusted_doses = []
    solubility_warnings = []

    fert_map = {f.id: f for f in fertilizers}

    for dose in doses:
        fert = fert_map.get(dose.get('id'))
        if not fert:
            adjusted_doses.append(dose)
            continue

        proposed_dose = dose.get('dose_g_per_liter', 0)
        is_ok, max_dose, warning = check_solubility(fert, proposed_dose, temperature_c)

        if is_ok:
            adjusted_doses.append(dose)
        else:
            adjusted_dose = dose.copy()
            adjusted_dose['dose_g_per_liter'] = round(max_dose, 3)
            adjusted_dose['original_dose'] = round(proposed_dose, 3)
            adjusted_dose['solubility_limited'] = True
            adjusted_doses.append(adjusted_dose)

            solubility_warnings.append({
                "type": "solubility_limit",
                "severity": "warning",
                "fertilizer": fert.name,
                "message": warning,
                "original_dose": round(proposed_dose, 3),
                "adjusted_dose": round(max_dose, 3)
            })

    return adjusted_doses, solubility_warnings


# ============================================================
# توابع بهینه‌سازی با در نظر گرفتن حلالیت (مرحله 2)
# ============================================================

def optimize_single_fertilizer(fertilizer, needs, max_dose=3.0, temperature_c=20.0):
    """
    محاسبه دوز بهینه برای یک کود با حداقل‌سازی خطای least squares.

    اصلاح: به جای میانگین‌گیری ساده دوزها (که منطق نادرستی دارد)،
    از حل least squares استفاده می‌شود تا بهترین دوز واحد پیدا شود.
    """
    # ساخت بردار ضرایب برای N, P, K
    coeffs = np.array([
        (fertilizer.n_percent or 0) * 10,
        (fertilizer.p_percent or 0) * 10,
        (fertilizer.k_percent or 0) * 10,
    ])

    targets = np.array([
        needs.get('N', 0),
        needs.get('P', 0),
        needs.get('K', 0),
    ])

    norm_sq = np.dot(coeffs, coeffs)
    if norm_sq < 1e-9:
        # کود هیچ عنصر NPK ندارد
        return [0.01], float('inf')

    # دوز بهینه از حل least squares یک متغیره: dose = (c·t) / (c·c)
    proposed_dose = float(np.dot(coeffs, targets) / norm_sq)

    solubility_limit = get_solubility_limit(fertilizer, temperature_c)
    max_limit = min(fertilizer.max_dose_g_per_liter or 5.0, max_dose, solubility_limit)
    min_limit = fertilizer.min_dose_g_per_liter or 0.01
    final_dose = max(min_limit, min(proposed_dose, max_limit))

    supply = coeffs * final_dose
    error = float(np.sum((targets - supply) ** 2))

    return [final_dose], error


def optimize_combination(fertilizers, needs, max_total_dose=3.0, temperature_c=20.0):
    """پیدا کردن دوز بهینه برای یک ترکیب مشخص از کودها با در نظر گرفتن محدودیت حلالیت"""
    if len(fertilizers) == 1:
        return optimize_single_fertilizer(fertilizers[0], needs, max_total_dose, temperature_c)

    try:
        from scipy.optimize import minimize

        n_fert = len(fertilizers)

        def cost_function(doses):
            total_n = sum(doses[i] * (fertilizers[i].n_percent or 0) * 10 for i in range(n_fert))
            total_p = sum(doses[i] * (fertilizers[i].p_percent or 0) * 10 for i in range(n_fert))
            total_k = sum(doses[i] * (fertilizers[i].k_percent or 0) * 10 for i in range(n_fert))

            penalty = sum(
                max(0, doses[i] - get_solubility_limit(fertilizers[i], temperature_c)) * 1000
                for i in range(n_fert)
            )

            return (
                (needs.get('N', 0) - total_n) ** 2 +
                (needs.get('P', 0) - total_p) ** 2 +
                (needs.get('K', 0) - total_k) ** 2 +
                penalty
            )

        bounds = []
        for fert in fertilizers:
            min_dose = fert.min_dose_g_per_liter or 0.01
            solubility_limit = get_solubility_limit(fert, temperature_c)
            max_dose = min(fert.max_dose_g_per_liter or 5.0, max_total_dose, solubility_limit)
            bounds.append((min_dose, max(min_dose, max_dose)))

        initial_doses = [0.5] * n_fert
        result = minimize(cost_function, initial_doses, bounds=bounds, method='L-BFGS-B')

        if result.success:
            return list(result.x), result.fun
        else:
            bounds_for_brute = []
            for fert in fertilizers:
                min_dose = fert.min_dose_g_per_liter or 0.01
                sol = get_solubility_limit(fert, temperature_c)
                max_dose = min(fert.max_dose_g_per_liter or 5.0, max_total_dose, sol)
                bounds_for_brute.append((min_dose, max(min_dose, max_dose)))
            return brute_force_optimization(fertilizers, needs, bounds_for_brute)

    except ImportError:
        bounds = []
        for fert in fertilizers:
            min_dose = fert.min_dose_g_per_liter or 0.01
            sol = get_solubility_limit(fert, temperature_c)
            max_dose = min(fert.max_dose_g_per_liter or 5.0, max_total_dose, sol)
            bounds.append((min_dose, max(min_dose, max_dose)))
        return brute_force_optimization(fertilizers, needs, bounds)


def solve_macro_layer_combined(needs: Dict[str, float], macro_fertilizers: List, max_total_dose: float = 3.0, temperature_c: float = 20.0) -> Tuple[List[Dict], Dict[str, float]]:
    """انتخاب ترکیبی از چند کود NPK برای تأمین دقیق N, P, K با در نظر گرفتن محدودیت حلالیت"""
    if len(macro_fertilizers) == 0:
        return [], {'N': 0.0, 'P': 0.0, 'K': 0.0}

    if len(macro_fertilizers) == 1:
        doses, _ = optimize_single_fertilizer(macro_fertilizers[0], needs, max_total_dose, temperature_c)
        return build_combination_result(macro_fertilizers, doses, needs)

    best_combination = None
    best_doses = None
    best_error = float('inf')

    combinations = generate_combinations(macro_fertilizers, max_fertilizers=3)

    if len(combinations) > 100:
        combinations = sorted(combinations, key=len)[:100]

    for combo in combinations:
        doses, error = optimize_combination(combo, needs, max_total_dose, temperature_c)
        if error < best_error:
            best_error = error
            best_combination = combo
            best_doses = doses

    if best_combination is None:
        doses, _ = optimize_single_fertilizer(macro_fertilizers[0], needs, max_total_dose, temperature_c)
        return build_combination_result([macro_fertilizers[0]], doses, needs)

    return build_combination_result(best_combination, best_doses, needs)


# ============================================================
# مرحله 5: انتخاب هوشمند ریز مغذی
# ============================================================

# ضرایب اهمیت عناصر ریز مغذی در مراحل مختلف رشد
MICRO_NUTRIENT_WEIGHTS = {
    "vegetative": {
        "Fe": 0.30, "Zn": 0.15, "Mn": 0.15, "Cu": 0.10, "B": 0.15, "Mo": 0.10, "Cl": 0.05
    },
    "flowering": {
        "Fe": 0.20, "Zn": 0.20, "Mn": 0.15, "Cu": 0.15, "B": 0.20, "Mo": 0.05, "Cl": 0.05
    },
    "fruiting": {
        "Fe": 0.25, "Zn": 0.20, "Mn": 0.15, "Cu": 0.10, "B": 0.15, "Mo": 0.10, "Cl": 0.05
    },
    "default": {
        "Fe": 0.25, "Zn": 0.17, "Mn": 0.15, "Cu": 0.11, "B": 0.17, "Mo": 0.08, "Cl": 0.07
    }
}


def score_micro_fertilizer(fertilizer, needs, growth_stage: str = None) -> float:
    """
    محاسبه امتیاز یک کود ریز مغذی بر اساس تطابق با نیازها

    Args:
        fertilizer: کود ریز مغذی
        needs: نیازهای عناصر (دیکشنری)
        growth_stage: مرحله رشد (برای وزن‌دهی)

    Returns:
        امتیاز (عدد بالاتر = بهتر)
    """
    weights = MICRO_NUTRIENT_WEIGHTS.get(growth_stage, MICRO_NUTRIENT_WEIGHTS["default"])

    total_score = 0.0
    total_need = 0.0

    for elem, weight in weights.items():
        need = needs.get(elem, 0)
        if need <= 0:
            continue

        total_need += need * weight

        elem_percent = getattr(fertilizer, f"{elem.lower()}_percent", 0) or 0

        if elem_percent > 0:
            max_dose = min(fertilizer.max_dose_g_per_liter or 0.5, 0.5)
            max_supply = max_dose * elem_percent * 10

            if max_supply >= need:
                contribution = need * weight
            else:
                contribution = max_supply * weight

            total_score += contribution

    if total_need > 0:
        final_score = total_score / total_need
    else:
        final_score = 0.5

    # پنالتی برای عناصری که نیاز نیست اما در کود موجودند
    penalty = 0
    for elem in weights.keys():
        elem_percent = getattr(fertilizer, f"{elem.lower()}_percent", 0) or 0
        need = needs.get(elem, 0)

        if need <= 0 and elem_percent > 0.1:
            penalty += 0.1

    final_score = max(0, min(1, final_score - penalty))

    return final_score


def select_best_micro_fertilizer(needs: Dict[str, float], micro_fertilizers: List, growth_stage: str = None) -> Tuple[object, float, Dict, float]:
    """
    انتخاب بهترین کود ریز مغذی بر اساس امتیازدهی هوشمند

    Args:
        needs: نیازهای عناصر ریز مغذی
        micro_fertilizers: لیست کودهای ریز مغذی موجود
        growth_stage: مرحله رشد (برای وزن‌دهی)

    Returns:
        (best_fertilizer, dose, supply, score)
    """
    if not micro_fertilizers:
        return None, 0, {}, 0

    best_fert = None
    best_dose = 0
    best_supply = {}
    best_score = -1

    for fert in micro_fertilizers:
        score = score_micro_fertilizer(fert, needs, growth_stage)

        required_dose = 0
        for elem in ['Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']:
            need = needs.get(elem, 0)
            if need > 0:
                elem_percent = getattr(fert, f"{elem.lower()}_percent", 0) or 0
                if elem_percent > 0:
                    dose_for_elem = need / (elem_percent * 10)
                    required_dose = max(required_dose, dose_for_elem)

        max_dose = min(fert.max_dose_g_per_liter or 0.5, 0.5)
        min_dose = fert.min_dose_g_per_liter or 0.01
        final_dose = max(min_dose, min(required_dose, max_dose))

        supply = calculate_element_ppm(fert, final_dose)

        if score > best_score:
            best_score = score
            best_fert = fert
            best_dose = final_dose
            best_supply = supply

    return best_fert, best_dose, best_supply, best_score


def select_multiple_micro_fertilizers(needs: Dict[str, float], micro_fertilizers: List, growth_stage: str = None) -> List[Tuple[object, float, Dict]]:
    """
    انتخاب ترکیبی از چند کود ریز مغذی برای پوشش بهتر نیازها.

    در صورت وجود کودهای تخصصی (مثل کود فقط آهن، فقط روی) از ترکیب آنها استفاده می‌کند.
    """
    if not micro_fertilizers:
        return []

    specialized = []
    complete = []

    for fert in micro_fertilizers:
        element_count = sum(
            1 for elem in ['Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']
            if (getattr(fert, f"{elem.lower()}_percent", 0) or 0) > 0
        )
        if element_count <= 2:
            specialized.append(fert)
        else:
            complete.append(fert)

    results = []
    remaining_needs = needs.copy()

    for fert in specialized:
        for elem in ['Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']:
            need = remaining_needs.get(elem, 0)
            if need <= 0:
                continue

            elem_percent = getattr(fert, f"{elem.lower()}_percent", 0) or 0
            if elem_percent > 0:
                dose = need / (elem_percent * 10)
                max_dose = min(fert.max_dose_g_per_liter or 0.5, 0.5)
                min_dose = fert.min_dose_g_per_liter or 0.01
                final_dose = max(min_dose, min(dose, max_dose))

                if final_dose >= min_dose:
                    supply = calculate_element_ppm(fert, final_dose)
                    results.append((fert, final_dose, supply))

                    for e, val in supply.items():
                        remaining_needs[e] = max(0, remaining_needs.get(e, 0) - val)

    if any(remaining_needs.get(e, 0) > 0.1 for e in ['Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']):
        if complete:
            best_fert, best_dose, best_supply, score = select_best_micro_fertilizer(
                remaining_needs, complete, growth_stage
            )
            if best_fert:
                results.append((best_fert, best_dose, best_supply))

    results = [(f, d, s) for f, d, s in results if d >= 0.005]

    return results


# ============================================================
# توابع اصلی
# ============================================================

def select_best_fertilizer_for_macro(needs: Dict[str, float], fertilizers: List) -> Tuple[object, float, Dict]:
    """نسخه قدیمی - حفظ شده برای سازگاری (fallback)"""
    best_fertilizer = None
    best_score = float('inf')
    best_dose = 0
    best_supply = {}

    for fert in fertilizers:
        # استفاده از least squares یک متغیره (مشابه optimize_single_fertilizer)
        coeffs = np.array([
            (fert.n_percent or 0) * 10,
            (fert.p_percent or 0) * 10,
            (fert.k_percent or 0) * 10,
        ])
        targets = np.array([needs.get('N', 0), needs.get('P', 0), needs.get('K', 0)])
        norm_sq = float(np.dot(coeffs, coeffs))

        if norm_sq < 1e-9:
            continue

        proposed_dose = float(np.dot(coeffs, targets) / norm_sq)
        max_dose = fert.max_dose_g_per_liter or 5.0
        min_dose = fert.min_dose_g_per_liter or 0.01
        proposed_dose = max(min_dose, min(proposed_dose, max_dose))

        supply = calculate_element_ppm(fert, proposed_dose)

        error = sum((needs.get(e, 0) - supply.get(e, 0)) ** 2 for e in ['N', 'P', 'K'])

        if error < best_score:
            best_score = error
            best_fertilizer = fert
            best_dose = proposed_dose
            best_supply = supply

    return best_fertilizer, best_dose, best_supply


def select_best_fertilizer_for_secondary(needs: Dict[str, float], fertilizers: List) -> List[Tuple[object, float, Dict]]:
    """
    انتخاب بهترین کود برای هر عنصر ثانویه (Ca, Mg, S).

    اصلاح: تأمین عناصر جانبی (مثل N در نیترات کلسیم) هم در supply
    ثبت می‌شود تا از دوبل‌شماری در لایه بالاتر جلوگیری شود.
    """
    results = []

    for elem in ['Ca', 'Mg', 'S']:
        need = needs.get(elem, 0)
        if need <= 0.5:
            continue

        best_fert = None
        best_dose = 0
        best_supply = {}
        best_error = float('inf')

        for fert in fertilizers:
            elem_percent = getattr(fert, f"{elem.lower()}_percent", 0) or 0
            if elem_percent <= 0:
                continue

            required_dose = need / (elem_percent * 10)
            max_dose = fert.max_dose_g_per_liter or 5.0
            min_dose = fert.min_dose_g_per_liter or 0.01
            final_dose = max(min_dose, min(required_dose, max_dose))

            # همه عناصر تأمین‌شده توسط این کود را ثبت کن (نه فقط elem)
            full_supply = calculate_element_ppm(fert, final_dose)
            supplied = full_supply.get(elem, 0)
            error = abs(need - supplied)

            if error < best_error:
                best_error = error
                best_fert = fert
                best_dose = final_dose
                best_supply = full_supply   # ← تمام عناصر، نه فقط elem

        if best_fert:
            results.append((best_fert, best_dose, best_supply))

    return results


def solve_macro_layer(
    needs: Dict[str, float],
    fertilizers: List,
    max_total_dose: float = 3.0,
    temperature_c: float = 20.0
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    """حل لایه NPK با قابلیت ترکیب چند کود و بررسی حلالیت"""
    macro_elements = ['N', 'P', 'K']
    warnings = []

    macro_fertilizers = [f for f in fertilizers if is_npk_fertilizer(f)]

    if not macro_fertilizers:
        for f in fertilizers:
            if (f.n_percent or 0) > 0 or (f.p_percent or 0) > 0 or (f.k_percent or 0) > 0:
                macro_fertilizers.append(f)
                break

    if not macro_fertilizers:
        warnings.append({
            "type": "missing_fertilizers",
            "severity": "warning",
            "message": "هیچ کود NPK مناسبی یافت نشد. لطفاً کودهای NPK را به دیتابیس اضافه کنید."
        })
        return [], {e: 0.0 for e in macro_elements}, warnings

    try:
        result_doses, total_supply = solve_macro_layer_combined(
            needs, macro_fertilizers, max_total_dose, temperature_c
        )

        result_doses, solubility_warnings = enforce_solubility_limit(
            result_doses, macro_fertilizers, temperature_c
        )
        warnings.extend(solubility_warnings)

        if len(result_doses) > 1:
            warnings.append({
                "type": "combination_used",
                "severity": "info",
                "message": f"از ترکیب {len(result_doses)} کود NPK برای تأمین دقیق‌تر استفاده شده است."
            })

        for elem in macro_elements:
            need = needs.get(elem, 0)
            supply = total_supply.get(elem, 0)
            if need > 10 and abs(need - supply) > need * 0.2:
                warnings.append({
                    "type": "high_error",
                    "severity": "warning",
                    "message": f"خطای تأمین {elem}: نیاز {need} ppm، تأمین {supply} ppm (خطای {abs(need - supply):.0f} ppm)"
                })

        return result_doses, total_supply, warnings

    except Exception as e:
        warnings.append({
            "type": "fallback_used",
            "severity": "warning",
            "message": f"خطا در بهینه‌سازی ترکیبی: {str(e)}. از روش ساده استفاده می‌شود."
        })

        best_fert, best_dose, best_supply = select_best_fertilizer_for_macro(needs, macro_fertilizers)

        if not best_fert:
            return [], {e: 0.0 for e in macro_elements}, warnings

        is_ok, max_dose, sol_warning = check_solubility(best_fert, best_dose, temperature_c)
        if not is_ok:
            best_dose = max_dose
            warnings.append({
                "type": "solubility_limit",
                "severity": "warning",
                "message": sol_warning
            })
            best_supply = calculate_element_ppm(best_fert, best_dose)

        result_doses = [{
            "id": best_fert.id,
            "name": best_fert.name,
            "brand_name": best_fert.brand_name,
            "dose_g_per_liter": round(best_dose, 3),
            "chemical_formula": best_fert.chemical_formula,
            "layer": "macro"
        }]

        final_supply = {e: best_supply.get(e, 0.0) for e in macro_elements}

        return result_doses, final_supply, warnings


def solve_secondary_layer(
    needs: Dict[str, float],
    fertilizers: List,
    max_total_dose: float = 2.0
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    """
    حل لایه عناصر ثانویه (Ca, Mg, S).

    اصلاح: فیلتر نوع کود گسترش یافته تا انواع رایج کودهای Ca/Mg/S
    (مثل 'ثانویه'، 'کلات'، 'تک عنصری') شامل شوند.
    """
    secondary_elements = ['Ca', 'Mg', 'S']
    warnings = []

    # انواع کودهایی که ممکن است Ca, Mg, S داشته باشند
    valid_types = {'تک عنصری', 'NPK', 'ثانویه', 'کلات', 'secondary', 'single'}
    secondary_fertilizers = [
        f for f in fertilizers
        if (f.fertilizer_type or '') in valid_types
        or (f.ca_percent or 0) > 0
        or (f.mg_percent or 0) > 0
        or (f.s_percent or 0) > 0
    ]

    if not secondary_fertilizers:
        warnings.append({
            "type": "missing_fertilizers",
            "severity": "warning",
            "message": "هیچ کود حاوی عناصر ثانویه (Ca, Mg, S) یافت نشد"
        })
        return [], {e: 0.0 for e in secondary_elements}, warnings

    selected = select_best_fertilizer_for_secondary(needs, secondary_fertilizers)

    result_doses = []
    final_supply = {e: 0.0 for e in secondary_elements}

    for fert, dose, supply in selected:
        result_doses.append({
            "id": fert.id,
            "name": fert.name,
            "brand_name": fert.brand_name,
            "dose_g_per_liter": round(dose, 3),
            "chemical_formula": fert.chemical_formula,
            "layer": "secondary"
        })
        for elem in secondary_elements:
            val = supply.get(elem, 0)
            if val:
                final_supply[elem] += val

    return result_doses, final_supply, warnings


# ============================================================
# حل لایه ریز مغذی با انتخاب هوشمند (مرحله 5)
# ============================================================

def solve_micro_layer(
    needs: Dict[str, float],
    fertilizers: List,
    max_dose: float = 0.5,
    growth_stage: str = None
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    """
    حل لایه ریز مغذی با انتخاب هوشمند.

    Args:
        needs: نیازهای عناصر ریز مغذی
        fertilizers: لیست تمام کودها
        max_dose: حداکثر دوز مجاز (g/L)
        growth_stage: مرحله رشد (برای وزن‌دهی)
    """
    micro_elements = ['Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']
    warnings = []

    micro_fertilizers = [f for f in fertilizers if f.fertilizer_type == 'ریزمغذی']

    if not micro_fertilizers:
        warnings.append({
            "type": "missing_fertilizers",
            "severity": "warning",
            "message": "هیچ کود ریز مغذی در دیتابیس یافت نشد"
        })
        return [], {e: 0.0 for e in micro_elements}, warnings

    selected_fertilizers = select_multiple_micro_fertilizers(needs, micro_fertilizers, growth_stage)

    result_doses = []
    final_supply = {e: 0.0 for e in micro_elements}

    for fert, dose, supply in selected_fertilizers:
        # اصلاح: روش انتخاب صرفاً بر اساس مسیر واقعی تعیین می‌شود
        result_doses.append({
            "id": fert.id,
            "name": fert.name,
            "brand_name": fert.brand_name,
            "dose_g_per_liter": round(dose, 3),
            "chemical_formula": fert.chemical_formula,
            "layer": "micro",
            "selection_method": "smart"
        })

        for elem, val in supply.items():
            if elem in final_supply:
                final_supply[elem] += val

    # fallback اگر هیچ کودی انتخاب نشد
    if not result_doses and micro_fertilizers:
        micro_fert = micro_fertilizers[0]

        required_dose = 0
        for elem in micro_elements:
            need = needs.get(elem, 0)
            if need > 0:
                elem_percent = getattr(micro_fert, f"{elem.lower()}_percent", 0) or 0
                if elem_percent > 0:
                    dose_for_elem = need / (elem_percent * 10)
                    required_dose = max(required_dose, dose_for_elem)

        dose = max(0.01, min(required_dose, max_dose))

        content = calculate_element_ppm(micro_fert, dose)
        final_supply = {e: content.get(e, 0.0) for e in micro_elements}

        result_doses = [{
            "id": micro_fert.id,
            "name": micro_fert.name,
            "brand_name": micro_fert.brand_name,
            "dose_g_per_liter": round(dose, 3),
            "chemical_formula": micro_fert.chemical_formula,
            "layer": "micro",
            "selection_method": "fallback"
        }]

        warnings.append({
            "type": "micro_fallback",
            "severity": "info",
            "message": f"از روش انتخاب سنتی برای کود {micro_fert.name} استفاده شد."
        })

    if len(selected_fertilizers) > 1:
        warnings.append({
            "type": "micro_combination",
            "severity": "info",
            "message": f"از ترکیب {len(selected_fertilizers)} کود ریز مغذی برای پوشش بهتر نیازها استفاده شده است."
        })

    uncovered = [
        elem for elem in micro_elements
        if needs.get(elem, 0) > 0.1 and final_supply.get(elem, 0) < needs.get(elem, 0) * 0.5
    ]

    if uncovered:
        warnings.append({
            "type": "partial_coverage",
            "severity": "warning",
            "message": f"عناصر ریز مغذی به طور کامل تامین نشدند: {', '.join(uncovered)}. می‌توانید از کودهای تخصصی استفاده کنید.",
            "fertilizers": [d['name'] for d in result_doses]
        })

    return result_doses, final_supply, warnings


def optimize_fertilizer_doses_professional(
    remaining_needs: Dict[str, float],
    fertilizers: List,
    brand_filter: Optional[str] = None,
    max_total_dose: float = 5.0,
    temperature_c: float = 20.0,
    growth_stage: str = None
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    """الگوریتم لایه‌به‌لایه - NPK → Secondary → Micro با پشتیبانی از دما و مرحله رشد"""

    final_supply = {elem: 0.0 for elem in SUPPORTED_ELEMENTS}

    if not fertilizers:
        return [], final_supply, []

    if brand_filter:
        fertilizers = [f for f in fertilizers if f.brand_name == brand_filter]
        if not fertilizers:
            return [], final_supply, [{
                "type": "brand_filter",
                "severity": "warning",
                "message": f"هیچ کودی برای برند {brand_filter} یافت نشد"
            }]

    all_warnings = []
    all_doses = []

    # مرحله 1: NPK
    macro_needs = {elem: remaining_needs.get(elem, 0) for elem in ['N', 'P', 'K']}
    macro_doses, macro_supply, macro_warnings = solve_macro_layer(
        macro_needs, fertilizers, 3.0, temperature_c
    )
    all_doses.extend(macro_doses)
    all_warnings.extend(macro_warnings)

    for elem, value in macro_supply.items():
        final_supply[elem] = final_supply.get(elem, 0.0) + value

    remaining = {
        elem: max(0, remaining_needs.get(elem, 0) - final_supply.get(elem, 0))
        for elem in SUPPORTED_ELEMENTS
    }

    # مرحله 2: Ca, Mg, S
    secondary_needs = {elem: remaining.get(elem, 0) for elem in ['Ca', 'Mg', 'S']}
    secondary_doses, secondary_supply, secondary_warnings = solve_secondary_layer(
        secondary_needs, fertilizers, 2.0
    )
    all_doses.extend(secondary_doses)
    all_warnings.extend(secondary_warnings)

    for elem, value in secondary_supply.items():
        final_supply[elem] = final_supply.get(elem, 0.0) + value

    for elem in SUPPORTED_ELEMENTS:
        remaining[elem] = max(0, remaining.get(elem, 0) - secondary_supply.get(elem, 0))

    # مرحله 3: ریز مغذی‌ها
    micro_needs = {elem: remaining.get(elem, 0) for elem in ['Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']}
    micro_doses, micro_supply, micro_warnings = solve_micro_layer(
        micro_needs, fertilizers, 0.5, growth_stage
    )
    all_doses.extend(micro_doses)
    all_warnings.extend(micro_warnings)

    for elem, value in micro_supply.items():
        final_supply[elem] = final_supply.get(elem, 0.0) + value

    # ادغام دوزهای تکراری (بر اساس id کود)
    unique_doses: Dict[str, Dict] = {}
    for dose in all_doses:
        key = dose.get('id') or dose['name']
        if key in unique_doses:
            unique_doses[key]['dose_g_per_liter'] += dose['dose_g_per_liter']
        else:
            unique_doses[key] = dose.copy()

    result_doses = list(unique_doses.values())
    result_doses.sort(key=lambda x: x['dose_g_per_liter'], reverse=True)

    for dose in result_doses:
        dose['dose_g_per_liter'] = round(dose['dose_g_per_liter'], 3)

    uncovered = [
        elem for elem in SUPPORTED_ELEMENTS
        if elem in ['N', 'P', 'K', 'Ca', 'Mg']
        and remaining_needs.get(elem, 0) > 10.0
        and final_supply.get(elem, 0) < remaining_needs.get(elem, 0) * 0.5
    ]

    if uncovered:
        all_warnings.append({
            "type": "partial_coverage",
            "severity": "info",
            "message": f"عناصر زیر به طور کامل تامین نشدند: {', '.join(uncovered)}. می‌توانید نیازها را به صورت دستی تنظیم کنید."
        })

    return result_doses, final_supply, all_warnings
