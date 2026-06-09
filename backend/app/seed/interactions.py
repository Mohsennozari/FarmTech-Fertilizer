# backend/app/seed/interactions.py
"""
Seed file for Chemical Interactions
Date: 1405/03/14
"""

from sqlalchemy.orm import Session
from app.models import Fertilizer, Interaction


def seed_interactions(db: Session):
    """Create chemical interactions between fertilizers"""
    print("\n⚠️ Seeding chemical interactions...")

    # دریافت کودهای مورد نیاز از دیتابیس
    calcium_nitrate = db.query(Fertilizer).filter(Fertilizer.name == "نیترات کلسیم").first()
    high_phosphorus = db.query(Fertilizer).filter(Fertilizer.name.ilike("%10-52-10%")).first()
    potassium_sulfate = db.query(Fertilizer).filter(Fertilizer.name == "سولفات پتاسیم").first()
    magnesium_sulfate = db.query(Fertilizer).filter(Fertilizer.name == "سولفات منیزیم").first()
    iron_chelate = db.query(Fertilizer).filter(Fertilizer.name == "کلات آهن EDDHA").first()

    interactions_data = []

    if calcium_nitrate and high_phosphorus:
        interactions_data.append({
            "fertilizer_a_id": calcium_nitrate.id,
            "fertilizer_b_id": high_phosphorus.id,
            "reaction_type": "precipitation",
            "severity": "critical",
            "precipitate_product": "Calcium Phosphate",
            "description": "⚠️ خطر رسوب کلسیم فسفات! این دو کود را هرگز با هم در یک مخزن مخلوط نکنید. ابتدا یکی را کاملاً حل کنید، سپس دیگری را اضافه کنید."
        })

    if calcium_nitrate and potassium_sulfate:
        interactions_data.append({
            "fertilizer_a_id": calcium_nitrate.id,
            "fertilizer_b_id": potassium_sulfate.id,
            "reaction_type": "precipitation",
            "severity": "high",
            "precipitate_product": "Calcium Sulfate",
            "description": "⚠️ خطر رسوب کلسیم سولفات (گچ). در غلظت‌های بالا ممکن است باعث گرفتگی قطره‌چکان‌ها شود."
        })

    if calcium_nitrate and magnesium_sulfate:
        interactions_data.append({
            "fertilizer_a_id": calcium_nitrate.id,
            "fertilizer_b_id": magnesium_sulfate.id,
            "reaction_type": "precipitation",
            "severity": "high",
            "precipitate_product": "Calcium Sulfate",
            "description": "⚠️ خطر رسوب کلسیم سولفات. در غلظت‌های بالا ممکن است باعث گرفتگی شود."
        })

    if iron_chelate and high_phosphorus:
        interactions_data.append({
            "fertilizer_a_id": iron_chelate.id,
            "fertilizer_b_id": high_phosphorus.id,
            "reaction_type": "precipitation",
            "severity": "medium",
            "precipitate_product": "Iron Phosphate",
            "description": "⚠️ فسفر بالا می‌تواند آهن را رسوب دهد. بهتر است با فاصله زمانی مصرف شوند."
        })

    created_count = 0
    for int_data in interactions_data:
        existing = db.query(Interaction).filter(
            Interaction.fertilizer_a_id == int_data["fertilizer_a_id"],
            Interaction.fertilizer_b_id == int_data["fertilizer_b_id"]
        ).first()
        
        if not existing:
            interaction = Interaction(**int_data)
            db.add(interaction)
            created_count += 1
            print(f"   ✅ Interaction: {int_data['fertilizer_a_id']} <-> {int_data['fertilizer_b_id']}")

    db.flush()
    print(f"   ✅ Total interactions: {created_count}")


if __name__ == "__main__":
    from app.database import SessionLocal
    from app.models import Base
    from app.database import engine

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_interactions(db)
        db.commit()
    print("\n✅ Test completed!")