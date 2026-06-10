# backend/app/calculator/tank.py

from typing import List, Dict


def calculate_tank_doses(doses: List[Dict], tank_volume_liters: float) -> List[Dict]:
    """
    محاسبه دوز برای کل مخزن و استوک 200x
    
    Args:
        doses: لیست دوزهای محاسبه شده (هر دوز شامل dose_g_per_liter و name)
        tank_volume_liters: حجم مخزن به لیتر
    
    Returns:
        لیست دوزها با فیلدهای جدید:
        - dose_g_for_tank: دوز کل برای مخزن (گرم)
        - stock_200x_g_per_liter: دوز برای استوک 200x (گرم در لیتر آب)
    """
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