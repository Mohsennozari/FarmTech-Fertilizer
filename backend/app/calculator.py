# Platform-v3\backend\app\calculator.py

import numpy as np
from typing import List, Dict, Tuple, Optional

SUPPORTED_ELEMENTS = ['N', 'P', 'K', 'Ca', 'Mg', 'S', 'Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']
MACRO_ELEMENTS = ['N', 'P', 'K', 'Ca', 'Mg', 'S']
MICRO_ELEMENTS = ['Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']

# ============================================================
# محدودیت‌های علمی و ایمنی
# ============================================================
ELEMENT_LIMITS = {
    'N': {'min': 50, 'max': 250, 'target_tolerance': 0.15},
    'P': {'min': 20, 'max': 80, 'target_tolerance': 0.15},
    'K': {'min': 50, 'max': 300, 'target_tolerance': 0.15},
    'Ca': {'min': 40, 'max': 200, 'target_tolerance': 0.15},
    'Mg': {'min': 15, 'max': 60, 'target_tolerance': 0.15},
    'S': {'min': 10, 'max': 50, 'target_tolerance': 0.20},
    'Fe': {'min': 1, 'max': 5, 'target_tolerance': 0.20},
    'Zn': {'min': 0.1, 'max': 2, 'target_tolerance': 0.20},
    'Mn': {'min': 0.1, 'max': 2, 'target_tolerance': 0.20},
    'Cu': {'min': 0.02, 'max': 0.5, 'target_tolerance': 0.20},
    'B': {'min': 0.1, 'max': 1, 'target_tolerance': 0.20},
    'Mo': {'min': 0.01, 'max': 0.1, 'target_tolerance': 0.20},
    'Cl': {'min': 0, 'max': 100, 'target_tolerance': 0.30},
}

# ============================================================
# توابع کمکی
# ============================================================
def calculate_element_ppm(fertilizer, dose_g_per_liter: float) -> Dict[str, float]:
    """محاسبه ppm عناصر برای کود پودری"""
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
    """محاسبه ppm عناصر برای کود مایع"""
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


def calculate_acid_for_hco3(hco3_ppm: float) -> Dict[str, float]:
    """محاسبه اسید مورد نیاز برای خنثی‌سازی بیکربنات"""
    if not hco3_ppm or hco3_ppm <= 0:
        return {"ml_per_1000L": 0, "element_added_ppm": 0}
    
    reference_hco3 = 61
    reference_acid_ml = 70
    reference_p_ppm = 31.58
    
    ratio = hco3_ppm / reference_hco3
    acid_ml_per_1000L = reference_acid_ml * ratio
    element_added_ppm = reference_p_ppm * ratio
    
    return {
        "ml_per_1000L": round(acid_ml_per_1000L, 2),
        "element_added_ppm": round(element_added_ppm, 2)
    }


def calculate_tank_doses(doses: List[Dict], tank_volume_liters: float) -> List[Dict]:
    """محاسبه دوز برای حجم مخزن و استوک 200 برابر"""
    result = []
    for dose in doses:
        if dose.get('fertilizer_form') == 'liquid' and dose.get('dose_ml_per_liter'):
            result.append({
                **dose,
                "dose_ml_for_tank": round(dose['dose_ml_per_liter'] * tank_volume_liters, 1),
                "stock_200x_ml_per_liter": round(dose['dose_ml_per_liter'] * 200, 1),
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


def generate_mixing_instructions(
    doses: List[Dict], 
    warnings: List[Dict], 
    tank_volume: float,
    acid_adjustment: Optional[Dict] = None
) -> str:
    """تولید دستورالعمل اختلاط"""
    instructions = []
    
    instructions.append("=" * 60)
    instructions.append("📋 دستورالعمل اختلاط کودها")
    instructions.append("=" * 60)
    instructions.append("")
    instructions.append(f"📐 حجم مخزن: {tank_volume} لیتر")
    instructions.append("")
    
    if acid_adjustment and acid_adjustment.get("ml_per_1000L", 0) > 0:
        instructions.append("🔸 تنظیم pH اولیه:")
        instructions.append(f"   {acid_adjustment['ml_per_1000L']} میلی‌لیتر اسید فسفریک 85% به ازای هر 1000 لیتر")
        instructions.append("   ⚠️ همیشه اسید را به آب اضافه کنید")
        instructions.append("")
    
    instructions.append("مراحل اختلاط:")
    instructions.append("")
    instructions.append("1️⃣ مخزن را تا 70% با آب پر کنید")
    instructions.append("")
    instructions.append("2️⃣ کودها را به ترتیب اضافه کنید:")
    
    for i, dose in enumerate(doses, 1):
        if dose.get('fertilizer_form') == 'liquid' and dose.get('dose_ml_per_liter'):
            dose_text = f"{dose['dose_ml_per_liter']} میلی‌لیتر/لیتر"
            tank_text = f"{dose['dose_ml_for_tank']} میلی‌لیتر"
        else:
            dose_text = f"{dose['dose_g_per_liter']} گرم/لیتر"
            tank_text = f"{dose['dose_g_for_tank']} گرم"
        
        instructions.append(f"   {i}. {dose['name']}: {dose_text}")
        instructions.append(f"      → {tank_text} کل")
    
    instructions.append("")
    instructions.append("3️⃣ پس از هر کود، 2 دقیقه هم بزنید")
    instructions.append("")
    instructions.append("4️⃣ آب را به حجم نهایی برسانید و 5 دقیقه هم بزنید")
    instructions.append("")
    instructions.append("5️⃣ EC و pH را اندازه‌گیری و تنظیم کنید")
    instructions.append("")
    instructions.append("=" * 60)
    instructions.append("🏺 استوک مادر 200 برابر")
    instructions.append("=" * 60)
    
    for dose in doses:
        if dose.get('fertilizer_form') == 'liquid' and dose.get('stock_200x_ml_per_liter'):
            instructions.append(f"• {dose['name']}: {dose['stock_200x_ml_per_liter']} میلی‌لیتر در 1 لیتر آب")
        else:
            instructions.append(f"• {dose['name']}: {dose['stock_200x_g_per_liter']} گرم در 1 لیتر آب")
    
    instructions.append("")
    instructions.append("روش استفاده: 5 میلی‌لیتر استوک به ازای هر 1 لیتر آب نهایی")
    instructions.append("")
    instructions.append("=" * 60)
    
    return "\n".join(instructions)


# ============================================================
# الگوریتم اصلی حرفه‌ای - 4 مرحله‌ای
# ============================================================

def optimize_fertilizer_professional(
    needs: Dict[str, float],
    fertilizers: List,
    brand_filter: Optional[str] = None,
    tank_water: Optional[Dict] = None
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    """
    الگوریتم 4 مرحله‌ای حرفه‌ای
    
    مرحله 1: تامین اجباری فسفر (P) - مهم‌ترین عنصر
    مرحله 2: تامین نیتروژن (N) و پتاسیم (K)
    مرحله 3: تامین کلسیم (Ca) و منیزیم (Mg)
    مرحله 4: تامین ریزمغذی‌ها (Fe, Zn, Mn, Cu, B, Mo, Cl)
    """
    
    if not fertilizers:
        return [], {elem: 0.0 for elem in SUPPORTED_ELEMENTS}, []
    
    # فیلتر برند
    if brand_filter:
        fertilizers = [f for f in fertilizers if f.brand_name == brand_filter]
        if not fertilizers:
            return [], {elem: 0.0 for elem in SUPPORTED_ELEMENTS}, [{
                "type": "brand_filter", "severity": "warning",
                "message": f"هیچ کودی از برند {brand_filter} یافت نشد"
            }]
    
    doses = []
    total_supply = {elem: 0.0 for elem in SUPPORTED_ELEMENTS}
    all_warnings = []
    used_fertilizer_ids = set()
    
    # ============================================================
    # مرحله 1: تامین اجباری فسفر (P)
    # ============================================================
    p_needed = needs.get('P', 0)
    p_current = 0
    
    if p_needed > 0:
        # پیدا کردن بهترین کود فسفره (P > 10%)
        p_fertilizers = [f for f in fertilizers if f.p_percent > 10 and f.id not in used_fertilizer_ids]
        p_fertilizers.sort(key=lambda x: x.p_percent, reverse=True)
        
        for fert in p_fertilizers:
            if p_current >= p_needed * 0.85:  # 85% تامین شده، کافی است
                break
            
            # محاسبه دوز مورد نیاز
            purity = (fert.purity_percent or 100) / 100.0
            factor = 10 * purity
            p_per_dose = fert.p_percent * factor
            
            if p_per_dose > 0:
                dose_needed = (p_needed - p_current) / p_per_dose
                max_allowed = fert.max_dose_g_per_liter or 5.0
                dose = min(dose_needed, max_allowed)
                
                if dose >= (fert.min_dose_g_per_liter or 0.01):
                    # محاسبه تامین واقعی
                    if fert.fertilizer_form == "liquid" and fert.density_g_per_ml:
                        dose_ml = dose / fert.density_g_per_ml
                        content = calculate_liquid_element_ppm(fert, dose_ml)
                        dose_display_ml = dose_ml
                        dose_display_g = dose
                    else:
                        content = calculate_element_ppm(fert, dose)
                        dose_display_ml = None
                        dose_display_g = dose
                    
                    for elem, val in content.items():
                        total_supply[elem] += val
                    
                    p_current = total_supply['P']
                    
                    doses.append({
                        "id": fert.id,
                        "name": fert.name,
                        "brand_name": fert.brand_name,
                        "fertilizer_form": fert.fertilizer_form,
                        "dose_g_per_liter": round(dose_display_g, 3),
                        "dose_ml_per_liter": round(dose_display_ml, 1) if dose_display_ml else None,
                        "chemical_formula": fert.chemical_formula
                    })
                    used_fertilizer_ids.add(fert.id)
        
        if p_current < p_needed * 0.7:
            all_warnings.append({
                "type": "p_deficiency", "severity": "critical",
                "message": f"⚠️ کمبود فسفر: {p_current:.1f} از {p_needed:.1f} ppm تامین شده ({((p_needed-p_current)/p_needed*100):.0f}% کمبود)"
            })
    
    # ============================================================
    # مرحله 2: تامین نیتروژن (N) و پتاسیم (K)
    # ============================================================
    n_needed = needs.get('N', 0)
    k_needed = needs.get('K', 0)
    n_current = total_supply['N']
    k_current = total_supply['K']
    
    # پیدا کردن کودهای NPK مناسب
    npk_fertilizers = [f for f in fertilizers if f.n_percent > 0 and f.id not in used_fertilizer_ids]
    npk_fertilizers.sort(key=lambda x: (x.n_percent + x.k_percent), reverse=True)
    
    for fert in npk_fertilizers:
        if n_current >= n_needed * 0.85 and k_current >= k_needed * 0.85:
            break
        
        purity = (fert.purity_percent or 100) / 100.0
        factor = 10 * purity
        
        n_per_dose = fert.n_percent * factor
        k_per_dose = fert.k_percent * factor
        
        if n_per_dose > 0 or k_per_dose > 0:
            # محاسبه دوز بر اساس نیتروژن و پتاسیم
            dose_by_n = (n_needed - n_current) / n_per_dose if n_per_dose > 0 else float('inf')
            dose_by_k = (k_needed - k_current) / k_per_dose if k_per_dose > 0 else float('inf')
            dose_needed = min(dose_by_n, dose_by_k, 5.0)  # حداکثر 5 g/L
            
            max_allowed = fert.max_dose_g_per_liter or 5.0
            dose = min(max(0, dose_needed), max_allowed)
            
            if dose >= (fert.min_dose_g_per_liter or 0.01):
                if fert.fertilizer_form == "liquid" and fert.density_g_per_ml:
                    dose_ml = dose / fert.density_g_per_ml
                    content = calculate_liquid_element_ppm(fert, dose_ml)
                    dose_display_ml = dose_ml
                    dose_display_g = dose
                else:
                    content = calculate_element_ppm(fert, dose)
                    dose_display_ml = None
                    dose_display_g = dose
                
                for elem, val in content.items():
                    total_supply[elem] += val
                
                n_current = total_supply['N']
                k_current = total_supply['K']
                
                doses.append({
                    "id": fert.id,
                    "name": fert.name,
                    "brand_name": fert.brand_name,
                    "fertilizer_form": fert.fertilizer_form,
                    "dose_g_per_liter": round(dose_display_g, 3),
                    "dose_ml_per_liter": round(dose_display_ml, 1) if dose_display_ml else None,
                    "chemical_formula": fert.chemical_formula
                })
                used_fertilizer_ids.add(fert.id)
    
    # ============================================================
    # مرحله 3: تامین کلسیم (Ca) و منیزیم (Mg)
    # ============================================================
    ca_needed = needs.get('Ca', 0)
    mg_needed = needs.get('Mg', 0)
    ca_current = total_supply['Ca']
    mg_current = total_supply['Mg']
    
    # نیترات کلسیم برای Ca
    if ca_current < ca_needed * 0.85:
        ca_fertilizer = None
        for fert in fertilizers:
            if fert.ca_percent > 0 and fert.id not in used_fertilizer_ids:
                ca_fertilizer = fert
                break
        
        if ca_fertilizer:
            purity = (ca_fertilizer.purity_percent or 100) / 100.0
            factor = 10 * purity
            ca_per_dose = ca_fertilizer.ca_percent * factor
            
            if ca_per_dose > 0:
                dose_needed = (ca_needed - ca_current) / ca_per_dose
                max_allowed = ca_fertilizer.max_dose_g_per_liter or 3.0
                dose = min(dose_needed, max_allowed)
                
                if dose >= (ca_fertilizer.min_dose_g_per_liter or 0.01):
                    if ca_fertilizer.fertilizer_form == "liquid" and ca_fertilizer.density_g_per_ml:
                        dose_ml = dose / ca_fertilizer.density_g_per_ml
                        content = calculate_liquid_element_ppm(ca_fertilizer, dose_ml)
                        dose_display_ml = dose_ml
                        dose_display_g = dose
                    else:
                        content = calculate_element_ppm(ca_fertilizer, dose)
                        dose_display_ml = None
                        dose_display_g = dose
                    
                    for elem, val in content.items():
                        total_supply[elem] += val
                    
                    doses.append({
                        "id": ca_fertilizer.id,
                        "name": ca_fertilizer.name,
                        "brand_name": ca_fertilizer.brand_name,
                        "fertilizer_form": ca_fertilizer.fertilizer_form,
                        "dose_g_per_liter": round(dose_display_g, 3),
                        "dose_ml_per_liter": round(dose_display_ml, 1) if dose_display_ml else None,
                        "chemical_formula": ca_fertilizer.chemical_formula
                    })
                    used_fertilizer_ids.add(ca_fertilizer.id)
    
    # سولفات منیزیم برای Mg
    if mg_current < mg_needed * 0.85:
        mg_fertilizer = None
        for fert in fertilizers:
            if fert.mg_percent > 0 and fert.id not in used_fertilizer_ids:
                mg_fertilizer = fert
                break
        
        if mg_fertilizer:
            purity = (mg_fertilizer.purity_percent or 100) / 100.0
            factor = 10 * purity
            mg_per_dose = mg_fertilizer.mg_percent * factor
            
            if mg_per_dose > 0:
                dose_needed = (mg_needed - mg_current) / mg_per_dose
                max_allowed = mg_fertilizer.max_dose_g_per_liter or 3.0
                dose = min(dose_needed, max_allowed)
                
                if dose >= (mg_fertilizer.min_dose_g_per_liter or 0.01):
                    if mg_fertilizer.fertilizer_form == "liquid" and mg_fertilizer.density_g_per_ml:
                        dose_ml = dose / mg_fertilizer.density_g_per_ml
                        content = calculate_liquid_element_ppm(mg_fertilizer, dose_ml)
                        dose_display_ml = dose_ml
                        dose_display_g = dose
                    else:
                        content = calculate_element_ppm(mg_fertilizer, dose)
                        dose_display_ml = None
                        dose_display_g = dose
                    
                    for elem, val in content.items():
                        total_supply[elem] += val
                    
                    doses.append({
                        "id": mg_fertilizer.id,
                        "name": mg_fertilizer.name,
                        "brand_name": mg_fertilizer.brand_name,
                        "fertilizer_form": mg_fertilizer.fertilizer_form,
                        "dose_g_per_liter": round(dose_display_g, 3),
                        "dose_ml_per_liter": round(dose_display_ml, 1) if dose_display_ml else None,
                        "chemical_formula": mg_fertilizer.chemical_formula
                    })
                    used_fertilizer_ids.add(mg_fertilizer.id)
    
    # ============================================================
    # مرحله 4: تامین ریزمغذی‌ها
    # ============================================================
    micro_elements = ['Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo']
    micro_current = {e: total_supply.get(e, 0) for e in micro_elements}
    
    # اولویت: یونی کمپلکس پودری
    micro_fertilizer = None
    for fert in fertilizers:
        if fert.name == "یونی کمپلکس پودری" and fert.id not in used_fertilizer_ids:
            micro_fertilizer = fert
            break
    
    if micro_fertilizer:
        # بررسی نیاز به ریزمغذی‌ها
        any_micro_needed = False
        for elem in micro_elements:
            needed = needs.get(elem, 0)
            current = micro_current.get(elem, 0)
            if current < needed * 0.5:
                any_micro_needed = True
                break
        
        if any_micro_needed:
            # دوز پیشنهادی برای یونی کمپلکس
            dose = 0.2  # دوز پایه
            max_allowed = micro_fertilizer.max_dose_g_per_liter or 2.0
            dose = min(dose, max_allowed)
            
            if dose >= (micro_fertilizer.min_dose_g_per_liter or 0.01):
                content = calculate_element_ppm(micro_fertilizer, dose)
                
                for elem, val in content.items():
                    total_supply[elem] += val
                
                doses.append({
                    "id": micro_fertilizer.id,
                    "name": micro_fertilizer.name,
                    "brand_name": micro_fertilizer.brand_name,
                    "fertilizer_form": micro_fertilizer.fertilizer_form,
                    "dose_g_per_liter": round(dose, 3),
                    "dose_ml_per_liter": None,
                    "chemical_formula": micro_fertilizer.chemical_formula
                })
                used_fertilizer_ids.add(micro_fertilizer.id)
    
    # ============================================================
    # بررسی نهایی کیفیت تامین
    # ============================================================
    for elem in SUPPORTED_ELEMENTS:
        target = needs.get(elem, 0)
        actual = total_supply.get(elem, 0)
        limits = ELEMENT_LIMITS.get(elem, {'target_tolerance': 0.2})
        tolerance = limits['target_tolerance']
        
        if target > 0:
            lower = target * (1 - tolerance)
            upper = target * (1 + tolerance)
            
            if actual < lower and actual > 0:
                deficit_pct = (lower - actual) / target * 100
                if deficit_pct > 30:
                    all_warnings.append({
                        "type": "deficiency", "severity": "critical",
                        "element": elem,
                        "message": f"⚠️ کمبود {elem}: {actual:.1f} از {target:.1f} ppm تامین شده (کمبود {deficit_pct:.0f}%)"
                    })
                else:
                    all_warnings.append({
                        "type": "deficiency", "severity": "warning",
                        "element": elem,
                        "message": f"⚠️ کمبود جزئی {elem}: {actual:.1f} از {target:.1f} ppm"
                    })
            elif actual > upper:
                excess_pct = (actual - upper) / target * 100
                if elem in ['Cu'] and excess_pct > 100:
                    all_warnings.append({
                        "type": "toxicity", "severity": "critical",
                        "element": elem,
                        "message": f"⚠️ سمیت {elem}: {actual:.1f} ppm تامین شده (حد مجاز {limits['max']} ppm)"
                    })
                else:
                    all_warnings.append({
                        "type": "excess", "severity": "warning",
                        "element": elem,
                        "message": f"⚠️ بیش‌بود {elem}: {actual:.1f} ppm تامین شده ({excess_pct:.0f}% بیش از نیاز)"
                    })
    
    return doses, total_supply, all_warnings


def optimize_fertilizer_doses_professional_v3(
    needs: Dict[str, float],
    fertilizers: List,
    brand_filter: Optional[str] = None,
    max_total_dose: float = 10.0
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    """
    نسخه نهایی الگوریتم حرفه‌ای (4 مرحله‌ای)
    """
    return optimize_fertilizer_professional(needs, fertilizers, brand_filter)