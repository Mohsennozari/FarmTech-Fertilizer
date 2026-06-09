# Platform-v3\backend\app\seed.py

import json
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import (
    Crop, Variety, GrowthStage, Brand, Fertilizer,
    Interaction, Acid, Tank, CalculationHistory
)
from datetime import datetime

# ============================================================
# ضرایب تبدیل اکسید به عنصر خالص (مقادیر دقیق علمی)
# ============================================================
P2O5_TO_P = 0.4364   # 61.9475 / 141.9445
K2O_TO_K = 0.8301    # 78.1966 / 94.196
CaO_TO_Ca = 0.7147   # 40.078 / 56.0774
MgO_TO_Mg = 0.603    # 24.305 / 40.3044


def convert_p2o5_to_p(p2o5_percent: float) -> float:
    """تبدیل P2O5 به P خالص"""
    return round(p2o5_percent * P2O5_TO_P, 2)


def convert_k2o_to_k(k2o_percent: float) -> float:
    """تبدیل K2O به K خالص"""
    return round(k2o_percent * K2O_TO_K, 2)


def convert_cao_to_ca(cao_percent: float) -> float:
    """تبدیل CaO به Ca خالص"""
    return round(cao_percent * CaO_TO_Ca, 2)


def convert_mgo_to_mg(mgo_percent: float) -> float:
    """تبدیل MgO به Mg خالص"""
    return round(mgo_percent * MgO_TO_Mg, 2)


def seed_database():
    db = SessionLocal()

    try:
        print("=" * 70)
        print("🚀 FarmTech Database Seeding Started")
        print("=" * 70)

        # ============================================================
        # پاک کردن داده‌های قبلی
        # ============================================================
        print("\n🗑️  Clearing existing data...")
        db.query(CalculationHistory).delete()
        db.query(Tank).delete()
        db.query(Interaction).delete()
        db.query(GrowthStage).delete()
        db.query(Fertilizer).delete()
        db.query(Variety).delete()
        db.query(Brand).delete()
        db.query(Crop).delete()
        db.query(Acid).delete()
        db.commit()
        print("✅ Previous data cleared")

        # ============================================================
        # محصولات (Crops)
        # ============================================================
        print("\n🌾 Creating crops...")
        
        strawberry = Crop(
            name="توت‌فرنگی",
            scientific_name="Fragaria × ananassa",
            cultivation_type="هیدروپونیک"
        )
        db.add(strawberry)
        db.flush()
        print(f"   ✅ Crop: {strawberry.name} - {strawberry.scientific_name}")

        # ============================================================
        # ارقام (Varieties)
        # ============================================================
        print("\n🍓 Creating varieties...")
        
        san_andreas = Variety(
            crop_id=strawberry.id,
            name="سن اندرسا",
            description="رقم پرمحصول مناسب برای کشت هیدروپونیک - میوه درشت و شیرین",
            growth_days=90,
            yield_potential="بسیار بالا - تا 2 کیلوگرم در هر بوته"
        )
        db.add(san_andreas)

        camarosa = Variety(
            crop_id=strawberry.id,
            name="کاماروسا",
            description="رقم زودرس با میوه‌های درشت - مقاوم به سرما",
            growth_days=80,
            yield_potential="بسیار بالا - مناسب برای صادرات"
        )
        db.add(camarosa)
        db.flush()
        print(f"   ✅ Variety: {san_andreas.name}")
        print(f"   ✅ Variety: {camarosa.name}")

        # ============================================================
        # برندها (Brands) - بر اساس اطلاعات شرکت رازاک شیمی و گل سم گرگان
        # ============================================================
        print("\n🏭 Creating brands...")
        
        # شرکت گل سم گرگان
        gol_sam = Brand(
            name="گل سم گرگان",
            country="ایران",
            website="www.golsam.com",
            notes="تولید کننده کودهای کشاورزی با کیفیت بالا - محصولات فرتی‌گل و یونی کمپلکس"
        )
        db.add(gol_sam)

        # شرکت رازاک شیمی
        razak = Brand(
            name="رازاک شیمی",
            country="ایران",
            website="www.razakshimi.com",
            notes="تولید کننده کودهای NPK، سولفات‌ها و محرک‌های رشد - برندهای گرین استار و زاگرا استار"
        )
        db.add(razak)

        # برند گرین استار (زیرمجموعه رازاک شیمی)
        green_star = Brand(
            name="گرین استار",
            country="ایران",
            website="www.greenstar.ir",
            notes="تولید کننده کودهای کامل NPK با کیفیت بالا - دارای کد ثبت مواد کودی معتبر"
        )
        db.add(green_star)

        # برند زاگرا استار (زیرمجموعه رازاک شیمی)
        zagara_star = Brand(
            name="زاگرا استار",
            country="ایران",
            website="www.zagrastar.ir",
            notes="تولید کننده کودهای کامل NPK، هیومیک اسید و مواد آلی"
        )
        db.add(zagara_star)
        
        db.flush()
        print(f"   ✅ Brand: {gol_sam.name}")
        print(f"   ✅ Brand: {razak.name}")
        print(f"   ✅ Brand: {green_star.name}")
        print(f"   ✅ Brand: {zagara_star.name}")

        # ============================================================
        # کودها (Fertilizers) - اطلاعات کامل از فایل‌های متنی
        # ============================================================
        print("\n🧪 Creating fertilizers...")

        fertilizers_data = [
            # ========================================================
            # محصولات شرکت گل سم گرگان
            # ========================================================
            {
                "name": "یونی کمپلکس پودری",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_type": "ریزمغذی",
                "chemical_formula": "Complete Micro",
                "registration_code": "36704",
                "description": """کود کامل ریزمغذی چندعنصری، کاملاً محلول در آب.
                
مزایا:
- تأمین همزمان عناصر ریزمغذی ضروری گیاه
- پیشگیری و درمان کمبود عناصر کم‌مصرف
- افزایش رشد رویشی و بهبود سبزینگی گیاه
- بهبود جذب عناصر غذایی و افزایش عملکرد محصول
- مناسب برای کشت‌های زراعی، باغی و گلخانه‌ای
- قابل استفاده به صورت محلول‌پاشی و آب آبیاری
- فاقد کلر و ناخالصی‌های مضر

ترکیبات:
آهن محلول (Fe): 5%
روی محلول (Zn): 5%
منگنز محلول (Mn): 4%
مس محلول (Cu): 4%
بر محلول (B): 1.5%
مولیبدن محلول (Mo): 0.07%
منیزیم محلول (MgO): 1.2%
گوگرد محلول (S): 25%""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "fe_percent": 5.0,
                "zn_percent": 5.0,
                "mn_percent": 4.0,
                "cu_percent": 4.0,
                "b_percent": 1.5,
                "mo_percent": 0.07,
                "mg_percent": convert_mgo_to_mg(1.2),
                "s_percent": 25.0,
                "solubility_g_per_l": 500,
                "ph_effect": "خنثی",
                "is_active": True
            },
            {
                "name": "فرتی‌گل 36-12-12",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 12-12-36",
                "registration_code": "08457",
                "description": """کود کامل کاملاً محلول در آب، غنی از پتاسیم، حاوی ریزمغذی‌های کلاته EDTA.

مزایا:
- قابل استفاده به صورت محلول‌پاشی و کود آبیاری
- تأمین پتاسیم بالا به همراه درصد مؤثری از نیتروژن و فسفر
- افزایش سایز میوه و افزایش عملکرد محصول
- بهبود کیفیت و بازارپسندی محصولات
- مناسب برای کلیه کشت‌های زراعی، باغی و گلخانه‌ای
- حاوی عناصر ریزمغذی به فرم کلات EDTA با قابلیت جذب بالا
- فاقد کلر و ناخالصی‌های مضر
- فرمولاسیون با pH مناسب برای خاک‌های قلیایی

ترکیبات:
نیتروژن (N): 12%
فسفر (P2O5): 12%
پتاسیم (K2O): 36%
آهن کلاته (EDTA): 0.016%
روی کلاته (EDTA): 0.037%
منگنز کلاته (EDTA): 0.006%
مس کلاته (EDTA): 0.0015%
منیزیم محلول (MgO): 1%""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 12.0,
                "p_percent": convert_p2o5_to_p(12.0),
                "k_percent": convert_k2o_to_k(36.0),
                "mg_percent": convert_mgo_to_mg(1.0),
                "fe_percent": 0.016,
                "zn_percent": 0.037,
                "mn_percent": 0.006,
                "cu_percent": 0.0015,
                "solubility_g_per_l": 400,
                "ph_effect": "اسیدی ملایم",
                "is_active": True
            },
            {
                "name": "فرتی‌گل 10-50-10",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 10-50-10",
                "registration_code": "78644",
                "description": """کود کاملاً محلول در آب با فسفر بالا.

مزایا:
- تأمین فسفر بالا برای تحریک ریشه‌زایی قوی
- افزایش استقرار گیاه در مراحل اولیه رشد
- بهبود گلدهی و تشکیل جوانه‌های زایشی
- افزایش جذب عناصر غذایی و بهبود رشد عمومی گیاه
- فاقد کلر و ناخالصی‌های مضر
- حلالیت کامل و جذب سریع
- مناسب برای خاک‌های سرد، فقیر و کم‌فسفر

ترکیبات:
نیتروژن (N): 10%
فسفر (P2O5): 50%
پتاسیم (K2O): 10%""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 10.0,
                "p_percent": convert_p2o5_to_p(50.0),
                "k_percent": convert_k2o_to_k(10.0),
                "solubility_g_per_l": 350,
                "ph_effect": "اسیدی",
                "is_active": True
            },
            {
                "name": "فرتی‌گل 30-5-15",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 15-5-30",
                "registration_code": "87260",
                "description": """کود کاملاً محلول در آب با پتاسیم بالا.

مزایا:
- تأمین پتاسیم بالا برای افزایش کیفیت، رنگ و وزن میوه
- تقویت مقاومت گیاه در برابر تنش‌های محیطی و بیماری‌ها
- کمک به بهبود انتقال و تجمع قندها در میوه
- افزایش استحکام بافت میوه و بهبود قابلیت انبارمانی
- فاقد کلر و ناخالصی‌های مضر
- حلالیت کامل و جذب سریع
- مناسب خاک‌های اسیدی تا قلیایی

ترکیبات:
نیتروژن (N): 15%
فسفر (P2O5): 5%
پتاسیم (K2O): 30%
منیزیم (MgO): 1%""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 15.0,
                "p_percent": convert_p2o5_to_p(5.0),
                "k_percent": convert_k2o_to_k(30.0),
                "mg_percent": convert_mgo_to_mg(1.0),
                "solubility_g_per_l": 400,
                "ph_effect": "اسیدی ملایم",
                "is_active": True
            },
            {
                "name": "فرتی‌گل 20-20-20",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 20-20-20",
                "registration_code": "68164",
                "description": """کود کامل میکروکریستال، کاملاً محلول در آب، حاوی ریزمغذی‌های کلاته EDTA.

مزایا:
- فرمولاسیون میکروکریستال با خلوص بسیار بالا، انحلال‌پذیری 100 درصد و جذب سریع توسط گیاه
- فاقد عناصر مضر مانند کلر و سدیم
- تقویت رشد رویشی و توسعه ریشه و برگ‌ها
- کمک به افزایش کمی و کیفی محصول، افزایش گلدهی و بهبود سایز و رنگ میوه
- وجود پتاسیم برای افزایش مقاومت گیاه در برابر آفات، بیماری‌ها و تنش‌های محیطی
- مناسب برای طیف گسترده‌ای از خاک‌های کشور (اسیدی تا قلیایی)
- قابل استفاده در گیاهان زراعی، باغی، گلخانه‌ای، زینتی و آپارتمانی
- حاوی عناصر میکرو کلاته EDTA با جذب بسیار سریع

ترکیبات:
نیتروژن (N): 20%
فسفر (P2O5): 20%
پتاسیم (K2O): 20%
منیزیم (MgO): 1%""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 20.0,
                "p_percent": convert_p2o5_to_p(20.0),
                "k_percent": convert_k2o_to_k(20.0),
                "mg_percent": convert_mgo_to_mg(1.0),
                "solubility_g_per_l": 400,
                "ph_effect": "خنثی",
                "is_active": True
            },
            # ========================================================
            # محصولات شرکت رازاک شیمی (سولفات‌ها و تک عنصری‌ها)
            # ========================================================
            {
                "name": "سولفات پتاسیم",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "K2SO4",
                "registration_code": "825289",
                "description": """کود پتاس بالا با 51% پتاسیم و گوگرد قابل جذب.

ویژگی‌ها:
- ترکیب سولوپتاس با داشتن 51% پتاس و وجود گوگرد به شکل سولفات به راحتی برای گیاه قابل جذب می باشد
- این کود در انواع کشت (خاکی، هیدروپونیک) و در انواع روش‌های آبیاری به کار می‌رود
- این ترکیب بالاترین کیفیت را در بین کودهای پتاسه دارا بوده
- مصرف صحیح آن باعث افزایش عملکرد کمی و کیفی محصولات کشاورزی می‌گردد
- تقریباً فاقد کلراید است و کمترین میزان نمک را در بین کودهای پتاسه دارد

دستور مصرف:
درختان میوه: 15-18 کیلوگرم در هکتار
سبزیجات: 10-12 کیلوگرم در هکتار
غلات: 12-15 کیلوگرم در هکتار
گیاهان صنعتی: 4-5 کیلوگرم در هکتار""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 2.0,
                "min_dose_g_per_liter": 0.2,
                "k_percent": 51.0,
                "s_percent": 18.0,
                "solubility_g_per_l": 120,
                "ph_effect": "خنثی",
                "is_active": True
            },
            {
                "name": "سولفات روی",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "ZnSO4",
                "registration_code": "79394",
                "description": """منبع غنی روی با 22% روی.

مهمترین نقش عنصر روی در گیاهان:
- تولید هورمون‌های گیاهی از جمله اکسین
- باعث تأخیر در پیری برگ‌ها می‌شود
- تولید کلروفیل را افزایش می‌دهد
- مقاومت گیاهان را نسبت به آفات و تنش‌های محیطی افزایش می‌دهد
- موجب استحکام ساختار و ظهور ریشه مؤثر در گیاه می‌شود

دستور مصرف:
درختان میوه: 3-5 کیلوگرم در 1000 لیتر آب (محلول‌پاشی)
مرکبات: 5 کیلوگرم در 1000 لیتر آب
پسته: 6 کیلوگرم در 1000 لیتر آب
غلات: 1.5 کیلوگرم در 1000 لیتر آب""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 1.0,
                "min_dose_g_per_liter": 0.1,
                "zn_percent": 22.0,
                "s_percent": 11.0,
                "solubility_g_per_l": 500,
                "ph_effect": "خنثی",
                "is_active": True
            },
            {
                "name": "سولفات منگنز",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "MnSO4",
                "registration_code": "47588",
                "description": """منبع غنی منگنز با 24% منگنز.

ویژگی‌ها:
- کاملاً پودری و محلول در آب
- مقدار عناصر سنگین سرب و کادمیم در حد استاندارد حذف و تصفیه شده است
- قابلیت استفاده به صورت خاکی، کود آبیاری و محلول پاشی

نقش منگنز در گیاه:
- در ساخت کلروفیل نقش اساسی دارد
- تولید آنزیم‌های رشد
- جذب و جابجایی فسفر

دستور مصرف:
باغات: 3-5 در هزار (محلول‌پاشی) - 200-300 گرم برای هر درخت (خاکی)
مزارع: 1-5 در هزار (محلول‌پاشی) - 5-10 کیلوگرم در هکتار (خاکی)""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 1.0,
                "min_dose_g_per_liter": 0.1,
                "mn_percent": 24.0,
                "s_percent": 14.0,
                "solubility_g_per_l": 500,
                "ph_effect": "خنثی",
                "is_active": True
            },
            {
                "name": "سولفات مس",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "CuSO4",
                "registration_code": "01318",
                "description": """منبع غنی مس با 25% مس.

کاربردها:
- به طور متداول به عنوان ضد قارچ در کشاورزی مورد استفاده قرار می‌گیرد
- در تشکیل کلروفیل و پدیده فتوسنتز دخالت دارد

دستور مصرف:
محصولات زراعی: 2 کیلوگرم در 1000 لیتر آب (محلول‌پاشی) - 10-20 کیلوگرم در هکتار (خاکی)
درختان میوه: 2-3 کیلوگرم در 1000 لیتر آب - 50-150 گرم برای هر درخت""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 1.0,
                "min_dose_g_per_liter": 0.05,
                "cu_percent": 25.0,
                "s_percent": 13.0,
                "solubility_g_per_l": 300,
                "ph_effect": "اسیدی",
                "is_active": True
            },
            {
                "name": "سولفات منیزیم",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "MgSO4",
                "registration_code": "97866",
                "description": """منبع غنی منیزیم با 9.8% منیزیم.

نقش منیزیم در گیاه:
- در ساخت کلروفیل نقش اساسی دارد
- تولید آنزیم‌های رشد
- جذب و جابجایی فسفر
- با افزایش طول عمر بخش‌های سبز گیاه، فتوسنتز را تقویت می‌کند
- باعث پرشدن کامل دانه‌ها و افزایش کمیت و کیفیت روغن در دانه‌های روغنی می‌شود

دستور مصرف:
محصولات زراعی: 5-10 کیلوگرم در 1000 لیتر آب - 30-50 کیلوگرم در هکتار
درختان میوه: 5-10 کیلوگرم در 1000 لیتر آب - 0.5-1 کیلوگرم برای هر درخت""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 2.0,
                "min_dose_g_per_liter": 0.2,
                "mg_percent": 9.8,
                "s_percent": 13.0,
                "solubility_g_per_l": 350,
                "ph_effect": "خنثی",
                "is_active": True
            },
            {
                "name": "سولفات آهن",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "FeSO4",
                "registration_code": "46489",
                "description": """منبع غنی آهن با 19% آهن.

ویژگی‌ها:
- به صورت کریستالی و کاملاً محلول در آب است
- کاربرد آن باعث کاهش pH خاک می‌شود
- برای مصرف در خاک‌های قلیایی مناسب می باشد

دستور مصرف:
باغات: 3-5 در هزار (محلول‌پاشی در بهار) - 50-250 گرم برای هر درخت (چالکود)
تاکستان‌ها: 200-400 گرم برای هر درخت (چالکود)
باغات جوان: 250-1000 گرم برای هر درخت
باغات بارور: 2-5 در هزار (محلول‌پاشی)""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 1.0,
                "min_dose_g_per_liter": 0.1,
                "fe_percent": 19.0,
                "s_percent": 11.0,
                "solubility_g_per_l": 400,
                "ph_effect": "اسیدی",
                "is_active": True
            },
            {
                "name": "نیترات کلسیم",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "Ca(NO3)2",
                "registration_code": "17704",
                "description": """کود نیترات کلسیم با داشتن درصد مناسبی از نیتروژن به فرم نیترات و کلسیم.

ویژگی‌ها:
- قابلیت جذب بالا و مستقیم کود
- افزایش عملکرد و کیفیت محصول و افزایش اندازه میوه‌ها
- استحکام دیواره سلولی و در پی آن استحکام شاخه، برگ و میوه گیاهان
- افزایش عمر انبارش محصولات باغی و سبزیجات
- کاهش از دست رفتن آب میوه‌ها و سبزیجات پس از برداشت
- افزایش مقاومت گیاه در برابر آفات و بیماریها و تنش‌های محیطی
- رشد و توسعه بیشتر ریشه
- افزایش جذب عناصر غذایی پتاسیم و منیزیم

دستور مصرف:
محصولات زراعی: 1-2 کیلوگرم در 1000 لیتر آب - 10-20 کیلوگرم در هکتار
درختان میوه: 2-4 کیلوگرم در 1000 لیتر آب - 20-30 کیلوگرم در هکتار""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 2.5,
                "min_dose_g_per_liter": 0.2,
                "n_percent": 15.5,
                "ca_percent": 19.0,
                "solubility_g_per_l": 1200,
                "ph_effect": "بازی ملایم",
                "is_active": True
            },
            {
                "name": "کلرید پتاسیم",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "KCl",
                "registration_code": "GR-789",
                "description": """منبع اقتصادی پتاسیم با 52% پتاسیم.

نکات مهم:
- حاوی کلر است (47%)
- برای گیاهان حساس به کلر با احتیاط مصرف شود
- مناسب برای خاک‌هایی که مشکل شوری ندارند

دستور مصرف:
محصولات مقاوم به کلر: 0.5-1 کیلوگرم در 1000 لیتر آب
برای توت‌فرنگی با احتیاط و در غلظت‌های پایین استفاده شود""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 1.0,
                "min_dose_g_per_liter": 0.1,
                "k_percent": 52.0,
                "cl_percent": 47.0,
                "solubility_g_per_l": 340,
                "ph_effect": "خنثی",
                "is_active": True
            },
            # ========================================================
            # محصولات شرکت گرین استار (NPKها)
            # ========================================================
            {
                "name": "NPK 20-20-20 گرین استار",
                "brand_id": green_star.id,
                "brand_name": green_star.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 20-20-20",
                "registration_code": "02705",
                "description": """کود کامل NPK با نسبت مساوی - جامد پودری به رنگ صورتی.

توضیحات محصول:
این کود شامل عناصر نیتروژن، فسفر و پتاسیم به نسبت مساوی 20 درصد است. این محصول علاوه بر رفع نیازهای گیاهان و بهبود تمامی مکانیسم‌های گیاهی، نقش مؤثری در برقراری موازنه عناصر در خاک و گیاه دارد که قابلیت جذب اکثر عناصر غذایی و ریزمغذی‌ها را از طریق ریشه و برگ برای گیاه فراهم می‌سازد.

دستور مصرف:
سبزیجات و گلخانه: 3-4 کیلوگرم در هکتار (آبیاری تحت فشار) - 4 کیلوگرم در 1000 لیتر آب (محلول‌پاشی)
غلات: 5 کیلوگرم در هکتار - 4 کیلوگرم در 1000 لیتر آب
درختان میوه: 8 کیلوگرم در هکتار - 4 کیلوگرم در 1000 لیتر آب""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 20.0,
                "p_percent": convert_p2o5_to_p(20.0),
                "k_percent": convert_k2o_to_k(20.0),
                "solubility_g_per_l": 400,
                "ph_effect": "خنثی",
                "is_active": True
            },
            {
                "name": "NPK 12-12-36 گرین استار",
                "brand_id": green_star.id,
                "brand_name": green_star.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 12-12-36",
                "registration_code": "77282",
                "description": """کود NPK با پتاسیم بالا - جامد پودری به رنگ فیروزه‌ای.

توضیحات محصول:
این کود علاوه بر مقادیر متناسب نیتروژن و فسفر، دارای میزان بالای پتاسیم (36%) می‌باشد. این محصول بطور اختصاصی در مراحل گلدهی و قبل از برداشت محصول و رسیدن میوه باعث افزایش متابولیسم و افزایش حرکت روزنه‌ها شده و تأثیر بسزایی در افزایش باردهی، درشت نمودن و رنگ‌آوری محصولات زراعی، باغی و گلخانه‌ای می‌گذارد.

دستور مصرف:
سبزیجات و گلخانه: 3-4 کیلوگرم در هکتار - 4 کیلوگرم در 1000 لیتر آب
غلات: 5 کیلوگرم در هکتار - 4 کیلوگرم در 1000 لیتر آب
درختان میوه: 8 کیلوگرم در هکتار - 4 کیلوگرم در 1000 لیتر آب""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 12.0,
                "p_percent": convert_p2o5_to_p(12.0),
                "k_percent": convert_k2o_to_k(36.0),
                "solubility_g_per_l": 400,
                "ph_effect": "خنثی",
                "is_active": True
            },
            # ========================================================
            # محصولات شرکت زاگرا استار (NPKها و محرک‌ها)
            # ========================================================
            {
                "name": "NPK 10-52-10 زاگرا استار",
                "brand_id": zagara_star.id,
                "brand_name": zagara_star.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 10-52-10",
                "registration_code": "32990",
                "description": """کود NPK با فسفر بالا - جامد پودری به رنگ فیروزه‌ای.

توضیحات محصول:
این کود حاوی عناصر ماکرویی مثل نیتروژن، پتاسیم و 52% فسفر بوده و دارای انواع میکروالمنت‌ها مانند آهن، روی، منگنز، بور و مس می‌باشد. استفاده از آن برای خاک‌هایی که در آنها فقدان فسفر (در نتیجه تجزیه خاک) مشهود است بسیار توصیه می‌شود. فسفر اصولاً جهت پایداری و استحکام نشاء و افزایش طول ریشه آن مورد استفاده قرار می‌گیرد.

دستور مصرف:
سبزیجات و گلخانه: 3-4 کیلوگرم در هکتار - 4 کیلوگرم در 1000 لیتر آب
غلات: 5 کیلوگرم در هکتار - 4 کیلوگرم در 1000 لیتر آب
درختان میوه: 8 کیلوگرم در هکتار - 4 کیلوگرم در 1000 لیتر آب""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 10.0,
                "p_percent": convert_p2o5_to_p(52.0),
                "k_percent": convert_k2o_to_k(10.0),
                "solubility_g_per_l": 350,
                "ph_effect": "اسیدی قوی",
                "is_active": True
            },
            {
                "name": "NPK 12-12-36 زاگرا استار",
                "brand_id": zagara_star.id,
                "brand_name": zagara_star.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 12-12-36",
                "registration_code": "77282",
                "description": """کود NPK با پتاسیم بالا - جامد پودری به رنگ فیروزه‌ای.

توضیحات محصول:
این کود که علاوه بر مقادیر متناسب نیتروژن و فسفر، دارای میزان بالای پتاسیم (36%) می‌باشد. این محصول بطور اختصاصی در مراحل گلدهی و قبل از برداشت محصول و رسیدن میوه باعث افزایش متابولیسم و افزایش حرکت روزنه‌ها شده و تأثیر بسزایی در افزایش باردهی، درشت نمودن و رنگ‌آوری محصولات می‌گذارد.

دستور مصرف:
سبزیجات و گلخانه: 3-4 کیلوگرم در هکتار - 4 کیلوگرم در 1000 لیتر آب
غلات: 5 کیلوگرم در هکتار - 4 کیلوگرم در 1000 لیتر آب
درختان میوه: 8 کیلوگرم در هکتار - 4 کیلوگرم در 1000 لیتر آب""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 12.0,
                "p_percent": convert_p2o5_to_p(12.0),
                "k_percent": convert_k2o_to_k(36.0),
                "solubility_g_per_l": 400,
                "ph_effect": "خنثی",
                "is_active": True
            },
            {
                "name": "NPK 15-5-30 زاگرا استار",
                "brand_id": zagara_star.id,
                "brand_name": zagara_star.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 15-5-30",
                "registration_code": "45974",
                "description": """کود NPK با پتاسیم بالا - جامد پودری به رنگ فیروزه‌ای.

توضیحات محصول:
کود کاملی است که علاوه بر نیتروژن و فسفر، دارای میزان بالای پتاسیم (30%) می باشد. این محصول بطور اختصاصی در مراحل گلدهی و قبل از برداشت محصول و رسیدن میوه باعث افزایش متابولیسم و افزایش حرکت روزنه ها شده و تأثیر بسزایی در افزایش باردهی، درشت نمودن و رنگ‌آوری محصولات می گذارد.

دستور مصرف:
درختان میوه: 3-4 کیلوگرم در هکتار (قبل از به شکوفه رفتن)
سبزیجات: 3-4 کیلوگرم در هکتار (اوج رشد رویشی)
غلات: 3-4 کیلوگرم در هکتار (بعد از پرشدن خوشه‌ها)
انگور: 3-4 کیلوگرم در هکتار (بعد از تبدیل شدن به انگور)""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 15.0,
                "p_percent": convert_p2o5_to_p(5.0),
                "k_percent": convert_k2o_to_k(30.0),
                "solubility_g_per_l": 400,
                "ph_effect": "خنثی",
                "is_active": True
            },
            {
                "name": "NPK 30-10-10 زاگرا استار",
                "brand_id": zagara_star.id,
                "brand_name": zagara_star.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 30-10-10",
                "registration_code": "05077",
                "description": """کود NPK با نیتروژن بالا.

توضیحات محصول:
این کود دارای 30% نیتروژن بوده که در تشکیل پروتوپلاسم، نوکلئیک اسید، پروتئین و اسید آمینه در گیاه نقش اساسی دارد. همچنین میزان کلروفیل در برگ را افزایش می‌دهد و در گیاهان علوفه‌ای باعث رشد، ترد و آبدار شدن گیاه می‌شود.

دستور مصرف:
درختان میوه: 1-3 کیلوگرم در هکتار (همزمان با رشد رویشی)
سبزیجات: 1-3 کیلوگرم در هکتار (مرحله رشد رویشی)
غلات: 1-3 کیلوگرم در هکتار (مرحله پنجه زنی)
گیاهان علوفه‌ای: 2-4 کیلوگرم در هکتار (در حین رشد به دفعات)""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 30.0,
                "p_percent": convert_p2o5_to_p(10.0),
                "k_percent": convert_k2o_to_k(10.0),
                "solubility_g_per_l": 400,
                "ph_effect": "خنثی",
                "is_active": True
            },
            {
                "name": "NPK 20-20-20 زاگرا استار",
                "brand_id": zagara_star.id,
                "brand_name": zagara_star.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 20-20-20",
                "registration_code": "02705",
                "description": """کود کامل NPK با نسبت مساوی - جامد پودری به رنگ صورتی.

توضیحات محصول:
این کود شامل عناصر نیتروژن، فسفر و پتاسیم به نسبت مساوی 20 درصد است. این محصول علاوه بر رفع نیازهای گیاهان و بهبود تمامی مکانیسم‌های گیاهی، نقش مؤثری در برقراری موازنه عناصر در خاک و گیاه دارد.

دستور مصرف:
سبزیجات و گلخانه: 3-4 کیلوگرم در هکتار - 4 کیلوگرم در 1000 لیتر آب
غلات: 5 کیلوگرم در هکتار - 4 کیلوگرم در 1000 لیتر آب
درختان میوه: 8 کیلوگرم در هکتار - 4 کیلوگرم در 1000 لیتر آب""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 20.0,
                "p_percent": convert_p2o5_to_p(20.0),
                "k_percent": convert_k2o_to_k(20.0),
                "solubility_g_per_l": 400,
                "ph_effect": "خنثی",
                "is_active": True
            },
            {
                "name": "هیومیک اسید 95%",
                "brand_id": zagara_star.id,
                "brand_name": zagara_star.name,
                "fertilizer_type": "محرک رشد",
                "chemical_formula": "Humic Acid",
                "registration_code": "973329",
                "description": """هیومیک اسید 95% پودری - بهترین کلات کننده طبیعی.

ویژگی‌ها:
- بهبود ساختار خاک و کمک به حفظ توازن آن و نیز کمک به ریشه‌زایی و نگهداری بیشتر آب در خاک
- کمک به انحلال و آزادسازی عناصر ماکرو و میکرو و در نتیجه کاهش نیاز به مصرف کودهای شیمیایی
- کمک به رشد سریع باکتری‌های مفید در خاک و نیز افزایش مقاومت گیاه در برابر شوری، کم آبی و سرما
- افزایش سرعت جوانه زنی بذر و کمک به بهبود کیفیت محصول
- کاهش خاصیت سمی کودها و همچنین کاهش عناصر اضافی موجود در خاک
- کمک به اصلاح خاک‌های قلیایی بدلیل pH اسیدی این محصول
- افزایش مقاومت گیاه در برابر انواع بیماری‌ها و کاهش نیاز به مصرف سموم
- سازگاری با طبیعت و نداشتن خطر برای گیاه و محیط زیست

دستور مصرف:
درختان میوه: 3-4 کیلوگرم در هکتار (3 بار در فصل)
غلات: 4 کیلوگرم در هکتار (3 بار در فصل)
گلخانه: 200-400 گرم در 1000 متر مربع (هر دو هفته یکبار)""",
                "purity_percent": 95,
                "max_dose_g_per_liter": 1.0,
                "min_dose_g_per_liter": 0.1,
                "solubility_g_per_l": 100,
                "ph_effect": "اسیدی",
                "is_active": True
            },
            {
                "name": "کلات آهن EDDHA",
                "brand_id": zagara_star.id,
                "brand_name": zagara_star.name,
                "fertilizer_type": "ریزمغذی",
                "chemical_formula": "Fe-EDDHA",
                "registration_code": "MIC-001",
                "description": """کلات آهن با پایداری بالا در pH های قلیایی.

ویژگی‌ها:
- پایداری بالا تا pH 9
- برای رفع زردی برگ ناشی از کمبود آهن در خاک‌های آهکی
- جذب سریع توسط گیاه
- قابل استفاده به صورت محلول‌پاشی و کود آبیاری

دستور مصرف:
محلول‌پاشی: 0.5-1 کیلوگرم در 1000 لیتر آب
آبیاری: 1-2 کیلوگرم در هکتار""",
                "purity_percent": 100,
                "max_dose_g_per_liter": 1.0,
                "min_dose_g_per_liter": 0.05,
                "fe_percent": 6.0,
                "solubility_g_per_l": 500,
                "ph_effect": "خنثی",
                "is_active": True
            }
        ]

        fertilizers = []
        for fert_data in fertilizers_data:
            fert = Fertilizer(**fert_data)
            db.add(fert)
            fertilizers.append(fert)

        db.flush()
        print(f"   ✅ {len(fertilizers)} fertilizers created")

        # ============================================================
        # نیازهای تغذیه‌ای برای مراحل رشد توت‌فرنگی
        # ============================================================
        print("\n📈 Creating growth stages...")

        # نیازهای تغذیه‌ای برای رقم سن اندرسا (بر اساس منابع علمی)
        san_andreas_needs = {
            "استقرار نشاء": {
                "N": 50, "P": 30, "K": 55, "Ca": 50, "Mg": 20, "S": 15,
                "Fe": 2, "Zn": 0.5, "Mn": 0.5, "Cu": 0.1, "B": 0.2, "Mo": 0.05, "Cl": 0
            },
            "ریشه‌زایی": {
                "N": 70, "P": 40, "K": 75, "Ca": 65, "Mg": 25, "S": 18,
                "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0
            },
            "رشد رویشی": {
                "N": 120, "P": 50, "K": 120, "Ca": 105, "Mg": 40, "S": 25,
                "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.4, "Mo": 0.05, "Cl": 0
            },
            "گلدهی": {
                "N": 100, "P": 60, "K": 130, "Ca": 105, "Mg": 35, "S": 22,
                "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.5, "Mo": 0.05, "Cl": 0
            },
            "میوه‌دهی": {
                "N": 80, "P": 40, "K": 140, "Ca": 115, "Mg": 30, "S": 20,
                "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0
            }
        }

        # نیازهای تغذیه‌ای برای رقم کاماروسا
        camarosa_needs = {
            "استقرار نشاء": {
                "N": 55, "P": 28, "K": 55, "Ca": 50, "Mg": 19, "S": 14,
                "Fe": 2, "Zn": 0.5, "Mn": 0.5, "Cu": 0.1, "B": 0.2, "Mo": 0.05, "Cl": 0
            },
            "ریشه‌زایی": {
                "N": 75, "P": 38, "K": 70, "Ca": 60, "Mg": 24, "S": 17,
                "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0
            },
            "رشد رویشی": {
                "N": 110, "P": 48, "K": 115, "Ca": 100, "Mg": 39, "S": 24,
                "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.4, "Mo": 0.05, "Cl": 0
            },
            "گلدهی": {
                "N": 95, "P": 58, "K": 125, "Ca": 100, "Mg": 34, "S": 21,
                "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.5, "Mo": 0.05, "Cl": 0
            },
            "میوه‌دهی": {
                "N": 75, "P": 38, "K": 135, "Ca": 105, "Mg": 29, "S": 19,
                "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0
            }
        }

        stage_names = ["استقرار نشاء", "ریشه‌زایی", "رشد رویشی", "گلدهی", "میوه‌دهی"]
        stage_orders = [0, 1, 2, 3, 4]

        # مقادیر هدف EC و pH برای هر مرحله
        ec_ph_targets = {
            "استقرار نشاء": (0.8, 1.2, 5.5, 6.0),
            "ریشه‌زایی": (1.0, 1.4, 5.6, 6.1),
            "رشد رویشی": (1.2, 1.6, 5.8, 6.2),
            "گلدهی": (1.4, 1.8, 5.8, 6.2),
            "میوه‌دهی": (1.6, 2.0, 5.8, 6.2)
        }

        priorities = {
            "استقرار نشاء": "high",
            "ریشه‌زایی": "high",
            "رشد رویشی": "medium",
            "گلدهی": "high",
            "میوه‌دهی": "critical"
        }

        stages = []

        # مراحل رشد برای سن اندرسا
        for i, name in enumerate(stage_names):
            ec_min, ec_max, ph_min, ph_max = ec_ph_targets[name]
            stage = GrowthStage(
                crop_id=strawberry.id,
                variety_id=san_andreas.id,
                name=name,
                stage_order=stage_orders[i],
                description=f"مرحله {name} برای رقم سن اندرسا - توت‌فرنگی هیدروپونیک",
                nutrient_needs=san_andreas_needs[name],
                target_ec_min=ec_min,
                target_ec_max=ec_max,
                target_ph_min=ph_min,
                target_ph_max=ph_max,
                priority=priorities[name]
            )
            db.add(stage)
            stages.append(stage)

        # مراحل رشد برای کاماروسا
        for i, name in enumerate(stage_names):
            ec_min, ec_max, ph_min, ph_max = ec_ph_targets[name]
            stage = GrowthStage(
                crop_id=strawberry.id,
                variety_id=camarosa.id,
                name=name,
                stage_order=stage_orders[i],
                description=f"مرحله {name} برای رقم کاماروسا - توت‌فرنگی هیدروپونیک",
                nutrient_needs=camarosa_needs[name],
                target_ec_min=ec_min,
                target_ec_max=ec_max,
                target_ph_min=ph_min,
                target_ph_max=ph_max,
                priority=priorities[name]
            )
            db.add(stage)
            stages.append(stage)

        # مراحل رشد عمومی (بدون رقم خاص)
        for i, name in enumerate(stage_names):
            ec_min, ec_max, ph_min, ph_max = ec_ph_targets[name]
            stage = GrowthStage(
                crop_id=strawberry.id,
                variety_id=None,
                name=name,
                stage_order=stage_orders[i],
                description=f"مرحله عمومی {name} برای توت‌فرنگی - قابل استفاده برای همه ارقام",
                nutrient_needs=san_andreas_needs[name],
                target_ec_min=ec_min,
                target_ec_max=ec_max,
                target_ph_min=ph_min,
                target_ph_max=ph_max,
                priority=priorities[name]
            )
            db.add(stage)
            stages.append(stage)

        db.flush()
        print(f"   ✅ {len(stages)} growth stages created")

        # ============================================================
        # تداخلات شیمیایی (Interactions)
        # ============================================================
        print("\n⚠️ Creating interactions...")

        calcium_nitrate = db.query(Fertilizer).filter(Fertilizer.name == "نیترات کلسیم").first()
        high_phosphorus = db.query(Fertilizer).filter(Fertilizer.name.ilike("%10-52-10%")).first()
        potassium_sulfate = db.query(Fertilizer).filter(Fertilizer.name == "سولفات پتاسیم").first()
        magnesium_sulfate = db.query(Fertilizer).filter(Fertilizer.name == "سولفات منیزیم").first()
        iron_chelate = db.query(Fertilizer).filter(Fertilizer.name == "کلات آهن EDDHA").first()

        if calcium_nitrate and high_phosphorus:
            interaction1 = Interaction(
                fertilizer_a_id=calcium_nitrate.id,
                fertilizer_b_id=high_phosphorus.id,
                reaction_type="precipitation",
                severity="critical",
                precipitate_product="Calcium Phosphate",
                description="⚠️ خطر رسوب کلسیم فسفات! این دو کود را هرگز با هم در یک مخزن مخلوط نکنید. ابتدا یکی را کاملاً حل کنید، سپس دیگری را اضافه کنید."
            )
            db.add(interaction1)
            print(f"   ✅ Interaction: {calcium_nitrate.name} <-> {high_phosphorus.name}")

        if calcium_nitrate and potassium_sulfate:
            interaction2 = Interaction(
                fertilizer_a_id=calcium_nitrate.id,
                fertilizer_b_id=potassium_sulfate.id,
                reaction_type="precipitation",
                severity="high",
                precipitate_product="Calcium Sulfate",
                description="⚠️ خطر رسوب کلسیم سولفات (گچ). در غلظت‌های بالا ممکن است باعث گرفتگی قطره‌چکان‌ها شود."
            )
            db.add(interaction2)
            print(f"   ✅ Interaction: {calcium_nitrate.name} <-> {potassium_sulfate.name}")

        if calcium_nitrate and magnesium_sulfate:
            interaction3 = Interaction(
                fertilizer_a_id=calcium_nitrate.id,
                fertilizer_b_id=magnesium_sulfate.id,
                reaction_type="precipitation",
                severity="high",
                precipitate_product="Calcium Sulfate",
                description="⚠️ خطر رسوب کلسیم سولفات. در غلظت‌های بالا ممکن است باعث گرفتگی شود."
            )
            db.add(interaction3)
            print(f"   ✅ Interaction: {calcium_nitrate.name} <-> {magnesium_sulfate.name}")

        if iron_chelate and high_phosphorus:
            interaction4 = Interaction(
                fertilizer_a_id=iron_chelate.id,
                fertilizer_b_id=high_phosphorus.id,
                reaction_type="precipitation",
                severity="medium",
                precipitate_product="Iron Phosphate",
                description="⚠️ فسفر بالا می‌تواند آهن را رسوب دهد. بهتر است با فاصله زمانی مصرف شوند."
            )
            db.add(interaction4)
            print(f"   ✅ Interaction: {iron_chelate.name} <-> {high_phosphorus.name}")

        db.flush()

        # ============================================================
        # اسیدها (Acids) برای تنظیم pH
        # ============================================================
        print("\n🧪 Creating acids...")
        
        acids_data = [
            {
                "name": "اسید فسفریک",
                "chemical_formula": "H3PO4",
                "concentration_percent": 85.0,
                "density_g_per_ml": 1.685,
                "supplies_element": "P",
                "element_percent": 27.0,
                "ml_per_1000L_per_ph_point": 50,
                "notes": "منبع فسفر و کاهش‌دهنده pH - مناسب برای مراحل اولیه رشد"
            },
            {
                "name": "اسید نیتریک",
                "chemical_formula": "HNO3",
                "concentration_percent": 68.0,
                "density_g_per_ml": 1.41,
                "supplies_element": "N",
                "element_percent": 15.0,
                "ml_per_1000L_per_ph_point": 30,
                "notes": "منبع نیتروژن و کاهش‌دهنده pH - مناسب برای مراحل رشد رویشی"
            },
            {
                "name": "اسید سولفوریک",
                "chemical_formula": "H2SO4",
                "concentration_percent": 98.0,
                "density_g_per_ml": 1.84,
                "supplies_element": "S",
                "element_percent": 32.7,
                "ml_per_1000L_per_ph_point": 25,
                "notes": "منبع گوگرد و کاهش‌دهنده pH - بسیار قوی، با احتیاط استفاده شود"
            }
        ]

        for acid_data in acids_data:
            acid = Acid(**acid_data)
            db.add(acid)

        db.flush()
        print(f"   ✅ {len(acids_data)} acids created")

        # ============================================================
        # نهایی کردن و گزارش
        # ============================================================
        db.commit()

        print("\n" + "=" * 70)
        print("✅ Database seeded successfully!")
        print("=" * 70)
        print(f"\n📊 Statistics:")
        print(f"   🌾 Crops: 1")
        print(f"   🍓 Varieties: 2")
        print(f"   🏭 Brands: 4")
        print(f"   🧪 Fertilizers: {len(fertilizers)}")
        print(f"   📈 Growth Stages: {len(stages)}")
        print(f"   🧪 Acids: {len(acids_data)}")
        print(f"   ⚠️ Interactions: 4")

        # نمایش نسبت‌های K/Ca برای تأیید کیفیت فرمولاسیون
        print("\n📊 K/Ca Ratios (San Andreas - هدف: کمتر از 1.3):")
        for stage, needs in san_andreas_needs.items():
            k_ca = needs['K'] / needs['Ca']
            status = "✅" if k_ca <= 1.3 else "⚠️"
            print(f"   {status} {stage}: K/Ca = {k_ca:.2f}")

        print("\n📊 K/Ca Ratios (Camarosa - هدف: کمتر از 1.3):")
        for stage, needs in camarosa_needs.items():
            k_ca = needs['K'] / needs['Ca']
            status = "✅" if k_ca <= 1.3 else "⚠️"
            print(f"   {status} {stage}: K/Ca = {k_ca:.2f}")

        # دسته‌بندی کودها
        print("\n📊 Fertilizers by type:")
        npk_count = len([f for f in fertilizers if f.fertilizer_type == "NPK"])
        single_count = len([f for f in fertilizers if f.fertilizer_type == "تک عنصری"])
        micro_count = len([f for f in fertilizers if f.fertilizer_type == "ریزمغذی"])
        stimulant_count = len([f for f in fertilizers if f.fertilizer_type == "محرک رشد"])
        
        print(f"   NPK Fertilizers: {npk_count}")
        print(f"   Single Element: {single_count}")
        print(f"   Micronutrients: {micro_count}")
        print(f"   Growth Stimulants: {stimulant_count}")

        print("\n" + "=" * 70)
        print("🎉 FarmTech Database is ready to use!")
        print("=" * 70)

    except Exception as e:
        db.rollback()
        print(f"\n❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def init_db():
    """تابع اصلی برای راه‌اندازی دیتابیس"""
    print("\n" + "=" * 70)
    print("🚀 Initializing FarmTech Database...")
    print("=" * 70)
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    seed_database()


if __name__ == "__main__":
    init_db()