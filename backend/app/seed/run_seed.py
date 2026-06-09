# backend/run_seed.py
"""
Standalone script to run database seeds from command line
Usage:
    python run_seed.py                    # Seed all companies
    python run_seed.py --list             # List available companies
    python run_seed.py --companies atlas  # Seed only ATLAS
    python run_seed.py --companies redsa  # Seed only REDSA
    python run_seed.py --companies gol_sam razak_shimi  # Seed multiple
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.seed import init_db
from app.seed.__init__ import run_selected_seeds
from app.database import SessionLocal


def main():
    import argparse

    parser = argparse.ArgumentParser(description='FarmTech Database Seeder CLI')
    parser.add_argument('--companies', nargs='+',
                       choices=['gol_sam', 'razak_shimi', 'atlas', 'redsa', 'all'],
                       default=['all'],
                       help='Companies to seed (default: all)')
    parser.add_argument('--list', action='store_true',
                       help='List available companies')
    parser.add_argument('--drop-tables', action='store_true',
                       help='Drop all tables before seeding (CAUTION!)')

    args = parser.parse_args()

    if args.list:
        print("\n📋 Available companies:")
        print("   ┌─────────────────────────────────────────────────────────┐")
        print("   │  gol_sam      : گل سم گرگان                             │")
        print("   │  razak_shimi  : رازاک شیمی (includes Green Star & Zagara Star) │")
        print("   │  atlas        : اطلس                                    │")
        print("   │  redsa        : ردسا                                    │")
        print("   │  all          : All companies (default)                 │")
        print("   └─────────────────────────────────────────────────────────┘")
        sys.exit(0)

    if args.drop_tables:
        print("\n⚠️  WARNING: This will drop ALL existing tables!")
        confirm = input("Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            from app.database import engine, Base
            Base.metadata.drop_all(bind=engine)
            print("✅ All tables dropped")
        else:
            print("❌ Cancelled")
            sys.exit(0)

    if args.companies == ['all']:
        init_db()
    else:
        print(f"\n🎯 Seeding selected companies: {', '.join(args.companies)}")
        from app.database import SessionLocal, engine, Base
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            try:
                run_selected_seeds(db, args.companies)
                db.commit()
                print("\n✅ Seed completed successfully!")
            except Exception as e:
                db.rollback()
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()
                sys.exit(1)


if __name__ == "__main__":
    main()