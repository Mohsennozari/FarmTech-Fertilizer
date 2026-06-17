# backend/app/calculator/ion_balance.py

from typing import Dict, List, Tuple, Optional

# ============================================================
# لیست عناصر ۱۶ گانه
# ============================================================

ELEMENTS_16 = [
    'N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl',
    'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo'
]

# ============================================================
# ثابت‌های مربوط به عناصر برای تبدیل به MEQ
# ============================================================

# جرم اتمی و ظرفیت هر عنصر (برای تبدیل PPM به MEQ)
ELEMENT_MEQ_CONSTANTS = {
    'N-NO3': {'atomic_mass': 62.0, 'valence': 1},
    'N-NH4': {'atomic_mass': 18.0, 'valence': 1},
    'P': {'atomic_mass': 31.0, 'valence': 1.8},
    'S': {'atomic_mass': 32.1, 'valence': 2},
    'K': {'atomic_mass': 39.1, 'valence': 1},
    'Ca': {'atomic_mass': 40.1, 'valence': 2},
    'Mg': {'atomic_mass': 24.3, 'valence': 2},
    'Na': {'atomic_mass': 23.0, 'valence': 1},
    'Cl': {'atomic_mass': 35.5, 'valence': 1},
    'Fe': {'atomic_mass': 55.8, 'valence': 2},
    'Mn': {'atomic_mass': 54.9, 'valence': 2},
    'Zn': {'atomic_mass': 65.4, 'valence': 2},
    'B': {'atomic_mass': 10.8, 'valence': 0.5},
    'Cu': {'atomic_mass': 63.5, 'valence': 2},
    'Mo': {'atomic_mass': 95.9, 'valence': 6}
}

# لیست کاتیون‌ها (بار مثبت)
CATIONS = ['K', 'Ca', 'Mg', 'Na', 'N-NH4']

# لیست آنیون‌ها (بار منفی)
ANIONS = ['N-NO3', 'P', 'S', 'Cl']

# نگاشت بین نام‌های ۱۶ گانه و کلیدهای ساده
ELEMENT_16_TO_SIMPLE = {
    'N-NO3': 'N-NO3',
    'N-NH4': 'N-NH4',
    'P': 'P',
    'S': 'S',
    'K': 'K',
    'Ca': 'Ca',
    'Mg': 'Mg',
    'Na': 'Na',
    'Cl': 'Cl',
    'Fe': 'Fe',
    'Mn': 'Mn',
    'Zn': 'Zn',
    'B': 'B',
    'Cu': 'Cu',
    'Mo': 'Mo'
}


def ppm_to_meq(ppm: float, element: str) -> float:
    if ppm <= 0:
        return 0.0
    constants = ELEMENT_MEQ_CONSTANTS.get(element)
    if not constants:
        return 0.0
    atomic_mass = constants['atomic_mass']
    valence = constants['valence']
    if atomic_mass <= 0:
        return 0.0
    meq = (ppm * valence) / atomic_mass
    return round(meq, 4)


def calculate_cation_meq(elements_ppm: Dict[str, float]) -> float:
    total = 0.0
    for cation in CATIONS:
        value = 0.0
        if cation in elements_ppm:
            value = elements_ppm[cation]
        elif cation in ELEMENT_16_TO_SIMPLE and ELEMENT_16_TO_SIMPLE[cation] in elements_ppm:
            value = elements_ppm[ELEMENT_16_TO_SIMPLE[cation]]
        else:
            continue
        meq = ppm_to_meq(value, cation)
        total += meq
    return round(total, 4)


def calculate_anion_meq(elements_ppm: Dict[str, float]) -> float:
    total = 0.0
    for anion in ANIONS:
        value = 0.0
        if anion in elements_ppm:
            value = elements_ppm[anion]
        elif anion in ELEMENT_16_TO_SIMPLE and ELEMENT_16_TO_SIMPLE[anion] in elements_ppm:
            value = elements_ppm[ELEMENT_16_TO_SIMPLE[anion]]
        else:
            continue
        meq = ppm_to_meq(value, anion)
        total += meq
    return round(total, 4)


def calculate_ion_balance(elements_ppm: Dict[str, float]) -> Tuple[float, float, float, bool, Optional[str]]:
    cation = calculate_cation_meq(elements_ppm)
    anion = calculate_anion_meq(elements_ppm)

    if cation == 0 and anion == 0:
        return 0.0, 0.0, 0.0, True, "هیچ داده‌ای برای محاسبه تعادل وجود ندارد."

    max_val = max(cation, anion)
    if max_val == 0:
        return cation, anion, 0.0, True, None

    diff = abs(cation - anion)
    diff_percent = (diff / max_val) * 100

    is_balanced = diff_percent <= 5.0

    warning_message = None
    if not is_balanced:
        if cation > anion:
            warning_message = f"⚠️ کاتیون‌ها ({cation:.2f} MEQ/L) بیشتر از آنیون‌ها ({anion:.2f} MEQ/L) هستند. اختلاف: {diff_percent:.1f}%"
        else:
            warning_message = f"⚠️ آنیون‌ها ({anion:.2f} MEQ/L) بیشتر از کاتیون‌ها ({cation:.2f} MEQ/L) هستند. اختلاف: {diff_percent:.1f}%"
        if diff_percent > 10:
            warning_message += " (اختلاف بحرانی! لطفاً مقادیر را تنظیم کنید.)"

    return cation, anion, diff_percent, is_balanced, warning_message


def get_ion_balance_summary(target_elements: Dict[str, float], final_solution: Dict[str, float]) -> Dict[str, any]:
    target_cation, target_anion, target_diff, target_balanced, target_warning = calculate_ion_balance(target_elements)
    final_cation, final_anion, final_diff, final_balanced, final_warning = calculate_ion_balance(final_solution)

    interpretation = []
    interpretation.append("=" * 50)
    interpretation.append("📊 گزارش تعادل یونی")
    interpretation.append("=" * 50)
    interpretation.append("\n🔹 عناصر هدف (Target):")
    interpretation.append(f"   کاتیون‌ها: {target_cation:.2f} MEQ/L")
    interpretation.append(f"   آنیون‌ها: {target_anion:.2f} MEQ/L")
    interpretation.append(f"   اختلاف: {target_diff:.1f}%")
    if target_balanced:
        interpretation.append("   ✅ متعادل")
    else:
        interpretation.append(f"   ❌ {target_warning}")
    interpretation.append("\n🔹 محلول نهایی (Final Solution):")
    interpretation.append(f"   کاتیون‌ها: {final_cation:.2f} MEQ/L")
    interpretation.append(f"   آنیون‌ها: {final_anion:.2f} MEQ/L")
    interpretation.append(f"   اختلاف: {final_diff:.1f}%")
    if final_balanced:
        interpretation.append("   ✅ متعادل")
    else:
        interpretation.append(f"   ❌ {final_warning}")
    if target_balanced and final_balanced:
        interpretation.append("\n✅ وضعیت کلی: تعادل یونی برقرار است.")
    elif target_balanced and not final_balanced:
        interpretation.append("\n⚠️ وضعیت کلی: تعادل هدف برقرار است اما محلول نهایی نامتعادل است.")
    elif not target_balanced and final_balanced:
        interpretation.append("\n⚠️ وضعیت کلی: تعادل هدف برقرار نیست اما محلول نهایی متعادل است.")
    else:
        interpretation.append("\n❌ وضعیت کلی: هر دو حالت نامتعادل هستند. لطفاً مقادیر را تنظیم کنید.")

    return {
        "target": {
            "cation": target_cation,
            "anion": target_anion,
            "diff_percent": target_diff,
            "is_balanced": target_balanced,
            "warning": target_warning
        },
        "final": {
            "cation": final_cation,
            "anion": final_anion,
            "diff_percent": final_diff,
            "is_balanced": final_balanced,
            "warning": final_warning
        },
        "interpretation": "\n".join(interpretation),
        "overall_balanced": target_balanced and final_balanced
    }
