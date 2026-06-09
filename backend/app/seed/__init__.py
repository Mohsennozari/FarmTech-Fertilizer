# backend/app/seed/__init__.py
"""
Main seed module - orchestrates all seed files
Run all seeds or individual seeds for specific companies
Date: 1405/03/14
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base

# Import all seed functions
from .brands import seed_brands
from .gol_sam import seed_gol_sam
from .razak_shimi import seed_razak_shimi
from .atlas import seed_atlas
from .redsa import seed_redsa
from .crops import seed_crops_and_stages
from .interactions import seed_interactions
from .acids import seed_acids


def run_all_seeds(db: Session):
    """
    Run all seeds in correct order
    
    Order matters because:
    1. Brands must exist before fertilizers (foreign key constraint)
    2. Crops and varieties must exist before growth stages
    3. Fertilizers must exist before interactions
    """
    print("\n" + "=" * 70)
    print("🚀 Running ALL Database Seeds...")
    print("=" * 70)

    # Step 1: Create all brands (required for fertilizers)
    seed_brands(db)

    # Step 2: Create crops, varieties, and growth stages
    seed_crops_and_stages(db)

    # Step 3: Seed fertilizers for each company
    seed_gol_sam(db)        # گل سم گرگان
    seed_razak_shimi(db)    # رازاک شیمی (includes Green Star and Zagara Star)
    seed_atlas(db)          # اطلس
    seed_redsa(db)          # ردسا

    # Step 4: Create chemical interactions (requires fertilizers to exist)
    seed_interactions(db)

    # Step 5: Create acids for pH adjustment
    seed_acids(db)

    print("\n" + "=" * 70)
    print("🎉 ALL seeds completed successfully!")
    print("=" * 70)


def init_db():
    """Main function to initialize database"""
    print("\n" + "=" * 70)
    print("🚀 Initializing FarmTech Database...")
    print("=" * 70)

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

    # Run seeds
    with SessionLocal() as db:
        try:
            run_all_seeds(db)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"\n❌ Error seeding database: {e}")
            import traceback
            traceback.print_exc()
            raise

    print("\n" + "=" * 70)
    print("🎉 FarmTech Database is ready to use!")
    print("=" * 70)


if __name__ == "__main__":
    init_db()