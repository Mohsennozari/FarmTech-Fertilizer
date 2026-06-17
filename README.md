
# 🌱 FarmTech - سیستم هوشمند نسخه‌دهی کود دیجیتال

**Version:** 3.4.0
**Release Date:** 1405/03/26
**Status:** ✅ Production Ready

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation Guide](#installation-guide)
- [API Documentation](#api-documentation)
- [Database Models](#database-models)
- [Version 3.4.0 Improvements](#version-340-improvements)
- [Seeding Database](#seeding-database)
- [Troubleshooting](#troubleshooting)
- [Development](#development)

---

## Overview

**FarmTech** is a professional digital fertilizer prescription system for hydroponic cultivation. Using advanced optimization algorithms (SLSQP) and agricultural chemistry knowledge, it calculates optimal fertilizer doses based on:

- ✅ **13 essential elements** (N, P, K, Ca, Mg, S, Fe, Zn, Mn, Cu, B, Mo, Cl)
- ✅ **Crop growth stage** nutritional requirements
- ✅ **Available fertilizers** (auto-selected by the system)
- ✅ **Water quality analysis** (EC, pH, Calcium, Magnesium, Bicarbonate)
- ✅ **Combined water & wastewater analysis** (NEW in v3.4.0)
- ✅ **Chemical interactions** (precipitation warnings)
- ✅ **Multi-brand filtering** (select multiple manufacturers)
- ✅ **Custom nutrient needs** (manual override)
- ✅ **Dual-tank system** (Calcium and Main tanks)
- ✅ **Stock solution system** (Injector ratio calculations)

---

## 🚀 Key Features

### 🧠 Algorithm Core

| Feature | Description |
|---------|-------------|
| **13 Essential Elements** | Complete nutritional profile (N, P, K, Ca, Mg, S, Fe, Zn, Mn, Cu, B, Mo, Cl) |
| **SLSQP Optimization** | Constrained optimization with physical limits |
| **Layer-by-Layer** | NPK → Secondary → Micro elements |
| **Solubility Check** | Automatic solubility limit enforcement |
| **Dual Tank System** | Separate calcium and main tanks |
| **Stock Solution** | Injector ratio (1:X) calculations |
| **Interaction Detection** | Automatic precipitation and antagonism warnings |
| **Dynamic N Split** | Nitrogen distribution based on crop & growth stage |
| **💧 Water & Wastewater Analysis** | Combined contribution calculation with percentage mixing |

### 🗄️ Database Management

| Feature | Description |
|---------|-------------|
| **Multi-Brand** | Support for 6+ fertilizer manufacturers |
| **JSON Fields** | Flexible nutrient requirements storage |
| **Variety Support** | San Andreas, Camarosa, and custom varieties |
| **Calculation History** | Full audit trail of all prescriptions |
| **Acids** | pH adjustment with H3PO4, HNO3, H2SO4 |

### 🎨 User Interface

| Feature | Description |
|---------|-------------|
| **REST API** | Auto-documented with Swagger UI & ReDoc |
| **Modern Design** | Vue.js 3 + Tailwind CSS |
| **Dark Mode** | Full dark/light theme support |
| **Responsive** | Mobile, tablet, and desktop ready |
| **Persian Fonts** | Vazirmatn, Sahel, Samim |
| **Print Ready** | Optimized print layout |
| **💧 Water Analysis UI** | Interactive tables for water/wastewater input |
| **Clean Results** | Focus on essential data (doses, EC, pH, stock calculations) |

---

## Tech Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11+ | Core language |
| **FastAPI** | 0.115.0 | Web framework (ASGI) |
| **SQLAlchemy** | 2.0.35 | ORM |
| **Uvicorn** | 0.30.0 | ASGI server |
| **Pydantic** | 2.9.0 | Data validation |
| **NumPy** | 1.26.0 | Numerical computing |
| **SciPy** | 1.13.0 | Constrained optimization (SLSQP) |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Vue.js** | 3.5+ | Core framework + TypeScript |
| **Tailwind CSS** | 3.4+ | Styling |
| **Axios** | 1.17+ | HTTP client |
| **Vue Router** | 4.6+ | SPA navigation |
| **Vite** | 8.0+ | Build tool & dev server |

---

## Prerequisites

| Software | Version | Check Command |
|----------|---------|---------------|
| **Python** | 3.11+ | `python --version` or `python3 --version` |
| **Node.js** | 20+ | `node --version` |
| **npm** | 9+ | `npm --version` |
| **pip** | Latest | `pip --version` |

---

## Quick Start

```bash
# 1. Clone or download the project
cd FarmTech-Fertilizer

# 2. Setup backend
cd backend
pip install -r requirements.txt
python -c "from app.seed import init_db; init_db()"
python run.py

# 3. Setup frontend (new terminal)
cd ../frontend
npm install
npm run dev

# 4. Open your browser
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

---

## Installation Guide

### Step 1: Backend Setup

#### Windows (PowerShell)

```powershell
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create environment file
echo DATABASE_URL=sqlite:///./farmtech.db > .env
echo DEBUG=True >> .env

# Initialize database with seed data
python -c "from app.seed import init_db; init_db()"

# Start the server
python run.py
```

#### Linux / macOS

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
echo "DATABASE_URL=sqlite:///./farmtech.db" > .env
echo "DEBUG=True" >> .env

# Initialize database with seed data
python3 -c "from app.seed import init_db; init_db()"

# Start the server
python3 run.py
```

### Step 2: Frontend Setup (New Terminal)

```bash
# Navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Step 3: Access the Application

| Service | URL | Port |
|---------|-----|------|
| **Frontend App** | http://localhost:5173 | 5173 |
| **Backend API** | http://localhost:8000 | 8000 |
| **Swagger UI** | http://localhost:8000/docs | 8000 |
| **ReDoc** | http://localhost:8000/redoc | 8000 |

---

## Project Structure

```
FarmTech-Fertilizer/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI entry point
│   │   ├── config.py             # Configuration settings
│   │   ├── database.py           # Database connection
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── schemas.py            # Pydantic schemas
│   │   ├── routes.py             # API endpoints
│   │   │
│   │   ├── calculator/           # Core optimization engine
│   │   │   ├── __init__.py
│   │   │   ├── core.py           # Base calculations
│   │   │   ├── dual_tank.py      # Dual tank system
│   │   │   ├── ec.py             # EC calculations
│   │   │   ├── instructions.py   # Mixing instructions
│   │   │   ├── optimization.py   # SLSQP optimizer
│   │   │   ├── stock.py          # Stock solution
│   │   │   ├── tank.py           # Tank calculations
│   │   │   └── water_analysis.py # 🆕 Water & wastewater analysis
│   │   │
│   │   └── seed/                 # Database seed data
│   │
│   ├── requirements.txt
│   ├── .env
│   ├── run.py
│   └── farmtech.db
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── calculator/
│   │   │   │   └── ResultsDisplay.vue  # Clean results view
│   │   │   ├── common/
│   │   │   │   ├── InputField.vue
│   │   │   │   └── ThemeToggle.vue
│   │   │   └── admin/
│   │   ├── views/
│   │   │   └── CalculatorView.vue
│   │   ├── router/
│   │   ├── App.vue
│   │   ├── main.ts
│   │   └── style.css
│   │
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── .gitignore
└── README.md
```

---

## API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/crops` | List all crops |
| GET | `/api/v1/varieties` | List varieties (filter by crop_id) |
| GET | `/api/v1/brands` | List all brands |
| GET | `/api/v1/fertilizers` | List fertilizers (filter by brand) |
| GET | `/api/v1/growth-stages` | List growth stages |
| GET | `/api/v1/acids` | List acids for pH adjustment |
| GET | `/api/v1/interactions` | List chemical interactions |
| POST | `/api/v1/tanks` | Create a new tank |
| GET | `/api/v1/tanks` | List all tanks |
| PUT | `/api/v1/tanks/{id}` | Update a tank |
| DELETE | `/api/v1/tanks/{id}` | Delete a tank |
| POST | `/api/v1/calculate-dual-tank` | **Calculate dual tank** (main + calcium) |
| GET | `/api/v1/history` | Get calculation history |
| DELETE | `/api/v1/history/{id}` | Delete history item |

### Example Request: Calculate Dual Tank

```json
POST /api/v1/calculate-dual-tank
{
  "crop_name": "توت‌فرنگی",
  "variety_name": "سن اندرسا",
  "stage_name": "رشد رویشی",
  "brand_filter": ["گل سم گرگان", "ردسا"],
  "custom_nutrient_needs": {
    "N": 120, "P": 50, "K": 120,
    "Ca": 105, "Mg": 40, "Fe": 3
  },
  "tank_main": {
    "name": "مخزن اصلی",
    "volume_liters": 1000,
    "water_ec_ms_cm": 0.4,
    "water_ph": 7.0,
    "water_ca_ppm": 50,
    "water_mg_ppm": 20,
    "water_hco3_ppm": 0
  },
  "tank_calcium": {
    "name": "مخزن کلسیم",
    "volume_liters": 1000,
    "water_ec_ms_cm": 0.4,
    "water_ph": 7.0,
    "water_ca_ppm": 50,
    "water_mg_ppm": 20,
    "water_hco3_ppm": 0
  },
  "stock_tank_volume_liters": 20,
  "injector_ratio": 200,
  "water_percent": 80,
  "wastewater_percent": 20,
  "water_analysis": {
    "n_no3": 10, "p": 2, "s": 5, "n_nh4": 0,
    "k": 8, "ca": 50, "mg": 20, "na": 5, "cl": 5,
    "fe": 0.5, "mn": 0.1, "zn": 0.05, "b": 0.2, "cu": 0.02, "mo": 0.01,
    "ec": 0.4, "ph": 7.0
  },
  "wastewater_analysis": {
    "n_no3": 25, "p": 5, "s": 10, "n_nh4": 2,
    "k": 15, "ca": 80, "mg": 30, "na": 10, "cl": 15,
    "fe": 1.0, "mn": 0.3, "zn": 0.1, "b": 0.5, "cu": 0.05, "mo": 0.02,
    "ec": 1.2, "ph": 6.5
  }
}
```

### Example Response

```json
{
  "success": true,
  "crop_name": "توت‌فرنگی",
  "variety_name": "سن اندرسا",
  "stage_name": "رشد رویشی",
  "water_analysis": {
    "water_percent": 80,
    "wastewater_percent": 20,
    "combined_water": {
      "n_no3": 13, "p": 2.6, "s": 6, "k": 9.4,
      "ca": 56, "mg": 22, "fe": 0.6, "mn": 0.14,
      "zn": 0.06, "b": 0.26, "cu": 0.026, "mo": 0.012
    },
    "deficit": { "N": 107, "P": 47.4, "K": 110.6, "Ca": 49 }
  },
  "tank_main_result": {
    "tank_name": "مخزن اصلی",
    "tank_volume_liters": 1000,
    "doses": [
      {
        "name": "NPK 20-20-20 گرین استار",
        "dose_g_per_liter": 1.85,
        "dose_g_for_tank": 1850,
        "dose_kg_for_stock": 7.4
      }
    ],
    "supplied_ppm": { "N": 120, "P": 50, "K": 120 },
    "target_ec": 1.8
  },
  "tank_calcium_result": {
    "tank_name": "مخزن کلسیم",
    "tank_volume_liters": 1000,
    "doses": [
      {
        "name": "نیترات کلسیم",
        "dose_g_per_liter": 0.85,
        "dose_g_for_tank": 850,
        "dose_kg_for_stock": 3.4
      }
    ],
    "supplied_ppm": { "Ca": 105, "N": 45 },
    "target_ec": 1.2
  },
  "calculation_time_ms": 45.2
}
```

---

## Database Models

| Model | Description |
|-------|-------------|
| **Crop** | Agricultural crops (e.g., Strawberry) |
| **Variety** | Different varieties (San Andreas, Camarosa) |
| **GrowthStage** | Growth stages with nutritional needs (5 stages) |
| **Brand** | Fertilizer manufacturers (6+ brands) |
| **Fertilizer** | Fertilizers with chemical composition |
| **Interaction** | Chemical interactions between fertilizers |
| **Acid** | Acids for pH adjustment (H3PO4, HNO3, H2SO4) |
| **Tank** | Nutrient solution tanks |
| **CalculationHistory** | Full audit trail of all calculations |

---

## Version 3.4.0 Improvements

### 🆕 New Features

| Feature | Description |
|---------|-------------|
| **💧 Combined Water & Wastewater Analysis** | Account for existing nutrients in irrigation water and wastewater |
| **Percentage Mixing** | Adjustable water/wastewater ratio |
| **17-Element Analysis** | Full water quality profile including EC and pH |
| **Automatic Deficit Calculation** | System subtracts water contribution from plant needs |
| **Interactive UI** | Dedicated section for water analysis input |

### 🧪 Algorithm Improvements

| Improvement | Description |
|-------------|-------------|
| **Water Contribution** | Weighted average of water and wastewater nutrients |
| **Deficit Calculation** | Remaining needs after water subtraction |
| **Validation** | Automatic validation of water analysis data |

### 🗄️ Database Updates

| Update | Description |
|--------|-------------|
| **DualTankRequest** | Added water_percent, wastewater_percent, water_analysis, wastewater_analysis fields |
| **Health Check** | Added water_analysis_support flag |

### 🎨 UI Updates

| Update | Description |
|--------|-------------|
| **Water Analysis Section** | Dedicated collapsible section with percentage inputs |
| **Water Analysis Tables** | Two tables for water and wastewater input |
| **Clean Results View** | Focused on essential data: doses, EC, pH, stock calculations |
| **Simplified Display** | Removed detailed mixing instructions and warnings from results |

---

## Seeding Database

### Quick Seed (All Data)

```bash
cd backend
python -c "from app.seed import init_db; init_db()"
```

### Seed Specific Companies

```bash
cd backend

# Seed only specific brands
python -c "from app.seed.run_seed import main; import sys; sys.argv = ['', '--companies', 'gol_sam', 'redsa']; main()"

# Available company options:
# - gol_sam     : گل سم گرگان
# - razak_shimi : رازاک شیمی (includes Green Star & Zagara Star)
# - atlas       : اطلس
# - redsa       : ردسا
# - all         : All companies (default)
```

### List Available Companies

```bash
cd backend
python -c "from app.seed.run_seed import main; import sys; sys.argv = ['', '--list']; main()"
```

### Reset Database (Delete All Data)

```bash
cd backend

# Option 1: Using Python
python -c "from app.database import Base, engine; Base.metadata.drop_all(bind=engine); print('✅ All tables dropped')"

# Option 2: Delete the file
rm farmtech.db        # Linux/macOS
del farmtech.db       # Windows

# Then re-seed
python -c "from app.seed import init_db; init_db()"
```

---

## Troubleshooting

### Error: "No module named 'scipy'"

```bash
pip install scipy==1.13.0
```

### Error: "No module named 'numpy'"

```bash
pip install numpy==1.26.0
```

### Error: Frontend can't connect to backend

1. Ensure backend is running: `http://localhost:8000/docs`
2. Check if port 8000 is blocked by firewall
3. Verify baseURL in `CalculatorView.vue` is `http://127.0.0.1:8000/api/v1`

### Error: Database issues

```bash
# Delete and recreate database
rm farmtech.db          # Linux/macOS
del farmtech.db         # Windows

# Re-initialize
python -c "from app.seed import init_db; init_db()"
```

### Error: Optimization doesn't converge

1. Add more fertilizers to the database
2. Widen dose bounds for existing fertilizers
3. Check solubility limits
4. Reduce custom nutrient needs

### Port already in use

```bash
# Change backend port (in run.py)
uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)

# Frontend will prompt automatically if 5173 is busy
```

---

## Development

### Adding a New Fertilizer

1. Edit appropriate seed file in `backend/app/seed/`
2. Add fertilizer data to the `fertilizers_data` list
3. Re-seed database:

```bash
cd backend
python -c "from app.seed import init_db; init_db()"
```

### Adding a New Brand

1. Add brand to `backend/app/seed/brands.py`
2. Create new seed file for the brand
3. Import and call in `backend/app/seed/__init__.py`

### Running Tests

```bash
# Comprehensive test
cd backend
python test_comprehensive.py
```

---

## Environment Variables

Create `.env` file in `backend/` folder:

```env
DATABASE_URL=sqlite:///./farmtech.db
DEBUG=True

# For PostgreSQL production:
# DATABASE_URL=postgresql://user:pass@localhost/farmtech
```

---

## Production Deployment

### Backend (using Gunicorn + Uvicorn)

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend (build for production)

```bash
cd frontend
npm run build
# Output in 'dist' folder - serve with nginx, caddy, or Vercel
```

---

## 📦 Supported Brands

| Brand (فارسی) | Brand (English) | Products |
|---------------|-----------------|----------|
| گل سم گرگان | Gol Sam Gorgan | Fertigol NPK, UniComplex |
| رازاک شیمی | Razak Shimi | Sulfates, Nitrates |
| گرین استار | Green Star | NPK Complete |
| زاگرا استار | Zagara Star | NPK, Humic Acid |
| اطلس | Atlas | Chelates (EDTA, EDDHA, Glycinate) |
| ردسا | Redsa | Micro, Macro, Bio, Stimulants |

---

## 📄 License

This project is private and not open source. All rights reserved.

---

**Built with 🌱 for sustainable agriculture**
```

---

## خلاصه تغییرات README:

| بخش | تغییر |
|------|--------|
| **Key Features > UI** | اضافه شدن `Clean Results` و `Simplified Display` |
| **Version 3.4.0 > UI Updates** | اضافه شدن `Clean Results View` و `Simplified Display` |
| **سایر بخش‌ها** | بدون تغییر |

---

**این فایل را کامیت کنید:**

```bash
git add README.md
git commit -m "docs: update README for v3.4.0 with clean results view"
git push origin mohsen-dev
```
