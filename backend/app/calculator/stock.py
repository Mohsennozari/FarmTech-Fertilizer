from typing import List, Dict, Tuple


def calculate_dose_kg_for_stock(
    dose_gpl: float,
    injector_ratio: float,
    stock_tank_volume_liters: float
) -> float:
    """
    محاسبه مقدار کود مورد نیاز برای ساخت استوک (کیلوگرم)

    فرمول: مقدار کود (کیلوگرم) = (دوز مصرف (گرم در لیتر) × نسبت تزریق (X) × حجم استوک (لیتر)) ÷ 1000
    """
    dose_kg = (dose_gpl * injector_ratio * stock_tank_volume_liters) / 1000
    return round(dose_kg, 2)


def calculate_stock_consumption(
    injector_ratio: float,
    main_tank_volume_liters: float
) -> Tuple[float, float]:
    """
    محاسبه مقدار مصرف استوک در مخزن اصلی
    """
    stock_liters_for_main_tank = round(main_tank_volume_liters / injector_ratio, 2)
    stock_ml_per_liter = round(1000 / injector_ratio, 1)
    return stock_liters_for_main_tank, stock_ml_per_liter


def get_injector_explanation(injector_ratio: float) -> str:
    """تولید توضیح ساده برای مفهوم نسبت تزریق"""
    water_ratio = injector_ratio - 1
    return f"""📖 نسبت تزریق 1:{int(injector_ratio)} یعنی:
   1 لیتر استوک + {int(water_ratio)} لیتر آب = {int(injector_ratio)} لیتر محلول نهایی

مثال با نسبت 1:{int(injector_ratio)}:
   1 لیتر استوک + {int(water_ratio)} لیتر آب = {int(injector_ratio)} لیتر محلول نهایی"""


def get_stock_mixing_instructions(fertilizer_names: List[str]) -> str:
    """تولید دستورالعمل گام به گام ساخت استوک"""
    instructions = """🔧 روش ساخت استوک:
1. مخزن تمیز با حجم مناسب آماده کنید
2. 70% حجم مخزن را آب بریزید
3. کودها را به ترتیب زیر اضافه کنید:\n"""

    for i, name in enumerate(fertilizer_names, 1):
        instructions += f"   {i}. {name}\n"

    instructions += """4. بعد از هر کود، 2 دقیقه هم بزنید
5. آب را به حجم نهایی برسانید
6. 5 دقیقه دیگر هم بزنید
7. برچسب بزنید: نام کودها، تاریخ ساخت، نسبت تزریق"""

    return instructions


def get_stock_usage_instructions(injector_ratio: float) -> str:
    """تولید دستورالعمل مصرف استوک در مخزن اصلی"""
    return f"""🔧 روش مصرف استوک در مخزن اصلی:

با نسبت تزریق 1:{int(injector_ratio)}:

1. قبل از مصرف، استوک را خوب تکان دهید
2. مقدار مورد نیاز را اندازه بگیرید
3. به آرامی به مخزن اصلی اضافه کنید
4. 5 دقیقه هم بزنید

⚠️ نکته: هیچگاه استوک حاوی کلسیم را با استوک حاوی سولفات/فسفات قبل از ورود به مخزن اصلی مخلوط نکنید."""


def get_storage_instructions() -> Tuple[str, str, str, str]:
    """تولید نکات نگهداری و ایمنی استوک"""
    storage_instructions = """⚠️ نکات نگهداری و ایمنی استوک:

• همیشه ظرف استوک را محکم ببندید
• دور از نور مستقیم خورشید و در جای خنک نگهداری کنید
• برچسب بزنید: نام کودها، تاریخ ساخت، نسبت تزریق
• دور از دسترس کودکان نگهداری شود"""

    shelf_life_fridge = "7 روز در یخچال (دمای 4 درجه)"
    shelf_life_room = "3 روز در دمای محیط (زیر 25 درجه)"
    warning_signs = "نشانه‌های خرابی: رسوب سفید، تغییر رنگ، بوی نامطبوع، باد کردگی ظرف"

    return storage_instructions, shelf_life_fridge, shelf_life_room, warning_signs


# ============================================================
# توابع جدید برای بررسی حلالیت در استوک (مرحله 2)
# ============================================================

def get_solubility_limit_stock(fertilizer, temperature_c: float = 20.0) -> float:
    """
    برگرداندن حد حلالیت برای محلول استوک
    """
    from .optimization import get_solubility_limit
    return get_solubility_limit(fertilizer, temperature_c)


def check_stock_solubility(
    fertilizer,
    dose_gpl: float,
    injector_ratio: int = 200,
    temperature_c: float = 20.0
) -> Tuple[bool, float, str]:
    """
    بررسی حلالیت در محلول استوک

    Returns:
        (is_ok, max_safe_dose_gpl, warning_message)
    """
    solubility_limit = get_solubility_limit_stock(fertilizer, temperature_c)

    stock_concentration = dose_gpl * injector_ratio

    if stock_concentration <= solubility_limit:
        return True, dose_gpl, ""

    max_safe_stock = solubility_limit * 0.95
    max_safe_dose_gpl = max_safe_stock / injector_ratio

    warning = (
        f"⚠️ غلظت استوک برای {fertilizer.name} ({stock_concentration:.0f} g/L) "
        f"بیشتر از حد حلالیت ({solubility_limit:.0f} g/L) است. "
        f"حداکثر دوز قابل استفاده در استوک: {max_safe_dose_gpl:.3f} g/L "
        f"(معادل {max_safe_stock:.0f} g/L در استوک)"
    )

    return False, max_safe_dose_gpl, warning


def validate_stock_doses(doses: List[Dict], injector_ratio: int = 200, temperature_c: float = 20.0) -> Tuple[List[Dict], List[Dict]]:
    """
    اعتبارسنجی دوزهای استوک از نظر حلالیت
    """
    adjusted_doses = []
    solubility_warnings = []

    for dose in doses:
        fert = dose.get('fertilizer')
        if not fert:
            adjusted_doses.append(dose)
            continue

        dose_gpl = dose.get('dose_g_per_liter', 0)
        is_ok, max_dose_gpl, warning = check_stock_solubility(
            fert, dose_gpl, injector_ratio, temperature_c
        )

        if is_ok:
            adjusted_doses.append(dose)
        else:
            adjusted_dose = dose.copy()
            adjusted_dose['dose_g_per_liter'] = round(max_dose_gpl, 3)
            adjusted_dose['original_dose_g_per_liter'] = round(dose_gpl, 3)
            adjusted_dose['solubility_limited_stock'] = True
            adjusted_doses.append(adjusted_dose)

            solubility_warnings.append({
                "type": "stock_solubility_limit",
                "severity": "warning",
                "fertilizer": fert.name,
                "message": warning,
                "original_dose": round(dose_gpl, 3),
                "adjusted_dose": round(max_dose_gpl, 3)
            })

    return adjusted_doses, solubility_warnings


def add_stock_calculations_to_doses(
    doses: List[Dict],
    tank_volume_liters: float,
    injector_ratio: float,
    stock_tank_volume_liters: float,
    temperature_c: float = 20.0
) -> List[Dict]:
    """
    اضافه کردن محاسبات استوک به لیست دوزها با بررسی حلالیت
    """
    from .optimization import get_solubility_limit

    result = []
    for dose in doses:
        dose_gpl = dose.get('dose_g_per_liter', 0)

        fert = dose.get('fertilizer')
        if fert:
            solubility_limit = get_solubility_limit(fert, temperature_c)
            stock_concentration = dose_gpl * injector_ratio

            if stock_concentration > solubility_limit:
                max_safe_stock = solubility_limit * 0.95
                max_safe_dose = max_safe_stock / injector_ratio

                dose['solubility_warning'] = True
                dose['original_dose_gpl'] = dose_gpl
                dose_gpl = max_safe_dose

        dose_kg_for_stock = calculate_dose_kg_for_stock(
            dose_gpl=dose_gpl,
            injector_ratio=injector_ratio,
            stock_tank_volume_liters=stock_tank_volume_liters
        )

        dose_g_for_stock_alternative = None
        if dose_kg_for_stock < 1 and dose_kg_for_stock > 0:
            dose_g_for_stock_alternative = round(dose_kg_for_stock * 1000, 0)

        new_dose = dose.copy()
        new_dose['dose_kg_for_stock'] = dose_kg_for_stock
        new_dose['dose_g_for_stock_alternative'] = dose_g_for_stock_alternative
        new_dose['dose_g_per_liter'] = round(dose_gpl, 3)

        result.append(new_dose)

    return result
