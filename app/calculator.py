# Platform-v3\backend\app\calculator.py

import numpy as np
from typing import List, Dict, Tuple, Optional

SUPPORTED_ELEMENTS = ['N', 'P', 'K', 'Ca', 'Mg', 'S', 'Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']


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


def optimize_fertilizer_doses_professional(
    remaining_needs: Dict[str, float],
    fertilizers: List,
    brand_filter: Optional[str] = None,
    max_total_dose: float = 10.0
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    
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
    
    A = []
    for fert in fertilizers:
        purity = (fert.purity_percent or 100) / 100.0
        factor = 10 * purity
        row = [
            (fert.n_percent or 0) * factor,
            (fert.p_percent or 0) * factor,
            (fert.k_percent or 0) * factor,
            (fert.ca_percent or 0) * factor,
            (fert.mg_percent or 0) * factor,
            (fert.s_percent or 0) * factor,
            (fert.fe_percent or 0) * factor,
            (fert.zn_percent or 0) * factor,
            (fert.mn_percent or 0) * factor,
            (fert.cu_percent or 0) * factor,
            (fert.b_percent or 0) * factor,
            (fert.mo_percent or 0) * factor,
            (fert.cl_percent or 0) * factor,
        ]
        A.append(row)
    
    A = np.array(A)
    b = np.array([remaining_needs.get(e, 0) for e in SUPPORTED_ELEMENTS])
    
    try:
        doses, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        doses = np.maximum(doses, 0)
    except Exception as e:
        print(f"Optimization error: {e}")
        doses = np.ones(len(fertilizers)) * 0.5
    
    total_dose = np.sum(doses)
    if total_dose > max_total_dose:
        doses = doses * (max_total_dose / total_dose)
    
    dose_warnings = []
    final_supply = {elem: 0.0 for elem in SUPPORTED_ELEMENTS}
    result_doses = []
    
    for i, fert in enumerate(fertilizers):
        if doses[i] > 0.01:
            content = calculate_element_ppm(fert, doses[i])
            for elem in SUPPORTED_ELEMENTS:
                final_supply[elem] += content[elem]
            
            if fert.max_dose_g_per_liter and doses[i] > fert.max_dose_g_per_liter:
                dose_warnings.append({
                    "type": "max_dose_exceeded",
                    "severity": "warning",
                    "fertilizer": fert.name,
                    "message": f"Dose for {fert.name} ({round(doses[i], 3)} g/L) exceeds maximum allowed ({fert.max_dose_g_per_liter} g/L)"
                })
            
            result_doses.append({
                "id": fert.id,
                "name": fert.name,
                "brand_name": fert.brand_name,
                "dose_g_per_liter": round(float(doses[i]), 3),
                "chemical_formula": fert.chemical_formula
            })
    
    result_doses.sort(key=lambda x: x['dose_g_per_liter'], reverse=True)
    return result_doses, final_supply, dose_warnings


def calculate_tank_doses(doses: List[Dict], tank_volume_liters: float) -> List[Dict]:
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
        for warn in warnings:
            instructions.append(f"   - {warn.get('description', warn.get('message', ''))}")
    
    return "\n".join(instructions)