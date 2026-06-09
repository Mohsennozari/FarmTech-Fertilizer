"""
FarmTech Context Generator
Simple script to generate core context file
"""

import os
from pathlib import Path
import datetime

PROJECT_ROOT = Path(__file__).parent
OUTPUT_FILE = "CORE_CONTEXT.md"

# فایل‌هایی که باید در کانتکست قرار بگیرند
BACKEND_FILES = [
    "backend/app/calculator.py",
    "backend/app/models.py",
    "backend/app/routes.py",
    "backend/app/schemas.py",
    "backend/app/seed.py",
    "backend/requirements.txt",
]

FRONTEND_FILES = [
    "frontend/src/views/CalculatorView.vue",
    "frontend/src/components/calculator/ResultsDisplay.vue",
    "frontend/package.json",
]

def read_file_safe(filepath):
    """Safe file reader"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"<!-- Error reading file: {e} -->"

def generate_context():
    """Generate core context file"""

    print("🚀 Generating Core Context...")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:

        # Header
        out.write(f"# 🌱 FarmTech Core Context\n\n")
        out.write(f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out.write(f"**Project:** FarmTech Fertilizer System\n\n")
        out.write("---\n\n")

        # Backend Section
        out.write("## 🔧 Backend Core\n\n")

        for filepath in BACKEND_FILES:
            full_path = PROJECT_ROOT / filepath
            if full_path.exists():
                content = read_file_safe(full_path)
                ext = "python" if filepath.endswith('.py') else "text"
                out.write(f"### 📄 `{filepath}`\n\n")
                out.write(f"```{ext}\n")
                out.write(content)
                out.write("\n```\n\n")
            else:
                out.write(f"<!-- File not found: {filepath} -->\n\n")

        out.write("---\n\n")

        # Frontend Section
        out.write("## 🎨 Frontend Core\n\n")

        for filepath in FRONTEND_FILES:
            full_path = PROJECT_ROOT / filepath
            if full_path.exists():
                content = read_file_safe(full_path)
                ext = "vue" if filepath.endswith('.vue') else "json" if filepath.endswith('.json') else "javascript"
                out.write(f"### 📄 `{filepath}`\n\n")
                out.write(f"```{ext}\n")
                out.write(content)
                out.write("\n```\n\n")
            else:
                out.write(f"<!-- File not found: {filepath} -->\n\n")

        # Project Structure
        out.write("---\n\n")
        out.write("## 📁 Project Structure\n\n")
        out.write("```\n")

        def print_tree(dir_path, prefix="", level=0, max_level=2):
            if level > max_level:
                return
            try:
                items = sorted([item for item in dir_path.iterdir()
                               if not item.name.startswith('.')
                               and item.name not in ['__pycache__', 'node_modules', 'venv', 'dist', '.git']])
                for i, item in enumerate(items):
                    is_last = i == len(items) - 1
                    current_prefix = "└── " if is_last else "├── "
                    out.write(f"{prefix}{current_prefix}{item.name}\n")
                    if item.is_dir():
                        extension = "    " if is_last else "│   "
                        print_tree(item, prefix + extension, level + 1, max_level)
            except PermissionError:
                pass

        print_tree(PROJECT_ROOT)
        out.write("```\n\n")

        # Summary
        out.write("---\n\n")
        out.write("## 📊 Summary\n\n")
        out.write(f"- **Backend Files:** {len(BACKEND_FILES)}\n")
        out.write(f"- **Frontend Files:** {len(FRONTEND_FILES)}\n")
        out.write(f"- **Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # File size info
    size = os.path.getsize(OUTPUT_FILE)
    print(f"✅ Context generated: {OUTPUT_FILE} ({size:,} bytes)")

if __name__ == "__main__":
    generate_context()
