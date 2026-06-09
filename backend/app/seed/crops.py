# backend/app/seed/crops.py
"""
Seed file for Crops, Varieties, and Growth Stages
Date: 1405/03/14
"""

from sqlalchemy.orm import Session
from app.models import Crop, Variety, GrowthStage


def seed_crops_and_stages(db: Session):
    """Create crops, varieties, and growth stages"""
    print("\n🌾 Seeding crops, varieties, and growth stages...")

    # ============================================================
    # محصولات (Crops)
    # ============================================================
    strawberry = Crop(
        name="توت‌فرنگی",
        scientific_name="Fragaria × ananassa",
        cultivation_type="هیدروپونیک"
    )
    db.add(strawberry)
    db.flush()
    print(f"   ✅ Crop: {strawberry.name}")

    # ============================================================
    # ارقام (Varieties)
    # ============================================================
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
    # نیازهای تغذیه‌ای برای مراحل رشد توت‌فرنگی
    # ============================================================
    
    # نیازهای تغذیه‌ای برای رقم سن اندرسا
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

    # نمایش نسبت‌های K/Ca برای تأیید کیفیت فرمولاسیون
    print("\n   📊 K/Ca Ratios (San Andreas - هدف: کمتر از 1.3):")
    for stage, needs in san_andreas_needs.items():
        k_ca = needs['K'] / needs['Ca']
        status = "✅" if k_ca <= 1.3 else "⚠️"
        print(f"      {status} {stage}: K/Ca = {k_ca:.2f}")

    print("\n   📊 K/Ca Ratios (Camarosa - هدف: کمتر از 1.3):")
    for stage, needs in camarosa_needs.items():
        k_ca = needs['K'] / needs['Ca']
        status = "✅" if k_ca <= 1.3 else "⚠️"
        print(f"      {status} {stage}: K/Ca = {k_ca:.2f}")


if __name__ == "__main__":
    from app.database import SessionLocal
    from app.models import Base
    from app.database import engine

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_crops_and_stages(db)
        db.commit()
    print("\n✅ Test completed!")