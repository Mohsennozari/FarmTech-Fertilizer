# Platform-v3\backend\app\calculator.py

import numpy as np
from typing import List, Dict, Tuple, Optional

SUPPORTED_ELEMENTS = ['N', 'P', 'K', 'Ca', 'Mg', 'S', 'Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']
MACRO_ELEMENTS = ['N', 'P', 'K', 'Ca', 'Mg', 'S']
MICRO_ELEMENTS = ['Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']

# ============================================================
# محدودیت‌های ایمنی و سمیت عناصر (بر اساس منابع علمی)
# ============================================================
ELEMENT_SAFETY_LIMITS = {
    'N': {'min': 50, 'max': 250, 'tolerance': 0.15},
    'P': {'min': 20, 'max': 80, 'tolerance': 0.15},
    'K': {'min': 50, 'max': 300, 'tolerance': 0.15},
    'Ca': {'min': 40, 'max': 200, 'tolerance': 0.15},
    'Mg': {'min': 15, 'max': 60, 'tolerance': 0.15},
    'S': {'min': 10, 'max': 50, 'tolerance': 0.15},
    'Fe': {'min': 1, 'max': 5, 'tolerance': 0.20},
    'Zn': {'min': 0.1, 'max': 2, 'tolerance': 0.20},
    'Mn': {'min': 0.1, 'max': 2, 'tolerance': 0.20},
    'Cu': {'min': 0.02, 'max': 0.5, 'tolerance': 0.20},
    'B': {'min': 0.1, 'max': 1, 'tolerance': 0.20},
    'Mo': {'min': 0.01, 'max': 0.1, 'tolerance': 0.20},
    'Cl': {'min': 0, 'max': 100, 'tolerance': 0.30},
}

# وزن دهی به عناصر (اهمیت در بهینه‌سازی)
ELEMENT_WEIGHTS = {
    'N': 1.0,
    'P': 2.0,      # فسفر مهم‌ترین عنصر برای ریشه‌زایی
    'K': 1.2,
    'Ca': 1.0,
    'Mg': 0.8,
    'S': 0.5,
    'Fe': 1.0,
    'Zn': 1.0,
    'Mn': 1.0,
    'Cu': 1.5,     # مس با وزن بالاتر برای جلوگیری از مصرف بیش از حد
    'B': 1.0,
    'Mo': 1.0,
    'Cl': 0.1,
}

# کودهایی که برای میکروها اولویت دارند (یونی کمپلکس)
MICRO_PRIORITY_FERTILIZERS = ['یونی کمپلکس پودری', 'کود مایع میکرو']


def calculate_element_ppm(fertilizer, dose_g_per_liter: float) -> Dict[str, float]:
    """محاسبه ppm هر عنصر بر اساس دوز کود پودری"""
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


def calculate_liquid_element_ppm(fertilizer, dose_ml_per_liter: float) -> Dict[str, float]:
    """محاسبه ppm هر عنصر بر اساس دوز کود مایع"""
    density = fertilizer.density_g_per_ml or 1.0
    factor = 10 * density
    
    return {
        'N': (fertilizer.n_percent or 0) * dose_ml_per_liter * factor,
        'P': (fertilizer.p_percent or 0) * dose_ml_per_liter * factor,
        'K': (fertilizer.k_percent or 0) * dose_ml_per_liter * factor,
        'Ca': (fertilizer.ca_percent or 0) * dose_ml_per_liter * factor,
        'Mg': (fertilizer.mg_percent or 0) * dose_ml_per_liter * factor,
        'S': (fertilizer.s_percent or 0) * dose_ml_per_liter * factor,
        'Fe': (fertilizer.fe_percent or 0) * dose_ml_per_liter * factor,
        'Zn': (fertilizer.zn_percent or 0) * dose_ml_per_liter * factor,
        'Mn': (fertilizer.mn_percent or 0) * dose_ml_per_liter * factor,
        'Cu': (fertilizer.cu_percent or 0) * dose_ml_per_liter * factor,
        'B': (fertilizer.b_percent or 0) * dose_ml_per_liter * factor,
        'Mo': (fertilizer.mo_percent or 0) * dose_ml_per_liter * factor,
        'Cl': (fertilizer.cl_percent or 0) * dose_ml_per_liter * factor,
    }


def calculate_water_contribution(tank) -> Dict[str, float]:
    """محاسبه سهم عناصر تامین شده توسط آب"""
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
    """محاسبه سهم عناصر تامین شده توسط اسید"""
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


def calculate_acid_for_hco3(hco3_ppm: float) -> Dict[str, float]:
    """محاسبه مقدار اسید مورد نیاز برای خنثی‌سازی بیکربنات آب"""
    if not hco3_ppm or hco3_ppm <= 0:
        return {"ml_per_1000L": 0, "element_added_ppm": 0, "element": "P"}
    
    reference_hco3 = 61
    reference_acid_ml = 70
    reference_p_ppm = 31.58
    
    ratio = hco3_ppm / reference_hco3
    acid_ml_per_1000L = reference_acid_ml * ratio
    element_added_ppm = reference_p_ppm * ratio
    
    return {
        "ml_per_1000L": round(acid_ml_per_1000L, 2),
        "element_added_ppm": round(element_added_ppm, 2),
        "element": "P"
    }


def get_target_range(needs: Dict[str, float]) -> Dict[str, Dict[str, float]]:
    """محاسبه بازه مجاز برای هر عنصر با در نظر گرفتن تحمل (tolerance)"""
    ranges = {}
    for elem in SUPPORTED_ELEMENTS:
        target = needs.get(elem, 0)
        limits = ELEMENT_SAFETY_LIMITS.get(elem, {'tolerance': 0.15, 'min': 0, 'max': 1000})
        tolerance = limits['tolerance']
        
        lower = max(limits['min'], target * (1 - tolerance))
        upper = min(limits['max'], target * (1 + tolerance) if target > 0 else limits['max'])
        
        ranges[elem] = {'min': lower, 'max': upper, 'target': target}
    
    return ranges


def optimize_macro_elements_professional(
    needs: Dict[str, float],
    fertilizers: List,
    brand_filter: Optional[str] = None,
    max_total_dose: float = 8.0
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    """
    مرحله 1: بهینه‌سازی عناصر ماکرو با وزن دهی و محدودیت‌های علمی
    """
    if not fertilizers:
        return [], {elem: 0.0 for elem in SUPPORTED_ELEMENTS}, []
    
    if brand_filter:
        fertilizers = [f for f in fertilizers if f.brand_name == brand_filter]
        if not fertilizers:
            return [], {elem: 0.0 for elem in SUPPORTED_ELEMENTS}, [{
                "type": "brand_filter",
                "severity": "warning",
                "message": f"هیچ کودی از برند {brand_filter} یافت نشد"
            }]
    
    # فیلتر کودهای حاوی عناصر ماکرو
    macro_fertilizers = []
    for fert in fertilizers:
        has_macro = any([
            fert.n_percent > 0, fert.p_percent > 0, fert.k_percent > 0,
            fert.ca_percent > 0, fert.mg_percent > 0, fert.s_percent > 0
        ])
        if has_macro:
            macro_fertilizers.append(fert)
    
    if not macro_fertilizers:
        return [], {elem: 0.0 for elem in SUPPORTED_ELEMENTS}, []
    
    # ساخت ماتریس A با وزن دهی
    A = []
    weights = [ELEMENT_WEIGHTS.get(e, 1.0) for e in MACRO_ELEMENTS]
    
    for fert in macro_fertilizers:
        purity = (fert.purity_percent or 100) / 100.0
        factor = 10 * purity
        
        if fert.fertilizer_form == "liquid" and fert.density_g_per_ml:
            factor = factor * fert.density_g_per_ml
        
        row = [
            (fert.n_percent or 0) * factor * weights[0],
            (fert.p_percent or 0) * factor * weights[1],
            (fert.k_percent or 0) * factor * weights[2],
            (fert.ca_percent or 0) * factor * weights[3],
            (fert.mg_percent or 0) * factor * weights[4],
            (fert.s_percent or 0) * factor * weights[5],
        ]
        A.append(row)
    
    A = np.array(A)
    b = np.array([needs.get(e, 0) * weights[i] for i, e in enumerate(MACRO_ELEMENTS)])
    
    try:
        doses, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        doses = np.maximum(doses, 0)
        
        # نرمالایز کردن دوزها با وزن‌ها
        for i in range(len(doses)):
            if weights[i % len(weights)] != 0:
                doses[i] = doses[i] / weights[i % len(weights)]
                
    except Exception as e:
        print(f"Macro optimization error: {e}")
        doses = np.ones(len(macro_fertilizers)) * 0.5
    
    total_dose = np.sum(doses)
    if total_dose > max_total_dose:
        doses = doses * (max_total_dose / total_dose)
    
    dose_warnings = []
    final_supply = {elem: 0.0 for elem in SUPPORTED_ELEMENTS}
    result_doses = []
    
    for i, fert in enumerate(macro_fertilizers):
        if doses[i] > (fert.min_dose_g_per_liter or 0.01):
            if fert.fertilizer_form == "liquid" and fert.density_g_per_ml:
                dose_ml = doses[i] / fert.density_g_per_ml
                content = calculate_liquid_element_ppm(fert, dose_ml)
                dose_value_ml = dose_ml
                dose_value_g = doses[i]
            else:
                content = calculate_element_ppm(fert, doses[i])
                dose_value_ml = None
                dose_value_g = doses[i]
            
            for elem in SUPPORTED_ELEMENTS:
                final_supply[elem] += content[elem]
            
            if fert.max_dose_g_per_liter and dose_value_g > fert.max_dose_g_per_liter:
                dose_warnings.append({
                    "type": "max_dose_exceeded",
                    "severity": "warning",
                    "fertilizer": fert.name,
                    "message": f"⚠️ دوز محاسبه شده برای {fert.name} ({round(dose_value_g, 2)} g/L) از حد مجاز ({fert.max_dose_g_per_liter} g/L) بیشتر است. مقدار به حداکثر مجاز کاهش یافت."
                })
                dose_value_g = min(dose_value_g, fert.max_dose_g_per_liter)
            
            result_doses.append({
                "id": fert.id,
                "name": fert.name,
                "brand_name": fert.brand_name,
                "fertilizer_form": fert.fertilizer_form,
                "dose_g_per_liter": round(dose_value_g, 3),
                "dose_ml_per_liter": round(dose_value_ml, 1) if dose_value_ml else None,
                "chemical_formula": fert.chemical_formula
            })
    
    return result_doses, final_supply, dose_warnings


def optimize_micro_elements_professional(
    needs: Dict[str, float],
    current_supply: Dict[str, float],
    fertilizers: List,
    macro_doses: List[Dict],
    max_total_dose: float = 1.0
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    """
    مرحله 2: بهینه‌سازی عناصر میکرو با اولویت کود یونی کمپلکس
    """
    if not fertilizers:
        return [], current_supply, []
    
    # محاسبه نیاز باقیمانده برای میکروها
    remaining_micro = {}
    for elem in MICRO_ELEMENTS:
        remaining = max(0, needs.get(elem, 0) - current_supply.get(elem, 0))
        limits = ELEMENT_SAFETY_LIMITS.get(elem, {'min': 0, 'max': 100})
        
        # اگر نیازی باقی نمانده یا از حد مجاز عبور کرده، نیازی به اضافه کردن نیست
        if remaining > 0.01 and current_supply.get(elem, 0) < limits['max']:
            remaining_micro[elem] = remaining
    
    if not remaining_micro:
        return [], current_supply, []
    
    used_ids = [d['id'] for d in macro_doses]
    
    # اولویت: کودهای تخصصی میکرو (یونی کمپلکس) در ابتدا
    micro_fertilizers_priority = []
    micro_fertilizers_other = []
    
    for fert in fertilizers:
        has_micro = any([
            fert.fe_percent > 0, fert.zn_percent > 0, fert.mn_percent > 0,
            fert.cu_percent > 0, fert.b_percent > 0, fert.mo_percent > 0,
            fert.cl_percent > 0
        ])
        if has_micro and fert.id not in used_ids:
            if fert.name in MICRO_PRIORITY_FERTILIZERS:
                micro_fertilizers_priority.append(fert)
            else:
                micro_fertilizers_other.append(fert)
    
    micro_fertilizers = micro_fertilizers_priority + micro_fertilizers_other
    
    if not micro_fertilizers:
        # هشدار کمبود ریزمغذی
        missing = [f"{e}: {remaining_micro[e]:.2f}ppm" for e in remaining_micro]
        return [], current_supply, [{
            "type": "micro_deficiency",
            "severity": "warning",
            "message": f"⚠️ کمبود ریزمغذی‌ها: {', '.join(missing)}. لطفاً کود ریزمغذی مناسب اضافه کنید."
        }]
    
    # ساخت ماتریس با وزن دهی
    micro_elements_list = MICRO_ELEMENTS
    weights = [ELEMENT_WEIGHTS.get(e, 1.0) for e in micro_elements_list]
    
    A = []
    for fert in micro_fertilizers:
        purity = (fert.purity_percent or 100) / 100.0
        factor = 10 * purity
        
        if fert.fertilizer_form == "liquid" and fert.density_g_per_ml:
            factor = factor * fert.density_g_per_ml
        
        row = [
            (fert.fe_percent or 0) * factor * weights[0],
            (fert.zn_percent or 0) * factor * weights[1],
            (fert.mn_percent or 0) * factor * weights[2],
            (fert.cu_percent or 0) * factor * weights[3],
            (fert.b_percent or 0) * factor * weights[4],
            (fert.mo_percent or 0) * factor * weights[5],
            (fert.cl_percent or 0) * factor * weights[6],
        ]
        A.append(row)
    
    A = np.array(A)
    b = np.array([remaining_micro.get(e, 0) * weights[i] for i, e in enumerate(micro_elements_list)])
    
    try:
        doses, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        doses = np.maximum(doses, 0)
        
        for i in range(len(doses)):
            if weights[i % len(weights)] != 0:
                doses[i] = doses[i] / weights[i % len(weights)]
                
    except Exception as e:
        print(f"Micro optimization error: {e}")
        doses = np.ones(len(micro_fertilizers)) * 0.1
    
    total_dose = np.sum(doses)
    if total_dose > max_total_dose:
        doses = doses * (max_total_dose / total_dose)
    
    result_doses = []
    final_supply = current_supply.copy()
    dose_warnings = []
    
    for i, fert in enumerate(micro_fertilizers):
        if doses[i] > (fert.min_dose_g_per_liter or 0.01):
            if fert.fertilizer_form == "liquid" and fert.density_g_per_ml:
                dose_ml = doses[i] / fert.density_g_per_ml
                content = calculate_liquid_element_ppm(fert, dose_ml)
                dose_value_ml = dose_ml
                dose_value_g = doses[i]
            else:
                content = calculate_element_ppm(fert, doses[i])
                dose_value_ml = None
                dose_value_g = doses[i]
            
            # بررسی محدودیت‌های ایمنی
            safety_warnings = []
            for elem, value in content.items():
                if elem in ELEMENT_SAFETY_LIMITS:
                    limits = ELEMENT_SAFETY_LIMITS[elem]
                    new_total = final_supply.get(elem, 0) + value
                    if new_total > limits['max']:
                        safety_warnings.append(f"{elem} از حد مجاز ({limits['max']} ppm) عبور خواهد کرد")
            
            if safety_warnings:
                dose_warnings.append({
                    "type": "safety_limit",
                    "severity": "warning",
                    "fertilizer": fert.name,
                    "message": f"⚠️ {fert.name}: {', '.join(safety_warnings)}"
                })
                # کاهش دوز برای جلوگیری از عبور از حد مجاز
                reduction_factor = 0.5
                dose_value_g = dose_value_g * reduction_factor
                if dose_value_ml:
                    dose_value_ml = dose_value_ml * reduction_factor
                content = calculate_element_ppm(fert, dose_value_g) if not dose_value_ml else calculate_liquid_element_ppm(fert, dose_value_ml)
            
            for elem in SUPPORTED_ELEMENTS:
                final_supply[elem] += content[elem]
            
            if fert.max_dose_g_per_liter and dose_value_g > fert.max_dose_g_per_liter:
                dose_warnings.append({
                    "type": "max_dose_exceeded",
                    "severity": "warning",
                    "fertilizer": fert.name,
                    "message": f"⚠️ دوز {fert.name} از حد مجاز بیشتر است"
                })
                dose_value_g = min(dose_value_g, fert.max_dose_g_per_liter)
            
            result_doses.append({
                "id": fert.id,
                "name": fert.name,
                "brand_name": fert.brand_name,
                "fertilizer_form": fert.fertilizer_form,
                "dose_g_per_liter": round(dose_value_g, 3),
                "dose_ml_per_liter": round(dose_value_ml, 1) if dose_value_ml else None,
                "chemical_formula": fert.chemical_formula
            })
    
    return result_doses, final_supply, dose_warnings


def calculate_tank_doses(doses: List[Dict], tank_volume_liters: float) -> List[Dict]:
    """محاسبه دوز برای حجم مخزن و استوک 200 برابر"""
    result = []
    for dose in doses:
        if dose.get('fertilizer_form') == 'liquid' and dose.get('dose_ml_per_liter'):
            dose_ml_for_tank = dose['dose_ml_per_liter'] * tank_volume_liters
            stock_200x_ml = dose['dose_ml_per_liter'] * 200
            result.append({
                **dose,
                "dose_ml_for_tank": round(dose_ml_for_tank, 1),
                "stock_200x_ml_per_liter": round(stock_200x_ml, 1),
                "dose_g_for_tank": round(dose['dose_g_per_liter'] * tank_volume_liters, 1),
                "stock_200x_g_per_liter": round(dose['dose_g_per_liter'] * 200, 1)
            })
        else:
            result.append({
                **dose,
                "dose_g_for_tank": round(dose['dose_g_per_liter'] * tank_volume_liters, 1),
                "stock_200x_g_per_liter": round(dose['dose_g_per_liter'] * 200, 1),
                "dose_ml_for_tank": None,
                "stock_200x_ml_per_liter": None
            })
    
    return result


def check_supply_quality(
    needs: Dict[str, float], 
    supply: Dict[str, float]
) -> List[Dict]:
    """
    بررسی کیفیت تامین عناصر و تولید هشدارهای علمی
    """
    warnings = []
    ranges = get_target_range(needs)
    
    for elem in SUPPORTED_ELEMENTS:
        target = needs.get(elem, 0)
        actual = supply.get(elem, 0)
        limits = ranges.get(elem, {})
        
        if target == 0:
            if actual > ELEMENT_SAFETY_LIMITS.get(elem, {'max': 100})['max']:
                warnings.append({
                    "type": "element_toxicity",
                    "severity": "critical" if actual > limits.get('max', 100) * 2 else "warning",
                    "element": elem,
                    "message": f"⚠️ عنصر {elem}: {actual:.2f} ppm تامین شده (نیازی نبوده، ممکن است سمی باشد)"
                })
        else:
            lower = limits.get('min', target * 0.7)
            upper = limits.get('max', target * 1.3)
            
            if actual < lower:
                deficiency_pct = ((lower - actual) / target) * 100
                warnings.append({
                    "type": "deficiency",
                    "severity": "critical" if deficiency_pct > 30 else "warning",
                    "element": elem,
                    "message": f"⚠️ کمبود {elem}: {actual:.2f} ppm تامین شده، نیاز {target:.2f} ppm (کمبود {deficiency_pct:.0f}%)"
                })
            elif actual > upper:
                excess_pct = ((actual - upper) / target) * 100
                warnings.append({
                    "type": "excess",
                    "severity": "critical" if excess_pct > 50 else "warning",
                    "element": elem,
                    "message": f"⚠️ بیش‌بود {elem}: {actual:.2f} ppm تامین شده، نیاز {target:.2f} ppm (زیادی {excess_pct:.0f}%)"
                })
    
    return warnings


def generate_scientific_mixing_instructions(
    doses: List[Dict], 
    warnings: List[Dict], 
    tank_volume: float,
    acid_adjustment: Optional[Dict] = None,
    supply_quality: Optional[List[Dict]] = None
) -> str:
    """تولید دستورالعمل اختلاط علمی و دقیق"""
    instructions = []
    
    instructions.append("=" * 60)
    instructions.append("📋 دستورالعمل علمی اختلاط کودها")
    instructions.append("=" * 60)
    instructions.append("")
    instructions.append(f"📐 حجم مخزن: {tank_volume} لیتر")
    instructions.append(f"🌡️ دمای محلول ایده‌آل: 18-22 درجه سانتی‌گراد")
    instructions.append("")
    
    if acid_adjustment and acid_adjustment.get("ml_per_1000L", 0) > 0:
        instructions.append("🔬 مرحله 0: تنظیم pH اولیه آب")
        instructions.append("-" * 40)
        instructions.append(f"   به دلیل وجود {acid_adjustment.get('hco3_ppm', 0)} ppm بیکربنات در آب:")
        instructions.append(f"   ➤ {acid_adjustment['ml_per_1000L']} میلی‌لیتر اسید فسفریک 85% به ازای هر 1000 لیتر آب")
        instructions.append("   ⚠️ نکته ایمنی: همیشه اسید را به آب اضافه کنید، هرگز آب را به اسید اضافه نکنید")
        instructions.append("   ⚠️ از دستکش و عینک ایمنی استفاده کنید")
        instructions.append("")
    
    instructions.append("🧪 مرحله 1: آماده‌سازی مخزن")
    instructions.append("-" * 40)
    instructions.append("   1️⃣ مخزن را تا 60% حجم مورد نظر با آب تصفیه شده پر کنید")
    instructions.append("   2️⃣ سیستم همزن (پمپ یا هواده) را روشن کنید")
    instructions.append("   3️⃣ صبر کنید تا جریان آب پایدار شود (حداقل 2 دقیقه)")
    instructions.append("")
    
    instructions.append("⚗️ مرحله 2: اضافه کردن کودها (به ترتیب اهمیت)")
    instructions.append("-" * 40)
    
    # ترتیب اختلاط علمی
    order_map = {
        'پتاسیم': 1,      # اول: کودهای پتاسیمی
        'فسفر': 2,        # دوم: کودهای فسفاته
        'نیتروژن': 3,     # سوم: کودهای نیتروژنه
        'کلسیم': 4,       # چهارم: کودهای کلسیمی
        'منیزیم': 5,      # پنجم: کودهای منیزیمی
        'گوگرد': 6,       # ششم: کودهای گوگردی
        'ریزمغذی': 7      # هفتم: ریزمغذی‌ها
    }
    
    def get_order(name):
        for key, val in order_map.items():
            if key in name:
                return val
        return 8
    
    sorted_doses = sorted(doses, key=lambda x: get_order(x['name']))
    
    for i, dose in enumerate(sorted_doses, 1):
        if dose.get('fertilizer_form') == 'liquid' and dose.get('dose_ml_per_liter'):
            dose_text = f"{dose['dose_ml_per_liter']} میلی‌لیتر به ازای هر لیتر"
            tank_text = f"{dose['dose_ml_for_tank']} میلی‌لیتر"
        else:
            dose_text = f"{dose['dose_g_per_liter']} گرم به ازای هر لیتر"
            tank_text = f"{dose['dose_g_for_tank']} گرم"
        
        instructions.append(f"   {i}. {dose['name']}: {dose_text}")
        instructions.append(f"      ➤ مقدار کل: {tank_text}")
        instructions.append(f"      ➤ زمان همزنی: 3-5 دقیقه")
    
    instructions.append("")
    instructions.append("🔍 مرحله 3: تکمیل و تنظیم نهایی")
    instructions.append("-" * 40)
    instructions.append("   1️⃣ آب را به حجم نهایی برسانید")
    instructions.append("   2️⃣ اجازه دهید محلول به مدت 10-15 دقیقه سیرکوله کند")
    instructions.append("   3️⃣ EC را اندازه‌گیری کنید (هدف: محدوده مشخص شده)")
    instructions.append("   4️⃣ pH را اندازه‌گیری کنید (هدف: محدوده مشخص شده)")
    instructions.append("   5️⃣ در صورت نیاز، با اسید (برای کاهش pH) یا باز (برای افزایش pH) تنظیم کنید")
    instructions.append("")
    
    instructions.append("🏺 مرحله 4: ساخت استوک مادر 200 برابری (اختیاری)")
    instructions.append("-" * 40)
    instructions.append("   برای ساخت محلول مادر 200 برابر:")
    
    for dose in doses:
        if dose.get('fertilizer_form') == 'liquid' and dose.get('stock_200x_ml_per_liter'):
            instructions.append(f"   ➤ {dose['name']}: {dose['stock_200x_ml_per_liter']} میلی‌لیتر در 1 لیتر آب")
        else:
            instructions.append(f"   ➤ {dose['name']}: {dose['stock_200x_g_per_liter']} گرم در 1 لیتر آب")
    
    instructions.append("")
    instructions.append("   📐 روش استفاده از استوک مادر:")
    instructions.append("   ➤ به ازای هر 1 لیتر آب نهایی، 5 میلی‌لیتر از استوک را اضافه کنید")
    instructions.append("   ➤ مثال: برای مخزن 1000 لیتری، 5 لیتر استوک مادر اضافه کنید")
    instructions.append("")
    
    instructions.append("=" * 60)
    
    if warnings or supply_quality:
        instructions.append("")
        instructions.append("⚠️ هشدارهای علمی و توصیه‌ها")
        instructions.append("=" * 60)
        
        for warn in warnings:
            instructions.append(f"   🔴 {warn.get('message', warn.get('description', ''))}")
        
        if supply_quality:
            for sq in supply_quality:
                if sq.get('severity') == 'critical':
                    instructions.append(f"   🔴 {sq.get('message', '')}")
                else:
                    instructions.append(f"   🟡 {sq.get('message', '')}")
    
    return "\n".join(instructions)


def optimize_fertilizer_doses_professional_v2(
    needs: Dict[str, float],
    fertilizers: List,
    brand_filter: Optional[str] = None,
    max_total_dose: float = 10.0
) -> Tuple[List[Dict], Dict[str, float], List[Dict], List[Dict]]:
    """
    الگوریتم حرفه‌ای نسخه 2:
    - وزن دهی به عناصر بر اساس اهمیت
    - محدودیت‌های ایمنی و سمیت
    - بازه خطای مجاز (تحمل)
    - اولویت کودهای تخصصی برای میکروها
    - هشدارهای کیفیت تامین
    """
    macro_doses, macro_supply, macro_warnings = optimize_macro_elements_professional(
        needs, fertilizers, brand_filter, max_total_dose
    )
    
    micro_doses, final_supply, micro_warnings = optimize_micro_elements_professional(
        needs, macro_supply, fertilizers, macro_doses, max_total_dose / 2
    )
    
    all_doses = macro_doses + micro_doses
    all_warnings = macro_warnings + micro_warnings
    
    # بررسی کیفیت تامین نهایی
    supply_quality = check_supply_quality(needs, final_supply)
    
    return all_doses, final_supply, all_warnings, supply_quality