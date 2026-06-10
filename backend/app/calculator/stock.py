# backend/app/calculator/stock.py

from typing import List, Dict, Tuple


def calculate_dose_kg_for_stock(
    dose_gpl: float,
    injector_ratio: float,
    stock_tank_volume_liters: float
) -> float:
    """
    محاسبه مقدار کود مورد نیاز برای ساخت استوک (کیلوگرم)
    
    فرمول: مقدار کود (کیلوگرم) = (دوز مصرف (گرم در لیتر) × نسبت تزریق (X) × حجم استوک (لیتر)) ÷ 1000
    
    Args:
        dose_gpl: دوز مصرف کود به گرم در لیتر (محلول نهایی)
        injector_ratio: نسبت تزریق (مثلاً 200 برای 1:200)
        stock_tank_volume_liters: حجم مخزن استوک به لیتر
    
    Returns:
        مقدار کود به کیلوگرم (با گردش به 2 رقم اعشار)
    """
    dose_kg = (dose_gpl * injector_ratio * stock_tank_volume_liters) / 1000
    return round(dose_kg, 2)


def calculate_stock_consumption(
    injector_ratio: float,
    main_tank_volume_liters: float
) -> Tuple[float, float]:
    """
    محاسبه مقدار مصرف استوک در مخزن اصلی
    
    Args:
        injector_ratio: نسبت تزریق (مثلاً 200 برای 1:200)
        main_tank_volume_liters: حجم مخزن اصلی به لیتر
    
    Returns:
        (stock_liters_for_main_tank, stock_ml_per_liter)
        - stock_liters_for_main_tank: مقدار استوک بر حسب لیتر برای کل مخزن
        - stock_ml_per_liter: مقدار استوک بر حسب میلی‌لیتر برای هر لیتر آب
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


def add_stock_calculations_to_doses(
    doses: List[Dict],
    tank_volume_liters: float,
    injector_ratio: float,
    stock_tank_volume_liters: float
) -> List[Dict]:
    """
    اضافه کردن محاسبات استوک به لیست دوزها
    
    Args:
        doses: لیست دوزهای محاسبه شده (هر دوز شامل dose_g_per_liter و name)
        tank_volume_liters: حجم مخزن اصلی
        injector_ratio: نسبت تزریق
        stock_tank_volume_liters: حجم مخزن استوک
    
    Returns:
        لیست دوزها با فیلدهای جدید استوک
    """
    result = []
    for dose in doses:
        dose_gpl = dose.get('dose_g_per_liter', 0)
        
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
        
        result.append(new_dose)
    
    return result