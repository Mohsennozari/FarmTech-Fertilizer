#!/usr/bin/env python
# manage.py - FarmTech Project Manager
# قرار دهید در: FarmTech-Fertilizer/manage.py
# اجرا: python manage.py

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

# تنظیمات مسیرها
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

# رنگ‌ها برای محیط CLI (اختیاری)
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header():
    """نمایش هدر برنامه"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print(Colors.CYAN + "=" * 60 + Colors.END)
    print(Colors.BOLD + Colors.GREEN + "         FarmTech Project Manager v1.0" + Colors.END)
    print(Colors.CYAN + "=" * 60 + Colors.END)
    print()

def print_menu():
    """نمایش منوی اصلی"""
    print(Colors.YELLOW + "📋 MAIN MENU:" + Colors.END)
    print()
    print("  1. 🚀 Start All (Backend + Frontend)")
    print("  2. 🐍 Start Backend Only")
    print("  3. 🎨 Start Frontend Only")
    print("  4. 💾 Seed Database (Initialize/Reset)")
    print("  5. 🔨 Build Frontend (Production)")
    print("  6. 🧪 Run Tests")
    print("  7. 📊 Show Database Status")
    print("  8. 🧹 Clean Database (Delete All Tables)")
    print("  9. 🔄 Full Reset (Clean + Seed)")
    print(" 10. ⚙️ Install All Dependencies")
    print(" 11. 📦 Install Backend Dependencies Only")
    print(" 12. 🎨 Install Frontend Dependencies Only")
    print(" 13. 📝 Check Missing Fertilizer Elements")
    print(" 14. ❌ Exit")
    print()

def run_command(cmd, cwd=None, shell=True):
    """اجرای دستور در ترمینال و نمایش خروجی"""
    try:
        if cwd:
            print(Colors.BLUE + f"\n📁 Running in: {cwd}" + Colors.END)
        print(Colors.YELLOW + f"💻 Command: {cmd}" + Colors.END)
        print("-" * 50)
        
        result = subprocess.run(cmd, cwd=cwd, shell=shell, text=True)
        
        if result.returncode == 0:
            print(Colors.GREEN + f"\n✅ Command completed successfully!" + Colors.END)
            return True
        else:
            print(Colors.RED + f"\n❌ Command failed with code {result.returncode}" + Colors.END)
            return False
    except Exception as e:
        print(Colors.RED + f"\n❌ Error: {e}" + Colors.END)
        return False

def start_background_process(cmd, cwd=None):
    """اجرای فرآیند در پس‌زمینه (برای سرورها)"""
    try:
        if platform.system() == 'Windows':
            subprocess.Popen(cmd, cwd=cwd, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(cmd, cwd=cwd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(Colors.RED + f"Error: {e}" + Colors.END)
        return False

def start_all():
    """شروع همزمان بک‌اند و فرانت‌اند در دو ترمینال مجزا"""
    print(Colors.CYAN + "\n🚀 Starting Backend and Frontend..." + Colors.END)
    
    # اجرای بک‌اند
    print("\n" + Colors.YELLOW + "1. Starting Backend Server..." + Colors.END)
    if not start_background_process("python run.py", BACKEND_DIR):
        return
    
    import time
    time.sleep(2)
    
    # اجرای فرانت‌اند
    print("\n" + Colors.YELLOW + "2. Starting Frontend Server..." + Colors.END)
    if not start_background_process("npm run dev", FRONTEND_DIR):
        return
    
    print(Colors.GREEN + "\n✅ Both servers started!" + Colors.END)
    print(Colors.CYAN + "📍 Backend:  http://localhost:8000" + Colors.END)
    print(Colors.CYAN + "📍 Backend API Docs: http://localhost:8000/docs" + Colors.END)
    print(Colors.CYAN + "📍 Frontend: http://localhost:5173" + Colors.END)
    print()

def start_backend():
    """شروع فقط بک‌اند"""
    print(Colors.CYAN + "\n🐍 Starting Backend Server..." + Colors.END)
    run_command("python run.py", BACKEND_DIR)

def start_frontend():
    """شروع فقط فرانت‌اند"""
    print(Colors.CYAN + "\n🎨 Starting Frontend Server..." + Colors.END)
    run_command("npm run dev", FRONTEND_DIR)

def seed_database():
    """سید کردن دیتابیس"""
    print(Colors.CYAN + "\n💾 Seeding Database..." + Colors.END)
    run_command('python -c "from app.seed import init_db; init_db()"', BACKEND_DIR)

def build_frontend():
    """بیلد فرانت‌اند برای تولید"""
    print(Colors.CYAN + "\n🔨 Building Frontend for Production..." + Colors.END)
    run_command("npm run build", FRONTEND_DIR)

def run_tests():
    """اجرای تست‌ها"""
    print(Colors.CYAN + "\n🧪 Running Tests..." + Colors.END)
    
    # تست بک‌اند
    print("\n" + Colors.YELLOW + "Backend Tests:" + Colors.END)
    run_command("pytest", BACKEND_DIR)
    
    # تست فرانت‌اند
    print("\n" + Colors.YELLOW + "Frontend Tests:" + Colors.END)
    run_command("npm run test", FRONTEND_DIR)

def show_db_status():
    """نمایش وضعیت دیتابیس (تعداد رکوردها)"""
    print(Colors.CYAN + "\n📊 Database Status:" + Colors.END)
    sql_query = """
    SELECT 
        (SELECT COUNT(*) FROM brands) as brands,
        (SELECT COUNT(*) FROM crops) as crops,
        (SELECT COUNT(*) FROM varieties) as varieties,
        (SELECT COUNT(*) FROM growth_stages) as growth_stages,
        (SELECT COUNT(*) FROM fertilizers) as fertilizers,
        (SELECT COUNT(*) FROM interactions) as interactions,
        (SELECT COUNT(*) FROM acids) as acids
    """
    
    # ذخیره موقت در فایل و اجرا
    sql_file = BACKEND_DIR / "temp_query.sql"
    with open(sql_file, "w") as f:
        f.write(sql_query)
    
    run_command(f"sqlite3 farmtech.db < {sql_file}", BACKEND_DIR)
    
    if sql_file.exists():
        sql_file.unlink()

def clean_database():
    """پاک کردن کامل دیتابیس (حذف همه جدول‌ها)"""
    print(Colors.RED + "\n⚠️  WARNING: This will DELETE ALL data!" + Colors.END)
    confirm = input("Type 'yes' to confirm: ")
    
    if confirm.lower() == 'yes':
        print(Colors.CYAN + "\n🧹 Cleaning Database..." + Colors.END)
        run_command('python -c "from app.database import Base, engine; Base.metadata.drop_all(bind=engine); print(\\"✅ All tables dropped\\")"', BACKEND_DIR)
    else:
        print(Colors.YELLOW + "❌ Cancelled." + Colors.END)

def full_reset():
    """بازنشانی کامل (پاک کردن + سید)"""
    print(Colors.CYAN + "\n🔄 Full Reset (Clean + Seed)..." + Colors.END)
    clean_database()
    
    confirm = input("\nReady to seed database? (y/n): ")
    if confirm.lower() == 'y':
        seed_database()
    else:
        print(Colors.YELLOW + "Skipped seeding." + Colors.END)

def install_all():
    """نصب همه وابستگی‌ها"""
    print(Colors.CYAN + "\n📦 Installing All Dependencies..." + Colors.END)
    
    print("\n" + Colors.YELLOW + "Backend dependencies:" + Colors.END)
    run_command("pip install -r requirements.txt", BACKEND_DIR)
    
    print("\n" + Colors.YELLOW + "Frontend dependencies:" + Colors.END)
    run_command("npm install", FRONTEND_DIR)
    
    print(Colors.GREEN + "\n✅ All dependencies installed!" + Colors.END)

def install_backend():
    """نصب وابستگی‌های بک‌اند"""
    print(Colors.CYAN + "\n📦 Installing Backend Dependencies..." + Colors.END)
    run_command("pip install -r requirements.txt", BACKEND_DIR)

def install_frontend():
    """نصب وابستگی‌های فرانت‌اند"""
    print(Colors.CYAN + "\n📦 Installing Frontend Dependencies..." + Colors.END)
    run_command("npm install", FRONTEND_DIR)

def check_missing_elements():
    """بررسی کودهایی که درصد عناصر آنها کامل نیست"""
    print(Colors.CYAN + "\n📝 Checking Fertilizers for Missing Elements..." + Colors.END)
    
    check_script = """
from app.database import SessionLocal
from app.models import Fertilizer

db = SessionLocal()
fertilizers = db.query(Fertilizer).all()

print("\\nFertilizers with missing element percentages:")
print("-" * 60)

for f in fertilizers:
    missing = []
    if f.fertilizer_type == "NPK":
        if f.n_percent is None or f.n_percent == 0:
            missing.append("N")
        if f.p_percent is None or f.p_percent == 0:
            missing.append("P")
        if f.k_percent is None or f.k_percent == 0:
            missing.append("K")
    elif f.fertilizer_type == "ریزمغذی":
        if f.fe_percent is None and f.zn_percent is None and f.mn_percent is None and f.cu_percent is None and f.b_percent is None:
            missing.append("No micro elements set")
    elif f.fertilizer_type == "تک عنصری":
        if f.fe_percent is None and f.zn_percent is None and f.mn_percent is None and f.cu_percent is None and f.k_percent is None and f.ca_percent is None and f.mg_percent is None:
            missing.append("No element set")
    
    if missing:
        print(f"  ⚠️ {f.name} ({f.brand_name}): missing {', '.join(missing)}")

db.close()
"""
    
    script_file = BACKEND_DIR / "temp_check.py"
    with open(script_file, "w", encoding="utf-8") as f:
        f.write(check_script)
    
    run_command(f"python {script_file}", BACKEND_DIR)
    
    if script_file.exists():
        script_file.unlink()

def main():
    """حلقه اصلی برنامه"""
    while True:
        print_header()
        print_menu()
        
        choice = input(Colors.BOLD + "Enter your choice (1-14): " + Colors.END).strip()
        
        if choice == '1':
            start_all()
        elif choice == '2':
            start_backend()
        elif choice == '3':
            start_frontend()
        elif choice == '4':
            seed_database()
        elif choice == '5':
            build_frontend()
        elif choice == '6':
            run_tests()
        elif choice == '7':
            show_db_status()
        elif choice == '8':
            clean_database()
        elif choice == '9':
            full_reset()
        elif choice == '10':
            install_all()
        elif choice == '11':
            install_backend()
        elif choice == '12':
            install_frontend()
        elif choice == '13':
            check_missing_elements()
        elif choice == '14':
            print(Colors.GREEN + "\n👋 Goodbye!" + Colors.END)
            break
        else:
            print(Colors.RED + "\n❌ Invalid choice. Please try again." + Colors.END)
        
        print("\n")
        input(Colors.YELLOW + "Press Enter to continue..." + Colors.END)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Colors.GREEN + "\n\n👋 Goodbye!" + Colors.END)
        sys.exit(0)