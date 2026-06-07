# Platform-v3\backend\app\calculator.py

import numpy as np
from typing import List, Dict, Tuple, Optional

# اضافه شدن import برای scipy
try:
    from scipy.optimize import minimize, Bounds
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("Warning: scipy not installed. Using fallback method.")

SUPPORTED_ELEMENTS = ['N', 'P', 'K', 'Ca', 'Mg', 'S', 'Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']


def calculate_element_ppm(fertilizer, dose_g_per_liter: float) -> Dict[str, float]:
    """محاسبه ppm هر عنصر از یک کود با دوز مشخص"""
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
    """محاسبه سهم عناصر از آب مخزن"""
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
    """محاسبه سهم عناصر از اسید مصرفی"""
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


def optimize_fertilizer_doses_professional(
    remaining_needs: Dict[str, float],
    fertilizers: List,
    brand_filter: Optional[str] = None,
    max_total_dose: float = 5.0
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    """
    بهینه‌سازی دوز کودها با استفاده از روش SLSQP (مقید)

    این نسخه بهبود یافته از الگوریتم قبلی است و:
    1. از محدودیت‌های min/max دوز هر کود استفاده می‌کند
    2. مجموع دوزها را محدود می‌کند
    3. پایدارتر از روش least squares است
    """

    if not fertilizers:
        return [], {elem: 0.0 for elem in SUPPORTED_ELEMENTS}, []

    # فیلتر برند
    if brand_filter:
        fertilizers = [f for f in fertilizers if f.brand_name == brand_filter]
        if not fertilizers:
            return [], {elem: 0.0 for elem in SUPPORTED_ELEMENTS}, [{
                "type": "brand_filter",
                "severity": "warning",
                "message": f"No fertilizers found for brand {brand_filter}"
            }]

    # حذف عناصر با نیاز بسیار کم (بهبود پایداری عددی)
    active_needs = {}
    for elem, value in remaining_needs.items():
        if value > 0.5:  # فقط عناصر با نیاز > 0.5 ppm
            active_needs[elem] = value

    # اگر تعداد عناصر فعال خیلی زیاد است، اولویت‌بندی کن
    if len(active_needs) > len(fertilizers) * 2:
        priority_elements = ['N', 'P', 'K', 'Ca', 'Mg', 'Fe']
        active_needs = {k: v for k, v in active_needs.items() if k in priority_elements}

    elem_list = list(active_needs.keys())

    # ساخت ماتریس A (m عنصر × n کود)
    A = []
    for fert in fertilizers:
        purity = (fert.purity_percent or 100) / 100.0
        factor = 10 * purity
        row = []
        for elem in elem_list:
            attr_name = f"{elem.lower()}_percent"
            value = getattr(fert, attr_name, 0) or 0
            row.append(value * factor)
        A.append(row)

    A = np.array(A).T  # transpose برای شکل (m × n)
    b = np.array([active_needs[e] for e in elem_list])

    # تنظیم محدوده دوز برای هر کود
    bounds = []
    for fert in fertilizers:
        min_dose = fert.min_dose_g_per_liter or 0.01
        max_dose = fert.max_dose_g_per_liter or 5.0
        bounds.append((min_dose, max_dose))

    # تابع هدف: minimize squared error
    def objective(x):
        return np.sum((A @ x - b) ** 2)

    # محدودیت مجموع دوز
    def total_dose_constraint(x):
        return max_total_dose - np.sum(x)

    constraints = {'type': 'ineq', 'fun': total_dose_constraint}

    # حدس اولیه (دوز متوسط)
    x0 = np.ones(len(fertilizers)) * 0.5

    # بهینه‌سازی با روش مناسب
    if SCIPY_AVAILABLE and len(elem_list) <= len(fertilizers) * 2:
        try:
            result = minimize(
                objective,
                x0,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints,
                options={'maxiter': 500, 'ftol': 1e-6, 'disp': False}
            )
            doses = result.x
            success = result.success
        except Exception as e:
            print(f"Optimization error: {e}")
            doses = x0
            success = False
    else:
        # Fallback: روش least squares ساده
        try:
            doses, _, _, _ = np.linalg.lstsq(A, b, rcond=1e-4)
            doses = np.maximum(doses, 0)
            doses = np.nan_to_num(doses, 0)
            success = True
        except Exception as e:
            print(f"Least squares error: {e}")
            doses = x0
            success = False

        # اعمال محدودیت‌ها
        for i, (low, high) in enumerate(bounds):
            doses[i] = np.clip(doses[i], low, high)

        total_dose = np.sum(doses)
        if total_dose > max_total_dose:
            doses = doses * (max_total_dose / total_dose)

    # ساخت خروجی
    final_supply = {elem: 0.0 for elem in SUPPORTED_ELEMENTS}
    result_doses = []
    warnings = []

    for i, fert in enumerate(fertilizers):
        if doses[i] > 0.01:
            content = calculate_element_ppm(fert, doses[i])
            for elem in SUPPORTED_ELEMENTS:
                final_supply[elem] += content[elem]

            # بررسی هشدار حداکثر دوز
            max_dose = fert.max_dose_g_per_liter
            if max_dose and doses[i] > max_dose * 0.95:
                warnings.append({
                    "type": "max_dose_approaching",
                    "severity": "warning",
                    "fertilizer": fert.name,
                    "message": f"Dose for {fert.name} ({round(doses[i], 3)} g/L) is near maximum ({max_dose} g/L)"
                })

            result_doses.append({
                "id": fert.id,
                "name": fert.name,
                "brand_name": fert.brand_name,
                "dose_g_per_liter": round(float(doses[i]), 3),
                "chemical_formula": fert.chemical_formula
            })

    # شناسایی عناصر پوشش داده نشده
    uncovered = []
    for elem in SUPPORTED_ELEMENTS:
        need = remaining_needs.get(elem, 0)
        supply = final_supply[elem]
        if need > 1.0 and supply < need * 0.7:
            uncovered.append(elem)

    if uncovered:
        warnings.append({
            "type": "partial_coverage",
            "severity": "warning",
            "message": f"Elements not fully supplied: {', '.join(uncovered)}",
            "fertilizers": []
        })

    if not success:
        warnings.append({
            "type": "optimization",
            "severity": "warning",
            "message": "Optimization did not fully converge. Results may be suboptimal.",
            "fertilizers": []
        })

    result_doses.sort(key=lambda x: x['dose_g_per_liter'], reverse=True)
    return result_doses, final_supply, warnings


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
    """تولید دستورالعمل اختلاط حرفه‌ای"""
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
    instructions.append("2. Add fertilizers in this order (avoid mixing incompatible ones):")
    instructions.append("")

    # تفکیک کودهای کلسیمی و فسفری (برای جلوگیری از رسوب)
    calcium_fertilizers = []
    phosphorus_fertilizers = []
    other_fertilizers = []

    for dose in doses:
        if 'calcium' in dose['name'].lower() or 'کلسیم' in dose['name']:
            calcium_fertilizers.append(dose)
        elif 'phosphate' in dose['name'].lower() or 'فسفر' in dose['name'] or '10-52' in dose['name']:
            phosphorus_fertilizers.append(dose)
        else:
            other_fertilizers.append(dose)

    step_num = 1
    for dose in other_fertilizers:
        instructions.append(f"   {step_num}. {dose['name']}: {dose['dose_g_per_liter']} g/L")
        instructions.append(f"      Total for tank: {dose['dose_g_for_tank']} g")
        step_num += 1

    if calcium_fertilizers:
        instructions.append("")
        instructions.append("   ⚠️ Add calcium fertilizers separately:")
        for dose in calcium_fertilizers:
            instructions.append(f"   {step_num}. {dose['name']}: {dose['dose_g_per_liter']} g/L")
            instructions.append(f"      Total for tank: {dose['dose_g_for_tank']} g")
            step_num += 1

    if phosphorus_fertilizers:
        instructions.append("")
        instructions.append("   ⚠️ Add phosphorus fertilizers last:")
        for dose in phosphorus_fertilizers:
            instructions.append(f"   {step_num}. {dose['name']}: {dose['dose_g_per_liter']} g/L")
            instructions.append(f"      Total for tank: {dose['dose_g_for_tank']} g")
            step_num += 1

    instructions.append("")
    instructions.append(f"{step_num}. After adding each fertilizer, mix well for 2 minutes")
    instructions.append("")
    instructions.append(f"{step_num+1}. Fill to final volume and mix for 5 more minutes")
    instructions.append("")
    instructions.append(f"{step_num+2}. Measure and adjust EC and pH")
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
        seen_messages = set()
        for warn in warnings:
            msg = warn.get('description', warn.get('message', ''))
            if msg not in seen_messages:
                instructions.append(f"   ⚠️ {msg}")
                seen_messages.add(msg)

    return "\n".join(instructions)
