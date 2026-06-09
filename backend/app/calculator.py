# Platform-v3\backend\app\calculator.py

import numpy as np
from typing import List, Dict, Tuple, Optional

try:
    from scipy.optimize import minimize
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("Warning: scipy not installed. Using fallback method.")

SUPPORTED_ELEMENTS = ['N', 'P', 'K', 'Ca', 'Mg', 'S', 'Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']


# ============================================================
# توابع پایه
# ============================================================

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


# ============================================================
# ضرایب EC و توابع محاسبه EC نهایی
# ============================================================

EC_COEFFICIENTS = {
    "فرتی‌گل 36-12-12": 0.70,
    "فرتی‌گل 20-20-20": 0.70,
    "فرتی‌گل 30-5-15": 0.68,
    "فرتی‌گل 10-50-10": 0.65,
    "NPK 20-20-20 گرین استار": 0.70,
    "NPK 12-12-36 گرین استار": 0.68,
    "NPK 10-52-10 زاگرا استار": 0.65,
    "نیترات کلسیم": 0.95,
    "سولفات پتاسیم": 0.80,
    "سولفات منیزیم": 0.75,
    "کلرید پتاسیم": 0.85,
    "یونی کمپلکس پودری": 0.40,
    "default": 0.65
}


def calculate_final_ec(water_ec: float, doses: List[Dict]) -> float:
    total_ec = water_ec or 0.0
    for dose in doses:
        coeff = EC_COEFFICIENTS.get(dose["name"], EC_COEFFICIENTS["default"])
        total_ec += dose["dose_g_per_liter"] * coeff
    return round(total_ec, 2)


def get_ec_warning(predicted_ec: float, target_ec_min: float, target_ec_max: float) -> Optional[str]:
    if target_ec_min is None or target_ec_max is None:
        return None
    if predicted_ec > target_ec_max:
        return f"⚠️ EC پیش‌بینی ({predicted_ec} mS/cm) بالاتر از حد مجاز ({target_ec_max} mS/cm) است. محلول را با آب شیرین رقیق کنید."
    elif predicted_ec < target_ec_min:
        return f"⚠️ EC پیش‌بینی ({predicted_ec} mS/cm) پایین‌تر از حد مجاز ({target_ec_min} mS/cm) است. دوز کودها را افزایش دهید."
    return None


# ============================================================
# توابع لایه‌به‌لایه
# ============================================================

def select_best_fertilizer_for_macro(needs: Dict[str, float], fertilizers: List) -> Tuple[object, float, Dict]:
    best_fertilizer = None
    best_score = float('inf')
    best_dose = 0
    best_supply = {}

    for fert in fertilizers:
        doses = []
        for elem in ['N', 'P', 'K']:
            need = needs.get(elem, 0)
            elem_percent = getattr(fert, f"{elem.lower()}_percent", 0) or 0
            if elem_percent > 0 and need > 0:
                dose_for_elem = need / (elem_percent * 10)
                doses.append(dose_for_elem)

        if not doses:
            continue

        proposed_dose = sum(doses) / len(doses)
        max_dose = fert.max_dose_g_per_liter or 5.0
        min_dose = fert.min_dose_g_per_liter or 0.01
        proposed_dose = max(min_dose, min(proposed_dose, max_dose))

        supply = calculate_element_ppm(fert, proposed_dose)

        error = 0
        for elem in ['N', 'P', 'K']:
            need = needs.get(elem, 0)
            sup = supply.get(elem, 0)
            error += (need - sup) ** 2

        if error < best_score:
            best_score = error
            best_fertilizer = fert
            best_dose = proposed_dose
            best_supply = supply

    return best_fertilizer, best_dose, best_supply


def select_best_fertilizer_for_secondary(needs: Dict[str, float], fertilizers: List) -> List[Tuple[object, float, Dict]]:
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

            supply = calculate_element_ppm(fert, final_dose)
            supplied = supply.get(elem, 0)
            error = abs(need - supplied)

            if error < best_error:
                best_error = error
                best_fert = fert
                best_dose = final_dose
                best_supply = {elem: supplied}

        if best_fert:
            results.append((best_fert, best_dose, best_supply))

    return results


def solve_macro_layer(
    needs: Dict[str, float],
    fertilizers: List,
    max_total_dose: float = 3.0
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    macro_elements = ['N', 'P', 'K']
    warnings = []

    macro_fertilizers = [f for f in fertilizers if f.fertilizer_type in ['NPK']]

    if not macro_fertilizers:
        warnings.append({
            "type": "missing_fertilizers",
            "severity": "error",
            "message": "No NPK fertilizers found in database"
        })
        return [], {e: 0 for e in macro_elements}, warnings

    best_fert, best_dose, best_supply = select_best_fertilizer_for_macro(needs, macro_fertilizers)

    if not best_fert:
        warnings.append({
            "type": "optimization_failed",
            "severity": "error",
            "message": "Could not find suitable NPK fertilizer"
        })
        return [], {e: 0 for e in macro_elements}, warnings

    result_doses = [{
        "id": best_fert.id,
        "name": best_fert.name,
        "brand_name": best_fert.brand_name,
        "dose_g_per_liter": round(best_dose, 3),
        "chemical_formula": best_fert.chemical_formula,
        "layer": "macro"
    }]

    final_supply = {e: best_supply.get(e, 0) for e in macro_elements}

    return result_doses, final_supply, warnings


def solve_secondary_layer(
    needs: Dict[str, float],
    fertilizers: List,
    max_total_dose: float = 2.0
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    secondary_elements = ['Ca', 'Mg', 'S']
    warnings = []

    secondary_fertilizers = [f for f in fertilizers if f.fertilizer_type in ['تک عنصری', 'NPK']]

    if not secondary_fertilizers:
        warnings.append({
            "type": "missing_fertilizers",
            "severity": "warning",
            "message": "No secondary element fertilizers found"
        })
        return [], {e: 0 for e in secondary_elements}, warnings

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
        for elem, val in supply.items():
            if elem in final_supply:
                final_supply[elem] += val

    return result_doses, final_supply, warnings


def solve_micro_layer(
    needs: Dict[str, float],
    fertilizers: List,
    max_dose: float = 0.5
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    micro_elements = ['Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']
    warnings = []

    micro_fertilizers = [f for f in fertilizers if f.fertilizer_type == 'ریزمغذی']

    if not micro_fertilizers:
        warnings.append({
            "type": "missing_fertilizers",
            "severity": "warning",
            "message": "No micronutrient fertilizers found"
        })
        return [], {e: 0 for e in micro_elements}, warnings

    micro_fert = micro_fertilizers[0]

    required_dose = 0
    for elem in micro_elements:
        need = needs.get(elem, 0)
        if need > 0:
            elem_percent = getattr(micro_fert, f"{elem.lower()}_percent", 0) or 0
            if elem_percent > 0:
                dose_for_elem = need / (elem_percent * 10)
                required_dose = max(required_dose, dose_for_elem)

    dose = min(required_dose, max_dose)
    if dose < 0.01:
        dose = 0.01

    content = calculate_element_ppm(micro_fert, dose)
    final_supply = {e: content.get(e, 0) for e in micro_elements}

    result_doses = [{
        "id": micro_fert.id,
        "name": micro_fert.name,
        "brand_name": micro_fert.brand_name,
        "dose_g_per_liter": round(dose, 3),
        "chemical_formula": micro_fert.chemical_formula,
        "layer": "micro"
    }]

    uncovered = []
    for elem in micro_elements:
        need = needs.get(elem, 0)
        supply = final_supply[elem]
        if need > 0.1 and supply < need * 0.5:
            uncovered.append(elem)

    if uncovered:
        warnings.append({
            "type": "partial_coverage",
            "severity": "warning",
            "message": f"Micronutrients not fully supplied: {', '.join(uncovered)}",
            "fertilizers": [micro_fert.name]
        })

    return result_doses, final_supply, warnings


# ============================================================
# تابع اصلی الگوریتم لایه‌به‌لایه
# ============================================================

def optimize_fertilizer_doses_professional(
    remaining_needs: Dict[str, float],
    fertilizers: List,
    brand_filter: Optional[str] = None,
    max_total_dose: float = 5.0
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    """الگوریتم لایه‌به‌لایه - NPK → Secondary → Micro"""

    if not fertilizers:
        return [], {elem: 0.0 for elem in SUPPORTED_ELEMENTS}, []

    if brand_filter:
        fertilizers = [f for f in fertilizers if f.brand_name == brand_filter]
        if not fertilizers:
            return [], {elem: 0.0 for elem in SUPPORTED_ELEMENTS}, [{
                "type": "brand_filter",
                "severity": "warning",
                "message": f"No fertilizers found for brand {brand_filter}"
            }]

    all_warnings = []
    all_doses = []
    final_supply = {elem: 0.0 for elem in SUPPORTED_ELEMENTS}

    # مرحله 1: NPK
    macro_needs = {elem: remaining_needs.get(elem, 0) for elem in ['N', 'P', 'K']}
    macro_doses, macro_supply, macro_warnings = solve_macro_layer(macro_needs, fertilizers, 3.0)
    all_doses.extend(macro_doses)
    all_warnings.extend(macro_warnings)
    for elem, value in macro_supply.items():
        final_supply[elem] += value

    # به‌روزرسانی نیاز باقیمانده
    remaining = {}
    for elem in SUPPORTED_ELEMENTS:
        remaining[elem] = max(0, remaining_needs.get(elem, 0) - final_supply[elem])

    # مرحله 2: Ca, Mg, S
    secondary_needs = {elem: remaining.get(elem, 0) for elem in ['Ca', 'Mg', 'S']}
    secondary_doses, secondary_supply, secondary_warnings = solve_secondary_layer(secondary_needs, fertilizers, 2.0)
    all_doses.extend(secondary_doses)
    all_warnings.extend(secondary_warnings)
    for elem, value in secondary_supply.items():
        final_supply[elem] += value

    for elem in ['Ca', 'Mg', 'S']:
        remaining[elem] = max(0, remaining.get(elem, 0) - secondary_supply.get(elem, 0))

    # مرحله 3: ریز مغذی‌ها
    micro_needs = {elem: remaining.get(elem, 0) for elem in ['Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']}
    micro_doses, micro_supply, micro_warnings = solve_micro_layer(micro_needs, fertilizers, 0.5)
    all_doses.extend(micro_doses)
    all_warnings.extend(micro_warnings)
    for elem, value in micro_supply.items():
        final_supply[elem] += value

    # حذف دوزهای تکراری
    unique_doses = {}
    for dose in all_doses:
        name = dose['name']
        if name in unique_doses:
            unique_doses[name]['dose_g_per_liter'] += dose['dose_g_per_liter']
        else:
            unique_doses[name] = dose

    result_doses = list(unique_doses.values())
    result_doses.sort(key=lambda x: x['dose_g_per_liter'], reverse=True)

    for dose in result_doses:
        dose['dose_g_per_liter'] = round(dose['dose_g_per_liter'], 3)

    # هشدار عناصر پوشش داده نشده
    uncovered = []
    for elem in SUPPORTED_ELEMENTS:
        need = remaining_needs.get(elem, 0)
        supply = final_supply[elem]
        if need > 1.0 and supply < need * 0.7:
            uncovered.append(elem)

    if uncovered:
        all_warnings.append({
            "type": "partial_coverage",
            "severity": "warning",
            "message": f"Elements not fully supplied: {', '.join(uncovered)}",
            "fertilizers": []
        })

    return result_doses, final_supply, all_warnings


def calculate_tank_doses(doses: List[Dict], tank_volume_liters: float) -> List[Dict]:
    """محاسبه دوز برای کل مخزن و استوک 200x"""
    result = []
    for dose in doses:
        dose_g_for_tank = dose['dose_g_per_liter'] * tank_volume_liters
        stock_200x = dose['dose_g_per_liter'] * 200

        result.append({
            **dose,
            "dose_g_for_tank": round(dose_g_for_tank, 1),
            "stock_200x_g_per_liter": round(stock_200x, 1)
        })

    return result


def generate_professional_mixing_instructions(doses: List[Dict], warnings: List[Dict], tank_volume: float) -> str:
    """تولید دستورالعمل اختلاط"""
    instructions = []

    instructions.append("=" * 50)
    instructions.append("Mixing Instructions")
    instructions.append("=" * 50)
    instructions.append("")
    instructions.append(f"Tank Volume: {tank_volume} liters")
    instructions.append("")
    instructions.append("Steps:")
    instructions.append("")
    instructions.append("1. Fill the tank to 70% with clean water")
    instructions.append("")
    instructions.append("2. Add fertilizers in this order:")

    for i, dose in enumerate(doses, 1):
        instructions.append(f"   {i}. {dose['name']}: {dose['dose_g_per_liter']} g/L")
        instructions.append(f"      Total for tank: {dose['dose_g_for_tank']} g")

    instructions.append("")
    instructions.append("3. After adding each fertilizer, mix well for 2 minutes")
    instructions.append("")
    instructions.append("4. Fill to final volume and mix for 5 more minutes")
    instructions.append("")
    instructions.append("5. Measure and adjust EC and pH")
    instructions.append("")
    instructions.append("=" * 50)
    instructions.append("Stock Solution Instructions (200x)")
    instructions.append("=" * 50)
    instructions.append("")

    for dose in doses:
        instructions.append(f"   {dose['name']}: {dose['stock_200x_g_per_liter']} g per 1 liter water")

    instructions.append("")
    instructions.append("Usage: Add 5 ml of stock solution per 1 liter of final water")
    instructions.append("")
    instructions.append("=" * 50)

    if warnings:
        instructions.append("")
        instructions.append("Warnings:")
        seen = set()
        for warn in warnings:
            msg = warn.get('description', warn.get('message', ''))
            if msg not in seen:
                instructions.append(f"   - {msg}")
                seen.add(msg)

    return "\n".join(instructions)


# ============================================================
# بهبود تابع تفکیک به مخازن A و B
# ============================================================

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


# ============================================================
# تابع جدید: محاسبه حرفه‌ای دو مخزن
# ============================================================

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
    
    این تابع از الگوریتم اصلی optimize_fertilizer_doses_professional استفاده می‌کند
    و کودها را به طور هوشمند بین دو مخزن تقسیم می‌کند
    
    Returns:
        result_main: نتایج مخزن اصلی (دوزها، تامین شده، هشدارها، دستورالعمل)
        result_calcium: نتایج مخزن کلسیم
        combined_warnings: هشدارهای ترکیبی هر دو مخزن
        general_instructions: دستورالعمل کلی فارسی برای کشاورز
    """
    
    import copy
    
    # ============================================================
    # مرحله 1: فیلتر برند
    # ============================================================
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
    
    # ============================================================
    # مرحله 2: تفکیک هوشمند کودها به دو دسته
    # ============================================================
    
    fertilizers_for_calcium = []  # مخزن A - کودهای حاوی کلسیم و آهن
    fertilizers_for_main = []      # مخزن B - بقیه کودها
    
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
    
    # ============================================================
    # مرحله 3: تقسیم نیازهای گیاه بین دو مخزن
    # ============================================================
    
    water_calcium = calculate_water_contribution(tank_calcium)
    water_main = calculate_water_contribution(tank_main)
    
    # نیازهای مخزن کلسیم (کلسیم، آهن، و بخشی از نیتروژن)
    needs_calcium = {
        'Ca': max(0, remaining_needs.get('Ca', 0) - water_calcium.get('Ca', 0)),
        'Fe': max(0, remaining_needs.get('Fe', 0) - water_calcium.get('Fe', 0)),
        'N': max(0, remaining_needs.get('N', 0) * 0.35),  # 35% نیتروژن از نیترات کلسیم
    }
    
    # نیازهای مخزن اصلی (بقیه عناصر)
    needs_main = copy.deepcopy(remaining_needs)
    needs_main['Ca'] = max(0, remaining_needs.get('Ca', 0) - water_main.get('Ca', 0) - needs_calcium.get('Ca', 0))
    needs_main['Fe'] = max(0, remaining_needs.get('Fe', 0) - water_main.get('Fe', 0) - needs_calcium.get('Fe', 0))
    needs_main['N'] = max(0, remaining_needs.get('N', 0) - needs_calcium.get('N', 0))
    
    # ============================================================
    # مرحله 4: محاسبه مخزن کلسیم با الگوریتم لایه‌به‌لایه
    # ============================================================
    
    doses_calcium_raw, supply_calcium, warnings_calcium = optimize_fertilizer_doses_professional(
        remaining_needs=needs_calcium,
        fertilizers=fertilizers_for_calcium,
        brand_filter=brand_filter,
        max_total_dose=3.0
    )
    
    doses_calcium = calculate_tank_doses(doses_calcium_raw, tank_calcium.volume_liters)
    
    # محاسبه EC پیش‌بینی شده برای مخزن کلسیم
    ec_calcium = calculate_final_ec(tank_calcium.water_ec_ms_cm or 0, doses_calcium)
    
    # دستورالعمل اختلاط فارسی برای مخزن کلسیم
    mixing_calcium = generate_persian_mixing_instructions(
        tank_name="مخزن کلسیم",
        tank_type="calcium",
        doses=doses_calcium,
        tank_volume=tank_calcium.volume_liters,
        target_ph_min=6.0,
        target_ph_max=6.5,
        warnings=warnings_calcium
    )
    
    # ============================================================
    # مرحله 5: محاسبه مخزن اصلی با الگوریتم لایه‌به‌لایه
    # ============================================================
    
    doses_main_raw, supply_main, warnings_main = optimize_fertilizer_doses_professional(
        remaining_needs=needs_main,
        fertilizers=fertilizers_for_main,
        brand_filter=brand_filter,
        max_total_dose=4.0
    )
    
    doses_main = calculate_tank_doses(doses_main_raw, tank_main.volume_liters)
    
    # محاسبه EC پیش‌بینی شده برای مخزن اصلی
    ec_main = calculate_final_ec(tank_main.water_ec_ms_cm or 0, doses_main)
    
    # دستورالعمل اختلاط فارسی برای مخزن اصلی
    mixing_main = generate_persian_mixing_instructions(
        tank_name="مخزن اصلی",
        tank_type="main",
        doses=doses_main,
        tank_volume=tank_main.volume_liters,
        target_ph_min=5.5,
        target_ph_max=6.2,
        warnings=warnings_main
    )
    
    # ============================================================
    # مرحله 6: جمع‌آوری هشدارهای ترکیبی
    # ============================================================
    
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
    
    # ============================================================
    # مرحله 7: دستورالعمل کلی فارسی برای کشاورز
    # ============================================================
    
    general_instructions = generate_persian_general_instructions(
        tank_main_volume=tank_main.volume_liters,
        tank_calcium_volume=tank_calcium.volume_liters,
        ec_main=ec_main,
        ec_calcium=ec_calcium,
        warnings=combined_warnings
    )
    
    # ============================================================
    # مرحله 8: ساخت نتایج نهایی
    # ============================================================
    
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


# ============================================================
# توابع جدید: تولید دستورالعمل‌های فارسی حرفه‌ای
# ============================================================

def generate_persian_mixing_instructions(
    tank_name: str,
    tank_type: str,
    doses: List[Dict],
    tank_volume: float,
    target_ph_min: float,
    target_ph_max: float,
    warnings: List[Dict]
) -> str:
    """تولید دستورالعمل اختلاط به زبان فارسی"""
    
    instructions = []
    
    instructions.append("=" * 60)
    instructions.append(f"📋 دستورالعمل ساخت {tank_name}")
    instructions.append("=" * 60)
    instructions.append("")
    instructions.append(f"📦 حجم مخزن: {tank_volume:,.0f} لیتر")
    instructions.append("")
    
    if tank_type == "calcium":
        instructions.append("⚠️ نکته مهم برای مخزن کلسیم:")
        instructions.append("   - این مخزن حاوی کلسیم است")
        instructions.append("   - هرگز کودهای این مخزن را با مخزن اصلی مخلوط نکنید")
        instructions.append("   - pH نهایی باید بین 6.0 تا 6.5 باشد")
    else:
        instructions.append("⚠️ نکته مهم برای مخزن اصلی:")
        instructions.append("   - این مخزن حاوی کودهای NPK، سولفات‌ها و ریز مغذی‌ها است")
        instructions.append("   - pH نهایی باید بین 5.5 تا 6.2 باشد")
    
    instructions.append("")
    instructions.append("🔧 مراحل ساخت:")
    instructions.append("")
    instructions.append("مرحله 1: مخزن را تا 70 درصد با آب تمیز پر کنید")
    instructions.append("")
    instructions.append("مرحله 2: کودها را به ترتیب زیر اضافه کنید:")
    instructions.append("")
    
    for i, dose in enumerate(doses, 1):
        stock_text = ""
        if dose.get('stock_200x_g_per_liter'):
            stock_text = f" (محلول مادر 200x: {dose['stock_200x_g_per_liter']} گرم در لیتر آب)"
        
        instructions.append(f"   {i}. {dose['name']}:")
        instructions.append(f"      - مقدار مصرف: {dose['dose_g_per_liter']} گرم در لیتر")
        instructions.append(f"      - مجموع برای مخزن: {dose['dose_g_for_tank']:,.1f} گرم{stock_text}")
        instructions.append("")
    
    instructions.append("مرحله 3: بعد از اضافه کردن هر کود، به مدت 2 دقیقه هم بزنید")
    instructions.append("")
    instructions.append("مرحله 4: مخزن را تا حجم نهایی پر کنید و 5 دقیقه دیگر هم بزنید")
    instructions.append("")
    instructions.append(f"مرحله 5: pH را با اسید فسفریک یا سولفوریک در محدوده {target_ph_min} تا {target_ph_max} تنظیم کنید")
    instructions.append("")
    instructions.append("=" * 60)
    
    # اضافه کردن هشدارها
    if warnings:
        instructions.append("")
        instructions.append("⚠️ هشدارهای مهم:")
        seen = set()
        for warn in warnings:
            msg = warn.get('message', str(warn))
            if msg not in seen:
                instructions.append(f"   • {msg}")
                seen.add(msg)
        instructions.append("")
        instructions.append("=" * 60)
    
    return "\n".join(instructions)


def generate_persian_general_instructions(
    tank_main_volume: float,
    tank_calcium_volume: float,
    ec_main: float,
    ec_calcium: float,
    warnings: List[Dict]
) -> str:
    """تولید دستورالعمل کلی فارسی برای استفاده از دو مخزن"""
    
    instructions = []
    
    instructions.append("=" * 60)
    instructions.append("🌱 دستورالعمل کلی استفاده از سیستم دو مخزن")
    instructions.append("=" * 60)
    instructions.append("")
    instructions.append("📌 اصل اساسی:")
    instructions.append("   در سیستم‌های هیدروپونیک حرفه‌ای، کودهای حاوی کلسیم باید جدا از سایر کودها")
    instructions.append("   نگهداری شوند تا از رسوب و واکنش‌های شیمیایی جلوگیری شود.")
    instructions.append("")
    instructions.append("=" * 60)
    instructions.append("🧪 مخزن A (مخزن کلسیم)")
    instructions.append("=" * 60)
    instructions.append(f"   حجم: {tank_calcium_volume:,.0f} لیتر")
    instructions.append(f"   EC پیش‌بینی: {ec_calcium} mS/cm")
    instructions.append("   محتویات: نیترات کلسیم، کلات آهن، سایر کودهای کلسیمی")
    instructions.append("   محدوده pH: 6.0 - 6.5")
    instructions.append("")
    instructions.append("=" * 60)
    instructions.append("🧪 مخزن B (مخزن اصلی)")
    instructions.append("=" * 60)
    instructions.append(f"   حجم: {tank_main_volume:,.0f} لیتر")
    instructions.append(f"   EC پیش‌بینی: {ec_main} mS/cm")
    instructions.append("   محتویات: کودهای NPK، سولفات پتاسیم، منیزیم سولفات، ریز مغذی‌ها")
    instructions.append("   محدوده pH: 5.5 - 6.2")
    instructions.append("")
    instructions.append("=" * 60)
    instructions.append("⚠️ نکات بسیار مهم")
    instructions.append("=" * 60)
    instructions.append("")
    instructions.append("1️⃣ هرگز کودهای دو مخزن را قبل از مصرف با هم مخلوط نکنید!")
    instructions.append("   - این کار باعث رسوب و از بین رفتن محلول غذایی می‌شود")
    instructions.append("")
    instructions.append("2️⃣ ترتیب ساخت مخازن:")
    instructions.append("   - ابتدا مخزن اصلی (B) را آماده کنید")
    instructions.append("   - سپس مخزن کلسیم (A) را آماده کنید")
    instructions.append("")
    instructions.append("3️⃣ نحوه تزریق به سیستم آبیاری:")
    instructions.append("   - از دو انژکتور جداگانه استفاده کنید")
    instructions.append("   - هر دو مخزن را همزمان و با دبی یکسان تزریق کنید")
    instructions.append("")
    instructions.append("4️⃣ برنامه تغذیه پیشنهادی:")
    instructions.append("   - هفته اول: 50% دوز محاسبه شده")
    instructions.append("   - هفته دوم: 75% دوز محاسبه شده")
    instructions.append("   - هفته سوم به بعد: 100% دوز محاسبه شده")
    instructions.append("")
    instructions.append("5️⃣ در صورت مشاهده رسوب سفید:")
    instructions.append("   - دوز کودهای کلسیمی را کاهش دهید")
    instructions.append("   - pH مخزن کلسیم را دقیقاً در 6.2 تنظیم کنید")
    instructions.append("   - آب ورودی را تصفیه کنید")
    instructions.append("")
    
    # اضافه کردن هشدارهای اضافی
    severe_warnings = [w for w in warnings if w.get('severity') == 'error']
    if severe_warnings:
        instructions.append("")
        instructions.append("=" * 60)
        instructions.append("🚨 هشدارهای بحرانی")
        instructions.append("=" * 60)
        for warn in severe_warnings:
            instructions.append(f"   • {warn.get('message', str(warn))}")
    
    instructions.append("")
    instructions.append("=" * 60)
    instructions.append("✅ موفق باشید!")
    instructions.append("=" * 60)
    
    return "\n".join(instructions)


# ============================================================
# تابع قبلی separate_into_tanks (حفظ شده برای سازگاری)
# ============================================================

def separate_into_tanks(doses: List[Dict]) -> List[Dict]:
    """
    تفکیک کودها به دو مخزن بر اساس استاندارد جهانی (نسخه قبلی برای سازگاری)
    """
    return separate_into_tanks_professional(doses)