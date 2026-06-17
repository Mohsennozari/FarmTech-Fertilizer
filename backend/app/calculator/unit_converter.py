# backend/app/calculator/unit_converter.py

from typing import Dict, List, Optional
from .ion_balance import ELEMENT_MEQ_CONSTANTS, ELEMENTS_16


# ============================================================
# توابع تبدیل واحدها
# ============================================================

def ppm_to_meq(ppm: float, element: str) -> float:
    """
    تبدیل PPM به میلی‌اکی‌والان (MEQ/L)

    فرمول: MEQ = (PPM × ظرفیت) / جرم اتمی

    Args:
        ppm: مقدار بر حسب PPM
        element: نام عنصر (به صورت کلید ۱۶ گانه)

    Returns:
        مقدار بر حسب MEQ/L
    """
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


def meq_to_ppm(meq: float, element: str) -> float:
    """
    تبدیل میلی‌اکی‌والان به PPM

    فرمول: PPM = (MEQ × جرم اتمی) / ظرفیت

    Args:
        meq: مقدار بر حسب MEQ/L
        element: نام عنصر (به صورت کلید ۱۶ گانه)

    Returns:
        مقدار بر حسب PPM
    """
    if meq <= 0:
        return 0.0

    constants = ELEMENT_MEQ_CONSTANTS.get(element)
    if not constants:
        return 0.0

    atomic_mass = constants['atomic_mass']
    valence = constants['valence']

    if valence <= 0:
        return 0.0

    ppm = (meq * atomic_mass) / valence
    return round(ppm, 2)


def ppm_to_mmol(ppm: float, element: str) -> float:
    """
    تبدیل PPM به میلی‌مول (MMOLS/L)

    فرمول: MMOLS = PPM / جرم اتمی

    Args:
        ppm: مقدار بر حسب PPM
        element: نام عنصر (به صورت کلید ۱۶ گانه)

    Returns:
        مقدار بر حسب MMOLS/L
    """
    if ppm <= 0:
        return 0.0

    constants = ELEMENT_MEQ_CONSTANTS.get(element)
    if not constants:
        return 0.0

    atomic_mass = constants['atomic_mass']

    if atomic_mass <= 0:
        return 0.0

    mmol = ppm / atomic_mass
    return round(mmol, 4)


def mmol_to_ppm(mmol: float, element: str) -> float:
    """
    تبدیل میلی‌مول به PPM

    فرمول: PPM = MMOLS × جرم اتمی

    Args:
        mmol: مقدار بر حسب MMOLS/L
        element: نام عنصر (به صورت کلید ۱۶ گانه)

    Returns:
        مقدار بر حسب PPM
    """
    if mmol <= 0:
        return 0.0

    constants = ELEMENT_MEQ_CONSTANTS.get(element)
    if not constants:
        return 0.0

    atomic_mass = constants['atomic_mass']

    if atomic_mass <= 0:
        return 0.0

    ppm = mmol * atomic_mass
    return round(ppm, 2)


def meq_to_mmol(meq: float, element: str) -> float:
    """
    تبدیل میلی‌اکی‌والان به میلی‌مول

    فرمول: MMOLS = MEQ / ظرفیت

    Args:
        meq: مقدار بر حسب MEQ/L
        element: نام عنصر (به صورت کلید ۱۶ گانه)

    Returns:
        مقدار بر حسب MMOLS/L
    """
    if meq <= 0:
        return 0.0

    constants = ELEMENT_MEQ_CONSTANTS.get(element)
    if not constants:
        return 0.0

    valence = constants['valence']

    if valence <= 0:
        return 0.0

    mmol = meq / valence
    return round(mmol, 4)


def mmol_to_meq(mmol: float, element: str) -> float:
    """
    تبدیل میلی‌مول به میلی‌اکی‌والان

    فرمول: MEQ = MMOLS × ظرفیت

    Args:
        mmol: مقدار بر حسب MMOLS/L
        element: نام عنصر (به صورت کلید ۱۶ گانه)

    Returns:
        مقدار بر حسب MEQ/L
    """
    if mmol <= 0:
        return 0.0

    constants = ELEMENT_MEQ_CONSTANTS.get(element)
    if not constants:
        return 0.0

    valence = constants['valence']

    if valence <= 0:
        return 0.0

    meq = mmol * valence
    return round(meq, 4)


# ============================================================
# تبدیل کامل یک جدول عناصر
# ============================================================

def convert_elements_table(
    elements_ppm: Dict[str, float]
) -> Dict[str, Dict[str, float]]:
    """
    تبدیل یک جدول کامل از عناصر به هر سه واحد

    Args:
        elements_ppm: دیکشنری عناصر با مقادیر PPM

    Returns:
        دیکشنری شامل سه جدول: ppm, meq, mmol
    """
    result = {
        'ppm': {},
        'meq': {},
        'mmol': {}
    }

    for element, ppm_value in elements_ppm.items():
        # اگر عنصر در لیست ۱۶ گانه نباشد، رد کن
        if element not in ELEMENTS_16:
            continue

        meq_value = ppm_to_meq(ppm_value, element)
        mmol_value = ppm_to_mmol(ppm_value, element)

        result['ppm'][element] = round(ppm_value, 2)
        result['meq'][element] = meq_value
        result['mmol'][element] = mmol_value

    return result


def get_unit_conversion_table(
    elements_ppm: Dict[str, float]
) -> List[Dict[str, any]]:
    """
    تولید جدول تبدیل واحدها برای نمایش در UI

    Args:
        elements_ppm: دیکشنری عناصر با مقادیر PPM

    Returns:
        لیستی از دیکشنری‌ها با فرمت:
        [
            {
                'element': 'N-NO3',
                'ppm': 150.0,
                'meq': 2.4194,
                'mmol': 2.4194
            },
            ...
        ]
    """
    result = []

    for element in ELEMENTS_16:
        ppm_value = elements_ppm.get(element, 0.0)

        meq_value = ppm_to_meq(ppm_value, element)
        mmol_value = ppm_to_mmol(ppm_value, element)

        result.append({
            'element': element,
            'ppm': round(ppm_value, 2),
            'meq': meq_value,
            'mmol': mmol_value
        })

    return result


# ============================================================
# تبدیل بر اساس واحد انتخابی
# ============================================================

def convert_from_unit(
    value: float,
    from_unit: str,
    to_unit: str,
    element: str
) -> float:
    """
    تبدیل یک مقدار از یک واحد به واحد دیگر

    Args:
        value: مقدار
        from_unit: واحد مبدأ (ppm, meq, mmol)
        to_unit: واحد مقصد (ppm, meq, mmol)
        element: نام عنصر

    Returns:
        مقدار تبدیل شده
    """
    if from_unit == to_unit:
        return round(value, 4)

    # تبدیل به PPM به عنوان واسط
    if from_unit == 'ppm':
        ppm_value = value
    elif from_unit == 'meq':
        ppm_value = meq_to_ppm(value, element)
    elif from_unit == 'mmol':
        ppm_value = mmol_to_ppm(value, element)
    else:
        return 0.0

    # تبدیل از PPM به واحد مقصد
    if to_unit == 'ppm':
        return round(ppm_value, 2)
    elif to_unit == 'meq':
        return ppm_to_meq(ppm_value, element)
    elif to_unit == 'mmol':
        return ppm_to_mmol(ppm_value, element)
    else:
        return 0.0


# ============================================================
# اعتبارسنجی مقادیر
# ============================================================

def validate_unit_value(
    value: float,
    unit: str,
    element: str
) -> Dict[str, any]:
    """
    اعتبارسنجی یک مقدار در یک واحد خاص

    Args:
        value: مقدار وارد شده
        unit: واحد (ppm, meq, mmol)
        element: نام عنصر

    Returns:
        دیکشنری شامل:
        - is_valid: bool
        - message: str (در صورت نامعتبر بودن)
        - min_value: float (حداقل مجاز)
        - max_value: float (حداکثر مجاز)
    """
    if value < 0:
        return {
            'is_valid': False,
            'message': f'مقدار نمی‌تواند منفی باشد: {value}',
            'min_value': 0,
            'max_value': None
        }

    # محدودیت‌های منطقی برای هر عنصر (بر اساس ppm)
    max_ppm_limits = {
        'N-NO3': 500,
        'P': 200,
        'S': 200,
        'N-NH4': 100,
        'K': 500,
        'Ca': 500,
        'Mg': 200,
        'Na': 100,
        'Cl': 200,
        'Fe': 10,
        'Mn': 5,
        'Zn': 5,
        'B': 5,
        'Cu': 2,
        'Mo': 1
    }

    # تبدیل به PPM برای بررسی محدودیت
    if unit == 'ppm':
        ppm_value = value
    elif unit == 'meq':
        ppm_value = meq_to_ppm(value, element)
    elif unit == 'mmol':
        ppm_value = mmol_to_ppm(value, element)
    else:
        ppm_value = value

    max_limit = max_ppm_limits.get(element, 1000)

    if ppm_value > max_limit * 1.5:  # 50% بیشتر از حد مجاز
        return {
            'is_valid': False,
            'message': f'مقدار {value} {unit} برای عنصر {element} بیش از حد مجاز است (حداکثر مجاز: {max_limit} ppm)',
            'min_value': 0,
            'max_value': max_limit
        }

    return {
        'is_valid': True,
        'message': None,
        'min_value': 0,
        'max_value': max_limit
    }
