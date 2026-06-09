# backend/app/seed/brands.py
"""
Seed file for all brands
Contains all fertilizer companies/brands
Date: 1405/03/14
"""

from sqlalchemy.orm import Session
from app.models import Brand
from .base import get_or_create_brand


def seed_brands(db: Session):
    """Create all brands in the database"""
    print("\n🏭 Seeding brands...")

    brands_data = [
        {
            "name": "گل سم گرگان",
            "country": "ایران",
            "website": "www.golsam.com",
            "notes": "تولید کننده کودهای کشاورزی با کیفیت بالا - محصولات فرتی‌گل و یونی کمپلکس"
        },
        {
            "name": "رازاک شیمی",
            "country": "ایران",
            "website": "www.razakshimi.com",
            "notes": "تولید کننده کودهای NPK، سولفات‌ها و محرک‌های رشد - برندهای گرین استار و زاگرا استار"
        },
        {
            "name": "گرین استار",
            "country": "ایران",
            "website": "www.greenstar.ir",
            "notes": "تولید کننده کودهای کامل NPK با کیفیت بالا - دارای کد ثبت مواد کودی معتبر"
        },
        {
            "name": "زاگرا استار",
            "country": "ایران",
            "website": "www.zagrastar.ir",
            "notes": "تولید کننده کودهای کامل NPK، هیومیک اسید و مواد آلی"
        },
        {
            "name": "اطلس",
            "country": "ایران",
            "website": "www.atlas-chem.ir",
            "notes": "تولید کننده کلات‌های پیشرفته EDTA، EDDHA و آمینو اسیدی (گلایسینات) - محصولات بدون سدیم"
        },
        {
            "name": "ردسا",
            "country": "ایران",
            "website": "www.redsa.ir",
            "notes": "تامین و توزیع کننده نهاده‌های کشاورزی - تولید کننده کودهای میکرو، ماکرو، محرک‌های رشد و کودهای زیستی"
        }
    ]

    created_count = 0
    existing_count = 0

    for brand_data in brands_data:
        brand = get_or_create_brand(db, brand_data)
        if brand.id:
            created_count += 1
        else:
            existing_count += 1

    db.flush()
    print(f"   ✅ Total brands: {len(brands_data)} (Created: {created_count}, Existing: {existing_count})")


# =================================================================
# Optional: Run this seed independently for testing
# =================================================================
if __name__ == "__main__":
    from app.database import SessionLocal
    from app.models import Base
    from app.database import engine

    print("=" * 70)
    print("Testing BRANDS seed independently...")
    print("=" * 70)

    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        seed_brands(db)
        db.commit()

    print("\n✅ Test completed!")