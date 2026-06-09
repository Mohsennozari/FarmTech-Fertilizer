# backend/app/seed/acids.py
"""
Seed file for pH adjustment Acids
Date: 1405/03/14
"""

from sqlalchemy.orm import Session
from app.models import Acid


def seed_acids(db: Session):
    """Create acids for pH adjustment"""
    print("\n🧪 Seeding acids...")

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

    created_count = 0
    for acid_data in acids_data:
        existing = db.query(Acid).filter(Acid.name == acid_data["name"]).first()
        if not existing:
            acid = Acid(**acid_data)
            db.add(acid)
            created_count += 1
            print(f"   ✅ Acid: {acid_data['name']}")
        else:
            print(f"   ⏭️  Skipping (already exists): {acid_data['name']}")

    db.flush()
    print(f"   ✅ Total acids: {created_count}")


if __name__ == "__main__":
    from app.database import SessionLocal
    from app.models import Base
    from app.database import engine

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_acids(db)
        db.commit()
    print("\n✅ Test completed!")