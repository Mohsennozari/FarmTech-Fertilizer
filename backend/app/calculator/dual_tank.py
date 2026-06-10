# backend/app/calculator/dual_tank.py

from typing import List, Dict, Tuple, Optional
import copy
from .core import calculate_water_contribution
from .ec import calculate_final_ec
from .optimization import optimize_fertilizer_doses_professional
from .tank import calculate_tank_doses
from .instructions import generate_persian_mixing_instructions, generate_persian_general_instructions


def separate_into_tanks_professional(doses: List[Dict]) -> List[Dict]:
    """
    تفکیک کودها به دو مخزن بر اساس استاندارد جهانی هیدروپونیک:
    
    مخزن A (کلسیم): 
        - کلیه کودهای حاوی کلسیم (نیترات کلسیم)
        - کلات آهن و سایر کودهای آهن
        - کودهای مخصوص مخزن کلسیم
        
    مخزن B (اصلی):
        - کودهای NPK
        - سولفات پتاسیم، سولفات منیزیم
        - ریز مغذی‌ها
        - سایر کودهای غیر کلسیمی
    """
    
    tank_a = {
        "name": "🧪 مخزن A - کلسیم",
        "type": "calcium",
        "description": "⚠️ این مخزن حاوی کلسیم است. هرگز با مخزن B مخلوط نشود!",
        "doses": []
    }
    
    tank_b = {
        "name": "🧪 مخزن B - اصلی",
        "type": "main",
        "description": "حاوی NPK، منیزیم، سولفات و ریز مغذی‌ها",
        "doses": []
    }
    
    # کلمات کلیدی برای شناسایی کودهای کلسیمی
    calcium_keywords = [
        'calcium', 'کلسیم', 'نیترات کلسیم', 'calcium nitrate', 
        'iron', 'آهن', 'chelate', 'کلات', 'fe'
    ]
    
    for dose in doses:
        name_lower = dose['name'].lower()
        fert_type = dose.get('fertilizer_type', '').lower() if 'fertilizer_type' in dose else ''
        
        # تشخیص کود کلسیمی یا آهنی
        is_calcium = (
            'calcium' in name_lower or 
            'کلسیم' in name_lower or
            fert_type == 'calcium' or
            (('iron' in name_lower or 'آهن' in name_lower) and 'chelate' in name_lower)
        )
        
        if is_calcium:
            dose['caution'] = "⚠️ فقط در مخزن کلسیم استفاده شود"
            tank_a["doses"].append(dose)
        else:
            tank_b["doses"].append(dose)
    
    # اضافه کردن هشدارها به توضیحات مخازن
    if tank_a["doses"]:
        total_dose_a = sum(d['dose_g_per_liter'] for d in tank_a["doses"])
        if total_dose_a > 2.0:
            tank_a["description"] += f"\n⚠️ هشدار: مجموع دوز ({total_dose_a} g/L) بالاست. احتمال رسوب را بررسی کنید."
    
    if tank_b["doses"]:
        total_dose_b = sum(d['dose_g_per_liter'] for d in tank_b["doses"])
        if total_dose_b > 3.5:
            tank_b["description"] += f"\n⚠️ هشدار: مجموع دوز ({total_dose_b} g/L) نزدیک به حد مجاز است."
    
    result = []
    if tank_a["doses"]:
        result.append(tank_a)
    if tank_b["doses"]:
        result.append(tank_b)
    
    return result


def separate_into_tanks(doses: List[Dict]) -> List[Dict]:
    """تفکیک کودها به دو مخزن (نسخه قبلی برای سازگاری)"""
    return separate_into_tanks_professional(doses)


def calculate_dual_tank_professional(
    remaining_needs: Dict[str, float],
    all_fertilizers: List,
    tank_main,
    tank_calcium,
    brand_filter: Optional[str] = None,
    max_total_dose: float = 5.0
) -> Tuple[Dict, Dict, List[Dict], str]:
    """
    محاسبه دوز بهینه برای دو مخزن با استفاده از الگوریتم لایه‌به‌لایه حرفه‌ای
    
    Returns:
        result_main: نتایج مخزن اصلی
        result_calcium: نتایج مخزن کلسیم
        combined_warnings: هشدارهای ترکیبی
        general_instructions: دستورالعمل کلی فارسی
    """
    
    if brand_filter:
        all_fertilizers = [f for f in all_fertilizers if f.brand_name == brand_filter]
    
    if not all_fertilizers:
        empty_result = {
            "doses": [],
            "supplied_ppm": {},
            "warnings": [{"type": "error", "severity": "error", "message": "هیچ کودی یافت نشد"}],
            "mixing_instructions": "",
            "ec_predicted": 0
        }
        return empty_result, empty_result, [], ""
    
    # تفکیک هوشمند کودها
    fertilizers_for_calcium = []
    fertilizers_for_main = []
    
    calcium_keywords = [
        'calcium', 'کلسیم', 'نیترات کلسیم', 'calcium nitrate',
        'iron', 'آهن', 'chelate', 'کلات', 'fe chelate', 'iron chelate'
    ]
    
    for fert in all_fertilizers:
        name_lower = (fert.name or "").lower()
        fert_type = (fert.fertilizer_type or "").lower()
        
        is_calcium_fertilizer = (
            (fert.ca_percent or 0) > 0 or
            any(keyword in name_lower for keyword in calcium_keywords) or
            fert_type == 'calcium'
        )
        
        if is_calcium_fertilizer:
            fertilizers_for_calcium.append(fert)
        else:
            fertilizers_for_main.append(fert)
    
    # تقسیم نیازها
    water_calcium = calculate_water_contribution(tank_calcium)
    water_main = calculate_water_contribution(tank_main)
    
    needs_calcium = {
        'Ca': max(0, remaining_needs.get('Ca', 0) - water_calcium.get('Ca', 0)),
        'Fe': max(0, remaining_needs.get('Fe', 0) - water_calcium.get('Fe', 0)),
        'N': max(0, remaining_needs.get('N', 0) * 0.35),
    }
    
    needs_main = copy.deepcopy(remaining_needs)
    needs_main['Ca'] = max(0, remaining_needs.get('Ca', 0) - water_main.get('Ca', 0) - needs_calcium.get('Ca', 0))
    needs_main['Fe'] = max(0, remaining_needs.get('Fe', 0) - water_main.get('Fe', 0) - needs_calcium.get('Fe', 0))
    needs_main['N'] = max(0, remaining_needs.get('N', 0) - needs_calcium.get('N', 0))
    
    # محاسبه مخزن کلسیم
    doses_calcium_raw, supply_calcium, warnings_calcium = optimize_fertilizer_doses_professional(
        remaining_needs=needs_calcium,
        fertilizers=fertilizers_for_calcium,
        brand_filter=brand_filter,
        max_total_dose=3.0
    )
    
    doses_calcium = calculate_tank_doses(doses_calcium_raw, tank_calcium.volume_liters)
    ec_calcium = calculate_final_ec(tank_calcium.water_ec_ms_cm or 0, doses_calcium)
    
    mixing_calcium = generate_persian_mixing_instructions(
        tank_name="مخزن کلسیم",
        tank_type="calcium",
        doses=doses_calcium,
        tank_volume=tank_calcium.volume_liters,
        target_ph_min=6.0,
        target_ph_max=6.5,
        warnings=warnings_calcium
    )
    
    # محاسبه مخزن اصلی
    doses_main_raw, supply_main, warnings_main = optimize_fertilizer_doses_professional(
        remaining_needs=needs_main,
        fertilizers=fertilizers_for_main,
        brand_filter=brand_filter,
        max_total_dose=4.0
    )
    
    doses_main = calculate_tank_doses(doses_main_raw, tank_main.volume_liters)
    ec_main = calculate_final_ec(tank_main.water_ec_ms_cm or 0, doses_main)
    
    mixing_main = generate_persian_mixing_instructions(
        tank_name="مخزن اصلی",
        tank_type="main",
        doses=doses_main,
        tank_volume=tank_main.volume_liters,
        target_ph_min=5.5,
        target_ph_max=6.2,
        warnings=warnings_main
    )
    
    # جمع‌آوری هشدارها
    combined_warnings = []
    combined_warnings.extend(warnings_calcium)
    combined_warnings.extend(warnings_main)
    
    if not fertilizers_for_calcium:
        combined_warnings.append({
            "type": "missing_calcium_fertilizers",
            "severity": "error",
            "message": "⚠️ هیچ کود کلسیمی در سیستم یافت نشد! لطفاً نیترات کلسیم یا کودهای حاوی کلسیم اضافه کنید."
        })
    
    if not fertilizers_for_main:
        combined_warnings.append({
            "type": "missing_main_fertilizers",
            "severity": "error",
            "message": "⚠️ هیچ کود اصلی (غیر کلسیمی) در سیستم یافت نشد!"
        })
    
    # دستورالعمل کلی
    general_instructions = generate_persian_general_instructions(
        tank_main_volume=tank_main.volume_liters,
        tank_calcium_volume=tank_calcium.volume_liters,
        ec_main=ec_main,
        ec_calcium=ec_calcium,
        warnings=combined_warnings
    )
    
    result_main = {
        "doses": doses_main,
        "supplied_ppm": supply_main,
        "warnings": warnings_main,
        "mixing_instructions": mixing_main,
        "ec_predicted": ec_main,
        "water_contribution": water_main
    }
    
    result_calcium = {
        "doses": doses_calcium,
        "supplied_ppm": supply_calcium,
        "warnings": warnings_calcium,
        "mixing_instructions": mixing_calcium,
        "ec_predicted": ec_calcium,
        "water_contribution": water_calcium
    }
    
    return result_main, result_calcium, combined_warnings, general_instructions