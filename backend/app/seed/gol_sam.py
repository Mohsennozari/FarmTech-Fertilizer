# backend/app/seed/gol_sam.py
"""
Seed file for GOL SAM GORGAN (گل سم گرگان) fertilizers
Date: 1405/03/14
"""

from sqlalchemy.orm import Session
from app.models import Fertilizer
from .base import (
    get_brand_id,
    convert_p2o5_to_p,
    convert_k2o_to_k,
    convert_mgo_to_mg
)


def seed_gol_sam(db: Session):
    """Create all fertilizers for GOL SAM GORGAN company"""
    print("\n🧪 Seeding GOL SAM GORGAN fertilizers...")

    brand_id = get_brand_id(db, "گل سم گرگان")

    fertilizers_data = [
        # =================================================================
        # Product 1: UniComplex Powder (یونی کمپلکس پودری)
        # =================================================================
        {
            "name": "یونی کمپلکس پودری",
            "brand_id": brand_id,
            "brand_name": "گل سم گرگان",
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
گوگرد محلول (S): 25%

ملاحظات:
- مصرف در زمان مشاهده علائم کمبود عناصر توصیه می‌شود.
- برای محلول‌پاشی، در ساعات خنک روز استفاده گردد.
- قبل از اختلاط با سایر کودها و سموم، تست سازگاری انجام شود.
- در محل خشک، خنک و دور از نور مستقیم خورشید نگهداری شود.

بسته‌بندی: وزن 10 کیلویی - کد محصول: 41000017""",
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
        # =================================================================
        # Product 2: Fertigol 36-12-12 (فرتی‌گل 36-12-12)
        # =================================================================
        {
            "name": "فرتی‌گل 36-12-12",
            "brand_id": brand_id,
            "brand_name": "گل سم گرگان",
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
منیزیم محلول (MgO): 1%

ملاحظات:
- بهترین زمان مصرف در مرحله رشد میوه و افزایش نیاز گیاه به پتاسیم است.
- محلول‌پاشی در ساعات خنک روز انجام شود.
- قبل از اختلاط با سایر کودها و سموم، تست سازگاری توصیه می‌شود.
- در محل خشک، خنک و دور از نور مستقیم خورشید نگهداری گردد.

بسته‌بندی: وزن 1 کیلویی (کد: 41000032) و 10 کیلویی (کد: 41000004)""",
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
        # =================================================================
        # Product 3: Fertigol 10-50-10 (فرتی‌گل 10-50-10)
        # =================================================================
        {
            "name": "فرتی‌گل 10-50-10",
            "brand_id": brand_id,
            "brand_name": "گل سم گرگان",
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
پتاسیم (K2O): 10%

ملاحظات:
- بهترین زمان مصرف در مراحل ابتدای رشد و پیش از گلدهی است.
- از مصرف در ساعات گرم روز برای محلول‌پاشی خودداری شود.
- قبل از اختلاط با کودها و سموم دیگر، تست سازگاری انجام شود.
- در محل خشک و خنک و دور از تابش مستقیم نور خورشید نگهداری گردد.

بسته‌بندی: وزن 2 کیلویی (کد: 41000013) و 10 کیلویی (کد: 41000008)""",
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
        # =================================================================
        # Product 4: Fertigol 30-5-15 (فرتی‌گل 30-5-15)
        # =================================================================
        {
            "name": "فرتی‌گل 30-5-15",
            "brand_id": brand_id,
            "brand_name": "گل سم گرگان",
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
منیزیم (MgO): 1%

ملاحظات:
- در ساعات خنک روز محلول‌پاشی شود.
- قبل از اختلاط با سایر کودها و سموم، تست سازگاری انجام شود.
- دور از نور مستقیم خورشید و در محل خشک و خنک نگهداری شود.

بسته‌بندی: وزن 10 کیلویی - کد محصول: 41000007""",
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
        # =================================================================
        # Product 5: Fertigol 20-20-20 (فرتی‌گل 20-20-20)
        # =================================================================
        {
            "name": "فرتی‌گل 20-20-20",
            "brand_id": brand_id,
            "brand_name": "گل سم گرگان",
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
منیزیم (MgO): 1%

تولیدکننده مواد اولیه: شرکت یوروسالیدز هلند

ملاحظات:
- مقدار دقیق مصرف بر اساس نیاز گیاه و سطح کمبود تعیین شود.
- قبل از اختلاط با کودها و سموم دیگر، در سطح محدود آزمایش شود.
- دور از نور مستقیم و در محل خشک و خنک نگهداری گردد.

بسته‌بندی: وزن 1 کیلویی (کد: 41000034) و 10 کیلویی (کد: 41000009)""",
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
        }
    ]

    # Insert fertilizers
    for fert_data in fertilizers_data:
        existing = db.query(Fertilizer).filter(
            Fertilizer.name == fert_data["name"],
            Fertilizer.brand_id == brand_id
        ).first()

        if not existing:
            fert = Fertilizer(**fert_data)
            db.add(fert)
            print(f"   ✅ Fertilizer: {fert_data['name']}")
        else:
            print(f"   ⏭️  Skipping (already exists): {fert_data['name']}")

    db.flush()
    print(f"   ✅ Total GOL SAM fertilizers: {len(fertilizers_data)}")


# =================================================================
# Optional: Run this seed independently for testing
# =================================================================
if __name__ == "__main__":
    from app.database import SessionLocal
    from app.models import Base
    from app.database import engine

    print("=" * 70)
    print("Testing GOL SAM seed independently...")
    print("=" * 70)

    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        # First ensure brand exists
        from .brands import seed_brands
        seed_brands(db)
        db.commit()

        # Then seed Gol Sam fertilizers
        seed_gol_sam(db)
        db.commit()

    print("\n✅ Test completed!")