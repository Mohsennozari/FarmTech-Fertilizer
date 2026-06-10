# backend/app/calculator/instructions.py

from typing import List, Dict


def generate_professional_mixing_instructions(doses: List[Dict], warnings: List[Dict], tank_volume: float) -> str:
    """تولید دستورالعمل اختلاط به زبان انگلیسی"""
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
    instructions.append("2️⃣ ترتیب ساخت: ابتدا مخزن اصلی، سپس مخزن کلسیم")
    instructions.append("3️⃣ از دو انژکتور جداگانه برای تزریق استفاده کنید")
    instructions.append("4️⃣ برنامه تغذیه: هفته اول 50%، هفته دوم 75%، هفته سوم 100%")
    instructions.append("")
    
    severe_warnings = [w for w in warnings if w.get('severity') == 'error']
    if severe_warnings:
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