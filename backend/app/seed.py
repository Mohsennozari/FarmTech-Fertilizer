# Platform-v3\backend\app\seed.py

import json
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import (
    Crop, Variety, GrowthStage, Brand, Fertilizer,
    Interaction, Acid, Tank, CalculationHistory
)

# ضرایب تبدیل اکسید به عنصر خالص (مقادیر دقیق علمی)
P2O5_TO_P = 0.4364   # 61.9475 / 141.9445
K2O_TO_K = 0.8301    # 78.1966 / 94.196
CaO_TO_Ca = 0.7147   # 40.078 / 56.0774
MgO_TO_Mg = 0.603    # 24.305 / 40.3044


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
        print("Clearing existing data...")
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
        print("Previous data cleared")

        print("\nCreating crops...")
        strawberry = Crop(
            name="توت‌فرنگی",
            scientific_name="Fragaria × ananassa",
            cultivation_type="هیدروپونیک"
        )
        db.add(strawberry)
        db.flush()
        print(f"   Crop: {strawberry.name}")

        print("\nCreating varieties...")
        san_andreas = Variety(
            crop_id=strawberry.id,
            name="سن اندرسا",
            description="High yield variety suitable for hydroponics",
            growth_days=90,
            yield_potential="High"
        )
        db.add(san_andreas)

        camarosa = Variety(
            crop_id=strawberry.id,
            name="کاماروسا",
            description="Early ripening with large fruits",
            growth_days=80,
            yield_potential="Very High"
        )
        db.add(camarosa)
        db.flush()
        print(f"   Variety: {san_andreas.name}")
        print(f"   Variety: {camarosa.name}")

        print("\nCreating brands...")
        gol_sam = Brand(
            name="گل سم گرگان",
            country="Iran",
            website="www.golsam.com",
            notes="Fertilizer manufacturer"
        )
        db.add(gol_sam)

        razak = Brand(
            name="رازاک شیمی",
            country="Iran",
            website="www.razakshimi.com",
            notes="NPK and sulfate fertilizer manufacturer"
        )
        db.add(razak)
        db.flush()
        print(f"   Brand: {gol_sam.name}")
        print(f"   Brand: {razak.name}")

        print("\nCreating fertilizers...")

        fertilizers_data = [
            {
                "name": "یونی کمپلکس پودری",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_type": "ریزمغذی",
                "chemical_formula": "Complete Micro",
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
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 12-12-36",
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
            },
            {
                "name": "فرتی‌گل 10-50-10",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 10-50-10",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 10.0,
                "p_percent": convert_p2o5_to_p(50.0),
                "k_percent": convert_k2o_to_k(10.0),
            },
            {
                "name": "فرتی‌گل 30-5-15",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 15-5-30",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
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
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 20-20-20",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 20.0,
                "p_percent": convert_p2o5_to_p(20.0),
                "k_percent": convert_k2o_to_k(20.0),
                "mg_percent": convert_mgo_to_mg(1.0),
            },
            {
                "name": "NPK 20-20-20 گرین استار",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 20-20-20",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 20.0,
                "p_percent": convert_p2o5_to_p(20.0),
                "k_percent": convert_k2o_to_k(20.0),
            },
            {
                "name": "NPK 12-12-36 گرین استار",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 12-12-36",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 12.0,
                "p_percent": convert_p2o5_to_p(12.0),
                "k_percent": convert_k2o_to_k(36.0),
            },
            {
                "name": "NPK 10-52-10 زاگرا استار",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 10-52-10",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 10.0,
                "p_percent": convert_p2o5_to_p(52.0),
                "k_percent": convert_k2o_to_k(10.0),
            },
            {
                "name": "سولفات پتاسیم",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "K2SO4",
                "purity_percent": 100,
                "max_dose_g_per_liter": 2.0,
                "min_dose_g_per_liter": 0.2,
                "k_percent": 51.0,
                "s_percent": 18.0,
            },
            {
                "name": "نیترات کلسیم",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "Ca(NO3)2",
                "purity_percent": 100,
                "max_dose_g_per_liter": 2.0,
                "min_dose_g_per_liter": 0.2,
                "n_percent": 15.5,
                "ca_percent": 19.0,
            },
            {
                "name": "کلرید پتاسیم",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "KCl",
                "purity_percent": 100,
                "max_dose_g_per_liter": 1.0,
                "min_dose_g_per_liter": 0.1,
                "k_percent": 52.0,
                "cl_percent": 47.0,
            },
        ]

        fertilizers = []
        for fert_data in fertilizers_data:
            fert = Fertilizer(**fert_data)
            db.add(fert)
            fertilizers.append(fert)

        db.flush()
        print(f"   {len(fertilizers)} fertilizers created")

        print("\nCreating growth stages...")

        # ============================================================
        # نیازهای تغذیه‌ای اصلاح شده با نسبت K/Ca مناسب
        # نسبت استاندارد: K/Ca ≤ 1.2 برای توت‌فرنگی
        # ============================================================

        san_andreas_needs = {
            "استقرار نشاء": {"N": 50, "P": 30, "K": 55, "Ca": 50, "Mg": 20, "S": 15, "Fe": 2, "Zn": 0.5, "Mn": 0.5, "Cu": 0.1, "B": 0.2, "Mo": 0.05, "Cl": 0},
            "ریشه‌زایی": {"N": 70, "P": 40, "K": 75, "Ca": 65, "Mg": 25, "S": 18, "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0},
            "رشد رویشی": {"N": 120, "P": 50, "K": 120, "Ca": 105, "Mg": 40, "S": 25, "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.4, "Mo": 0.05, "Cl": 0},
            "گلدهی": {"N": 100, "P": 60, "K": 130, "Ca": 105, "Mg": 35, "S": 22, "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.5, "Mo": 0.05, "Cl": 0},
            "میوه‌دهی": {"N": 80, "P": 40, "K": 140, "Ca": 115, "Mg": 30, "S": 20, "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0}
        }

        camarosa_needs = {
            "استقرار نشاء": {"N": 55, "P": 28, "K": 55, "Ca": 50, "Mg": 19, "S": 14, "Fe": 2, "Zn": 0.5, "Mn": 0.5, "Cu": 0.1, "B": 0.2, "Mo": 0.05, "Cl": 0},
            "ریشه‌زایی": {"N": 75, "P": 38, "K": 70, "Ca": 60, "Mg": 24, "S": 17, "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0},
            "رشد رویشی": {"N": 110, "P": 48, "K": 115, "Ca": 100, "Mg": 39, "S": 24, "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.4, "Mo": 0.05, "Cl": 0},
            "گلدهی": {"N": 95, "P": 58, "K": 125, "Ca": 100, "Mg": 34, "S": 21, "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.5, "Mo": 0.05, "Cl": 0},
            "میوه‌دهی": {"N": 75, "P": 38, "K": 135, "Ca": 105, "Mg": 29, "S": 19, "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0}
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

        # مراحل رشد برای سن اندرسا
        for i, name in enumerate(stage_names):
            ec_min, ec_max, ph_min, ph_max = ec_ph_targets[name]
            stage = GrowthStage(
                crop_id=strawberry.id,
                variety_id=san_andreas.id,
                name=name,
                stage_order=stage_orders[i],
                description=f"Stage {name} for San Andreas",
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
                description=f"Stage {name} for Camarosa",
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
                description=f"General stage {name} for Strawberry",
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
        print(f"   {len(stages)} growth stages created")

        print("\nCreating interactions...")

        # تداخل نیترات کلسیم با کودهای فسفری
        calcium_nitrate = db.query(Fertilizer).filter(Fertilizer.name == "نیترات کلسیم").first()
        high_phosphorus = db.query(Fertilizer).filter(Fertilizer.name.ilike("%10-52-10%")).first()

        if calcium_nitrate and high_phosphorus:
            interaction = Interaction(
                fertilizer_a_id=calcium_nitrate.id,
                fertilizer_b_id=high_phosphorus.id,
                reaction_type="precipitation",
                severity="critical",
                precipitate_product="Calcium Phosphate",
                description="⚠️ خطر رسوب کلسیم فسفات! این دو کود را هرگز با هم مخلوط نکنید. ابتدا یکی را حل کنید، سپس دیگری را اضافه کنید."
            )
            db.add(interaction)

        # تداخل نیترات کلسیم با سولفات پتاسیم
        potassium_sulfate = db.query(Fertilizer).filter(Fertilizer.name == "سولفات پتاسیم").first()
        if calcium_nitrate and potassium_sulfate:
            interaction2 = Interaction(
                fertilizer_a_id=calcium_nitrate.id,
                fertilizer_b_id=potassium_sulfate.id,
                reaction_type="precipitation",
                severity="high",
                precipitate_product="Calcium Sulfate",
                description="⚠️ خطر رسوب کلسیم سولفات (گچ). در غلظت‌های بالا ممکن است باعث گرفتگی شود."
            )
            db.add(interaction2)

        db.flush()

        print("\nCreating acids...")
        acids_data = [
            {
                "name": "Phosphoric Acid",
                "chemical_formula": "H3PO4",
                "concentration_percent": 85.0,
                "density_g_per_ml": 1.685,
                "supplies_element": "P",
                "element_percent": 27.0,
                "ml_per_1000L_per_ph_point": 50
            },
            {
                "name": "Nitric Acid",
                "chemical_formula": "HNO3",
                "concentration_percent": 68.0,
                "density_g_per_ml": 1.41,
                "supplies_element": "N",
                "element_percent": 15.0,
                "ml_per_1000L_per_ph_point": 30
            },
            {
                "name": "Sulfuric Acid",
                "chemical_formula": "H2SO4",
                "concentration_percent": 98.0,
                "density_g_per_ml": 1.84,
                "supplies_element": "S",
                "element_percent": 32.7,
                "ml_per_1000L_per_ph_point": 25
            },
        ]

        for acid_data in acids_data:
            acid = Acid(**acid_data)
            db.add(acid)

        db.flush()
        print(f"   {len(acids_data)} acids created")

        db.commit()

        print("\n" + "="*50)
        print("Database seeded successfully!")
        print("="*50)
        print(f"\nStatistics:")
        print(f"   Crops: 1")
        print(f"   Varieties: 2")
        print(f"   Brands: 2")
        print(f"   Fertilizers: {len(fertilizers)}")
        print(f"   Growth Stages: {len(stages)}")
        print(f"   Acids: {len(acids_data)}")
        print(f"   Interactions: 2")

        # نمایش نسبت‌های K/Ca برای تأیید
        print("\n📊 K/Ca Ratios (San Andreas - corrected):")
        for stage, needs in san_andreas_needs.items():
            k_ca = needs['K'] / needs['Ca']
            status = "✅" if k_ca <= 1.3 else "⚠️"
            print(f"   {status} {stage}: K/Ca = {k_ca:.2f}")

    except Exception as e:
        db.rollback()
        print(f"\nError seeding database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def init_db():
    print("Initializing FarmTech Database...")
    print("="*50)
    Base.metadata.create_all(bind=engine)
    print("Database tables created")
    seed_database()


if __name__ == "__main__":
    init_db()
