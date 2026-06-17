# backend/app/calculator/core.py

from typing import List, Dict, Tuple, Optional

# ============================================================
# لیست عناصر و ثابت‌های مربوطه
# ============================================================

# لیست ۱۶ عنصر مطابق پرامپت جدید "تغذیه سبز"
ELEMENTS_16 = [
    'N-NO3',
    'P',
    'S',
    'N-NH4',
    'K',
    'Ca',
    'Mg',
    'Na',
    'Cl',
    'Fe',
    'Mn',
    'Zn',
    'B',
    'Cu',
    'Mo'
]

# عناصر پشتیبانی شده قبلی (برای سازگاری با کد موجود)
SUPPORTED_ELEMENTS = ['N', 'P', 'K', 'Ca', 'Mg', 'S', 'Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']

# نگاشت عناصر ۱۶ گانه به کلیدهای قدیمی
ELEMENT_MAPPING_16_TO_OLD = {
    'N-NO3': 'N',
    'N-NH4': 'N',  # نیتروژن آمونیومی هم به N تبدیل می‌شود
}

# عناصری که در مدل‌های قدیمی وجود ندارند
NEW_ELEMENTS_16 = ['Na', 'Cl']


def get_element_key_16(element_name: str) -> str:
    """
    تبدیل نام عنصر به کلید استاندارد ۱۶ گانه
    """
    if element_name in ELEMENTS_16:
        return element_name
    # اگر عنصر با کلید قدیمی داده شد، تبدیل کن
    mapping = {
        'N': 'N-NO3',
        'P': 'P',
        'S': 'S',
        'K': 'K',
        'Ca': 'Ca',
        'Mg': 'Mg',
        'Fe': 'Fe',
        'Mn': 'Mn',
        'Zn': 'Zn',
        'B': 'B',
        'Cu': 'Cu',
        'Mo': 'Mo',
        'Cl': 'Cl'
    }
    return mapping.get(element_name, element_name)


def normalize_target_elements(target_elements: Dict[str, float]) -> Dict[str, float]:
    """
    نرمال‌سازی عناصر هدف: اطمینان از وجود همه ۱۶ عنصر
    """
    normalized = {}
    for elem in ELEMENTS_16:
        normalized[elem] = target_elements.get(elem, 0.0)
    return normalized


def convert_16_to_supported(target_16: Dict[str, float]) -> Dict[str, float]:
    """
    تبدیل عناصر ۱۶ گانه به فرمت پشتیبانی شده قدیمی (برای سازگاری با الگوریتم)
    """
    result = {}
    for elem in SUPPORTED_ELEMENTS:
        if elem == 'N':
            # N ترکیبی از N-NO3 و N-NH4 است
            result[elem] = target_16.get('N-NO3', 0) + target_16.get('N-NH4', 0)
        elif elem in target_16:
            result[elem] = target_16[elem]
        else:
            result[elem] = 0.0
    return result


def calculate_element_ppm(fertilizer, dose_g_per_liter: float) -> Dict[str, float]:
    purity = (fertilizer.purity_percent or 100) / 100.0
    factor = 10 * purity

    return {
        'N': (fertilizer.n_percent or 0) * dose_g_per_liter * factor,
        'P': (fertilizer.p_percent or 0) * dose_g_per_liter * factor,
        'K': (fertilizer.k_percent or 0) * dose_g_per_liter * factor,
        'Ca': (fertilizer.ca_percent or 0) * dose_g_per_liter * factor,
        'Mg': (fertilizer.mg_percent or 0) * dose_g_per_liter * factor,
        'S': (fertilizer.s_percent or 0) * dose_g_per_liter * factor,
        'Fe': (fertilizer.fe_percent or 0) * dose_g_per_liter * factor,
        'Zn': (fertilizer.zn_percent or 0) * dose_g_per_liter * factor,
        'Mn': (fertilizer.mn_percent or 0) * dose_g_per_liter * factor,
        'Cu': (fertilizer.cu_percent or 0) * dose_g_per_liter * factor,
        'B': (fertilizer.b_percent or 0) * dose_g_per_liter * factor,
        'Mo': (fertilizer.mo_percent or 0) * dose_g_per_liter * factor,
        'Cl': (fertilizer.cl_percent or 0) * dose_g_per_liter * factor,
    }


def calculate_water_contribution(tank) -> Dict[str, float]:
    if not tank:
        return {elem: 0.0 for elem in SUPPORTED_ELEMENTS}

    return {
        'N': tank.water_no3_ppm or 0,
        'P': 0,
        'K': 0,
        'Ca': tank.water_ca_ppm or 0,
        'Mg': tank.water_mg_ppm or 0,
        'S': tank.water_so4_ppm or 0,
        'Fe': tank.water_fe_ppm or 0,
        'Zn': 0,
        'Mn': 0,
        'Cu': 0,
        'B': 0,
        'Mo': 0,
        'Cl': tank.water_cl_ppm or 0,
    }


def calculate_acid_contribution(acid, dose_ml_per_liter: float) -> Dict[str, float]:
    if not acid or not acid.supplies_element:
        return {elem: 0.0 for elem in SUPPORTED_ELEMENTS}

    density = acid.density_g_per_ml or 1.0
    acid_concentration = acid.concentration_percent / 100.0
    element_percent = (acid.element_percent or 0) / 100.0

    ppm = acid_concentration * element_percent * dose_ml_per_liter * density * 1000

    result = {elem: 0.0 for elem in SUPPORTED_ELEMENTS}
    if acid.supplies_element == 'P':
        result['P'] = ppm
    elif acid.supplies_element == 'N':
        result['N'] = ppm
    elif acid.supplies_element == 'S':
        result['S'] = ppm

    return result
