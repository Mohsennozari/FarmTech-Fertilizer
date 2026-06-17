# backend/app/calculator/dual_tank.py

from typing import List, Dict, Tuple, Optional
import copy
from .core import calculate_water_contribution, SUPPORTED_ELEMENTS
from .ec import calculate_final_ec
from .optimization import optimize_fertilizer_doses_professional
from .tank import calculate_tank_doses
from .instructions import generate_persian_mixing_instructions, generate_persian_general_instructions


# ============================================================
# ماتریس تداخلات شیمیایی (مرحله 3)
# ============================================================

# گروه‌بندی کودها بر اساس خطر تداخل
FERTILIZER_GROUPS = {
    "calcium": ["calcium nitrate", "نیترات کلسیم", "calcium chloride", "کلرید کلسیم"],
    "sulfate": ["magnesium sulfate", "سولفات منیزیم", "potassium sulfate", "سولفات پتاسیم", "ammonium sulfate", "سولفات آمونیوم"],
    "phosphate": ["mkp", "monopotassium phosphate", "مونو پتاسیم فسفات", "map", "ammonium phosphate", "فسفات آمونیوم", "dap"],
    "iron_chelate": ["fe edta", "fe eddha", "iron chelate", "کلات آهن", "fe chelate"],
    "micro": ["zinc sulfate", "سولفات روی", "manganese sulfate", "سولفات منگنز", "copper sulfate", "سولفات مس"]
}

# ماتریس ناسازگاری: (group1, group2) -> (severity, warning_message)
INCOMPATIBILITY_MATRIX = {
    ("calcium", "sulfate"): {
        "severity": "high",
        "message": "⚠️ خطر رسوب گچ (کلسیم سولفات)! این دو گروه هرگز نباید در یک مخزن مخلوط شوند.",
        "reaction": "Ca²⁺ + SO₄²⁻ → CaSO₄ ↓ (رسوب سفید)",
        "prevention": "حتماً در مخازن جداگانه نگهداری شوند."
    },
    ("calcium", "phosphate"): {
        "severity": "critical",
        "message": "🚨 خطر رسوب کلسیم فسفات! این ترکیب لوله‌ها و قطره‌چکان‌ها را مسدود می‌کند.",
        "reaction": "3Ca²⁺ + 2PO₄³⁻ → Ca₃(PO₄)₂ ↓ (رسوب نامحلول)",
        "prevention": "هرگز در یک مخزن مخلوط نشوند. حتماً در مخازن A و B جداگانه."
    },
    ("iron_chelate", "phosphate"): {
        "severity": "medium",
        "message": "⚠️ کلات آهن با فسفات تداخل دارد. ممکن است آهن رسوب کند.",
        "reaction": "Fe-EDTA + PO₄³⁻ → FePO₄ ↓ + EDTA",
        "prevention": "بهتر است در مخازن جداگانه نگهداری شوند."
    },
    ("iron_chelate", "sulfate"): {
        "severity": "low",
        "message": "⚠️ کلات آهن با سولفات‌ها تداخل متوسطی دارد.",
        "reaction": "احتمال رسوب جزئی آهن",
        "prevention": "قابل قبول در یک مخزن، اما pH را کنترل کنید."
    },
    ("calcium", "micro"): {
        "severity": "medium",
        "message": "⚠️ کلسیم با برخی ریز مغذی‌ها (روی، منگنز، مس) تداخل دارد.",
        "reaction": "احتمال رسوب هیدروکسیدهای فلزی",
        "prevention": "ریز مغذی‌ها بهتر است در مخزن اصلی (B) باشند."
    }
}


# ============================================================
# مرحله 4: ضریب پویای تقسیم نیتروژن
# ============================================================

# جدول ضرایب تقسیم نیتروژن بین مخزن کلسیم و اصلی
# بر اساس نوع گیاه و مرحله رشد
NITROGEN_SPLIT_RATIOS = {
    # گیاهان گلخانه‌ای رایج
    "tomato": {
        "vegetative": 0.45,      # مرحله رویشی: نیاز N بالا
        "flowering": 0.35,       # مرحله گلدهی: نیاز N متوسط
        "fruiting": 0.30,        # مرحله میوه‌دهی: نیاز N کمتر
        "ripening": 0.25         # مرحله رسیدگی: نیاز N کم
    },
    "cucumber": {
        "vegetative": 0.50,
        "flowering": 0.40,
        "fruiting": 0.35,
        "ripening": 0.30
    },
    "pepper": {
        "vegetative": 0.45,
        "flowering": 0.38,
        "fruiting": 0.32,
        "ripening": 0.28
    },
    "strawberry": {
        "vegetative": 0.40,
        "flowering": 0.35,
        "fruiting": 0.30,
        "ripening": 0.25
    },
    "lettuce": {
        "vegetative": 0.55,       # کاهو همیشه نیاز N بالایی دارد
        "harvest": 0.50
    },
    "eggplant": {
        "vegetative": 0.45,
        "flowering": 0.38,
        "fruiting": 0.32,
        "ripening": 0.28
    },
    "bean": {
        "vegetative": 0.35,       # لوبیا N کمتری نیاز دارد (تثبیت نیتروژن)
        "flowering": 0.30,
        "fruiting": 0.25
    },
    # گیاهان زینتی
    "rose": {
        "vegetative": 0.50,
        "flowering": 0.40,
        "dormant": 0.30
    },
    "gerbera": {
        "vegetative": 0.45,
        "flowering": 0.38,
        "dormant": 0.30
    },
    # پیش‌فرض برای گیاهان دیگر
    "default": {
        "vegetative": 0.40,
        "flowering": 0.35,
        "fruiting": 0.30,
        "ripening": 0.25,
        "default": 0.35
    }
}

# مترادف‌های نام گیاهان برای تطابق بهتر
CROP_SYNONYMS = {
    "tomato": ["tomato", "گوجه", "گوجه فرنگی", "گوجه‌فرنگی", "solanum lycopersicum"],
    "cucumber": ["cucumber", "خیار", "cucumis sativus"],
    "pepper": ["pepper", "فلفل", "capsicum", "فلفل دلمه‌ای"],
    "strawberry": ["strawberry", "توت فرنگی", "توت‌فرنگی", "fragaria"],
    "lettuce": ["lettuce", "کاهو", "lactuca sativa"],
    "eggplant": ["eggplant", "بادمجان", "aubergine", "solanum melongena"],
    "bean": ["bean", "لوبیا", "phaseolus"],
    "rose": ["rose", "رز", "گل رز", "rosa"],
    "gerbera": ["gerbera", "ژربرا", "gerbera jamesonii"]
}


def get_fertilizer_group(fertilizer) -> str:
    """
    تشخیص گروه یک کود بر اساس نام و ترکیبات

    Returns:
        نام گروه (calcium, sulfate, phosphate, iron_chelate, micro, unknown)
    """
    if not fertilizer:
        return "unknown"

    fert_name = (fertilizer.name or "").lower()
    fert_type = (fertilizer.fertilizer_type or "").lower()

    # بررسی کلسیم
    if (fertilizer.ca_percent or 0) > 0:
        return "calcium"
    if any(keyword in fert_name for keyword in FERTILIZER_GROUPS["calcium"]):
        return "calcium"

    # بررسی فسفات
    if (fertilizer.p_percent or 0) > 0 and (fertilizer.ca_percent or 0) == 0:
        if any(keyword in fert_name for keyword in FERTILIZER_GROUPS["phosphate"]):
            return "phosphate"
        if fert_type in ["phosphate", "pk"]:
            return "phosphate"

    # بررسی سولفات
    if (fertilizer.s_percent or 0) > 0 and (fertilizer.ca_percent or 0) == 0:
        if any(keyword in fert_name for keyword in FERTILIZER_GROUPS["sulfate"]):
            return "sulfate"
        if "sulfate" in fert_name or "سولفات" in fert_name:
            return "sulfate"

    # بررسی کلات آهن
    if (fertilizer.fe_percent or 0) > 0:
        if any(keyword in fert_name for keyword in FERTILIZER_GROUPS["iron_chelate"]):
            return "iron_chelate"
        if "chelate" in fert_name or "کلات" in fert_name:
            return "iron_chelate"

    # بررسی ریز مغذی‌ها
    micro_elements = ['zn', 'mn', 'cu', 'b', 'mo']
    for elem in micro_elements:
        if getattr(fertilizer, f"{elem}_percent", 0) > 0:
            return "micro"

    return "unknown"


def check_incompatibility(fertilizers: List) -> List[Dict]:
    """
    بررسی تداخلات شیمیایی بین لیستی از کودها

    Args:
        fertilizers: لیست کودها (هر کود شامل object یا id)

    Returns:
        لیستی از هشدارهای تداخل
    """
    warnings = []

    # گرفتن گروه هر کود
    groups = []
    for fert in fertilizers:
        group = get_fertilizer_group(fert)
        groups.append({
            "fertilizer": fert,
            "name": fert.name,
            "group": group
        })

    # بررسی جفت‌های ناسازگار
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            group1 = groups[i]["group"]
            group2 = groups[j]["group"]

            # بررسی هر دو جهت
            key = (group1, group2)
            if key in INCOMPATIBILITY_MATRIX:
                incompat = INCOMPATIBILITY_MATRIX[key]
                warnings.append({
                    "type": "incompatibility",
                    "severity": incompat["severity"],
                    "fertilizer1": groups[i]["name"],
                    "fertilizer2": groups[j]["name"],
                    "message": incompat["message"],
                    "reaction": incompat.get("reaction", ""),
                    "prevention": incompat.get("prevention", "")
                })

            # بررسی جهت معکوس
            key_rev = (group2, group1)
            if key_rev in INCOMPATIBILITY_MATRIX:
                incompat = INCOMPATIBILITY_MATRIX[key_rev]
                warnings.append({
                    "type": "incompatibility",
                    "severity": incompat["severity"],
                    "fertilizer1": groups[j]["name"],
                    "fertilizer2": groups[i]["name"],
                    "message": incompat["message"],
                    "reaction": incompat.get("reaction", ""),
                    "prevention": incompat.get("prevention", "")
                })

    # حذف هشدارهای تکراری
    unique_warnings = []
    seen = set()
    for warn in warnings:
        key = f"{warn['fertilizer1']}_{warn['fertilizer2']}"
        if key not in seen:
            seen.add(key)
            unique_warnings.append(warn)

    return unique_warnings


def get_crop_type(crop_name: str) -> str:
    """
    تشخیص نوع گیاه از روی نام وارد شده

    Args:
        crop_name: نام گیاه (می‌تواند فارسی یا انگلیسی باشد)

    Returns:
        کلید استاندارد گیاه (مثل tomato, cucumber, ...)
    """
    if not crop_name:
        return "default"

    crop_lower = crop_name.lower().strip()

    for standard_name, synonyms in CROP_SYNONYMS.items():
        if crop_lower in synonyms or any(syn in crop_lower for syn in synonyms):
            return standard_name

    return "default"


def get_growth_stage(stage_name: str) -> str:
    """
    تشخیص مرحله رشد از روی نام وارد شده

    Args:
        stage_name: نام مرحله رشد

    Returns:
        کلید استاندارد مرحله (vegetative, flowering, fruiting, ripening, dormant, harvest)
    """
    if not stage_name:
        return "default"

    stage_lower = stage_name.lower().strip()

    # نگاشت مراحل مختلف به کلیدهای استاندارد
    stage_mapping = {
        "vegetative": ["vegetative", "رویشی", "رشد رویشی", "vegetation", "growth"],
        "flowering": ["flowering", "گلدهی", "شکوفه", "bloom", "flower"],
        "fruiting": ["fruiting", "میوه‌دهی", "تشکیل میوه", "fruit", "fruit set"],
        "ripening": ["ripening", "رسیدگی", "رسیدن", "ripe", "maturation"],
        "dormant": ["dormant", "خواب", "استراحت", "dormancy"],
        "harvest": ["harvest", "برداشت", "harvesting", "ready"]
    }

    for standard_stage, synonyms in stage_mapping.items():
        if stage_lower in synonyms or any(syn in stage_lower for syn in synonyms):
            return standard_stage

    return "default"


def get_nitrogen_split_ratio(crop_type: str = None, growth_stage: str = None) -> float:
    """
    محاسبه ضریب تقسیم نیتروژن بر اساس نوع گیاه و مرحله رشد

    Args:
        crop_type: نوع گیاه (مثال: tomato, cucumber, گوجه, خیار)
        growth_stage: مرحله رشد (مثال: vegetative, flowering, رویشی, گلدهی)

    Returns:
        ضریب تقسیم نیتروژن (بین 0.2 تا 0.6)
    """
    # تشخیص نوع گیاه
    crop_key = get_crop_type(crop_type) if crop_type else "default"

    # تشخیص مرحله رشد
    stage_key = get_growth_stage(growth_stage) if growth_stage else "default"

    # دریافت ضرایب برای این گیاه
    crop_ratios = NITROGEN_SPLIT_RATIOS.get(crop_key, NITROGEN_SPLIT_RATIOS["default"])

    # دریافت ضریب برای این مرحله
    ratio = crop_ratios.get(stage_key, crop_ratios.get("default", 0.35))

    # محدودیت منطقی (بین 0.2 و 0.6)
    ratio = max(0.20, min(0.60, ratio))

    return ratio


def get_split_ratio_explanation(crop_type: str = None, growth_stage: str = None) -> str:
    """
    تولید توضیح برای ضریب تقسیم نیتروژن انتخاب شده
    """
    ratio = get_nitrogen_split_ratio(crop_type, growth_stage)

    crop_display = crop_type if crop_type else "نامشخص"
    stage_display = growth_stage if growth_stage else "نامشخص"

    explanation = f"""📊 ضریب تقسیم نیتروژن: {ratio:.0%}

🧫 بر اساس:
   • نوع گیاه: {crop_display}
   • مرحله رشد: {stage_display}

📌 معنی این ضریب:
   {ratio:.0%} از نیتروژن مورد نیاز گیاه توسط مخزن کلسیم (نیترات کلسیم) تأمین می‌شود.
   بقیه نیتروژن ({1-ratio:.0%}) توسط مخزن اصلی (کودهای NPK) تأمین می‌شود.

💡 نکته: این تقسیم‌بندی از رسوب کلسیم با سولفات و فسفات جلوگیری می‌کند."""

    return explanation


def separate_into_tanks_professional(doses: List[Dict]) -> List[Dict]:
    """
    تفکیک کودها به دو مخزن بر اساس استاندارد جهانی هیدروپونیک
    با در نظر گرفتن تداخلات شیمیایی
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

    incompatibility_warnings = []

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

    # بررسی تداخلات شیمیایی در مخازن
    if tank_a["doses"]:
        class DummyFertilizer:
            def __init__(self, name, ca_percent=0, p_percent=0, s_percent=0, fe_percent=0):
                self.name = name
                self.ca_percent = ca_percent
                self.p_percent = p_percent
                self.s_percent = s_percent
                self.fe_percent = fe_percent

        tank_a_ferts = []
        for dose in tank_a["doses"]:
            ca = 19 if 'calcium' in dose['name'].lower() or 'کلسیم' in dose['name'] else 0
            fert = DummyFertilizer(dose['name'], ca_percent=ca)
            tank_a_ferts.append(fert)

        a_warnings = check_incompatibility(tank_a_ferts)
        for warn in a_warnings:
            warn["tank"] = "A (کلسیم)"
            incompatibility_warnings.append(warn)

    if tank_b["doses"]:
        class DummyFertilizer:
            def __init__(self, name, ca_percent=0, p_percent=0, s_percent=0, fe_percent=0):
                self.name = name
                self.ca_percent = ca_percent
                self.p_percent = p_percent
                self.s_percent = s_percent
                self.fe_percent = fe_percent

        tank_b_ferts = []
        for dose in tank_b["doses"]:
            name_lower = dose['name'].lower()
            p = 20 if 'npk' in name_lower or 'phosphate' in name_lower else 0
            s = 13 if 'sulfate' in name_lower or 'سولفات' in name_lower else 0
            fe = 6 if 'iron' in name_lower or 'آهن' in name_lower else 0
            fert = DummyFertilizer(dose['name'], p_percent=p, s_percent=s, fe_percent=fe)
            tank_b_ferts.append(fert)

        b_warnings = check_incompatibility(tank_b_ferts)
        for warn in b_warnings:
            warn["tank"] = "B (اصلی)"
            incompatibility_warnings.append(warn)

    # اضافه کردن هشدارهای تداخل به توضیحات مخازن
    critical_warnings = [w for w in incompatibility_warnings if w.get('severity') == 'critical']
    high_warnings = [w for w in incompatibility_warnings if w.get('severity') == 'high']

    if critical_warnings:
        tank_b["description"] += "\n\n🚨 هشدار بحرانی - تداخل شیمیایی:\n"
        for warn in critical_warnings:
            tank_b["description"] += f"   • {warn['message']}\n"

    if high_warnings:
        tank_a["description"] += "\n\n⚠️ هشدار مهم - تداخل شیمیایی:\n"
        for warn in high_warnings:
            tank_a["description"] += f"   • {warn['message']}\n"

    # اضافه کردن هشدارهای قبلی برای دوز بالا
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
    max_total_dose: float = 5.0,
    crop_type: Optional[str] = None,        # پارامتر جدید برای تشخیص نوع گیاه
    growth_stage: Optional[str] = None      # پارامتر جدید برای تشخیص مرحله رشد
) -> Tuple[Dict, Dict, List[Dict], str]:
    """
    محاسبه دوز بهینه برای دو مخزن با استفاده از الگوریتم لایه‌به‌لایه حرفه‌ای
    با در نظر گرفتن تداخلات شیمیایی و ضریب پویای تقسیم نیتروژن

    Args:
        remaining_needs: نیازهای باقیمانده پس از کسر آب
        all_fertilizers: لیست همه کودهای موجود
        tank_main: اطلاعات مخزن اصلی
        tank_calcium: اطلاعات مخزن کلسیم
        brand_filter: فیلتر برند (اختیاری)
        max_total_dose: حداکثر دوز کل
        crop_type: نوع گیاه (برای ضریب تقسیم نیتروژن)
        growth_stage: مرحله رشد (برای ضریب تقسیم نیتروژن)
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

    # ============================================================
    # محاسبه ضریب پویای تقسیم نیتروژن (مرحله 4)
    # ============================================================

    nitrogen_split_ratio = get_nitrogen_split_ratio(crop_type, growth_stage)
    split_explanation = get_split_ratio_explanation(crop_type, growth_stage)

    # ============================================================
    # تفکیک هوشمند کودها با در نظر گرفتن تداخلات
    # ============================================================

    fertilizers_for_calcium = []
    fertilizers_for_main = []

    calcium_keywords = [
        'calcium', 'کلسیم', 'نیترات کلسیم', 'calcium nitrate',
        'iron', 'آهن', 'chelate', 'کلات', 'fe chelate', 'iron chelate'
    ]

    incompatibility_warnings = []

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

    # بررسی تداخلات در مخازن
    if fertilizers_for_calcium:
        ca_warnings = check_incompatibility(fertilizers_for_calcium)
        for warn in ca_warnings:
            warn["tank"] = "مخزن کلسیم"
            incompatibility_warnings.append(warn)

    if fertilizers_for_main:
        main_warnings = check_incompatibility(fertilizers_for_main)
        for warn in main_warnings:
            warn["tank"] = "مخزن اصلی"
            incompatibility_warnings.append(warn)

    # تقسیم نیازها با ضریب پویا
    water_calcium = calculate_water_contribution(tank_calcium)
    water_main = calculate_water_contribution(tank_main)

    # استفاده از ضریب پویا به جای 35% ثابت
    needs_calcium = {
        'Ca': max(0, remaining_needs.get('Ca', 0) - water_calcium.get('Ca', 0)),
        'Fe': max(0, remaining_needs.get('Fe', 0) - water_calcium.get('Fe', 0)),
        'N': max(0, remaining_needs.get('N', 0) * nitrogen_split_ratio),
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

    # اضافه کردن توضیح ضریب تقسیم به هشدارها
    warnings_calcium.append({
        "type": "nitrogen_split_info",
        "severity": "info",
        "message": split_explanation
    })

    # اضافه کردن هشدارهای تداخل
    for warn in incompatibility_warnings:
        if warn.get("tank") == "مخزن کلسیم":
            warnings_calcium.append({
                "type": "incompatibility",
                "severity": warn.get("severity", "warning"),
                "message": f"{warn.get('message', '')} (کود: {warn.get('fertilizer1', '')} و {warn.get('fertilizer2', '')})"
            })

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

    # اضافه کردن هشدارهای تداخل به warnings_main
    for warn in incompatibility_warnings:
        if warn.get("tank") == "مخزن اصلی":
            warnings_main.append({
                "type": "incompatibility",
                "severity": warn.get("severity", "warning"),
                "message": f"{warn.get('message', '')} (کود: {warn.get('fertilizer1', '')} و {warn.get('fertilizer2', '')})"
            })

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

    # اضافه کردن هشدارهای تداخل بحرانی
    critical_incompat = [w for w in incompatibility_warnings if w.get('severity') == 'critical']
    for warn in critical_incompat:
        combined_warnings.append({
            "type": "critical_incompatibility",
            "severity": "error",
            "message": f"🚨 {warn.get('message', '')} در {warn.get('tank', 'مخزن')}",
            "reaction": warn.get('reaction', ''),
            "prevention": warn.get('prevention', '')
        })

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
        "water_contribution": water_main,
        "nitrogen_split_ratio": nitrogen_split_ratio
    }

    result_calcium = {
        "doses": doses_calcium,
        "supplied_ppm": supply_calcium,
        "warnings": warnings_calcium,
        "mixing_instructions": mixing_calcium,
        "ec_predicted": ec_calcium,
        "water_contribution": water_calcium,
        "nitrogen_split_ratio": nitrogen_split_ratio
    }

    return result_main, result_calcium, combined_warnings, general_instructions
