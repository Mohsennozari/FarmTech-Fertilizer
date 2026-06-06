# Platform-v3\backend\app\seed.py

import json
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import (
    Crop, Variety, GrowthStage, Brand, Fertilizer, 
    Interaction, Acid, Tank, CalculationHistory
)

# ============================================================
# ضرایب تبدیل و توابع کمکی
# ============================================================
P2O5_TO_P = 0.436
K2O_TO_K = 0.83
CaO_TO_Ca = 0.715
MgO_TO_Mg = 0.603


def convert_p2o5_to_p(p2o5_percent: float) -> float:
    return round(p2o5_percent * P2O5_TO_P, 2)


def convert_k2o_to_k(k2o_percent: float) -> float:
    return round(k2o_percent * K2O_TO_K, 2)


def convert_cao_to_ca(cao_percent: float) -> float:
    return round(cao_percent * CaO_TO_Ca, 2)


def convert_mgo_to_mg(mgo_percent: float) -> float:
    return round(mgo_percent * MgO_TO_Mg, 2)


def seed_database():
    db = SessionLocal()
    
    try:
        print("🗑️ حذف داده‌های قبلی...")
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
        print("✅ داده‌های قبلی حذف شدند")
        
        print("\n📦 ایجاد محصولات...")
        strawberry = Crop(
            name="توت‌فرنگی",
            scientific_name="Fragaria × ananassa",
            cultivation_type="هیدروپونیک"
        )
        db.add(strawberry)
        db.flush()
        print(f"   ✅ محصول: {strawberry.name}")
        
        print("\n🌱 ایجاد ارقام...")
        san_andreas = Variety(
            crop_id=strawberry.id,
            name="سن اندرسا",
            description="رقم پابلند با عملکرد بالا، مناسب کشت هیدروپونیک و خاکی",
            growth_days=90,
            yield_potential="بالا"
        )
        db.add(san_andreas)
        
        camarosa = Variety(
            crop_id=strawberry.id,
            name="کاماروسا",
            description="رقم زودرس با میوه درشت و بازارپسند، مناسب مناطق معتدل",
            growth_days=80,
            yield_potential="بسیار بالا"
        )
        db.add(camarosa)
        db.flush()
        print(f"   ✅ رقم: {san_andreas.name}")
        print(f"   ✅ رقم: {camarosa.name}")
        
        print("\n🏭 ایجاد برندها...")
        gol_sam = Brand(
            name="گل سم گرگان",
            country="ایران",
            website="www.golsam.com",
            notes="تولیدکننده کودهای تخصصی گلخانه‌ای"
        )
        db.add(gol_sam)
        
        razak = Brand(
            name="رازاک شیمی",
            country="ایران",
            website="www.razakshimi.com",
            notes="تولیدکننده کودهای کامل NPK و سولفات‌ها"
        )
        db.add(razak)
        db.flush()
        print(f"   ✅ برند: {gol_sam.name}")
        print(f"   ✅ برند: {razak.name}")
        
        print("\n🧪 ایجاد کودها...")
        
        fertilizers_data = [
            # ========== گل سم گرگان - کود پودری ==========
            {
                "name": "یونی کمپلکس پودری",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "ریزمغذی",
                "chemical_formula": "کامل ریزمغذی",
                "purity_percent": 100,
                "max_dose_g_per_liter": 5.0,
                "min_dose_g_per_liter": 0.5,
                "fe_percent": 5.0,
                "zn_percent": 5.0,
                "mn_percent": 4.0,
                "cu_percent": 4.0,
                "b_percent": 1.5,
                "mo_percent": 0.07,
                "mg_percent": convert_mgo_to_mg(1.2),
                "s_percent": 25.0,
            },
            {
                "name": "فرتی‌گل 36-12-12",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 12-12-36",
                "purity_percent": 100,
                "max_dose_g_per_liter": 5.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 12.0,
                "p_percent": convert_p2o5_to_p(12.0),
                "k_percent": convert_k2o_to_k(36.0),
                "mg_percent": convert_mgo_to_mg(1.0),
                "fe_percent": 0.016,
                "zn_percent": 0.037,
                "mn_percent": 0.006,
                "cu_percent": 0.0015,
            },
            {
                "name": "فرتی‌گل 10-50-10",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 10-50-10",
                "purity_percent": 100,
                "max_dose_g_per_liter": 5.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 10.0,
                "p_percent": convert_p2o5_to_p(50.0),
                "k_percent": convert_k2o_to_k(10.0),
            },
            {
                "name": "فرتی‌گل 30-5-15",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 15-5-30",
                "purity_percent": 100,
                "max_dose_g_per_liter": 5.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 15.0,
                "p_percent": convert_p2o5_to_p(5.0),
                "k_percent": convert_k2o_to_k(30.0),
                "mg_percent": convert_mgo_to_mg(1.0),
            },
            {
                "name": "فرتی‌گل 20-20-20",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 20-20-20",
                "purity_percent": 100,
                "max_dose_g_per_liter": 5.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 20.0,
                "p_percent": convert_p2o5_to_p(20.0),
                "k_percent": convert_k2o_to_k(20.0),
                "mg_percent": convert_mgo_to_mg(1.0),
            },
            # ========== رازاک شیمی - کود پودری ==========
            {
                "name": "NPK 20-20-20 گرین استار",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 20-20-20",
                "purity_percent": 100,
                "max_dose_g_per_liter": 5.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 20.0,
                "p_percent": convert_p2o5_to_p(20.0),
                "k_percent": convert_k2o_to_k(20.0),
            },
            {
                "name": "NPK 12-12-36 گرین استار",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 12-12-36",
                "purity_percent": 100,
                "max_dose_g_per_liter": 5.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 12.0,
                "p_percent": convert_p2o5_to_p(12.0),
                "k_percent": convert_k2o_to_k(36.0),
            },
            {
                "name": "NPK 10-52-10 زاگرا استار",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 10-52-10",
                "purity_percent": 100,
                "max_dose_g_per_liter": 5.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 10.0,
                "p_percent": convert_p2o5_to_p(52.0),
                "k_percent": convert_k2o_to_k(10.0),
            },
            {
                "name": "NPK 12-12-36 زاگرا استار",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 12-12-36",
                "purity_percent": 100,
                "max_dose_g_per_liter": 5.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 12.0,
                "p_percent": convert_p2o5_to_p(12.0),
                "k_percent": convert_k2o_to_k(36.0),
            },
            {
                "name": "NPK 15-5-30 زاگرا استار",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 15-5-30",
                "purity_percent": 100,
                "max_dose_g_per_liter": 5.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 15.0,
                "p_percent": convert_p2o5_to_p(5.0),
                "k_percent": convert_k2o_to_k(30.0),
            },
            {
                "name": "NPK 30-10-10 زاگرا استار",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 30-10-10",
                "purity_percent": 100,
                "max_dose_g_per_liter": 5.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 30.0,
                "p_percent": convert_p2o5_to_p(10.0),
                "k_percent": convert_k2o_to_k(10.0),
            },
            {
                "name": "NPK 20-20-20 زاگرا استار",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 20-20-20",
                "purity_percent": 100,
                "max_dose_g_per_liter": 5.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 20.0,
                "p_percent": convert_p2o5_to_p(20.0),
                "k_percent": convert_k2o_to_k(20.0),
            },
            # ========== رازاک شیمی - سولفات‌ها ==========
            {
                "name": "سولفات پتاسیم",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "K2SO4",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.2,
                "k_percent": 51.0,
                "s_percent": 18.0,
            },
            {
                "name": "سولفات روی",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "ZnSO4",
                "purity_percent": 100,
                "max_dose_g_per_liter": 2.0,
                "min_dose_g_per_liter": 0.1,
                "zn_percent": 35.0,
            },
            {
                "name": "سولفات منگنز",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "MnSO4",
                "purity_percent": 100,
                "max_dose_g_per_liter": 2.0,
                "min_dose_g_per_liter": 0.1,
                "mn_percent": 32.0,
            },
            {
                "name": "سولفات مس",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "CuSO4",
                "purity_percent": 100,
                "max_dose_g_per_liter": 1.0,
                "min_dose_g_per_liter": 0.05,
                "cu_percent": 25.0,
            },
            {
                "name": "سولفات منیزیم",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "MgSO4",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.2,
                "mg_percent": 9.8,
                "s_percent": 13.0,
            },
            {
                "name": "سولفات آهن",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "FeSO4",
                "purity_percent": 100,
                "max_dose_g_per_liter": 2.0,
                "min_dose_g_per_liter": 0.1,
                "fe_percent": 19.0,
            },
            {
                "name": "نیترات کلسیم",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "Ca(NO3)2",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.2,
                "n_percent": 15.5,
                "ca_percent": 19.0,
            },
            {
                "name": "هیومیک اسید",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_form": "powder",
                "fertilizer_type": "آلی",
                "chemical_formula": "Humic Acid",
                "purity_percent": 95,
                "max_dose_g_per_liter": 2.0,
                "min_dose_g_per_liter": 0.1,
            },
        ]
        
        fertilizers = []
        for fert_data in fertilizers_data:
            fert = Fertilizer(**fert_data)
            db.add(fert)
            fertilizers.append(fert)
        
        db.flush()
        print(f"   ✅ {len(fertilizers)} کود ایجاد شد")
        
        print("\n📈 ایجاد مراحل رشد...")
        
        san_andreas_needs = {
            "استقرار نشاء": {"N": 50, "P": 30, "K": 60, "Ca": 40, "Mg": 20, "S": 15, "Fe": 2, "Zn": 0.5, "Mn": 0.5, "Cu": 0.1, "B": 0.2, "Mo": 0.05, "Cl": 0},
            "ریشه‌زایی": {"N": 70, "P": 40, "K": 80, "Ca": 50, "Mg": 25, "S": 18, "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0},
            "رشد رویشی": {"N": 120, "P": 50, "K": 150, "Ca": 80, "Mg": 40, "S": 25, "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.4, "Mo": 0.05, "Cl": 0},
            "گلدهی": {"N": 100, "P": 60, "K": 180, "Ca": 70, "Mg": 35, "S": 22, "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.5, "Mo": 0.05, "Cl": 0},
            "میوه‌دهی": {"N": 80, "P": 40, "K": 200, "Ca": 60, "Mg": 30, "S": 20, "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0}
        }
        
        camarosa_needs = {
            "استقرار نشاء": {"N": 55, "P": 28, "K": 55, "Ca": 38, "Mg": 19, "S": 14, "Fe": 2, "Zn": 0.5, "Mn": 0.5, "Cu": 0.1, "B": 0.2, "Mo": 0.05, "Cl": 0},
            "ریشه‌زایی": {"N": 75, "P": 38, "K": 75, "Ca": 48, "Mg": 24, "S": 17, "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0},
            "رشد رویشی": {"N": 110, "P": 48, "K": 140, "Ca": 78, "Mg": 39, "S": 24, "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.4, "Mo": 0.05, "Cl": 0},
            "گلدهی": {"N": 95, "P": 58, "K": 170, "Ca": 68, "Mg": 34, "S": 21, "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.5, "Mo": 0.05, "Cl": 0},
            "میوه‌دهی": {"N": 75, "P": 38, "K": 190, "Ca": 58, "Mg": 29, "S": 19, "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0}
        }
        
        stage_names = ["استقرار نشاء", "ریشه‌زایی", "رشد رویشی", "گلدهی", "میوه‌دهی"]
        stage_orders = [0, 1, 2, 3, 4]
        
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
        
        for i, name in enumerate(stage_names):
            ec_min, ec_max, ph_min, ph_max = ec_ph_targets[name]
            stage = GrowthStage(
                crop_id=strawberry.id,
                variety_id=san_andreas.id,
                name=name,
                stage_order=stage_orders[i],
                description=f"مرحله {name} توت‌فرنگی رقم سن اندرسا",
                nutrient_needs=san_andreas_needs[name],
                target_ec_min=ec_min,
                target_ec_max=ec_max,
                target_ph_min=ph_min,
                target_ph_max=ph_max,
                priority=priorities[name]
            )
            db.add(stage)
            stages.append(stage)
        
        for i, name in enumerate(stage_names):
            ec_min, ec_max, ph_min, ph_max = ec_ph_targets[name]
            stage = GrowthStage(
                crop_id=strawberry.id,
                variety_id=camarosa.id,
                name=name,
                stage_order=stage_orders[i],
                description=f"مرحله {name} توت‌فرنگی رقم کاماروسا",
                nutrient_needs=camarosa_needs[name],
                target_ec_min=ec_min,
                target_ec_max=ec_max,
                target_ph_min=ph_min,
                target_ph_max=ph_max,
                priority=priorities[name]
            )
            db.add(stage)
            stages.append(stage)
        
        for i, name in enumerate(stage_names):
            ec_min, ec_max, ph_min, ph_max = ec_ph_targets[name]
            stage = GrowthStage(
                crop_id=strawberry.id,
                variety_id=None,
                name=name,
                stage_order=stage_orders[i],
                description=f"مرحله عمومی {name} توت‌فرنگی",
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
        print(f"   ✅ {len(stages)} مرحله رشد ایجاد شد")
        
        print("\n⚠️ ایجاد تداخلات شیمیایی...")
        
        calcium_nitrate = db.query(Fertilizer).filter(Fertilizer.name == "نیترات کلسیم").first()
        high_phosphorus = db.query(Fertilizer).filter(Fertilizer.name.ilike("%10-52-10%")).first()
        
        if calcium_nitrate and high_phosphorus:
            interaction = Interaction(
                fertilizer_a_id=calcium_nitrate.id,
                fertilizer_b_id=high_phosphorus.id,
                reaction_type="precipitation",
                severity="critical",
                precipitate_product="کلسیم فسفات",
                description="ترکیب نیترات کلسیم با کودهای فسفره باعث رسوب کلسیم فسفات و انسداد قطره‌چکان‌ها می‌شود"
            )
            db.add(interaction)
        
        db.flush()
        
        print("\n🧪 ایجاد اسیدهای رایج...")
        
        acids_data = [
            {
                "name": "اسید فسفریک",
                "chemical_formula": "H3PO4",
                "concentration_percent": 85.0,
                "density_g_per_ml": 1.685,
                "supplies_element": "P",
                "element_percent": 27.0,
                "ml_per_1000L_per_ph_point": 50,
                "notes": "برای خنثی‌سازی بیکربنات و تنظیم pH"
            },
            {
                "name": "اسید نیتریک",
                "chemical_formula": "HNO3",
                "concentration_percent": 68.0,
                "density_g_per_ml": 1.41,
                "supplies_element": "N",
                "element_percent": 15.0,
                "ml_per_1000L_per_ph_point": 30,
                "notes": "منبع نیتروژن و تنظیم pH"
            },
            {
                "name": "اسید سولفوریک",
                "chemical_formula": "H2SO4",
                "concentration_percent": 98.0,
                "density_g_per_ml": 1.84,
                "supplies_element": "S",
                "element_percent": 32.0,
                "ml_per_1000L_per_ph_point": 20,
                "notes": "تنظیم pH و تامین گوگرد"
            }
        ]
        
        for acid_data in acids_data:
            acid = Acid(**acid_data)
            db.add(acid)
        
        db.flush()
        print(f"   ✅ {len(acids_data)} اسید ایجاد شد")
        
        db.commit()
        
        print("\n" + "="*50)
        print("🎉 دیتابیس با موفقیت سید شد!")
        print("="*50)
        print(f"\n📊 آمار نهایی:")
        print(f"   - محصولات: 1")
        print(f"   - ارقام: 2")
        print(f"   - برندها: 2")
        print(f"   - کودها: {len(fertilizers)}")
        print(f"   - مراحل رشد: {len(stages)}")
        print(f"   - تداخلات: 1")
        print(f"   - اسیدها: {len(acids_data)}")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ خطا در سید دیتابیس: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def init_db():
    print("🚀 راه‌اندازی دیتابیس FarmTech...")
    print("="*50)
    Base.metadata.create_all(bind=engine)
    print("✅ جداول دیتابیس ایجاد شدند")
    seed_database()


if __name__ == "__main__":
    init_db()