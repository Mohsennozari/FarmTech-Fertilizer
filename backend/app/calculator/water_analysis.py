# backend/app/calculator/water_analysis.py
"""
ماژول محاسبات آنالیز آب و پساب ترکیبی
نسخه: 3.4.0

این ماژول وظیفه محاسبه مقادیر تامینی آب و پساب ترکیبی و
محاسبه کمبود عناصر نسبت به نیازهای هدف را بر عهده دارد.
"""

from typing import Dict, List, Optional, Tuple, Set


# ============================================================
# لیست عناصر استاندارد برای آنالیز آب و پساب
# ============================================================
STANDARD_ELEMENTS: List[str] = [
    "n_no3",   # نیترات
    "p",       # فسفر
    "s",       # گوگرد
    "n_nh4",   # آمونیوم
    "k",       # پتاسیم
    "ca",      # کلسیم
    "mg",      # منیزیم
    "na",      # سدیم
    "cl",      # کلر
    "fe",      # آهن
    "mn",      # منگنز
    "zn",      # روی
    "b",       # بور
    "cu",      # مس
    "mo",      # مولیبدن
    "ec",      # EC (هدایت الکتریکی)
    "ph"       # pH
]

# عناصر ضروری که باید در آنالیز وجود داشته باشند
REQUIRED_KEYS: List[str] = ["n_no3", "p", "k", "ca", "mg", "ec", "ph"]

# مپ کردن نام عناصر بین فرمت‌های مختلف
ELEMENT_MAPPING: Dict[str, str] = {
    "N": "n_no3",
    "N-NO3": "n_no3",
    "NO3": "n_no3",
    "N-NH4": "n_nh4",
    "NH4": "n_nh4",
    "P": "p",
    "S": "s",
    "K": "k",
    "Ca": "ca",
    "Mg": "mg",
    "Na": "na",
    "Cl": "cl",
    "Fe": "fe",
    "Mn": "mn",
    "Zn": "zn",
    "B": "b",
    "Cu": "cu",
    "Mo": "mo"
}


# ============================================================
# توابع اصلی محاسباتی
# ============================================================

def calculate_combined_water(
    water_percent: float,
    wastewater_percent: float,
    water_analysis: Dict[str, float],
    wastewater_analysis: Dict[str, float]
) -> Dict[str, float]:
    """
    محاسبه مقادیر تامینی ترکیبی از آب و پساب

    فرمول: (درصد آب × مقدار آب + درصد پساب × مقدار پساب) / 100

    Args:
        water_percent: درصد آب تامینی (مثلاً 80)
        wastewater_percent: درصد پساب تامینی (مثلاً 20)
        water_analysis: دیکشنری آنالیز آب
        wastewater_analysis: دیکشنری آنالیز پساب

    Returns:
        دیکشنری مقادیر تامینی ترکیبی (با همان کلیدهای ورودی)

    Example:
        >>> combined = calculate_combined_water(
        ...     80, 20,
        ...     {"n_no3": 10, "k": 8, "ca": 50, "ec": 0.4, "ph": 7.0},
        ...     {"n_no3": 25, "k": 15, "ca": 80, "ec": 1.2, "ph": 6.5}
        ... )
        >>> print(combined)
        {"n_no3": 13.0, "k": 9.4, "ca": 56.0, "ec": 0.56, "ph": 6.9}
    """
    combined: Dict[str, float] = {}

    # دریافت همه کلیدهای موجود در هر دو آنالیز
    all_keys: Set[str] = set(water_analysis.keys()) | set(wastewater_analysis.keys())

    for key in all_keys:
        water_val = water_analysis.get(key, 0.0)
        wastewater_val = wastewater_analysis.get(key, 0.0)

        # محاسبه وزنی
        combined[key] = (water_val * water_percent + wastewater_val * wastewater_percent) / 100

    return combined


def calculate_deficit_from_target(
    target_needs: Dict[str, float],
    combined_water: Dict[str, float]
) -> Dict[str, float]:
    """
    محاسبه کمبود عناصر با کسر مقادیر تامینی آب از نیازهای هدف

    Args:
        target_needs: نیازهای هدف گیاه (از دیتابیس یا سفارشی کاربر)
        combined_water: مقادیر تامینی آب و پساب

    Returns:
        دیکشنری کمبود عناصر (مقدار مثبت = نیاز به تأمین، مقدار منفی = بیش‌بود)

    Example:
        >>> target = {"N": 120, "K": 120, "Ca": 105}
        >>> water = {"n_no3": 13, "k": 9.4, "ca": 56}
        >>> deficit = calculate_deficit_from_target(target, water)
        >>> print(deficit)
        {"N": 107, "K": 110.6, "Ca": 49}
    """
    deficit: Dict[str, float] = {}

    for target_key, target_value in target_needs.items():
        # پیدا کردن کلید متناظر در combined_water
        water_key = ELEMENT_MAPPING.get(target_key, target_key.lower())
        water_value = combined_water.get(water_key, 0.0)

        # محاسبه کمبود (نیاز - مقدار تامینی)
        deficit[target_key] = round(target_value - water_value, 4)

    return deficit


def get_remaining_needs(
    target_needs: Dict[str, float],
    combined_water: Dict[str, float]
) -> Dict[str, float]:
    """
    محاسبه نیاز باقیمانده پس از کسر مقادیر تامینی آب

    این تابع مشابه calculate_deficit_from_target است اما
    مقادیر منفی را صفر می‌کند (فقط نیازهای مثبت باقی می‌مانند)

    Args:
        target_needs: نیازهای هدف گیاه
        combined_water: مقادیر تامینی آب و پساب

    Returns:
        دیکشنری نیاز باقیمانده (مقادیر منفی صفر می‌شوند)

    Example:
        >>> target = {"N": 120, "K": 120, "Ca": 105}
        >>> water = {"n_no3": 130, "k": 9.4, "ca": 56}
        >>> remaining = get_remaining_needs(target, water)
        >>> print(remaining)
        {"N": 0, "K": 110.6, "Ca": 49}
    """
    deficit = calculate_deficit_from_target(target_needs, combined_water)

    # صفر کردن مقادیر منفی
    remaining: Dict[str, float] = {}
    for key, value in deficit.items():
        remaining[key] = max(0.0, value)

    return remaining


# ============================================================
# توابع کمکی
# ============================================================

def get_water_analysis_keys() -> List[str]:
    """برگرداندن لیست کلیدهای استاندارد برای آنالیز آب و پساب"""
    return STANDARD_ELEMENTS.copy()


def get_required_keys() -> List[str]:
    """برگرداندن لیست کلیدهای ضروری که باید در آنالیز وجود داشته باشند"""
    return REQUIRED_KEYS.copy()


def get_element_mapping() -> Dict[str, str]:
    """برگرداندن مپ نام عناصر برای تبدیل بین فرمت‌های مختلف"""
    return ELEMENT_MAPPING.copy()


def validate_water_analysis(analysis: Dict[str, float]) -> Tuple[bool, List[str]]:
    """
    اعتبارسنجی آنالیز آب یا پساب

    Args:
        analysis: دیکشنری آنالیز

    Returns:
        (آیا معتبر است, لیست خطاها)

    Example:
        >>> valid, errors = validate_water_analysis({"n_no3": 10, "ec": 0.4, "ph": 7.0})
        >>> print(valid)
        True
    """
    errors: List[str] = []

    # بررسی وجود کلیدهای ضروری
    for key in REQUIRED_KEYS:
        if key not in analysis:
            errors.append(f"کلید '{key}' در آنالیز وجود ندارد")
        elif analysis.get(key, 0) < 0:
            errors.append(f"مقدار '{key}' نمی‌تواند منفی باشد (مقدار فعلی: {analysis.get(key)})")

    # بررسی مقادیر منطقی
    ec = analysis.get("ec", 0)
    if ec > 10:
        errors.append(f"EC نمی‌تواند بیشتر از 10 mS/cm باشد (مقدار فعلی: {ec})")
    elif ec < 0:
        errors.append(f"EC نمی‌تواند منفی باشد (مقدار فعلی: {ec})")

    ph = analysis.get("ph", 0)
    if ph > 14 or ph < 0:
        errors.append(f"pH باید بین 0 تا 14 باشد (مقدار فعلی: {ph})")

    # بررسی مقادیر عناصر (نمی‌توانند خیلی بزرگ باشند)
    for key in ["n_no3", "p", "k", "ca", "mg"]:
        if key in analysis:
            val = analysis.get(key, 0)
            if val > 1000:
                errors.append(f"مقدار '{key}' بسیار زیاد است ({val} ppm - حداکثر منطقی 1000 ppm)")

    return len(errors) == 0, errors


def validate_water_percentages(water_percent: float, wastewater_percent: float) -> Tuple[bool, List[str]]:
    """
    اعتبارسنجی درصدهای آب و پساب

    Args:
        water_percent: درصد آب
        wastewater_percent: درصد پساب

    Returns:
        (آیا معتبر است, لیست خطاها)
    """
    errors: List[str] = []

    if water_percent < 0 or water_percent > 100:
        errors.append(f"درصد آب باید بین 0 تا 100 باشد (مقدار فعلی: {water_percent})")

    if wastewater_percent < 0 or wastewater_percent > 100:
        errors.append(f"درصد پساب باید بین 0 تا 100 باشد (مقدار فعلی: {wastewater_percent})")

    total = water_percent + wastewater_percent
    if abs(total - 100) > 0.01:
        errors.append(f"مجموع درصد آب و پساب باید 100 باشد (مقدار فعلی: {total})")

    return len(errors) == 0, errors


# ============================================================
# توابع تولید نمونه داده
# ============================================================

def get_sample_water_analysis() -> Dict[str, float]:
    """
    برگرداندن یک نمونه آنالیز آب برای تست

    Returns:
        دیکشنری نمونه آنالیز آب
    """
    return {
        "n_no3": 10.0,
        "p": 2.0,
        "s": 5.0,
        "n_nh4": 0.0,
        "k": 8.0,
        "ca": 50.0,
        "mg": 20.0,
        "na": 5.0,
        "cl": 5.0,
        "fe": 0.5,
        "mn": 0.1,
        "zn": 0.05,
        "b": 0.2,
        "cu": 0.02,
        "mo": 0.01,
        "ec": 0.4,
        "ph": 7.0
    }


def get_sample_wastewater_analysis() -> Dict[str, float]:
    """
    برگرداندن یک نمونه آنالیز پساب برای تست

    Returns:
        دیکشنری نمونه آنالیز پساب
    """
    return {
        "n_no3": 25.0,
        "p": 5.0,
        "s": 10.0,
        "n_nh4": 2.0,
        "k": 15.0,
        "ca": 80.0,
        "mg": 30.0,
        "na": 10.0,
        "cl": 15.0,
        "fe": 1.0,
        "mn": 0.3,
        "zn": 0.1,
        "b": 0.5,
        "cu": 0.05,
        "mo": 0.02,
        "ec": 1.2,
        "ph": 6.5
    }


def get_sample_target_needs() -> Dict[str, float]:
    """
    برگرداندن نمونه نیازهای هدف گیاه (توت‌فرنگی - مرحله رشد رویشی)

    Returns:
        دیکشنری نمونه نیازهای هدف
    """
    return {
        "N": 120.0,
        "P": 50.0,
        "K": 120.0,
        "Ca": 105.0,
        "Mg": 40.0,
        "S": 30.0,
        "Fe": 3.0,
        "Mn": 0.5,
        "Zn": 0.3,
        "B": 0.5,
        "Cu": 0.1,
        "Mo": 0.05,
        "Cl": 0.0
    }


# ============================================================
# تابع محاسبه کامل (یکجا)
# ============================================================

def calculate_complete_water_contribution(
    water_percent: float,
    wastewater_percent: float,
    water_analysis: Dict[str, float],
    wastewater_analysis: Dict[str, float],
    target_needs: Dict[str, float]
) -> Dict[str, any]:
    """
    محاسبه کامل سهم آب و پساب در تغذیه گیاه

    این تابع همه مراحل را یکجا انجام می‌دهد:
    1. اعتبارسنجی ورودی‌ها
    2. محاسبه مقادیر تامینی
    3. محاسبه کمبود عناصر
    4. محاسبه نیاز باقیمانده

    Args:
        water_percent: درصد آب تامینی
        wastewater_percent: درصد پساب تامینی
        water_analysis: آنالیز آب
        wastewater_analysis: آنالیز پساب
        target_needs: نیازهای هدف گیاه

    Returns:
        دیکشنری شامل:
        - success: bool
        - errors: List[str]
        - combined_water: Dict[str, float]
        - deficit: Dict[str, float]
        - remaining_needs: Dict[str, float]

    Example:
        >>> result = calculate_complete_water_contribution(
        ...     80, 20,
        ...     get_sample_water_analysis(),
        ...     get_sample_wastewater_analysis(),
        ...     get_sample_target_needs()
        ... )
        >>> print(result["success"])
        True
    """
    # اعتبارسنجی درصدها
    valid_pct, errors_pct = validate_water_percentages(water_percent, wastewater_percent)
    if not valid_pct:
        return {
            "success": False,
            "errors": errors_pct,
            "combined_water": {},
            "deficit": {},
            "remaining_needs": {}
        }

    # اعتبارسنجی آنالیز آب
    valid_water, errors_water = validate_water_analysis(water_analysis)
    if not valid_water:
        return {
            "success": False,
            "errors": errors_water,
            "combined_water": {},
            "deficit": {},
            "remaining_needs": {}
        }

    # اعتبارسنجی آنالیز پساب
    valid_waste, errors_waste = validate_water_analysis(wastewater_analysis)
    if not valid_waste:
        return {
            "success": False,
            "errors": errors_waste,
            "combined_water": {},
            "deficit": {},
            "remaining_needs": {}
        }

    # محاسبه مقادیر تامینی
    combined_water = calculate_combined_water(
        water_percent,
        wastewater_percent,
        water_analysis,
        wastewater_analysis
    )

    # محاسبه کمبود عناصر
    deficit = calculate_deficit_from_target(target_needs, combined_water)

    # محاسبه نیاز باقیمانده (مقادیر مثبت)
    remaining_needs = get_remaining_needs(target_needs, combined_water)

    return {
        "success": True,
        "errors": [],
        "combined_water": combined_water,
        "deficit": deficit,
        "remaining_needs": remaining_needs
    }


# ============================================================
# تست سریع (در صورت اجرای مستقیم فایل)
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 تست ماژول water_analysis")
    print("=" * 60)

    # دریافت نمونه داده
    water = get_sample_water_analysis()
    wastewater = get_sample_wastewater_analysis()
    target = get_sample_target_needs()

    print("\n📊 آنالیز آب:")
    for key, val in water.items():
        print(f"  {key}: {val}")

    print("\n📊 آنالیز پساب:")
    for key, val in wastewater.items():
        print(f"  {key}: {val}")

    print("\n🌱 نیازهای هدف گیاه:")
    for key, val in target.items():
        print(f"  {key}: {val}")

    # محاسبه کامل
    result = calculate_complete_water_contribution(80, 20, water, wastewater, target)

    print("\n📈 نتایج محاسبه:")
    if result["success"]:
        print("\n✅ محاسبه با موفقیت انجام شد")

        print("\n💧 مقادیر تامینی ترکیبی:")
        for key, val in result["combined_water"].items():
            if key not in ["ec", "ph"]:
                print(f"  {key}: {val:.2f} ppm")

        print(f"\n  EC: {result['combined_water'].get('ec', 0):.2f} mS/cm")
        print(f"  pH: {result['combined_water'].get('ph', 0):.2f}")

        print("\n📉 کمبود عناصر (نیاز - تامینی):")
        for key, val in result["deficit"].items():
            status = "✅" if val <= 0 else "⚠️"
            print(f"  {status} {key}: {val:.2f} ppm")

        print("\n📋 نیاز باقیمانده (فقط مقادیر مثبت):")
        for key, val in result["remaining_needs"].items():
            if val > 0:
                print(f"  {key}: {val:.2f} ppm")
    else:
        print("\n❌ خطا در محاسبه:")
        for err in result["errors"]:
            print(f"  - {err}")

    print("\n" + "=" * 60)
    print("✅ تست کامل شد")
