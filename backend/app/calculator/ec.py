# backend/app/calculator/ec.py

from typing import List, Dict, Optional

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