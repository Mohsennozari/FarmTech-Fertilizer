#!/usr/bin/env python3
"""
Core Code Exporter - فقط هسته اصلی الگوریتم و API (بدون فایل‌های اضافی)
"""

import os
from pathlib import Path
from typing import List, Tuple
import datetime

# ============================================================
# تنظیمات
# ============================================================
PROJECT_ROOT = Path(__file__).parent.absolute()
OUTPUT_FILE = "CORE_CODE.md"

# ============================================================
# ✅ فایل‌های هسته اصلی (فقط چیزی که برای فهم الگوریتم لازمه)
# ============================================================
CORE_FILES = [
    # ====== BACKEND CORE (فقط فایل‌های ضروری) ======
    "backend/app/main.py",
    "backend/app/models.py",
    "backend/app/routes.py",
    "backend/app/schemas.py",
    "backend/app/database.py",
    "backend/requirements.txt",
    "backend/run.py",

    # ====== CALCULATOR ENGINE (هسته اصلی الگوریتم) ======
    "backend/app/calculator/__init__.py",
    "backend/app/calculator/core.py",
    "backend/app/calculator/dual_tank.py",
    "backend/app/calculator/ec.py",
    "backend/app/calculator/instructions.py",
    "backend/app/calculator/optimization.py",
    "backend/app/calculator/stock.py",
    "backend/app/calculator/tank.py",

    # ====== FRONTEND CORE (فقط صفحه اصلی و کامپوننت‌های کلیدی) ======
    "frontend/src/views/CalculatorView.vue",
    "frontend/src/components/calculator/ResultsDisplay.vue",
    "frontend/src/components/common/InputField.vue",
    "frontend/src/components/common/ThemeToggle.vue",
    "frontend/src/App.vue",
    "frontend/src/main.ts",
    "frontend/src/style.css",
    "frontend/package.json",
]

# ============================================================
# ⚠️ فایل‌هایی که نباید خروجی داده شوند
# ============================================================
EXCLUDED_PATTERNS = [
    # Database
    "farmtech.db",
    "*.db",
    "*.sqlite",
    "*.sqlite3",

    # Seed files
    "backend/app/seed/",
    "seed.py",
    "run_seed.py",

    # Project management
    "manage.py",
    "README.md",
    "backup.py",
    "export_core.py",

    # Config files (نیاز نیست برای فهم الگوریتم)
    "tailwind.config.js",
    "vite.config.ts",
    "postcss.config.js",
    "tsconfig.json",
    "tsconfig.app.json",
    "tsconfig.node.json",

    # Simple UI components (نیاز نیست)
    "Button.vue",
    "Card.vue",
    "Input.vue",
    "Select.vue",
    "ErrorAlert.vue",
    "LoadingSpinner.vue",
    "index.ts",

    # Router
    "router/",

    # Admin
    "FertilizerList.vue",

    # Logs and cache
    "*.log",
    "*.pyc",
    "__pycache__",

    # Test files
    "test_*.py",
    "*_test.py",

    # Backup
    "backup",
    "*.zip",

    # IDE
    ".vscode",
    ".idea",
    ".git",

    # Empty files
    "__init__.py",
]

# ============================================================
# توابع اصلی
# ============================================================

def is_excluded(filepath: str) -> bool:
    """بررسی اینکه فایل نباید خروجی داده شود"""
    for pattern in EXCLUDED_PATTERNS:
        if pattern.endswith('/'):
            if pattern in filepath:
                return True
        elif pattern in filepath:
            return True
        if pattern.startswith('*') and pattern[1:] in filepath:
            return True
    return False

def read_file_safe(filepath: Path) -> str:
    """خواندن امن فایل"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"<!-- Error reading file: {e} -->"

def get_language(filepath: str) -> str:
    """تشخیص زبان برای syntax highlighting"""
    ext = Path(filepath).suffix.lower()
    mapping = {
        '.py': 'python',
        '.vue': 'vue',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.json': 'json',
        '.css': 'css',
        '.html': 'html',
        '.txt': 'text',
    }
    return mapping.get(ext, 'text')

def get_file_size(filepath: Path) -> str:
    """دریافت حجم فایل"""
    try:
        size = filepath.stat().st_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
    except:
        return "N/A"

def generate_markdown() -> str:
    """تولید فایل Markdown از فایل‌های اصلی"""

    lines = []

    # Header
    lines.append("# 🎯 FarmTech Core Algorithm & API Export")
    lines.append("")
    lines.append(f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Project:** FarmTech Fertilizer System v3.3.1")
    lines.append(f"**Core Files:** {len(CORE_FILES)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # فهرست مطالب
    lines.append("## 📑 Table of Contents")
    lines.append("")
    for i, filepath in enumerate(CORE_FILES, 1):
        full_path = PROJECT_ROOT / filepath
        status = "✅" if full_path.exists() else "❌"
        lines.append(f"{i}. {status} [`{filepath}`](#file-{i})")
    lines.append("")
    lines.append("---")
    lines.append("")

    # محتوای فایل‌ها
    found_count = 0

    for i, filepath in enumerate(CORE_FILES, 1):
        full_path = PROJECT_ROOT / filepath

        if is_excluded(filepath):
            continue

        if full_path.exists():
            found_count += 1
            content = read_file_safe(full_path)
            lang = get_language(filepath)
            size = get_file_size(full_path)

            lines.append(f"## File {i}: `{filepath}`")
            lines.append("")
            lines.append(f"**Size:** {size}")
            lines.append("")
            lines.append(f"```{lang}")
            lines.append(content)
            lines.append("```")
            lines.append("")
        else:
            lines.append(f"## File {i}: `{filepath}`")
            lines.append("")
            lines.append("```text")
            lines.append("❌ FILE NOT FOUND")
            lines.append("```")
            lines.append("")

        if i < len(CORE_FILES):
            lines.append("---")
            lines.append("")

    # Summary
    lines.append("---")
    lines.append("")
    lines.append("## 📊 Summary")
    lines.append("")
    lines.append(f"- **Total Core Files:** {len(CORE_FILES)}")
    lines.append(f"- **Found:** {found_count} ✅")
    lines.append("")
    lines.append("### 🚀 What's Included:")
    lines.append("")
    lines.append("1. **Backend API** - FastAPI routes, models, schemas")
    lines.append("2. **Calculator Engine** - Core optimization algorithm")
    lines.append("3. **Dual Tank System** - Calcium/Main tank separation logic")
    lines.append("4. **Stock Solution** - Injector ratio calculations")
    lines.append("5. **Frontend UI** - Main calculator view and results")
    lines.append("")
    lines.append("### ❌ What's Excluded (Not needed for understanding):")
    lines.append("")
    lines.append("- Database files")
    lines.append("- Seed data")
    lines.append("- Config files (tailwind, vite, tsconfig)")
    lines.append("- Simple UI components (Button, Card, Input, etc.)")
    lines.append("- Router files")
    lines.append("- Admin components")
    lines.append("- Test files")
    lines.append("- Project management files")
    lines.append("")
    lines.append(f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return "\n".join(lines)

def main():
    """تابع اصلی"""
    print("=" * 60)
    print("🎯 FarmTech Core Algorithm Exporter")
    print("=" * 60)
    print(f"📁 Project Root: {PROJECT_ROOT}")
    print(f"📄 Output: {OUTPUT_FILE}")
    print(f"📋 Core Files: {len(CORE_FILES)}")
    print("=" * 60)
    print()

    print("🔍 Checking core files...")
    found = 0
    missing = []

    for filepath in CORE_FILES:
        full_path = PROJECT_ROOT / filepath

        if is_excluded(filepath):
            continue

        if full_path.exists():
            found += 1
            print(f"   ✅ {filepath}")
        else:
            missing.append(filepath)
            print(f"   ❌ {filepath} (MISSING)")

    print()
    print(f"📊 Found: {found}/{len(CORE_FILES)} files")
    if missing:
        print(f"⚠️ Missing {len(missing)} files:")
        for m in missing:
            print(f"   - {m}")
    print()

    print("📝 Generating Markdown...")
    markdown = generate_markdown()

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(markdown)

    size_mb = Path(OUTPUT_FILE).stat().st_size / (1024 * 1024)
    print(f"✅ Done! Output saved to: {OUTPUT_FILE}")
    print(f"   Size: {size_mb:.2f} MB")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback#!/usr/bin/env python3
"""
Core Algorithm Exporter - فقط الگوریتم و API (بدون فرانت‌اند)
"""

import os
from pathlib import Path
from typing import List, Tuple
import datetime

# ============================================================
# تنظیمات
# ============================================================
PROJECT_ROOT = Path(__file__).parent.absolute()
OUTPUT_FILE = "ALGORITHM_CORE.md"

# ============================================================
# ✅ فقط فایل‌های بک‌اند و الگوریتم
# ============================================================
CORE_FILES = [
    # ====== BACKEND CORE ======
    "backend/app/main.py",
    "backend/app/models.py",
    "backend/app/routes.py",
    "backend/app/schemas.py",
    "backend/app/database.py",
    "backend/app/config.py",
    "backend/requirements.txt",
    "backend/run.py",

    # ====== CALCULATOR ENGINE (هسته الگوریتم) ======
    "backend/app/calculator/__init__.py",
    "backend/app/calculator/core.py",
    "backend/app/calculator/dual_tank.py",
    "backend/app/calculator/ec.py",
    "backend/app/calculator/instructions.py",
    "backend/app/calculator/optimization.py",
    "backend/app/calculator/stock.py",
    "backend/app/calculator/tank.py",
]

# ============================================================
# ⚠️ فایل‌هایی که نباید خروجی داده شوند
# ============================================================
EXCLUDED_PATTERNS = [
    # Database
    "farmtech.db",
    "*.db",
    "*.sqlite",
    "*.sqlite3",

    # Seed files
    "backend/app/seed/",
    "seed.py",
    "run_seed.py",

    # Frontend (کاملاً حذف)
    "frontend/",

    # Project management
    "manage.py",
    "README.md",
    "backup.py",
    "export_core.py",

    # Logs and cache
    "*.log",
    "*.pyc",
    "__pycache__",

    # Test files
    "test_*.py",
    "*_test.py",

    # Backup
    "backup",
    "*.zip",

    # IDE
    ".vscode",
    ".idea",
    ".git",

    # Empty files
    "__init__.py",
]

# ============================================================
# توابع اصلی
# ============================================================

def is_excluded(filepath: str) -> bool:
    """بررسی اینکه فایل نباید خروجی داده شود"""
    for pattern in EXCLUDED_PATTERNS:
        if pattern.endswith('/'):
            if pattern in filepath:
                return True
        elif pattern in filepath:
            return True
        if pattern.startswith('*') and pattern[1:] in filepath:
            return True
    return False

def read_file_safe(filepath: Path) -> str:
    """خواندن امن فایل"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"<!-- Error reading file: {e} -->"

def get_language(filepath: str) -> str:
    """تشخیص زبان برای syntax highlighting"""
    ext = Path(filepath).suffix.lower()
    mapping = {
        '.py': 'python',
        '.json': 'json',
        '.txt': 'text',
    }
    return mapping.get(ext, 'text')

def get_file_size(filepath: Path) -> str:
    """دریافت حجم فایل"""
    try:
        size = filepath.stat().st_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
    except:
        return "N/A"

def generate_markdown() -> str:
    """تولید فایل Markdown از فایل‌های اصلی"""

    lines = []

    # Header
    lines.append("# 🧮 FarmTech Algorithm Core")
    lines.append("")
    lines.append(f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Project:** FarmTech Fertilizer System v3.3.1")
    lines.append(f"**Core Files:** {len(CORE_FILES)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # فهرست مطالب
    lines.append("## 📑 Table of Contents")
    lines.append("")
    for i, filepath in enumerate(CORE_FILES, 1):
        full_path = PROJECT_ROOT / filepath
        status = "✅" if full_path.exists() else "❌"
        lines.append(f"{i}. {status} [`{filepath}`](#file-{i})")
    lines.append("")
    lines.append("---")
    lines.append("")

    # محتوای فایل‌ها
    found_count = 0

    for i, filepath in enumerate(CORE_FILES, 1):
        full_path = PROJECT_ROOT / filepath

        if is_excluded(filepath):
            continue

        if full_path.exists():
            found_count += 1
            content = read_file_safe(full_path)
            lang = get_language(filepath)
            size = get_file_size(full_path)

            lines.append(f"## File {i}: `{filepath}`")
            lines.append("")
            lines.append(f"**Size:** {size}")
            lines.append("")
            lines.append(f"```{lang}")
            lines.append(content)
            lines.append("```")
            lines.append("")
        else:
            lines.append(f"## File {i}: `{filepath}`")
            lines.append("")
            lines.append("```text")
            lines.append("❌ FILE NOT FOUND")
            lines.append("```")
            lines.append("")

        if i < len(CORE_FILES):
            lines.append("---")
            lines.append("")

    # Summary
    lines.append("---")
    lines.append("")
    lines.append("## 📊 Summary")
    lines.append("")
    lines.append(f"- **Total Core Files:** {len(CORE_FILES)}")
    lines.append(f"- **Found:** {found_count} ✅")
    lines.append("")
    lines.append("### 🚀 What's Included:")
    lines.append("")
    lines.append("1. **API Layer** - routes.py, schemas.py, models.py")
    lines.append("2. **Calculator Engine** - core optimization algorithm")
    lines.append("3. **Dual Tank System** - Calcium/Main tank separation")
    lines.append("4. **Stock Solution** - Injector ratio calculations")
    lines.append("5. **EC & pH Calculations** - Final EC prediction")
    lines.append("6. **Layer-by-Layer Optimization** - NPK → Secondary → Micro")
    lines.append("")
    lines.append("### ❌ What's Excluded:")
    lines.append("")
    lines.append("- Database files")
    lines.append("- Seed data")
    lines.append("- Frontend (Vue components, CSS, router)")
    lines.append("- Config files")
    lines.append("- Test files")
    lines.append("- Project management files")
    lines.append("- Simple UI components")
    lines.append("")
    lines.append(f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return "\n".join(lines)

def main():
    """تابع اصلی"""
    print("=" * 60)
    print("🧮 FarmTech Algorithm Core Exporter")
    print("=" * 60)
    print(f"📁 Project Root: {PROJECT_ROOT}")
    print(f"📄 Output: {OUTPUT_FILE}")
    print(f"📋 Core Files: {len(CORE_FILES)}")
    print("=" * 60)
    print()

    print("🔍 Checking algorithm files...")
    found = 0
    missing = []

    for filepath in CORE_FILES:
        full_path = PROJECT_ROOT / filepath

        if is_excluded(filepath):
            continue

        if full_path.exists():
            found += 1
            print(f"   ✅ {filepath}")
        else:
            missing.append(filepath)
            print(f"   ❌ {filepath} (MISSING)")

    print()
    print(f"📊 Found: {found}/{len(CORE_FILES)} files")
    if missing:
        print(f"⚠️ Missing {len(missing)} files:")
        for m in missing:
            print(f"   - {m}")
    print()

    print("📝 Generating Markdown...")
    markdown = generate_markdown()

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(markdown)

    size_mb = Path(OUTPUT_FILE).stat().st_size / (1024 * 1024)
    print(f"✅ Done! Output saved to: {OUTPUT_FILE}")
    print(f"   Size: {size_mb:.2f} MB")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        traceback.print_exc()
