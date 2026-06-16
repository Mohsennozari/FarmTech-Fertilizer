# 🎯 FarmTech Core Algorithm & API Export

**Generated:** 2026-06-16 18:36:37
**Project:** FarmTech Fertilizer System v3.3.1
**Core Files:** 23

---

## 📑 Table of Contents

1. ✅ [`backend/app/main.py`](#file-1)
2. ✅ [`backend/app/models.py`](#file-2)
3. ✅ [`backend/app/routes.py`](#file-3)
4. ✅ [`backend/app/schemas.py`](#file-4)
5. ✅ [`backend/app/database.py`](#file-5)
6. ✅ [`backend/requirements.txt`](#file-6)
7. ✅ [`backend/run.py`](#file-7)
8. ✅ [`backend/app/calculator/__init__.py`](#file-8)
9. ✅ [`backend/app/calculator/core.py`](#file-9)
10. ✅ [`backend/app/calculator/dual_tank.py`](#file-10)
11. ✅ [`backend/app/calculator/ec.py`](#file-11)
12. ✅ [`backend/app/calculator/instructions.py`](#file-12)
13. ✅ [`backend/app/calculator/optimization.py`](#file-13)
14. ✅ [`backend/app/calculator/stock.py`](#file-14)
15. ✅ [`backend/app/calculator/tank.py`](#file-15)
16. ✅ [`frontend/src/views/CalculatorView.vue`](#file-16)
17. ✅ [`frontend/src/components/calculator/ResultsDisplay.vue`](#file-17)
18. ✅ [`frontend/src/components/common/InputField.vue`](#file-18)
19. ✅ [`frontend/src/components/common/ThemeToggle.vue`](#file-19)
20. ✅ [`frontend/src/App.vue`](#file-20)
21. ✅ [`frontend/src/main.ts`](#file-21)
22. ✅ [`frontend/src/style.css`](#file-22)
23. ✅ [`frontend/package.json`](#file-23)

---

## File 1: `backend/app/main.py`

**Size:** 1.6 KB

```python
# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
import logging

# تنظیم لاگینگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ایجاد اپلیکیشن FastAPI
app = FastAPI(
    title="FarmTech API",
    description="سیستم هوشمند نسخه‌دهی کود دیجیتال",
    version="3.3.1",
    docs_url="/docs",
    redoc_url="/redoc"
)

# تنظیم CORS برای ارتباط با فرانت‌اند
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# اضافه کردن router با prefix /api/v1
app.include_router(router)

# مسیر اصلی برای تست
@app.get("/")
def root():
    return {
        "message": "FarmTech API is running",
        "version": "3.3.1",
        "docs": "/docs",
        "api": "/api/v1"
    }

# مسیر سلامت ساده بدون prefix (برای تست سریع)
@app.get("/health")
def simple_health():
    return {"status": "ok", "server": "running"}

# رویداد استارتاپ
@app.on_event("startup")
async def startup_event():
    logger.info("FarmTech API Server Started Successfully")
    logger.info("API Documentation available at /docs")

# رویداد شات‌داون
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FarmTech API Server Shutting Down")
```

---

## File 2: `backend/app/models.py`

**Size:** 9.8 KB

```python
# Platform-v3\backend\app\models.py

from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, Table, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# ============================================================
# جدول واسط برای رابطه چند به چند (بدون تعریف کلاس جداگانه)
# ============================================================
growth_stage_fertilizer = Table(
    'growth_stage_fertilizer',
    Base.metadata,
    Column('growth_stage_id', Integer, ForeignKey('growth_stages.id'), primary_key=True),
    Column('fertilizer_id', Integer, ForeignKey('fertilizers.id'), primary_key=True)
)


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    country = Column(String, nullable=True)
    website = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    fertilizers = relationship("Fertilizer", back_populates="brand", lazy="select")


class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    scientific_name = Column(String, nullable=True)
    cultivation_type = Column(String, nullable=True)

    varieties = relationship("Variety", back_populates="crop", cascade="all, delete-orphan", lazy="select")
    growth_stages = relationship("GrowthStage", back_populates="crop", lazy="select")


class Variety(Base):
    __tablename__ = "varieties"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    growth_days = Column(Integer, nullable=True)
    yield_potential = Column(String, nullable=True)

    crop = relationship("Crop", back_populates="varieties", lazy="select")
    growth_stages = relationship("GrowthStage", back_populates="variety", lazy="select")


class Fertilizer(Base):
    __tablename__ = "fertilizers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=True)
    brand_name = Column(String, nullable=True)

    # اطلاعات پایه کود
    fertilizer_form = Column(String, default="powder")
    chemical_formula = Column(String, nullable=True)
    molecular_weight = Column(Float, nullable=True)
    purity_percent = Column(Float, default=100.0)
    fertilizer_type = Column(String, nullable=True)
    
    # کد ثبت و اطلاعات شناسایی
    registration_code = Column(String, nullable=True)
    product_code = Column(String, nullable=True)
    color = Column(String, nullable=True)
    
    # دوز مصرف
    max_dose_g_per_liter = Column(Float, nullable=True)
    max_dose_ml_per_liter = Column(Float, nullable=True)
    min_dose_g_per_liter = Column(Float, nullable=True, default=0.01)
    density_g_per_ml = Column(Float, nullable=True)
    
    # عناصر ماکرو (درصد)
    n_percent = Column(Float, default=0)
    p_percent = Column(Float, default=0)
    k_percent = Column(Float, default=0)
    ca_percent = Column(Float, default=0)
    mg_percent = Column(Float, default=0)
    s_percent = Column(Float, default=0)

    # عناصر میکرو (درصد)
    fe_percent = Column(Float, default=0)
    zn_percent = Column(Float, default=0)
    mn_percent = Column(Float, default=0)
    cu_percent = Column(Float, default=0)
    b_percent = Column(Float, default=0)
    mo_percent = Column(Float, default=0)
    cl_percent = Column(Float, default=0)

    # خواص فیزیکی و شیمیایی
    solubility_g_per_l = Column(Float, nullable=True)
    ph_effect = Column(String, nullable=True)
    
    # توضیحات و اطلاعات اضافی
    description = Column(Text, nullable=True)
    benefits = Column(Text, nullable=True)
    usage_instructions = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # وضعیت
    is_active = Column(Boolean, default=True)

    brand = relationship("Brand", back_populates="fertilizers", lazy="select")
    growth_stages = relationship("GrowthStage", secondary=growth_stage_fertilizer, back_populates="fertilizers", lazy="select")


class GrowthStage(Base):
    __tablename__ = "growth_stages"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    variety_id = Column(Integer, ForeignKey("varieties.id"), nullable=True)
    name = Column(String, nullable=False)
    stage_order = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    nutrient_needs = Column(JSON, nullable=True)
    target_ec_min = Column(Float, nullable=True)
    target_ec_max = Column(Float, nullable=True)
    target_ph_min = Column(Float, nullable=True)
    target_ph_max = Column(Float, nullable=True)
    priority = Column(String, nullable=True)

    crop = relationship("Crop", back_populates="growth_stages", lazy="select")
    variety = relationship("Variety", back_populates="growth_stages", lazy="select")
    fertilizers = relationship("Fertilizer", secondary=growth_stage_fertilizer, back_populates="growth_stages", lazy="select")


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    fertilizer_a_id = Column(Integer, ForeignKey("fertilizers.id"), nullable=False)
    fertilizer_b_id = Column(Integer, ForeignKey("fertilizers.id"), nullable=False)
    reaction_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    precipitate_product = Column(String, nullable=True)
    description = Column(Text, nullable=True)

    fertilizer_a = relationship("Fertilizer", foreign_keys=[fertilizer_a_id], lazy="select")
    fertilizer_b = relationship("Fertilizer", foreign_keys=[fertilizer_b_id], lazy="select")


class Acid(Base):
    __tablename__ = "acids"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    chemical_formula = Column(String, nullable=True)
    concentration_percent = Column(Float, nullable=False)
    density_g_per_ml = Column(Float, nullable=True)
    supplies_element = Column(String, nullable=True)
    element_percent = Column(Float, nullable=True)
    ml_per_1000L_per_ph_point = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)


class Tank(Base):
    __tablename__ = "tanks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tank_type = Column(String, default="main")
    volume_liters = Column(Float, nullable=False)
    water_ec_ms_cm = Column(Float, nullable=True)
    water_ph = Column(Float, nullable=True)
    water_ca_ppm = Column(Float, default=0)
    water_mg_ppm = Column(Float, default=0)
    water_na_ppm = Column(Float, default=0)
    water_cl_ppm = Column(Float, default=0)
    water_so4_ppm = Column(Float, default=0)
    water_hco3_ppm = Column(Float, default=0)
    water_no3_ppm = Column(Float, default=0)
    water_fe_ppm = Column(Float, default=0)
    notes = Column(Text, nullable=True)


class CalculationHistory(Base):
    __tablename__ = "calculation_history"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    crop_name = Column(String, nullable=False)
    variety_name = Column(String, nullable=False)
    stage_name = Column(String, nullable=False)
    brand_filter = Column(String, nullable=True)

    tank_main_name = Column(String, nullable=False)
    tank_main_volume_liters = Column(Float, nullable=False)
    tank_main_water_ec_ms_cm = Column(Float, nullable=True)
    tank_main_water_ph = Column(Float, nullable=True)
    tank_main_water_hco3_ppm = Column(Float, default=0)
    tank_main_water_ca_ppm = Column(Float, default=0)
    tank_main_water_mg_ppm = Column(Float, default=0)

    tank_calcium_name = Column(String, nullable=False)
    tank_calcium_volume_liters = Column(Float, nullable=False)
    tank_calcium_water_ec_ms_cm = Column(Float, nullable=True)
    tank_calcium_water_ph = Column(Float, nullable=True)
    tank_calcium_water_hco3_ppm = Column(Float, default=0)
    tank_calcium_water_ca_ppm = Column(Float, default=0)
    tank_calcium_water_mg_ppm = Column(Float, default=0)

    target_needs_ppm = Column(JSON, nullable=False)
    water_contribution_main_ppm = Column(JSON, nullable=False)
    water_contribution_calcium_ppm = Column(JSON, nullable=False)
    remaining_needs_main_ppm = Column(JSON, nullable=False)
    remaining_needs_calcium_ppm = Column(JSON, nullable=False)

    calculated_supply_main_ppm = Column(JSON, nullable=False)
    calculated_supply_calcium_ppm = Column(JSON, nullable=False)

    doses_main = Column(JSON, nullable=False)
    doses_calcium = Column(JSON, nullable=False)

    warnings_main = Column(JSON, nullable=False)
    warnings_calcium = Column(JSON, nullable=False)
    combined_warnings = Column(JSON, nullable=False)

    mixing_instructions_main = Column(Text, nullable=True)
    mixing_instructions_calcium = Column(Text, nullable=True)
    general_mixing_instructions = Column(Text, nullable=True)

    acid_adjustment_main = Column(JSON, nullable=True)
    acid_adjustment_calcium = Column(JSON, nullable=True)

    target_ec_min = Column(Float, nullable=True)
    target_ec_max = Column(Float, nullable=True)
    target_ph_min = Column(Float, nullable=True)
    target_ph_max = Column(Float, nullable=True)

    success = Column(Integer, default=1)
    error_message = Column(Text, nullable=True)
```

---

## File 3: `backend/app/routes.py`

**Size:** 24.2 KB

```python
# backend/app/routes.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional, Dict, Any
from datetime import datetime
import time

from app.database import get_db
from app import models, schemas
from app.calculator import (
    calculate_water_contribution,
    calculate_final_ec,
    get_ec_warning,
    optimize_fertilizer_doses_professional,
    calculate_tank_doses,
    generate_professional_mixing_instructions,
    separate_into_tanks,
    calculate_dual_tank_professional,
    calculate_dose_kg_for_stock,
    calculate_stock_consumption,
    get_injector_explanation,
    get_stock_mixing_instructions,
    get_stock_usage_instructions,
    get_storage_instructions,
    add_stock_calculations_to_doses
)

# ============================================================
# 🆕 Import جدید برای آنالیز آب و پساب ترکیبی (نسخه 3.4.0)
# ============================================================
from app.calculator.water_analysis import (
    calculate_complete_water_contribution,
    validate_water_percentages,
    get_water_analysis_keys,
    get_remaining_needs
)

import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["FarmTech API"])


# ============================================================
# Health Check
# ============================================================
@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": "3.4.0",
        "dual_tank_support": True,
        "stock_system": True,
        "custom_needs_support": True,
        "multi_brand_support": True,
        "water_analysis_support": True  # 🆕 نسخه 3.4.0
    }


# ============================================================
# Crops
# ============================================================
@router.get("/crops", response_model=List[schemas.CropResponse])
def get_crops(db: Session = Depends(get_db)):
    crops = db.query(models.Crop).all()
    return crops


@router.post("/crops", response_model=schemas.CropResponse)
def create_crop(crop: schemas.CropCreate, db: Session = Depends(get_db)):
    db_crop = models.Crop(**crop.dict())
    db.add(db_crop)
    db.commit()
    db.refresh(db_crop)
    return db_crop


# ============================================================
# Varieties
# ============================================================
@router.get("/varieties", response_model=List[schemas.VarietyResponse])
def get_varieties(crop_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(models.Variety)
    if crop_id:
        query = query.filter(models.Variety.crop_id == crop_id)
    return query.all()


@router.post("/varieties", response_model=schemas.VarietyResponse)
def create_variety(variety: schemas.VarietyCreate, db: Session = Depends(get_db)):
    db_variety = models.Variety(**variety.dict())
    db.add(db_variety)
    db.commit()
    db.refresh(db_variety)
    return db_variety


# ============================================================
# Growth Stages
# ============================================================
@router.get("/growth-stages", response_model=List[schemas.GrowthStageResponse])
def get_growth_stages(
    crop_id: Optional[int] = None,
    variety_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.GrowthStage)
    if crop_id:
        query = query.filter(models.GrowthStage.crop_id == crop_id)
    if variety_id:
        query = query.filter(models.GrowthStage.variety_id == variety_id)
    return query.order_by(models.GrowthStage.stage_order).all()


@router.post("/growth-stages", response_model=schemas.GrowthStageResponse)
def create_growth_stage(stage: schemas.GrowthStageCreate, db: Session = Depends(get_db)):
    db_stage = models.GrowthStage(**stage.dict())
    db.add(db_stage)
    db.commit()
    db.refresh(db_stage)
    return db_stage


# ============================================================
# Brands
# ============================================================
@router.get("/brands", response_model=List[schemas.BrandResponse])
def get_brands(db: Session = Depends(get_db)):
    return db.query(models.Brand).all()


@router.post("/brands", response_model=schemas.BrandResponse)
def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db)):
    db_brand = models.Brand(**brand.dict())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand


# ============================================================
# Fertilizers
# ============================================================
@router.get("/fertilizers", response_model=List[schemas.FertilizerResponse])
def get_fertilizers(
    brand_id: Optional[int] = None,
    fertilizer_type: Optional[str] = None,
    is_active: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    query = db.query(models.Fertilizer).filter(models.Fertilizer.is_active == is_active)
    if brand_id:
        query = query.filter(models.Fertilizer.brand_id == brand_id)
    if fertilizer_type:
        query = query.filter(models.Fertilizer.fertilizer_type == fertilizer_type)
    return query.all()


@router.post("/fertilizers", response_model=schemas.FertilizerResponse)
def create_fertilizer(fertilizer: schemas.FertilizerCreate, db: Session = Depends(get_db)):
    db_fertilizer = models.Fertilizer(**fertilizer.dict())
    db.add(db_fertilizer)
    db.commit()
    db.refresh(db_fertilizer)
    return db_fertilizer


# ============================================================
# Interactions
# ============================================================
@router.get("/interactions", response_model=List[schemas.InteractionResponse])
def get_interactions(db: Session = Depends(get_db)):
    return db.query(models.Interaction).all()


@router.post("/interactions", response_model=schemas.InteractionResponse)
def create_interaction(interaction: schemas.InteractionCreate, db: Session = Depends(get_db)):
    db_interaction = models.Interaction(**interaction.dict())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction


# ============================================================
# Acids
# ============================================================
@router.get("/acids", response_model=List[schemas.AcidResponse])
def get_acids(db: Session = Depends(get_db)):
    return db.query(models.Acid).all()


@router.post("/acids", response_model=schemas.AcidResponse)
def create_acid(acid: schemas.AcidCreate, db: Session = Depends(get_db)):
    db_acid = models.Acid(**acid.dict())
    db.add(db_acid)
    db.commit()
    db.refresh(db_acid)
    return db_acid


# ============================================================
# Tanks
# ============================================================
@router.get("/tanks", response_model=List[schemas.TankResponse])
def get_tanks(
    tank_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Tank)
    if tank_type:
        query = query.filter(models.Tank.tank_type == tank_type)
    return query.all()


@router.post("/tanks", response_model=schemas.TankResponse)
def create_tank(tank: schemas.TankCreate, db: Session = Depends(get_db)):
    db_tank = models.Tank(**tank.dict())
    db.add(db_tank)
    db.commit()
    db.refresh(db_tank)
    return db_tank


@router.get("/tanks/{tank_id}", response_model=schemas.TankResponse)
def get_tank(tank_id: int, db: Session = Depends(get_db)):
    tank = db.query(models.Tank).filter(models.Tank.id == tank_id).first()
    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")
    return tank


@router.put("/tanks/{tank_id}", response_model=schemas.TankResponse)
def update_tank(tank_id: int, tank: schemas.TankCreate, db: Session = Depends(get_db)):
    db_tank = db.query(models.Tank).filter(models.Tank.id == tank_id).first()
    if not db_tank:
        raise HTTPException(status_code=404, detail="Tank not found")

    for key, value in tank.dict().items():
        setattr(db_tank, key, value)

    db.commit()
    db.refresh(db_tank)
    return db_tank


@router.delete("/tanks/{tank_id}")
def delete_tank(tank_id: int, db: Session = Depends(get_db)):
    db_tank = db.query(models.Tank).filter(models.Tank.id == tank_id).first()
    if not db_tank:
        raise HTTPException(status_code=404, detail="Tank not found")

    db.delete(db_tank)
    db.commit()
    return {"message": "Tank deleted successfully"}


# ============================================================
# ============================================================
# محاسبه با دو مخزن (نسخه 3.4.0 با پشتیبانی از آنالیز آب و پساب)
# ============================================================
# ============================================================
@router.post("/calculate-dual-tank")
async def calculate_dual_tank(
    request: schemas.DualTankRequest,
    db: Session = Depends(get_db)
):
    """
    محاسبه دوز بهینه کودها برای دو مخزن جداگانه - نسخه 3.4.0

    قابلیت‌های جدید:
    - پشتیبانی از آنالیز آب و پساب ترکیبی (Water + Wastewater Analysis)
    - محاسبه تامینی آب و پساب با درصد دلخواه
    - کسر مقادیر تامینی از نیازهای گیاه
    - پشتیبانی از انتخاب چند برند همزمان (Multi Brand Filter)
    - پشتیبانی از نیازهای سفارشی کاربر (Custom Nutrient Needs)
    - محاسبه دقیق مقدار استوک (کیلوگرم) بر اساس نسبت تزریق

    مخزن اصلی (Main): برای کودهای غیر کلسیمی (NPK، سولفات‌ها، ریز مغذی‌ها)
    مخزن کلسیم (Calcium): برای کودهای حاوی کلسیم (نیترات کلسیم، کلات آهن)
    """
    start_time = time.time()

    try:
        # ============================================================
        # مرحله 1: دریافت اطلاعات اولیه
        # ============================================================

        growth_stage = db.query(models.GrowthStage).join(models.Crop).join(models.Variety).filter(
            models.Crop.name == request.crop_name,
            models.Variety.name == request.variety_name,
            models.GrowthStage.name == request.stage_name
        ).first()

        if not growth_stage:
            return {
                "success": False,
                "error_message": f"مرحله رشدی '{request.stage_name}' برای محصول '{request.crop_name}' و رقم '{request.variety_name}' یافت نشد"
            }

        # ============================================================
        # 🆕 مرحله 2: محاسبه تامینی آب و پساب (نسخه 3.4.0)
        # ============================================================

        water_analysis_result = calculate_complete_water_contribution(
            water_percent=request.water_percent,
            wastewater_percent=request.wastewater_percent,
            water_analysis=request.water_analysis,
            wastewater_analysis=request.wastewater_analysis,
            target_needs={}  # موقتاً خالی، بعداً پر می‌شود
        )

        # بررسی خطاهای آنالیز آب
        if not water_analysis_result["success"]:
            return {
                "success": False,
                "error_message": "خطا در آنالیز آب و پساب",
                "details": water_analysis_result["errors"]
            }

        combined_water = water_analysis_result["combined_water"]

        # ============================================================
        # مرحله 3: تعیین نیازهای گیاه (اولویت با سفارشی کاربر)
        # ============================================================

        if request.custom_nutrient_needs and len(request.custom_nutrient_needs) > 0:
            plant_needs = request.custom_nutrient_needs
            logger.info(f"Using custom nutrient needs: {plant_needs}")
            needs_source = "custom"
        else:
            plant_needs = growth_stage.nutrient_needs or {}
            logger.info(f"Using default nutrient needs from database: {plant_needs}")
            needs_source = "database"

        # ============================================================
        # 🆕 مرحله 4: محاسبه نیاز باقیمانده پس از کسر آب و پساب
        # ============================================================

        # محاسبه کمبود عناصر با در نظر گرفتن آب و پساب
        remaining_needs = get_remaining_needs(plant_needs, combined_water)

        # استفاده از remaining_needs به جای plant_needs برای محاسبه کود
        # (آب و پساب قبلاً از نیازها کسر شده‌اند)
        adjusted_needs = remaining_needs

        logger.info(f"Original needs: {plant_needs}")
        logger.info(f"Combined water contribution: {combined_water}")
        logger.info(f"Remaining needs after water: {remaining_needs}")

        # ============================================================
        # مرحله 5: فیلتر برند (Multi Brand Filter - پشتیبانی از لیست)
        # ============================================================

        query = db.query(models.Fertilizer).filter(models.Fertilizer.is_active == True)

        if request.brand_filter and len(request.brand_filter) > 0:
            query = query.filter(models.Fertilizer.brand_name.in_(request.brand_filter))
            logger.info(f"Filtering brands: {request.brand_filter}")
            brand_filter_str = ",".join(request.brand_filter)
        else:
            brand_filter_str = None

        all_fertilizers = query.all()

        if not all_fertilizers:
            return {
                "success": False,
                "error_message": "هیچ کود فعالی در دیتابیس یافت نشد"
            }

        # ============================================================
        # مرحله 6: انجام محاسبات حرفه‌ای دو مخزن (با نیازهای تعدیل شده)
        # ============================================================

        result_main, result_calcium, combined_warnings, general_instructions = calculate_dual_tank_professional(
            remaining_needs=adjusted_needs,  # استفاده از نیازهای باقیمانده
            all_fertilizers=all_fertilizers,
            tank_main=request.tank_main,
            tank_calcium=request.tank_calcium,
            brand_filter=brand_filter_str
        )

        # ============================================================
        # مرحله 7: اضافه کردن محاسبات استوک به دوزها
        # ============================================================

        if result_main.get("doses"):
            result_main["doses"] = add_stock_calculations_to_doses(
                doses=result_main["doses"],
                tank_volume_liters=request.tank_main.volume_liters,
                injector_ratio=request.injector_ratio,
                stock_tank_volume_liters=request.stock_tank_volume_liters
            )

        if result_calcium.get("doses"):
            result_calcium["doses"] = add_stock_calculations_to_doses(
                doses=result_calcium["doses"],
                tank_volume_liters=request.tank_calcium.volume_liters,
                injector_ratio=request.injector_ratio,
                stock_tank_volume_liters=request.stock_tank_volume_liters
            )

        # ============================================================
        # مرحله 8: محاسبه مصرف استوک
        # ============================================================

        stock_liters_for_main_tank, stock_ml_per_liter = calculate_stock_consumption(
            injector_ratio=request.injector_ratio,
            main_tank_volume_liters=request.tank_main.volume_liters
        )

        stock_liters_for_calcium_tank, stock_ml_per_liter_calcium = calculate_stock_consumption(
            injector_ratio=request.injector_ratio,
            main_tank_volume_liters=request.tank_calcium.volume_liters
        )

        # ============================================================
        # مرحله 9: ساخت دستورالعمل‌ها
        # ============================================================

        injector_explanation = get_injector_explanation(request.injector_ratio)
        usage_instructions = get_stock_usage_instructions(request.injector_ratio)
        storage_instructions, shelf_life_fridge, shelf_life_room, warning_signs = get_storage_instructions()

        main_fertilizer_names = [d.get("name", "") for d in result_main.get("doses", [])]
        main_mixing_instructions = get_stock_mixing_instructions(main_fertilizer_names)

        calcium_fertilizer_names = [d.get("name", "") for d in result_calcium.get("doses", [])]
        calcium_mixing_instructions = get_stock_mixing_instructions(calcium_fertilizer_names)

        # ============================================================
        # مرحله 10: آماده‌سازی پاسخ
        # ============================================================

        calculation_time = (time.time() - start_time) * 1000

        warnings_main_list = [w.get('message', str(w)) for w in result_main.get('warnings', [])]
        warnings_calcium_list = [w.get('message', str(w)) for w in result_calcium.get('warnings', [])]
        combined_warnings_list = [w.get('message', str(w)) for w in combined_warnings]

        return {
            "success": True,
            "crop_name": request.crop_name,
            "variety_name": request.variety_name,
            "stage_name": request.stage_name,
            "target_needs": growth_stage.nutrient_needs or {},
            "custom_needs": plant_needs if needs_source == "custom" else None,
            "needs_source": needs_source,

            # 🆕 اطلاعات آب و پساب ترکیبی (نسخه 3.4.0)
            "water_analysis": {
                "water_percent": request.water_percent,
                "wastewater_percent": request.wastewater_percent,
                "combined_water": combined_water,
                "deficit": water_analysis_result["deficit"],
                "remaining_needs": adjusted_needs
            },

            "tank_main_result": {
                "tank_name": request.tank_main.name,
                "tank_type": "main",
                "tank_volume_liters": request.tank_main.volume_liters,
                "doses": result_main.get("doses", []),
                "water_contribution_ppm": result_main.get("water_contribution", {}),
                "remaining_needs_ppm": result_main.get("remaining_needs", {}),
                "supplied_ppm": result_main.get("supplied_ppm", {}),
                "warnings": warnings_main_list,
                "mixing_instructions": result_main.get("mixing_instructions", ""),
                "target_ec": result_main.get("ec_predicted"),
                "target_ph": growth_stage.target_ph_max,
                "stock_instructions": {
                    "stock_tank_volume_liters": request.stock_tank_volume_liters,
                    "injector_ratio": request.injector_ratio,
                    "injector_explanation": injector_explanation,
                    "mixing_instructions": main_mixing_instructions,
                    "stock_liters_for_tank": stock_liters_for_main_tank,
                    "stock_ml_per_liter": stock_ml_per_liter,
                    "usage_instructions": usage_instructions
                }
            },
            "tank_calcium_result": {
                "tank_name": request.tank_calcium.name,
                "tank_type": "calcium",
                "tank_volume_liters": request.tank_calcium.volume_liters,
                "doses": result_calcium.get("doses", []),
                "water_contribution_ppm": result_calcium.get("water_contribution", {}),
                "remaining_needs_ppm": result_calcium.get("remaining_needs", {}),
                "supplied_ppm": result_calcium.get("supplied_ppm", {}),
                "warnings": warnings_calcium_list,
                "mixing_instructions": result_calcium.get("mixing_instructions", ""),
                "target_ec": result_calcium.get("ec_predicted"),
                "target_ph": growth_stage.target_ph_min,
                "stock_instructions": {
                    "stock_tank_volume_liters": request.stock_tank_volume_liters,
                    "injector_ratio": request.injector_ratio,
                    "injector_explanation": injector_explanation,
                    "mixing_instructions": calcium_mixing_instructions,
                    "stock_liters_for_tank": stock_liters_for_calcium_tank,
                    "stock_ml_per_liter": stock_ml_per_liter_calcium,
                    "usage_instructions": usage_instructions
                }
            },
            "combined_warnings": combined_warnings_list,
            "general_mixing_instructions": general_instructions,
            "storage_instructions": storage_instructions,
            "shelf_life_fridge": shelf_life_fridge,
            "shelf_life_room": shelf_life_room,
            "warning_signs": warning_signs,
            "calculation_time_ms": calculation_time,
            "error_message": None
        }

    except Exception as e:
        logger.error(f"Dual tank calculation error: {str(e)}")
        return {
            "success": False,
            "error_message": str(e)
        }


# ============================================================
# History
# ============================================================
@router.get("/history", response_model=List[schemas.HistoryResponse])
def get_history(limit: int = 50, db: Session = Depends(get_db)):
    history = db.query(models.CalculationHistory).order_by(
        desc(models.CalculationHistory.created_at)
    ).limit(limit).all()
    return history


@router.get("/history/{history_id}", response_model=schemas.HistoryResponse)
def get_history_item(history_id: int, db: Session = Depends(get_db)):
    history = db.query(models.CalculationHistory).filter(
        models.CalculationHistory.id == history_id
    ).first()
    if not history:
        raise HTTPException(status_code=404, detail="History item not found")
    return history


@router.delete("/history/{history_id}")
def delete_history_item(history_id: int, db: Session = Depends(get_db)):
    history = db.query(models.CalculationHistory).filter(
        models.CalculationHistory.id == history_id
    ).first()
    if not history:
        raise HTTPException(status_code=404, detail="History item not found")

    db.delete(history)
    db.commit()
    return {"message": "History item deleted successfully"}


# ============================================================
# ذخیره محاسبه در تاریخچه
# ============================================================
@router.post("/save-calculation")
def save_calculation(
    calculation_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """ذخیره یک محاسبه در تاریخچه"""
    try:
        history = models.CalculationHistory(
            crop_name=calculation_data.get("crop_name"),
            variety_name=calculation_data.get("variety_name"),
            stage_name=calculation_data.get("stage_name"),
            tank_name=calculation_data.get("tank_name"),
            tank_volume_liters=calculation_data.get("tank_volume_liters"),
            result_summary=calculation_data.get("result_summary", {})
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return {"success": True, "id": history.id}
    except Exception as e:
        logger.error(f"Save calculation error: {str(e)}")
        return {"success": False, "error": str(e)}

```

---

## File 4: `backend/app/schemas.py`

**Size:** 23.5 KB

```python
# backend/app/schemas.py

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============================================================
# Tank Schemas
# ============================================================
class TankBase(BaseModel):
    name: str
    volume_liters: float = Field(..., gt=0, description="حجم مخزن به لیتر")
    water_ec_ms_cm: Optional[float] = Field(0.4, ge=0, le=10, description="EC آب به میلی‌زیمنس بر سانتی‌متر - بازه ایده‌آل: 0.2-0.8")
    water_ph: Optional[float] = Field(7.0, ge=0, le=14, description="pH آب - بازه ایده‌آل: 6.0-7.0")
    water_ca_ppm: float = Field(50, ge=0, description="کلسیم آب به ppm - بازه ایده‌آل: 40-80")
    water_mg_ppm: float = Field(20, ge=0, description="منیزیم آب به ppm - بازه ایده‌آل: 15-30")
    water_hco3_ppm: float = Field(0, ge=0, description="بیکربنات آب به ppm - بازه ایده‌آل: 0-100")
    water_cl_ppm: float = Field(0, ge=0, description="کلر آب به ppm - بازه ایده‌آل: 0-50")
    water_na_ppm: float = Field(0, ge=0, description="سدیم آب به ppm")
    water_so4_ppm: float = Field(0, ge=0, description="سولفات آب به ppm")
    water_no3_ppm: float = Field(0, ge=0, description="نیترات آب به ppm")
    water_fe_ppm: float = Field(0, ge=0, description="آهن آب به ppm")


class TankCreate(TankBase):
    pass


class TankResponse(TankBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============================================================
# Calculation Request Schemas
# ============================================================
class CalculationRequest(BaseModel):
    """درخواست محاسبه ترکیب کود - نسخه 3.3.0 با پشتیبانی از استوک"""

    # اطلاعات محصول و مرحله رشد
    crop_name: str = Field(..., description="نام محصول (مثال: توت‌فرنگی)")
    variety_name: str = Field(..., description="نام رقم (مثال: سن اندرسا)")
    stage_name: str = Field(..., description="مرحله رشد (مثال: رشد رویشی)")

    # فیلتر برند (اختیاری)
    brand_filter: Optional[str] = Field(None, description="فیلتر برند کود (اختیاری)")

    # اطلاعات مخزن اصلی (تغذیه گیاهان)
    tank: TankCreate = Field(..., description="اطلاعات مخزن اصلی")

    # ============================================================
    # فیلدهای جدید نسخه 3.3.0 - سیستم مدیریت استوک
    # ============================================================

    # حجم مخزن استوک (ظرفی که کود در آن حل می‌شود)
    stock_tank_volume_liters: float = Field(
        20.0,
        ge=1.0,
        le=500.0,
        description="حجم مخزن استوک به لیتر (ظرفی که محلول مادر در آن ساخته می‌شود) - پیش‌فرض 20 لیتر"
    )

    # نسبت تزریق (Injector Ratio) - فرمت 1:X
    injector_ratio: float = Field(
        200.0,
        ge=50,
        le=1000,
        description="نسبت تزریق 1:X - مثلاً 200 یعنی 1 لیتر استوک + 199 لیتر آب = 200 لیتر محلول نهایی"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "crop_name": "توت‌فرنگی",
                "variety_name": "سن اندرسا",
                "stage_name": "رشد رویشی",
                "brand_filter": None,
                "tank": {
                    "name": "مخزن A",
                    "volume_liters": 1000,
                    "water_ec_ms_cm": 0.4,
                    "water_ph": 7.0,
                    "water_ca_ppm": 50,
                    "water_mg_ppm": 20
                },
                "stock_tank_volume_liters": 20,
                "injector_ratio": 200
            }
        }

    @validator('injector_ratio')
    def validate_injector_ratio(cls, v):
        """اعتبارسنجی نسبت تزریق - باید بین 50 تا 1000 باشد"""
        if v < 50:
            raise ValueError(f"نسبت تزریق نمی‌تواند کمتر از 50 باشد. مقدار وارد شده: {v}")
        if v > 1000:
            raise ValueError(f"نسبت تزریق نمی‌تواند بیشتر از 1000 باشد. مقدار وارد شده: {v}")
        return v

    @validator('stock_tank_volume_liters')
    def validate_stock_tank_volume(cls, v):
        """اعتبارسنجی حجم مخزن استوک - باید بین 1 تا 500 لیتر باشد"""
        if v < 1:
            raise ValueError(f"حجم مخزن استوک نمی‌تواند کمتر از 1 لیتر باشد. مقدار وارد شده: {v}")
        if v > 500:
            raise ValueError(f"حجم مخزن استوک نمی‌تواند بیشتر از 500 لیتر باشد. مقدار وارد شده: {v}")
        return v


# ============================================================
# Calculation Response Schemas
# ============================================================
class FertilizerDose(BaseModel):
    """مقدار مصرف هر کود"""
    name: str = Field(..., description="نام کود")
    dose_g_per_liter: float = Field(..., description="دوز مصرف به گرم در لیتر (محلول نهایی)")
    dose_g_for_tank: float = Field(..., description="دوز مصرف کل برای مخزن اصلی به گرم")

    # ============================================================
    # فیلدهای جدید نسخه 3.3.0 - سیستم مدیریت استوک
    # ============================================================
    dose_kg_for_stock: float = Field(
        ...,
        description="مقدار کود مورد نیاز برای ساخت استوک (کیلوگرم) - بر اساس حجم مخزن استوک و نسبت تزریق"
    )
    dose_g_for_stock_alternative: Optional[float] = Field(
        None,
        description="مقدار کود به گرم برای استوک‌های کوچک (کمتر از 1 کیلوگرم)"
    )


class StockInstructions(BaseModel):
    """دستورالعمل ساخت و مصرف استوک - نسخه 3.3.0"""

    # تنظیمات کاربر
    stock_tank_volume_liters: float = Field(..., description="حجم مخزن استوک به لیتر")
    injector_ratio: float = Field(..., description="نسبت تزریق 1:X")
    main_tank_volume_liters: float = Field(..., description="حجم مخزن اصلی به لیتر")

    # توضیح مفهوم نسبت تزریق
    injector_explanation: str = Field(..., description="توضیح ساده نسبت تزریق برای کاربر")

    # دستورالعمل ساخت استوک
    fertilizers_for_stock: List[Dict[str, Any]] = Field(..., description="لیست کودها با مقدار کیلوگرم برای استوک")
    mixing_instructions: str = Field(..., description="روش ساخت استوک گام به گام")

    # دستورالعمل مصرف استوک
    stock_liters_for_main_tank: float = Field(..., description="مقدار استوک بر حسب لیتر برای کل مخزن اصلی")
    stock_ml_per_liter: float = Field(..., description="مقدار استوک بر حسب میلی‌لیتر برای هر لیتر آب")
    usage_instructions: str = Field(..., description="روش مصرف استوک در مخزن اصلی")

    # نکات نگهداری
    storage_instructions: str = Field(..., description="نکات نگهداری و ایمنی استوک")
    shelf_life_fridge: str = Field(..., description="ماندگاری در یخچال")
    shelf_life_room: str = Field(..., description="ماندگاری در دمای محیط")
    warning_signs: str = Field(..., description="نشانه‌های خرابی استوک")


class NutrientComparison(BaseModel):
    """مقایسه عناصر مورد نیاز با عناصر تامین شده"""
    element: str
    required_ppm: float
    supplied_ppm: float
    difference_ppm: float
    status: str


class CalculationResponse(BaseModel):
    """پاسخ نهایی محاسبه - نسخه 3.3.0 با ساختار چهاربخشی"""

    success: bool = Field(..., description="موفقیت آمیز بودن محاسبه")
    message: Optional[str] = Field(None, description="پیام خطا در صورت ناموفق بودن")

    crop_name: str = Field(..., description="نام محصول")
    variety_name: str = Field(..., description="نام رقم")
    stage_name: str = Field(..., description="مرحله رشد")

    tank_name: str = Field(..., description="نام مخزن اصلی")
    tank_volume_liters: float = Field(..., description="حجم مخزن اصلی به لیتر")

    doses: List[FertilizerDose] = Field(..., description="لیست دوز کودها")
    stock_instructions: StockInstructions = Field(..., description="دستورالعمل کامل ساخت و مصرف استوک")

    warnings: List[str] = Field(default_factory=list, description="لیست هشدارها")
    interactions: List[Dict[str, str]] = Field(default_factory=list, description="لیست تداخلات شیمیایی")

    nutrient_comparison: Optional[List[NutrientComparison]] = Field(None, description="مقایسه عناصر")

    # ============================================================
    # فیلدهای جدید نسخه 3.3.1 - نیازهای سفارشی کاربر
    # ============================================================
    custom_needs: Optional[Dict[str, float]] = Field(None, description="نیازهای سفارشی وارد شده توسط کاربر")

    target_ec: Optional[float] = Field(None, description="EC هدف")
    target_ph: Optional[float] = Field(None, description="pH هدف")
    calculation_time: datetime = Field(default_factory=datetime.now, description="زمان محاسبه")


# ============================================================
# Create Schemas (برای دریافت داده از فرانت‌اند)
# ============================================================

class CropCreate(BaseModel):
    name: str
    scientific_name: Optional[str] = None
    cultivation_type: Optional[str] = None


class VarietyCreate(BaseModel):
    crop_id: int
    name: str
    description: Optional[str] = None
    growth_days: Optional[int] = None
    yield_potential: Optional[str] = None


class GrowthStageCreate(BaseModel):
    crop_id: int
    variety_id: Optional[int] = None
    name: str
    stage_order: int
    description: Optional[str] = None
    nutrient_needs: Optional[Dict[str, float]] = None
    target_ec_min: Optional[float] = None
    target_ec_max: Optional[float] = None
    target_ph_min: Optional[float] = None
    target_ph_max: Optional[float] = None
    priority: Optional[str] = None


class BrandCreate(BaseModel):
    name: str
    country: Optional[str] = None
    website: Optional[str] = None
    notes: Optional[str] = None


class FertilizerCreate(BaseModel):
    name: str
    brand_id: int
    brand_name: str
    fertilizer_type: str
    chemical_formula: Optional[str] = None
    registration_code: Optional[str] = None
    description: Optional[str] = None
    purity_percent: Optional[float] = 100
    max_dose_g_per_liter: Optional[float] = 3.0
    min_dose_g_per_liter: Optional[float] = 0.1
    n_percent: Optional[float] = None
    p_percent: Optional[float] = None
    k_percent: Optional[float] = None
    ca_percent: Optional[float] = None
    mg_percent: Optional[float] = None
    s_percent: Optional[float] = None
    fe_percent: Optional[float] = None
    zn_percent: Optional[float] = None
    mn_percent: Optional[float] = None
    cu_percent: Optional[float] = None
    b_percent: Optional[float] = None
    mo_percent: Optional[float] = None
    cl_percent: Optional[float] = None
    solubility_g_per_l: Optional[float] = None
    ph_effect: Optional[str] = None
    is_active: bool = True


class InteractionCreate(BaseModel):
    fertilizer_a_id: int
    fertilizer_b_id: int
    reaction_type: str
    severity: str
    precipitate_product: Optional[str] = None
    description: str


class AcidCreate(BaseModel):
    name: str
    chemical_formula: Optional[str] = None
    concentration_percent: Optional[float] = None
    density_g_per_ml: Optional[float] = None
    supplies_element: Optional[str] = None
    element_percent: Optional[float] = None
    ml_per_1000L_per_ph_point: Optional[float] = None
    notes: Optional[str] = None


# ============================================================
# ============================================================
# 🆕 DualTankRequest با پشتیبانی از آنالیز آب و پساب ترکیبی
# ============================================================
# ============================================================
class DualTankRequest(BaseModel):
    """درخواست محاسبه دو مخزن - نسخه 3.4.0 با پشتیبانی از آنالیز آب و پساب ترکیبی"""

    # اطلاعات محصول و مرحله رشد
    crop_name: str = Field(..., description="نام محصول (مثال: توت‌فرنگی)")
    variety_name: str = Field(..., description="نام رقم (مثال: سن اندرسا)")
    stage_name: str = Field(..., description="مرحله رشد (مثال: رشد رویشی)")

    # فیلتر برند (چندگانه)
    brand_filter: Optional[List[str]] = Field(None, description="لیست برندهای انتخاب شده - در صورت خالی بودن یعنی همه برندها")

    # اطلاعات مخازن
    tank_main: TankCreate = Field(..., description="اطلاعات مخزن اصلی (کودهای غیر کلسیمی)")
    tank_calcium: TankCreate = Field(..., description="اطلاعات مخزن کلسیم (کودهای حاوی کلسیم)")

    # تنظیمات سیستم استوک
    stock_tank_volume_liters: float = Field(20.0, ge=1.0, le=500.0, description="حجم مخزن استوک به لیتر - پیش‌فرض 20 لیتر")
    injector_ratio: float = Field(200.0, ge=50, le=1000, description="نسبت تزریق 1:X - پیش‌فرض 200")

    # نیازهای سفارشی کاربر
    custom_nutrient_needs: Optional[Dict[str, float]] = Field(None, description="نیازهای تغذیه‌ای سفارشی وارد شده توسط کاربر")

    # ============================================================
    # 🆕 فیلدهای جدید برای آنالیز آب و پساب ترکیبی (نسخه 3.4.0)
    # ============================================================
    water_percent: float = Field(
        80.0,
        ge=0,
        le=100,
        description="درصد آب تامینی (مثلاً 80% آب و 20% پساب)"
    )
    wastewater_percent: float = Field(
        20.0,
        ge=0,
        le=100,
        description="درصد پساب تامینی (مثلاً 20%)"
    )

    # آنالیز آب (14 عنصر + EC + pH)
    water_analysis: Dict[str, float] = Field(
        default_factory=dict,
        description="آنالیز آب شامل عناصر (N-NO3, P, S, N-NH4, K, Ca, Fe, Mn, Zn, B, Cu, Mo) و EC و pH"
    )

    # آنالیز پساب (14 عنصر + EC + pH)
    wastewater_analysis: Dict[str, float] = Field(
        default_factory=dict,
        description="آنالیز پساب شامل عناصر (N-NO3, P, S, N-NH4, K, Ca, Fe, Mn, Zn, B, Cu, Mo) و EC و pH"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "crop_name": "توت‌فرنگی",
                "variety_name": "سن اندرسا",
                "stage_name": "رشد رویشی",
                "brand_filter": ["گل سم گرگان", "ردسا"],
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
                "custom_nutrient_needs": {
                    "N": 120,
                    "P": 50,
                    "K": 120,
                    "Ca": 105,
                    "Mg": 40,
                    "Fe": 3
                },
                "water_percent": 80,
                "wastewater_percent": 20,
                "water_analysis": {
                    "n_no3": 10,
                    "p": 2,
                    "s": 5,
                    "n_nh4": 0,
                    "k": 8,
                    "ca": 50,
                    "fe": 0.5,
                    "mn": 0.1,
                    "zn": 0.05,
                    "b": 0.2,
                    "cu": 0.02,
                    "mo": 0.01,
                    "ec": 0.4,
                    "ph": 7.0
                },
                "wastewater_analysis": {
                    "n_no3": 25,
                    "p": 5,
                    "s": 10,
                    "n_nh4": 2,
                    "k": 15,
                    "ca": 80,
                    "fe": 1.0,
                    "mn": 0.3,
                    "zn": 0.1,
                    "b": 0.5,
                    "cu": 0.05,
                    "mo": 0.02,
                    "ec": 1.2,
                    "ph": 6.5
                }
            }
        }

    @validator('water_percent', 'wastewater_percent')
    def validate_percentages(cls, v, values):
        """اعتبارسنجی درصدها - مجموع باید 100 باشد"""
        if 'water_percent' in values and 'wastewater_percent' in values:
            total = values['water_percent'] + values['wastewater_percent']
            if abs(total - 100) > 0.01:
                raise ValueError(f"مجموع درصد آب و پساب باید 100 باشد. مقدار فعلی: {total}")
        return v

    @validator('injector_ratio')
    def validate_injector_ratio(cls, v):
        if v < 50:
            raise ValueError(f"نسبت تزریق نمی‌تواند کمتر از 50 باشد. مقدار وارد شده: {v}")
        if v > 1000:
            raise ValueError(f"نسبت تزریق نمی‌تواند بیشتر از 1000 باشد. مقدار وارد شده: {v}")
        return v

    @validator('stock_tank_volume_liters')
    def validate_stock_tank_volume(cls, v):
        if v < 1:
            raise ValueError(f"حجم مخزن استوک نمی‌تواند کمتر از 1 لیتر باشد. مقدار وارد شده: {v}")
        if v > 500:
            raise ValueError(f"حجم مخزن استوک نمی‌تواند بیشتر از 500 لیتر باشد. مقدار وارد شده: {v}")
        return v


# ============================================================
# Response Schemas
# ============================================================

class CropResponse(BaseModel):
    id: int
    name: str
    scientific_name: Optional[str] = None
    cultivation_type: Optional[str] = None

    class Config:
        from_attributes = True


class VarietyResponse(BaseModel):
    id: int
    crop_id: int
    name: str
    description: Optional[str] = None
    growth_days: Optional[int] = None
    yield_potential: Optional[str] = None

    class Config:
        from_attributes = True


class GrowthStageResponse(BaseModel):
    id: int
    crop_id: int
    variety_id: Optional[int] = None
    name: str
    stage_order: int
    description: Optional[str] = None
    nutrient_needs: Optional[Dict[str, float]] = None
    target_ec_min: Optional[float] = None
    target_ec_max: Optional[float] = None
    target_ph_min: Optional[float] = None
    target_ph_max: Optional[float] = None
    priority: Optional[str] = None

    class Config:
        from_attributes = True


class BrandResponse(BaseModel):
    id: int
    name: str
    country: Optional[str] = None
    website: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class FertilizerResponse(BaseModel):
    id: int
    brand_id: int
    brand_name: str
    name: str
    fertilizer_type: str
    chemical_formula: Optional[str] = None
    registration_code: Optional[str] = None
    description: Optional[str] = None
    n_percent: Optional[float] = None
    p_percent: Optional[float] = None
    k_percent: Optional[float] = None
    ca_percent: Optional[float] = None
    mg_percent: Optional[float] = None
    s_percent: Optional[float] = None
    fe_percent: Optional[float] = None
    zn_percent: Optional[float] = None
    mn_percent: Optional[float] = None
    cu_percent: Optional[float] = None
    b_percent: Optional[float] = None
    mo_percent: Optional[float] = None
    cl_percent: Optional[float] = None
    max_dose_g_per_liter: Optional[float] = None
    min_dose_g_per_liter: Optional[float] = None
    solubility_g_per_l: Optional[float] = None
    ph_effect: Optional[str] = None
    is_active: bool = True

    class Config:
        from_attributes = True


class InteractionResponse(BaseModel):
    id: int
    fertilizer_a_id: int
    fertilizer_b_id: int
    fertilizer_a_name: Optional[str] = None
    fertilizer_b_name: Optional[str] = None
    reaction_type: str
    severity: str
    precipitate_product: Optional[str] = None
    description: str

    class Config:
        from_attributes = True


class AcidResponse(BaseModel):
    id: int
    name: str
    chemical_formula: Optional[str] = None
    concentration_percent: Optional[float] = None
    density_g_per_ml: Optional[float] = None
    supplies_element: Optional[str] = None
    element_percent: Optional[float] = None
    ml_per_1000L_per_ph_point: Optional[float] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class HistoryResponse(BaseModel):
    id: int
    calculation_date: datetime
    crop_name: str
    variety_name: str
    stage_name: str
    tank_name: str
    tank_volume_liters: float
    result_summary: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


# ============================================================
# Reset Database Schema
# ============================================================

class ResetRequest(BaseModel):
    confirm: bool = Field(..., description="تأیید برای ریست دیتابیس")
    password: Optional[str] = Field(None, description="رمز عبور برای ریست (در صورت نیاز)")


class ResetResponse(BaseModel):
    success: bool
    message: str
    tables_dropped: Optional[List[str]] = None
    tables_created: Optional[List[str]] = None

```

---

## File 5: `backend/app/database.py`

**Size:** 634 B

```python
# Platform-v3\backend\app\database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

connect_args = {}
if "sqlite" in settings.DATABASE_URL:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## File 6: `backend/requirements.txt`

**Size:** 134 B

```text
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.35
pydantic==2.9.0
python-dotenv==1.0.0
numpy==1.26.0
scipy==1.13.0

```

---

## File 7: `backend/run.py`

**Size:** 555 B

```python
# Platform-v3\backend\run.py

import uvicorn

if __name__ == "__main__":
    print("=" * 50)
    print("FarmTech API Server")
    print("=" * 50)
    print("\nStarting server...")
    print("API Documentation: http://127.0.0.1:8000/docs")
    print("Swagger UI: http://127.0.0.1:8000/docs")
    print("ReDoc: http://127.0.0.1:8000/redoc")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    print()
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
```

---

## File 9: `backend/app/calculator/core.py`

**Size:** 2.5 KB

```python
# backend/app/calculator/core.py

from typing import List, Dict, Tuple, Optional

SUPPORTED_ELEMENTS = ['N', ' P', 'K', 'Ca', 'Mg', 'S', 'Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']


def calculate_element_ppm(fertilizer, dose_g_per_liter: float) -> Dict[str, float]:
    purity = (fertilizer.purity_percent or 100) / 100.0
    factor = 10 * purity

    return {
        'N': (fertilizer.n_percent or 0) * dose_g_per_liter * factor,
        'P': (fertilizer.p_percent or 0) * dose_g_per_liter * factor,
        'K': (fertilizer.k_percent or 0) * dose_g_per_liter * factor,
        'Ca': (fertilizer.ca_percent or 0) * dose_g_per_liter * factor,
        'Mg': (fertilizer.mg_percent or 0) * dose_g_per_liter * factor,
        'S': (fertilizer.s_percent or 0) * dose_g_per_liter * factor,
        'Fe': (fertilizer.fe_percent or 0) * dose_g_per_liter * factor,
        'Zn': (fertilizer.zn_percent or 0) * dose_g_per_liter * factor,
        'Mn': (fertilizer.mn_percent or 0) * dose_g_per_liter * factor,
        'Cu': (fertilizer.cu_percent or 0) * dose_g_per_liter * factor,
        'B': (fertilizer.b_percent or 0) * dose_g_per_liter * factor,
        'Mo': (fertilizer.mo_percent or 0) * dose_g_per_liter * factor,
        'Cl': (fertilizer.cl_percent or 0) * dose_g_per_liter * factor,
    }


def calculate_water_contribution(tank) -> Dict[str, float]:
    if not tank:
        return {elem: 0.0 for elem in SUPPORTED_ELEMENTS}

    return {
        'N': tank.water_no3_ppm or 0,
        'P': 0,
        'K': 0,
        'Ca': tank.water_ca_ppm or 0,
        'Mg': tank.water_mg_ppm or 0,
        'S': tank.water_so4_ppm or 0,
        'Fe': tank.water_fe_ppm or 0,
        'Zn': 0,
        'Mn': 0,
        'Cu': 0,
        'B': 0,
        'Mo': 0,
        'Cl': tank.water_cl_ppm or 0,
    }


def calculate_acid_contribution(acid, dose_ml_per_liter: float) -> Dict[str, float]:
    if not acid or not acid.supplies_element:
        return {elem: 0.0 for elem in SUPPORTED_ELEMENTS}

    density = acid.density_g_per_ml or 1.0
    acid_concentration = acid.concentration_percent / 100.0
    element_percent = (acid.element_percent or 0) / 100.0

    ppm = acid_concentration * element_percent * dose_ml_per_liter * density * 1000

    result = {elem: 0.0 for elem in SUPPORTED_ELEMENTS}
    if acid.supplies_element == 'P':
        result['P'] = ppm
    elif acid.supplies_element == 'N':
        result['N'] = ppm
    elif acid.supplies_element == 'S':
        result['S'] = ppm

    return result
```

---

## File 10: `backend/app/calculator/dual_tank.py`

**Size:** 28.1 KB

```python
from typing import List, Dict, Tuple, Optional
import copy
from .core import calculate_water_contribution
from .ec import calculate_final_ec
from .optimization import optimize_fertilizer_doses_professional
from .tank import calculate_tank_doses
from .instructions import generate_persian_mixing_instructions, generate_persian_general_instructions


# ============================================================
# ماتریس تداخلات شیمیایی (مرحله 3)
# ============================================================

# گروه‌بندی کودها بر اساس خطر تداخل
FERTILIZER_GROUPS = {
    "calcium": ["calcium nitrate", "نیترات کلسیم", "calcium chloride", "کلرید کلسیم"],
    "sulfate": ["magnesium sulfate", "سولفات منیزیم", "potassium sulfate", "سولفات پتاسیم", "ammonium sulfate", "سولفات آمونیوم"],
    "phosphate": ["mkp", "monopotassium phosphate", "مونو پتاسیم فسفات", "map", "ammonium phosphate", "فسفات آمونیوم", "dap"],
    "iron_chelate": ["fe edta", "fe eddha", "iron chelate", "کلات آهن", "fe chelate"],
    "micro": ["zinc sulfate", "سولفات روی", "manganese sulfate", "سولفات منگنز", "copper sulfate", "سولفات مس"]
}

# ماتریس ناسازگاری: (group1, group2) -> (severity, warning_message)
INCOMPATIBILITY_MATRIX = {
    ("calcium", "sulfate"): {
        "severity": "high",
        "message": "⚠️ خطر رسوب گچ (کلسیم سولفات)! این دو گروه هرگز نباید در یک مخزن مخلوط شوند.",
        "reaction": "Ca²⁺ + SO₄²⁻ → CaSO₄ ↓ (رسوب سفید)",
        "prevention": "حتماً در مخازن جداگانه نگهداری شوند."
    },
    ("calcium", "phosphate"): {
        "severity": "critical",
        "message": "🚨 خطر رسوب کلسیم فسفات! این ترکیب لوله‌ها و قطره‌چکان‌ها را مسدود می‌کند.",
        "reaction": "3Ca²⁺ + 2PO₄³⁻ → Ca₃(PO₄)₂ ↓ (رسوب نامحلول)",
        "prevention": "هرگز در یک مخزن مخلوط نشوند. حتماً در مخازن A و B جداگانه."
    },
    ("iron_chelate", "phosphate"): {
        "severity": "medium",
        "message": "⚠️ کلات آهن با فسفات تداخل دارد. ممکن است آهن رسوب کند.",
        "reaction": "Fe-EDTA + PO₄³⁻ → FePO₄ ↓ + EDTA",
        "prevention": "بهتر است در مخازن جداگانه نگهداری شوند."
    },
    ("iron_chelate", "sulfate"): {
        "severity": "low",
        "message": "⚠️ کلات آهن با سولفات‌ها تداخل متوسطی دارد.",
        "reaction": "احتمال رسوب جزئی آهن",
        "prevention": "قابل قبول در یک مخزن، اما pH را کنترل کنید."
    },
    ("calcium", "micro"): {
        "severity": "medium",
        "message": "⚠️ کلسیم با برخی ریز مغذی‌ها (روی، منگنز، مس) تداخل دارد.",
        "reaction": "احتمال رسوب هیدروکسیدهای فلزی",
        "prevention": "ریز مغذی‌ها بهتر است در مخزن اصلی (B) باشند."
    }
}


# ============================================================
# مرحله 4: ضریب پویای تقسیم نیتروژن
# ============================================================

# جدول ضرایب تقسیم نیتروژن بین مخزن کلسیم و اصلی
# بر اساس نوع گیاه و مرحله رشد
NITROGEN_SPLIT_RATIOS = {
    # گیاهان گلخانه‌ای رایج
    "tomato": {
        "vegetative": 0.45,      # مرحله رویشی: نیاز N بالا
        "flowering": 0.35,       # مرحله گلدهی: نیاز N متوسط
        "fruiting": 0.30,        # مرحله میوه‌دهی: نیاز N کمتر
        "ripening": 0.25         # مرحله رسیدگی: نیاز N کم
    },
    "cucumber": {
        "vegetative": 0.50,
        "flowering": 0.40,
        "fruiting": 0.35,
        "ripening": 0.30
    },
    "pepper": {
        "vegetative": 0.45,
        "flowering": 0.38,
        "fruiting": 0.32,
        "ripening": 0.28
    },
    "strawberry": {
        "vegetative": 0.40,
        "flowering": 0.35,
        "fruiting": 0.30,
        "ripening": 0.25
    },
    "lettuce": {
        "vegetative": 0.55,       # کاهو همیشه نیاز N بالایی دارد
        "harvest": 0.50
    },
    "eggplant": {
        "vegetative": 0.45,
        "flowering": 0.38,
        "fruiting": 0.32,
        "ripening": 0.28
    },
    "bean": {
        "vegetative": 0.35,       # لوبیا N کمتری نیاز دارد (تثبیت نیتروژن)
        "flowering": 0.30,
        "fruiting": 0.25
    },
    # گیاهان زینتی
    "rose": {
        "vegetative": 0.50,
        "flowering": 0.40,
        "dormant": 0.30
    },
    "gerbera": {
        "vegetative": 0.45,
        "flowering": 0.38,
        "dormant": 0.30
    },
    # پیش‌فرض برای گیاهان دیگر
    "default": {
        "vegetative": 0.40,
        "flowering": 0.35,
        "fruiting": 0.30,
        "ripening": 0.25,
        "default": 0.35
    }
}

# مترادف‌های نام گیاهان برای تطابق بهتر
CROP_SYNONYMS = {
    "tomato": ["tomato", "گوجه", "گوجه فرنگی", "گوجه‌فرنگی", "solanum lycopersicum"],
    "cucumber": ["cucumber", "خیار", "cucumis sativus"],
    "pepper": ["pepper", "فلفل", "capsicum", "فلفل دلمه‌ای"],
    "strawberry": ["strawberry", "توت فرنگی", "توت‌فرنگی", "fragaria"],
    "lettuce": ["lettuce", "کاهو", "lactuca sativa"],
    "eggplant": ["eggplant", "بادمجان", "aubergine", "solanum melongena"],
    "bean": ["bean", "لوبیا", "phaseolus"],
    "rose": ["rose", "رز", "گل رز", "rosa"],
    "gerbera": ["gerbera", "ژربرا", "gerbera jamesonii"]
}


def get_fertilizer_group(fertilizer) -> str:
    """
    تشخیص گروه یک کود بر اساس نام و ترکیبات

    Returns:
        نام گروه (calcium, sulfate, phosphate, iron_chelate, micro, unknown)
    """
    if not fertilizer:
        return "unknown"

    fert_name = (fertilizer.name or "").lower()
    fert_type = (fertilizer.fertilizer_type or "").lower()

    # بررسی کلسیم
    if (fertilizer.ca_percent or 0) > 0:
        return "calcium"
    if any(keyword in fert_name for keyword in FERTILIZER_GROUPS["calcium"]):
        return "calcium"

    # بررسی فسفات
    if (fertilizer.p_percent or 0) > 0 and (fertilizer.ca_percent or 0) == 0:
        if any(keyword in fert_name for keyword in FERTILIZER_GROUPS["phosphate"]):
            return "phosphate"
        if fert_type in ["phosphate", "pk"]:
            return "phosphate"

    # بررسی سولفات
    if (fertilizer.s_percent or 0) > 0 and (fertilizer.ca_percent or 0) == 0:
        if any(keyword in fert_name for keyword in FERTILIZER_GROUPS["sulfate"]):
            return "sulfate"
        if "sulfate" in fert_name or "سولفات" in fert_name:
            return "sulfate"

    # بررسی کلات آهن
    if (fertilizer.fe_percent or 0) > 0:
        if any(keyword in fert_name for keyword in FERTILIZER_GROUPS["iron_chelate"]):
            return "iron_chelate"
        if "chelate" in fert_name or "کلات" in fert_name:
            return "iron_chelate"

    # بررسی ریز مغذی‌ها
    micro_elements = ['zn', 'mn', 'cu', 'b', 'mo']
    for elem in micro_elements:
        if getattr(fertilizer, f"{elem}_percent", 0) > 0:
            return "micro"

    return "unknown"


def check_incompatibility(fertilizers: List) -> List[Dict]:
    """
    بررسی تداخلات شیمیایی بین لیستی از کودها

    Args:
        fertilizers: لیست کودها (هر کود شامل object یا id)

    Returns:
        لیستی از هشدارهای تداخل
    """
    warnings = []

    # گرفتن گروه هر کود
    groups = []
    for fert in fertilizers:
        group = get_fertilizer_group(fert)
        groups.append({
            "fertilizer": fert,
            "name": fert.name,
            "group": group
        })

    # بررسی جفت‌های ناسازگار
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            group1 = groups[i]["group"]
            group2 = groups[j]["group"]

            # بررسی هر دو جهت
            key = (group1, group2)
            if key in INCOMPATIBILITY_MATRIX:
                incompat = INCOMPATIBILITY_MATRIX[key]
                warnings.append({
                    "type": "incompatibility",
                    "severity": incompat["severity"],
                    "fertilizer1": groups[i]["name"],
                    "fertilizer2": groups[j]["name"],
                    "message": incompat["message"],
                    "reaction": incompat.get("reaction", ""),
                    "prevention": incompat.get("prevention", "")
                })

            # بررسی جهت معکوس
            key_rev = (group2, group1)
            if key_rev in INCOMPATIBILITY_MATRIX:
                incompat = INCOMPATIBILITY_MATRIX[key_rev]
                warnings.append({
                    "type": "incompatibility",
                    "severity": incompat["severity"],
                    "fertilizer1": groups[j]["name"],
                    "fertilizer2": groups[i]["name"],
                    "message": incompat["message"],
                    "reaction": incompat.get("reaction", ""),
                    "prevention": incompat.get("prevention", "")
                })

    # حذف هشدارهای تکراری
    unique_warnings = []
    seen = set()
    for warn in warnings:
        key = f"{warn['fertilizer1']}_{warn['fertilizer2']}"
        if key not in seen:
            seen.add(key)
            unique_warnings.append(warn)

    return unique_warnings


def get_crop_type(crop_name: str) -> str:
    """
    تشخیص نوع گیاه از روی نام وارد شده

    Args:
        crop_name: نام گیاه (می‌تواند فارسی یا انگلیسی باشد)

    Returns:
        کلید استاندارد گیاه (مثل tomato, cucumber, ...)
    """
    if not crop_name:
        return "default"

    crop_lower = crop_name.lower().strip()

    for standard_name, synonyms in CROP_SYNONYMS.items():
        if crop_lower in synonyms or any(syn in crop_lower for syn in synonyms):
            return standard_name

    return "default"


def get_growth_stage(stage_name: str) -> str:
    """
    تشخیص مرحله رشد از روی نام وارد شده

    Args:
        stage_name: نام مرحله رشد

    Returns:
        کلید استاندارد مرحله (vegetative, flowering, fruiting, ripening, dormant, harvest)
    """
    if not stage_name:
        return "default"

    stage_lower = stage_name.lower().strip()

    # نگاشت مراحل مختلف به کلیدهای استاندارد
    stage_mapping = {
        "vegetative": ["vegetative", "رویشی", "رشد رویشی", "vegetation", "growth"],
        "flowering": ["flowering", "گلدهی", "شکوفه", "bloom", "flower"],
        "fruiting": ["fruiting", "میوه‌دهی", "تشکیل میوه", "fruit", "fruit set"],
        "ripening": ["ripening", "رسیدگی", "رسیدن", "ripe", "maturation"],
        "dormant": ["dormant", "خواب", "استراحت", "dormancy"],
        "harvest": ["harvest", "برداشت", "harvesting", "ready"]
    }

    for standard_stage, synonyms in stage_mapping.items():
        if stage_lower in synonyms or any(syn in stage_lower for syn in synonyms):
            return standard_stage

    return "default"


def get_nitrogen_split_ratio(crop_type: str = None, growth_stage: str = None) -> float:
    """
    محاسبه ضریب تقسیم نیتروژن بر اساس نوع گیاه و مرحله رشد

    Args:
        crop_type: نوع گیاه (مثال: tomato, cucumber, گوجه, خیار)
        growth_stage: مرحله رشد (مثال: vegetative, flowering, رویشی, گلدهی)

    Returns:
        ضریب تقسیم نیتروژن (بین 0.2 تا 0.6)
    """
    # تشخیص نوع گیاه
    crop_key = get_crop_type(crop_type) if crop_type else "default"

    # تشخیص مرحله رشد
    stage_key = get_growth_stage(growth_stage) if growth_stage else "default"

    # دریافت ضرایب برای این گیاه
    crop_ratios = NITROGEN_SPLIT_RATIOS.get(crop_key, NITROGEN_SPLIT_RATIOS["default"])

    # دریافت ضریب برای این مرحله
    ratio = crop_ratios.get(stage_key, crop_ratios.get("default", 0.35))

    # محدودیت منطقی (بین 0.2 و 0.6)
    ratio = max(0.20, min(0.60, ratio))

    return ratio


def get_split_ratio_explanation(crop_type: str = None, growth_stage: str = None) -> str:
    """
    تولید توضیح برای ضریب تقسیم نیتروژن انتخاب شده
    """
    ratio = get_nitrogen_split_ratio(crop_type, growth_stage)

    crop_display = crop_type if crop_type else "نامشخص"
    stage_display = growth_stage if growth_stage else "نامشخص"

    explanation = f"""📊 ضریب تقسیم نیتروژن: {ratio:.0%}

🧫 بر اساس:
   • نوع گیاه: {crop_display}
   • مرحله رشد: {stage_display}

📌 معنی این ضریب:
   {ratio:.0%} از نیتروژن مورد نیاز گیاه توسط مخزن کلسیم (نیترات کلسیم) تأمین می‌شود.
   بقیه نیتروژن ({1-ratio:.0%}) توسط مخزن اصلی (کودهای NPK) تأمین می‌شود.

💡 نکته: این تقسیم‌بندی از رسوب کلسیم با سولفات و فسفات جلوگیری می‌کند."""

    return explanation


def separate_into_tanks_professional(doses: List[Dict]) -> List[Dict]:
    """
    تفکیک کودها به دو مخزن بر اساس استاندارد جهانی هیدروپونیک
    با در نظر گرفتن تداخلات شیمیایی
    """

    tank_a = {
        "name": "🧪 مخزن A - کلسیم",
        "type": "calcium",
        "description": "⚠️ این مخزن حاوی کلسیم است. هرگز با مخزن B مخلوط نشود!",
        "doses": []
    }

    tank_b = {
        "name": "🧪 مخزن B - اصلی",
        "type": "main",
        "description": "حاوی NPK، منیزیم، سولفات و ریز مغذی‌ها",
        "doses": []
    }

    # کلمات کلیدی برای شناسایی کودهای کلسیمی
    calcium_keywords = [
        'calcium', 'کلسیم', 'نیترات کلسیم', 'calcium nitrate',
        'iron', 'آهن', 'chelate', 'کلات', 'fe'
    ]

    incompatibility_warnings = []

    for dose in doses:
        name_lower = dose['name'].lower()
        fert_type = dose.get('fertilizer_type', '').lower() if 'fertilizer_type' in dose else ''

        # تشخیص کود کلسیمی یا آهنی
        is_calcium = (
            'calcium' in name_lower or
            'کلسیم' in name_lower or
            fert_type == 'calcium' or
            (('iron' in name_lower or 'آهن' in name_lower) and 'chelate' in name_lower)
        )

        if is_calcium:
            dose['caution'] = "⚠️ فقط در مخزن کلسیم استفاده شود"
            tank_a["doses"].append(dose)
        else:
            tank_b["doses"].append(dose)

    # بررسی تداخلات شیمیایی در مخازن
    if tank_a["doses"]:
        class DummyFertilizer:
            def __init__(self, name, ca_percent=0, p_percent=0, s_percent=0, fe_percent=0):
                self.name = name
                self.ca_percent = ca_percent
                self.p_percent = p_percent
                self.s_percent = s_percent
                self.fe_percent = fe_percent

        tank_a_ferts = []
        for dose in tank_a["doses"]:
            ca = 19 if 'calcium' in dose['name'].lower() or 'کلسیم' in dose['name'] else 0
            fert = DummyFertilizer(dose['name'], ca_percent=ca)
            tank_a_ferts.append(fert)

        a_warnings = check_incompatibility(tank_a_ferts)
        for warn in a_warnings:
            warn["tank"] = "A (کلسیم)"
            incompatibility_warnings.append(warn)

    if tank_b["doses"]:
        class DummyFertilizer:
            def __init__(self, name, ca_percent=0, p_percent=0, s_percent=0, fe_percent=0):
                self.name = name
                self.ca_percent = ca_percent
                self.p_percent = p_percent
                self.s_percent = s_percent
                self.fe_percent = fe_percent

        tank_b_ferts = []
        for dose in tank_b["doses"]:
            name_lower = dose['name'].lower()
            p = 20 if 'npk' in name_lower or 'phosphate' in name_lower else 0
            s = 13 if 'sulfate' in name_lower or 'سولفات' in name_lower else 0
            fe = 6 if 'iron' in name_lower or 'آهن' in name_lower else 0
            fert = DummyFertilizer(dose['name'], p_percent=p, s_percent=s, fe_percent=fe)
            tank_b_ferts.append(fert)

        b_warnings = check_incompatibility(tank_b_ferts)
        for warn in b_warnings:
            warn["tank"] = "B (اصلی)"
            incompatibility_warnings.append(warn)

    # اضافه کردن هشدارهای تداخل به توضیحات مخازن
    critical_warnings = [w for w in incompatibility_warnings if w.get('severity') == 'critical']
    high_warnings = [w for w in incompatibility_warnings if w.get('severity') == 'high']

    if critical_warnings:
        tank_b["description"] += "\n\n🚨 هشدار بحرانی - تداخل شیمیایی:\n"
        for warn in critical_warnings:
            tank_b["description"] += f"   • {warn['message']}\n"

    if high_warnings:
        tank_a["description"] += "\n\n⚠️ هشدار مهم - تداخل شیمیایی:\n"
        for warn in high_warnings:
            tank_a["description"] += f"   • {warn['message']}\n"

    # اضافه کردن هشدارهای قبلی برای دوز بالا
    if tank_a["doses"]:
        total_dose_a = sum(d['dose_g_per_liter'] for d in tank_a["doses"])
        if total_dose_a > 2.0:
            tank_a["description"] += f"\n⚠️ هشدار: مجموع دوز ({total_dose_a} g/L) بالاست. احتمال رسوب را بررسی کنید."

    if tank_b["doses"]:
        total_dose_b = sum(d['dose_g_per_liter'] for d in tank_b["doses"])
        if total_dose_b > 3.5:
            tank_b["description"] += f"\n⚠️ هشدار: مجموع دوز ({total_dose_b} g/L) نزدیک به حد مجاز است."

    result = []
    if tank_a["doses"]:
        result.append(tank_a)
    if tank_b["doses"]:
        result.append(tank_b)

    return result


def separate_into_tanks(doses: List[Dict]) -> List[Dict]:
    """تفکیک کودها به دو مخزن (نسخه قبلی برای سازگاری)"""
    return separate_into_tanks_professional(doses)


def calculate_dual_tank_professional(
    remaining_needs: Dict[str, float],
    all_fertilizers: List,
    tank_main,
    tank_calcium,
    brand_filter: Optional[str] = None,
    max_total_dose: float = 5.0,
    crop_type: Optional[str] = None,        # پارامتر جدید مرحله 4
    growth_stage: Optional[str] = None      # پارامتر جدید مرحله 4
) -> Tuple[Dict, Dict, List[Dict], str]:
    """
    محاسبه دوز بهینه برای دو مخزن با استفاده از الگوریتم لایه‌به‌لایه حرفه‌ای
    با در نظر گرفتن تداخلات شیمیایی و ضریب پویای تقسیم نیتروژن
    """

    if brand_filter:
        all_fertilizers = [f for f in all_fertilizers if f.brand_name == brand_filter]

    if not all_fertilizers:
        empty_result = {
            "doses": [],
            "supplied_ppm": {},
            "warnings": [{"type": "error", "severity": "error", "message": "هیچ کودی یافت نشد"}],
            "mixing_instructions": "",
            "ec_predicted": 0
        }
        return empty_result, empty_result, [], ""

    # ============================================================
    # محاسبه ضریب پویای تقسیم نیتروژن (مرحله 4)
    # ============================================================

    nitrogen_split_ratio = get_nitrogen_split_ratio(crop_type, growth_stage)
    split_explanation = get_split_ratio_explanation(crop_type, growth_stage)

    # ============================================================
    # تفکیک هوشمند کودها با در نظر گرفتن تداخلات
    # ============================================================

    fertilizers_for_calcium = []
    fertilizers_for_main = []

    calcium_keywords = [
        'calcium', 'کلسیم', 'نیترات کلسیم', 'calcium nitrate',
        'iron', 'آهن', 'chelate', 'کلات', 'fe chelate', 'iron chelate'
    ]

    incompatibility_warnings = []

    for fert in all_fertilizers:
        name_lower = (fert.name or "").lower()
        fert_type = (fert.fertilizer_type or "").lower()

        is_calcium_fertilizer = (
            (fert.ca_percent or 0) > 0 or
            any(keyword in name_lower for keyword in calcium_keywords) or
            fert_type == 'calcium'
        )

        if is_calcium_fertilizer:
            fertilizers_for_calcium.append(fert)
        else:
            fertilizers_for_main.append(fert)

    # بررسی تداخلات در مخازن
    if fertilizers_for_calcium:
        ca_warnings = check_incompatibility(fertilizers_for_calcium)
        for warn in ca_warnings:
            warn["tank"] = "مخزن کلسیم"
            incompatibility_warnings.append(warn)

    if fertilizers_for_main:
        main_warnings = check_incompatibility(fertilizers_for_main)
        for warn in main_warnings:
            warn["tank"] = "مخزن اصلی"
            incompatibility_warnings.append(warn)

    # تقسیم نیازها با ضریب پویا
    water_calcium = calculate_water_contribution(tank_calcium)
    water_main = calculate_water_contribution(tank_main)

    # استفاده از ضریب پویا به جای 35% ثابت
    needs_calcium = {
        'Ca': max(0, remaining_needs.get('Ca', 0) - water_calcium.get('Ca', 0)),
        'Fe': max(0, remaining_needs.get('Fe', 0) - water_calcium.get('Fe', 0)),
        'N': max(0, remaining_needs.get('N', 0) * nitrogen_split_ratio),
    }

    needs_main = copy.deepcopy(remaining_needs)
    needs_main['Ca'] = max(0, remaining_needs.get('Ca', 0) - water_main.get('Ca', 0) - needs_calcium.get('Ca', 0))
    needs_main['Fe'] = max(0, remaining_needs.get('Fe', 0) - water_main.get('Fe', 0) - needs_calcium.get('Fe', 0))
    needs_main['N'] = max(0, remaining_needs.get('N', 0) - needs_calcium.get('N', 0))

    # محاسبه مخزن کلسیم
    doses_calcium_raw, supply_calcium, warnings_calcium = optimize_fertilizer_doses_professional(
        remaining_needs=needs_calcium,
        fertilizers=fertilizers_for_calcium,
        brand_filter=brand_filter,
        max_total_dose=3.0
    )

    doses_calcium = calculate_tank_doses(doses_calcium_raw, tank_calcium.volume_liters)
    ec_calcium = calculate_final_ec(tank_calcium.water_ec_ms_cm or 0, doses_calcium)

    # اضافه کردن توضیح ضریب تقسیم به هشدارها
    warnings_calcium.append({
        "type": "nitrogen_split_info",
        "severity": "info",
        "message": split_explanation
    })

    # اضافه کردن هشدارهای تداخل
    for warn in incompatibility_warnings:
        if warn.get("tank") == "مخزن کلسیم":
            warnings_calcium.append({
                "type": "incompatibility",
                "severity": warn.get("severity", "warning"),
                "message": f"{warn.get('message', '')} (کود: {warn.get('fertilizer1', '')} و {warn.get('fertilizer2', '')})"
            })

    mixing_calcium = generate_persian_mixing_instructions(
        tank_name="مخزن کلسیم",
        tank_type="calcium",
        doses=doses_calcium,
        tank_volume=tank_calcium.volume_liters,
        target_ph_min=6.0,
        target_ph_max=6.5,
        warnings=warnings_calcium
    )

    # محاسبه مخزن اصلی
    doses_main_raw, supply_main, warnings_main = optimize_fertilizer_doses_professional(
        remaining_needs=needs_main,
        fertilizers=fertilizers_for_main,
        brand_filter=brand_filter,
        max_total_dose=4.0
    )

    doses_main = calculate_tank_doses(doses_main_raw, tank_main.volume_liters)
    ec_main = calculate_final_ec(tank_main.water_ec_ms_cm or 0, doses_main)

    # اضافه کردن هشدارهای تداخل به warnings_main
    for warn in incompatibility_warnings:
        if warn.get("tank") == "مخزن اصلی":
            warnings_main.append({
                "type": "incompatibility",
                "severity": warn.get("severity", "warning"),
                "message": f"{warn.get('message', '')} (کود: {warn.get('fertilizer1', '')} و {warn.get('fertilizer2', '')})"
            })

    mixing_main = generate_persian_mixing_instructions(
        tank_name="مخزن اصلی",
        tank_type="main",
        doses=doses_main,
        tank_volume=tank_main.volume_liters,
        target_ph_min=5.5,
        target_ph_max=6.2,
        warnings=warnings_main
    )

    # جمع‌آوری هشدارها
    combined_warnings = []
    combined_warnings.extend(warnings_calcium)
    combined_warnings.extend(warnings_main)

    # اضافه کردن هشدارهای تداخل بحرانی
    critical_incompat = [w for w in incompatibility_warnings if w.get('severity') == 'critical']
    for warn in critical_incompat:
        combined_warnings.append({
            "type": "critical_incompatibility",
            "severity": "error",
            "message": f"🚨 {warn.get('message', '')} در {warn.get('tank', 'مخزن')}",
            "reaction": warn.get('reaction', ''),
            "prevention": warn.get('prevention', '')
        })

    if not fertilizers_for_calcium:
        combined_warnings.append({
            "type": "missing_calcium_fertilizers",
            "severity": "error",
            "message": "⚠️ هیچ کود کلسیمی در سیستم یافت نشد! لطفاً نیترات کلسیم یا کودهای حاوی کلسیم اضافه کنید."
        })

    if not fertilizers_for_main:
        combined_warnings.append({
            "type": "missing_main_fertilizers",
            "severity": "error",
            "message": "⚠️ هیچ کود اصلی (غیر کلسیمی) در سیستم یافت نشد!"
        })

    # دستورالعمل کلی
    general_instructions = generate_persian_general_instructions(
        tank_main_volume=tank_main.volume_liters,
        tank_calcium_volume=tank_calcium.volume_liters,
        ec_main=ec_main,
        ec_calcium=ec_calcium,
        warnings=combined_warnings
    )

    result_main = {
        "doses": doses_main,
        "supplied_ppm": supply_main,
        "warnings": warnings_main,
        "mixing_instructions": mixing_main,
        "ec_predicted": ec_main,
        "water_contribution": water_main,
        "nitrogen_split_ratio": nitrogen_split_ratio
    }

    result_calcium = {
        "doses": doses_calcium,
        "supplied_ppm": supply_calcium,
        "warnings": warnings_calcium,
        "mixing_instructions": mixing_calcium,
        "ec_predicted": ec_calcium,
        "water_contribution": water_calcium,
        "nitrogen_split_ratio": nitrogen_split_ratio
    }

    return result_main, result_calcium, combined_warnings, general_instructions

```

---

## File 11: `backend/app/calculator/ec.py`

**Size:** 1.5 KB

```python
# backend/app/calculator/ec.py

from typing import List, Dict, Optional

EC_COEFFICIENTS = {
    "فرتی‌گل 36-12-12": 0.70,
    "فرتی‌گل 20-20-20": 0.70,
    "فرتی‌گل 30-5-15": 0.68,
    "فرتی‌گل 10-50-10": 0.65,
    "NPK 20-20-20 گرین استار": 0.70,
    "NPK 12-12-36 گرین استار": 0.68,
    "NPK 10-52-10 زاگرا استار": 0.65,
    "نیترات کلسیم": 0.95,
    "سولفات پتاسیم": 0.80,
    "سولفات منیزیم": 0.75,
    "کلرید پتاسیم": 0.85,
    "یونی کمپلکس پودری": 0.40,
    "default": 0.65
}


def calculate_final_ec(water_ec: float, doses: List[Dict]) -> float:
    total_ec = water_ec or 0.0
    for dose in doses:
        coeff = EC_COEFFICIENTS.get(dose["name"], EC_COEFFICIENTS["default"])
        total_ec += dose["dose_g_per_liter"] * coeff
    return round(total_ec, 2)


def get_ec_warning(predicted_ec: float, target_ec_min: float, target_ec_max: float) -> Optional[str]:
    if target_ec_min is None or target_ec_max is None:
        return None
    if predicted_ec > target_ec_max:
        return f"⚠️ EC پیش‌بینی ({predicted_ec} mS/cm) بالاتر از حد مجاز ({target_ec_max} mS/cm) است. محلول را با آب شیرین رقیق کنید."
    elif predicted_ec < target_ec_min:
        return f"⚠️ EC پیش‌بینی ({predicted_ec} mS/cm) پایین‌تر از حد مجاز ({target_ec_min} mS/cm) است. دوز کودها را افزایش دهید."
    return None
```

---

## File 12: `backend/app/calculator/instructions.py`

**Size:** 8.5 KB

```python
# backend/app/calculator/instructions.py

from typing import List, Dict


def generate_professional_mixing_instructions(doses: List[Dict], warnings: List[Dict], tank_volume: float) -> str:
    """تولید دستورالعمل اختلاط به زبان انگلیسی"""
    instructions = []

    instructions.append("=" * 50)
    instructions.append("Mixing Instructions")
    instructions.append("=" * 50)
    instructions.append("")
    instructions.append(f"Tank Volume: {tank_volume} liters")
    instructions.append("")
    instructions.append("Steps:")
    instructions.append("")
    instructions.append("1. Fill the tank to 70% with clean water")
    instructions.append("")
    instructions.append("2. Add fertilizers in this order:")

    for i, dose in enumerate(doses, 1):
        instructions.append(f"   {i}. {dose['name']}: {dose['dose_g_per_liter']} g/L")
        instructions.append(f"      Total for tank: {dose['dose_g_for_tank']} g")

    instructions.append("")
    instructions.append("3. After adding each fertilizer, mix well for 2 minutes")
    instructions.append("")
    instructions.append("4. Fill to final volume and mix for 5 more minutes")
    instructions.append("")
    instructions.append("5. Measure and adjust EC and pH")
    instructions.append("")
    instructions.append("=" * 50)
    instructions.append("Stock Solution Instructions (200x)")
    instructions.append("=" * 50)
    instructions.append("")

    for dose in doses:
        instructions.append(f"   {dose['name']}: {dose['stock_200x_g_per_liter']} g per 1 liter water")

    instructions.append("")
    instructions.append("Usage: Add 5 ml of stock solution per 1 liter of final water")
    instructions.append("")
    instructions.append("=" * 50)

    if warnings:
        instructions.append("")
        instructions.append("Warnings:")
        seen = set()
        for warn in warnings:
            msg = warn.get('description', warn.get('message', ''))
            if msg not in seen:
                instructions.append(f"   - {msg}")
                seen.add(msg)

    return "\n".join(instructions)


def generate_persian_mixing_instructions(
    tank_name: str,
    tank_type: str,
    doses: List[Dict],
    tank_volume: float,
    target_ph_min: float,
    target_ph_max: float,
    warnings: List[Dict]
) -> str:
    """تولید دستورالعمل اختلاط به زبان فارسی"""
    
    instructions = []
    
    instructions.append("=" * 60)
    instructions.append(f"📋 دستورالعمل ساخت {tank_name}")
    instructions.append("=" * 60)
    instructions.append("")
    instructions.append(f"📦 حجم مخزن: {tank_volume:,.0f} لیتر")
    instructions.append("")
    
    if tank_type == "calcium":
        instructions.append("⚠️ نکته مهم برای مخزن کلسیم:")
        instructions.append("   - این مخزن حاوی کلسیم است")
        instructions.append("   - هرگز کودهای این مخزن را با مخزن اصلی مخلوط نکنید")
        instructions.append("   - pH نهایی باید بین 6.0 تا 6.5 باشد")
    else:
        instructions.append("⚠️ نکته مهم برای مخزن اصلی:")
        instructions.append("   - این مخزن حاوی کودهای NPK، سولفات‌ها و ریز مغذی‌ها است")
        instructions.append("   - pH نهایی باید بین 5.5 تا 6.2 باشد")
    
    instructions.append("")
    instructions.append("🔧 مراحل ساخت:")
    instructions.append("")
    instructions.append("مرحله 1: مخزن را تا 70 درصد با آب تمیز پر کنید")
    instructions.append("")
    instructions.append("مرحله 2: کودها را به ترتیب زیر اضافه کنید:")
    instructions.append("")
    
    for i, dose in enumerate(doses, 1):
        stock_text = ""
        if dose.get('stock_200x_g_per_liter'):
            stock_text = f" (محلول مادر 200x: {dose['stock_200x_g_per_liter']} گرم در لیتر آب)"
        
        instructions.append(f"   {i}. {dose['name']}:")
        instructions.append(f"      - مقدار مصرف: {dose['dose_g_per_liter']} گرم در لیتر")
        instructions.append(f"      - مجموع برای مخزن: {dose['dose_g_for_tank']:,.1f} گرم{stock_text}")
        instructions.append("")
    
    instructions.append("مرحله 3: بعد از اضافه کردن هر کود، به مدت 2 دقیقه هم بزنید")
    instructions.append("")
    instructions.append("مرحله 4: مخزن را تا حجم نهایی پر کنید و 5 دقیقه دیگر هم بزنید")
    instructions.append("")
    instructions.append(f"مرحله 5: pH را با اسید فسفریک یا سولفوریک در محدوده {target_ph_min} تا {target_ph_max} تنظیم کنید")
    instructions.append("")
    instructions.append("=" * 60)
    
    if warnings:
        instructions.append("")
        instructions.append("⚠️ هشدارهای مهم:")
        seen = set()
        for warn in warnings:
            msg = warn.get('message', str(warn))
            if msg not in seen:
                instructions.append(f"   • {msg}")
                seen.add(msg)
        instructions.append("")
        instructions.append("=" * 60)
    
    return "\n".join(instructions)


def generate_persian_general_instructions(
    tank_main_volume: float,
    tank_calcium_volume: float,
    ec_main: float,
    ec_calcium: float,
    warnings: List[Dict]
) -> str:
    """تولید دستورالعمل کلی فارسی برای استفاده از دو مخزن"""
    
    instructions = []
    
    instructions.append("=" * 60)
    instructions.append("🌱 دستورالعمل کلی استفاده از سیستم دو مخزن")
    instructions.append("=" * 60)
    instructions.append("")
    instructions.append("📌 اصل اساسی:")
    instructions.append("   در سیستم‌های هیدروپونیک حرفه‌ای، کودهای حاوی کلسیم باید جدا از سایر کودها")
    instructions.append("   نگهداری شوند تا از رسوب و واکنش‌های شیمیایی جلوگیری شود.")
    instructions.append("")
    instructions.append("=" * 60)
    instructions.append("🧪 مخزن A (مخزن کلسیم)")
    instructions.append("=" * 60)
    instructions.append(f"   حجم: {tank_calcium_volume:,.0f} لیتر")
    instructions.append(f"   EC پیش‌بینی: {ec_calcium} mS/cm")
    instructions.append("   محتویات: نیترات کلسیم، کلات آهن، سایر کودهای کلسیمی")
    instructions.append("   محدوده pH: 6.0 - 6.5")
    instructions.append("")
    instructions.append("=" * 60)
    instructions.append("🧪 مخزن B (مخزن اصلی)")
    instructions.append("=" * 60)
    instructions.append(f"   حجم: {tank_main_volume:,.0f} لیتر")
    instructions.append(f"   EC پیش‌بینی: {ec_main} mS/cm")
    instructions.append("   محتویات: کودهای NPK، سولفات پتاسیم، منیزیم سولفات، ریز مغذی‌ها")
    instructions.append("   محدوده pH: 5.5 - 6.2")
    instructions.append("")
    instructions.append("=" * 60)
    instructions.append("⚠️ نکات بسیار مهم")
    instructions.append("=" * 60)
    instructions.append("")
    instructions.append("1️⃣ هرگز کودهای دو مخزن را قبل از مصرف با هم مخلوط نکنید!")
    instructions.append("2️⃣ ترتیب ساخت: ابتدا مخزن اصلی، سپس مخزن کلسیم")
    instructions.append("3️⃣ از دو انژکتور جداگانه برای تزریق استفاده کنید")
    instructions.append("4️⃣ برنامه تغذیه: هفته اول 50%، هفته دوم 75%، هفته سوم 100%")
    instructions.append("")
    
    severe_warnings = [w for w in warnings if w.get('severity') == 'error']
    if severe_warnings:
        instructions.append("=" * 60)
        instructions.append("🚨 هشدارهای بحرانی")
        instructions.append("=" * 60)
        for warn in severe_warnings:
            instructions.append(f"   • {warn.get('message', str(warn))}")
    
    instructions.append("")
    instructions.append("=" * 60)
    instructions.append("✅ موفق باشید!")
    instructions.append("=" * 60)
    
    return "\n".join(instructions)
```

---

## File 13: `backend/app/calculator/optimization.py`

**Size:** 27.9 KB

```python
from typing import List, Dict, Tuple, Optional
from .core import SUPPORTED_ELEMENTS, calculate_element_ppm
import numpy as np

# ============================================================
# توابع کمکی برای ترکیب چند کود NPK (مرحله 1)
# ============================================================

def is_npk_fertilizer(fertilizer) -> bool:
    """تشخیص اینکه آیا کود NPK است یا خیر"""
    fert_type = (fertilizer.fertilizer_type or "").upper()
    if fert_type == 'NPK' or 'NPK' in fert_type:
        return True

    has_n = (fertilizer.n_percent or 0) > 0
    has_p = (fertilizer.p_percent or 0) > 0
    has_k = (fertilizer.k_percent or 0) > 0

    return has_n and has_p and has_k


def generate_combinations(fertilizers, max_fertilizers=3):
    """تولید تمام ترکیب‌های ممکن از 1 تا max_fertilizers کود"""
    from itertools import combinations

    all_combinations = []

    for fert in fertilizers:
        all_combinations.append([fert])

    for fert1, fert2 in combinations(fertilizers, 2):
        all_combinations.append([fert1, fert2])

    if max_fertilizers >= 3:
        for fert1, fert2, fert3 in combinations(fertilizers, 3):
            all_combinations.append([fert1, fert2, fert3])

    return all_combinations


def brute_force_optimization(fertilizers, needs, bounds, steps=10):
    """جستجوی网格 برای ترکیب‌های کوچک (2-3 کود)"""
    best_doses = None
    best_error = float('inf')

    if len(fertilizers) == 2:
        min1, max1 = bounds[0]
        min2, max2 = bounds[1]

        for i in range(steps + 1):
            dose1 = min1 + (max1 - min1) * i / steps
            for j in range(steps + 1):
                dose2 = min2 + (max2 - min2) * j / steps

                n = (dose1 * (fertilizers[0].n_percent or 0) +
                     dose2 * (fertilizers[1].n_percent or 0)) * 10
                p = (dose1 * (fertilizers[0].p_percent or 0) +
                     dose2 * (fertilizers[1].p_percent or 0)) * 10
                k = (dose1 * (fertilizers[0].k_percent or 0) +
                     dose2 * (fertilizers[1].k_percent or 0)) * 10

                error = ((needs.get('N', 0) - n) ** 2 +
                        (needs.get('P', 0) - p) ** 2 +
                        (needs.get('K', 0) - k) ** 2)

                if error < best_error:
                    best_error = error
                    best_doses = [dose1, dose2]

    elif len(fertilizers) == 3:
        min1, max1 = bounds[0]
        min2, max2 = bounds[1]
        min3, max3 = bounds[2]

        steps_3d = max(5, steps // 2)

        for i in range(steps_3d + 1):
            dose1 = min1 + (max1 - min1) * i / steps_3d
            for j in range(steps_3d + 1):
                dose2 = min2 + (max2 - min2) * j / steps_3d
                for k_idx in range(steps_3d + 1):
                    dose3 = min3 + (max3 - min3) * k_idx / steps_3d

                    n = (dose1 * (fertilizers[0].n_percent or 0) +
                         dose2 * (fertilizers[1].n_percent or 0) +
                         dose3 * (fertilizers[2].n_percent or 0)) * 10
                    p = (dose1 * (fertilizers[0].p_percent or 0) +
                         dose2 * (fertilizers[1].p_percent or 0) +
                         dose3 * (fertilizers[2].p_percent or 0)) * 10
                    k = (dose1 * (fertilizers[0].k_percent or 0) +
                         dose2 * (fertilizers[1].k_percent or 0) +
                         dose3 * (fertilizers[2].k_percent or 0)) * 10

                    error = ((needs.get('N', 0) - n) ** 2 +
                            (needs.get('P', 0) - p) ** 2 +
                            (needs.get('K', 0) - k) ** 2)

                    if error < best_error:
                        best_error = error
                        best_doses = [dose1, dose2, dose3]

    return best_doses, best_error


def build_combination_result(fertilizers, doses, needs):
    """ساخت خروجی استاندارد از ترکیب بهینه"""
    result_doses = []
    total_supply = {'N': 0.0, 'P': 0.0, 'K': 0.0}

    for fert, dose in zip(fertilizers, doses):
        if dose <= 0.01:
            continue

        result_doses.append({
            "id": fert.id,
            "name": fert.name,
            "brand_name": fert.brand_name,
            "dose_g_per_liter": round(dose, 3),
            "chemical_formula": fert.chemical_formula,
            "layer": "macro",
            "combination_order": len(result_doses) + 1
        })

        total_supply['N'] += dose * (fert.n_percent or 0) * 10
        total_supply['P'] += dose * (fert.p_percent or 0) * 10
        total_supply['K'] += dose * (fert.k_percent or 0) * 10

    total_supply = {k: round(v, 1) for k, v in total_supply.items()}

    return result_doses, total_supply


# ============================================================
# توابع جدید برای بررسی حلالیت (مرحله 2)
# ============================================================

def get_solubility_limit(fertilizer, temperature_c: float = 20.0) -> float:
    """
    برگرداندن حد حلالیت کود بر حسب g/L در دمای مشخص

    Args:
        fertilizer: شیء کود
        temperature_c: دمای آب بر حسب سانتی‌گراد (پیش‌فرض 20 درجه)

    Returns:
        حد حلالیت بر حسب g/L
    """
    if hasattr(fertilizer, 'solubility_g_per_l') and fertilizer.solubility_g_per_l:
        base_solubility = fertilizer.solubility_g_per_l
    else:
        default_solubility = {
            'calcium_nitrate': 1200,
            'potassium_sulfate': 120,
            'magnesium_sulfate': 350,
            'mkp': 230,
            'potassium_nitrate': 320,
            'ammonium_nitrate': 2000,
            'default': 400
        }

        fert_name = (fertilizer.name or "").lower()
        if 'calcium' in fert_name or 'نیترات کلسیم' in fert_name:
            base_solubility = default_solubility['calcium_nitrate']
        elif 'potassium sulfate' in fert_name or 'سولفات پتاسیم' in fert_name:
            base_solubility = default_solubility['potassium_sulfate']
        elif 'magnesium sulfate' in fert_name or 'سولفات منیزیم' in fert_name:
            base_solubility = default_solubility['magnesium_sulfate']
        elif 'mkp' in fert_name or 'monopotassium' in fert_name:
            base_solubility = default_solubility['mkp']
        elif 'potassium nitrate' in fert_name or 'نیترات پتاسیم' in fert_name:
            base_solubility = default_solubility['potassium_nitrate']
        else:
            base_solubility = default_solubility['default']

    if temperature_c != 20.0:
        temp_factor = 1 + (temperature_c - 20.0) * 0.005
        base_solubility = base_solubility * temp_factor

    return base_solubility


def check_solubility(fertilizer, proposed_dose: float, temperature_c: float = 20.0) -> Tuple[bool, float, str]:
    """
    بررسی اینکه دوز پیشنهادی از حد حلالیت تجاوز نمی‌کند

    Returns:
        (is_ok, max_safe_dose, warning_message)
    """
    solubility_limit = get_solubility_limit(fertilizer, temperature_c)

    if proposed_dose <= solubility_limit:
        return True, proposed_dose, ""

    max_safe_dose = solubility_limit * 0.95

    warning = (
        f"⚠️ دوز پیشنهادی {proposed_dose:.2f} g/L برای {fertilizer.name} "
        f"بیشتر از حد حلالیت ({solubility_limit:.0f} g/L) است. "
        f"حداکثر دوز قابل استفاده: {max_safe_dose:.2f} g/L"
    )

    return False, max_safe_dose, warning


def enforce_solubility_limit(doses: List[Dict], fertilizers: List, temperature_c: float = 20.0) -> Tuple[List[Dict], List[Dict]]:
    """
    اعمال محدودیت حلالیت روی لیست دوزها
    """
    adjusted_doses = []
    solubility_warnings = []

    fert_map = {f.id: f for f in fertilizers}

    for dose in doses:
        fert = fert_map.get(dose.get('id'))
        if not fert:
            adjusted_doses.append(dose)
            continue

        proposed_dose = dose.get('dose_g_per_liter', 0)
        is_ok, max_dose, warning = check_solubility(fert, proposed_dose, temperature_c)

        if is_ok:
            adjusted_doses.append(dose)
        else:
            adjusted_dose = dose.copy()
            adjusted_dose['dose_g_per_liter'] = round(max_dose, 3)
            adjusted_dose['original_dose'] = round(proposed_dose, 3)
            adjusted_dose['solubility_limited'] = True
            adjusted_doses.append(adjusted_dose)

            solubility_warnings.append({
                "type": "solubility_limit",
                "severity": "warning",
                "fertilizer": fert.name,
                "message": warning,
                "original_dose": round(proposed_dose, 3),
                "adjusted_dose": round(max_dose, 3)
            })

    return adjusted_doses, solubility_warnings


# ============================================================
# توابع بهینه‌سازی با در نظر گرفتن حلالیت (مرحله 2)
# ============================================================

def optimize_single_fertilizer(fertilizer, needs, max_dose=3.0, temperature_c=20.0):
    """روش ساده برای یک کود با در نظر گرفتن حلالیت"""
    doses = []
    for elem in ['N', 'P', 'K']:
        need = needs.get(elem, 0)
        elem_percent = getattr(fertilizer, f"{elem.lower()}_percent", 0) or 0
        if elem_percent > 0 and need > 0:
            dose = need / (elem_percent * 10)
            doses.append(dose)

    if not doses:
        return [0.1], float('inf')

    proposed_dose = sum(doses) / len(doses)

    solubility_limit = get_solubility_limit(fertilizer, temperature_c)
    max_limit = min(fertilizer.max_dose_g_per_liter or 5.0, max_dose, solubility_limit)
    min_limit = fertilizer.min_dose_g_per_liter or 0.01
    final_dose = max(min_limit, min(proposed_dose, max_limit))

    n_supply = final_dose * (fertilizer.n_percent or 0) * 10
    p_supply = final_dose * (fertilizer.p_percent or 0) * 10
    k_supply = final_dose * (fertilizer.k_percent or 0) * 10

    error = ((needs.get('N', 0) - n_supply) ** 2 +
             (needs.get('P', 0) - p_supply) ** 2 +
             (needs.get('K', 0) - k_supply) ** 2)

    return [final_dose], error


def optimize_combination(fertilizers, needs, max_total_dose=3.0, temperature_c=20.0):
    """
    پیدا کردن دوز بهینه برای یک ترکیب مشخص از کودها
    با در نظر گرفتن محدودیت حلالیت
    """
    if len(fertilizers) == 1:
        return optimize_single_fertilizer(fertilizers[0], needs, max_total_dose, temperature_c)

    try:
        from scipy.optimize import minimize

        n_fert = len(fertilizers)

        def cost_function(doses):
            total_n = 0
            total_p = 0
            total_k = 0

            for i, fert in enumerate(fertilizers):
                dose = doses[i]
                total_n += dose * (fert.n_percent or 0) * 10
                total_p += dose * (fert.p_percent or 0) * 10
                total_k += dose * (fert.k_percent or 0) * 10

            penalty = 0
            for i, fert in enumerate(fertilizers):
                solubility_limit = get_solubility_limit(fert, temperature_c)
                if doses[i] > solubility_limit:
                    penalty += (doses[i] - solubility_limit) * 1000

            error_n = (needs.get('N', 0) - total_n) ** 2
            error_p = (needs.get('P', 0) - total_p) ** 2
            error_k = (needs.get('K', 0) - total_k) ** 2

            return error_n + error_p + error_k + penalty

        bounds = []
        for fert in fertilizers:
            min_dose = fert.min_dose_g_per_liter or 0.01
            solubility_limit = get_solubility_limit(fert, temperature_c)
            max_dose = min(fert.max_dose_g_per_liter or 5.0, max_total_dose, solubility_limit)
            bounds.append((min_dose, max_dose))

        initial_doses = [0.5] * n_fert
        result = minimize(cost_function, initial_doses, bounds=bounds, method='L-BFGS-B')

        if result.success:
            doses = result.x
            error = result.fun
        else:
            doses, error = brute_force_optimization(fertilizers, needs, bounds)

    except ImportError:
        bounds = []
        for fert in fertilizers:
            min_dose = fert.min_dose_g_per_liter or 0.01
            solubility_limit = get_solubility_limit(fert, temperature_c)
            max_dose = min(fert.max_dose_g_per_liter or 5.0, max_total_dose, solubility_limit)
            bounds.append((min_dose, max_dose))
        doses, error = brute_force_optimization(fertilizers, needs, bounds)

    return doses, error


def solve_macro_layer_combined(needs: Dict[str, float], macro_fertilizers: List, max_total_dose: float = 3.0, temperature_c: float = 20.0) -> Tuple[List[Dict], Dict[str, float]]:
    """
    انتخاب ترکیبی از چند کود NPK برای تأمین دقیق N, P, K
    با در نظر گرفتن محدودیت حلالیت
    """
    if len(macro_fertilizers) == 0:
        return [], {'N': 0.0, 'P': 0.0, 'K': 0.0}

    if len(macro_fertilizers) == 1:
        doses, _ = optimize_single_fertilizer(macro_fertilizers[0], needs, max_total_dose, temperature_c)
        return build_combination_result(macro_fertilizers, doses, needs)

    best_combination = None
    best_doses = None
    best_error = float('inf')

    combinations = generate_combinations(macro_fertilizers, max_fertilizers=3)

    if len(combinations) > 100:
        combinations = sorted(combinations, key=len)[:100]

    for combo in combinations:
        doses, error = optimize_combination(combo, needs, max_total_dose, temperature_c)
        if error < best_error:
            best_error = error
            best_combination = combo
            best_doses = doses

    if best_combination is None:
        doses, _ = optimize_single_fertilizer(macro_fertilizers[0], needs, max_total_dose, temperature_c)
        return build_combination_result([macro_fertilizers[0]], doses, needs)

    return build_combination_result(best_combination, best_doses, needs)


# ============================================================
# توابع اصلی (اصلاح شده با حلالیت)
# ============================================================

def select_best_fertilizer_for_macro(needs: Dict[str, float], fertilizers: List) -> Tuple[object, float, Dict]:
    """نسخه قدیمی - حفظ شده برای سازگاری"""
    best_fertilizer = None
    best_score = float('inf')
    best_dose = 0
    best_supply = {}

    for fert in fertilizers:
        doses = []
        for elem in ['N', 'P', 'K']:
            need = needs.get(elem, 0)
            elem_percent = getattr(fert, f"{elem.lower()}_percent", 0) or 0
            if elem_percent > 0 and need > 0:
                dose_for_elem = need / (elem_percent * 10)
                doses.append(dose_for_elem)

        if not doses:
            continue

        proposed_dose = sum(doses) / len(doses)
        max_dose = fert.max_dose_g_per_liter or 5.0
        min_dose = fert.min_dose_g_per_liter or 0.01
        proposed_dose = max(min_dose, min(proposed_dose, max_dose))

        supply = calculate_element_ppm(fert, proposed_dose)

        error = 0
        for elem in ['N', 'P', 'K']:
            need = needs.get(elem, 0)
            sup = supply.get(elem, 0)
            error += (need - sup) ** 2

        if error < best_score:
            best_score = error
            best_fertilizer = fert
            best_dose = proposed_dose
            best_supply = supply

    return best_fertilizer, best_dose, best_supply


def select_best_fertilizer_for_secondary(needs: Dict[str, float], fertilizers: List) -> List[Tuple[object, float, Dict]]:
    results = []

    for elem in ['Ca', 'Mg', 'S']:
        need = needs.get(elem, 0)
        if need <= 0.5:
            continue

        best_fert = None
        best_dose = 0
        best_supply = {}
        best_error = float('inf')

        for fert in fertilizers:
            elem_percent = getattr(fert, f"{elem.lower()}_percent", 0) or 0
            if elem_percent <= 0:
                continue

            required_dose = need / (elem_percent * 10)
            max_dose = fert.max_dose_g_per_liter or 5.0
            min_dose = fert.min_dose_g_per_liter or 0.01
            final_dose = max(min_dose, min(required_dose, max_dose))

            supply = calculate_element_ppm(fert, final_dose)
            supplied = supply.get(elem, 0)
            error = abs(need - supplied)

            if error < best_error:
                best_error = error
                best_fert = fert
                best_dose = final_dose
                best_supply = {elem: supplied}

        if best_fert:
            results.append((best_fert, best_dose, best_supply))

    return results


def solve_macro_layer(
    needs: Dict[str, float],
    fertilizers: List,
    max_total_dose: float = 3.0,
    temperature_c: float = 20.0
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    """
    حل لایه NPK با قابلیت ترکیب چند کود و بررسی حلالیت
    """
    macro_elements = ['N', 'P', 'K']
    warnings = []

    macro_fertilizers = []
    for f in fertilizers:
        if is_npk_fertilizer(f):
            macro_fertilizers.append(f)

    if not macro_fertilizers:
        for f in fertilizers:
            if (f.n_percent or 0) > 0 and (f.p_percent or 0) > 0 and (f.k_percent or 0) > 0:
                macro_fertilizers.append(f)

    if not macro_fertilizers:
        for f in fertilizers:
            if (f.n_percent or 0) > 0 or (f.p_percent or 0) > 0 or (f.k_percent or 0) > 0:
                macro_fertilizers.append(f)
                break

    if not macro_fertilizers:
        warnings.append({
            "type": "missing_fertilizers",
            "severity": "warning",
            "message": "هیچ کود NPK مناسبی یافت نشد. لطفاً کودهای NPK را به دیتابیس اضافه کنید."
        })
        return [], {e: 0.0 for e in macro_elements}, warnings

    try:
        result_doses, total_supply = solve_macro_layer_combined(
            needs, macro_fertilizers, max_total_dose, temperature_c
        )

        result_doses, solubility_warnings = enforce_solubility_limit(result_doses, macro_fertilizers, temperature_c)
        warnings.extend(solubility_warnings)

        if len(result_doses) > 1:
            warnings.append({
                "type": "combination_used",
                "severity": "info",
                "message": f"از ترکیب {len(result_doses)} کود NPK برای تأمین دقیق تر استفاده شده است."
            })

        for elem in macro_elements:
            need = needs.get(elem, 0)
            supply = total_supply.get(elem, 0)
            if need > 10 and abs(need - supply) > need * 0.2:
                warnings.append({
                    "type": "high_error",
                    "severity": "warning",
                    "message": f"خطای تأمین {elem}: نیاز {need} ppm، تأمین {supply} ppm (خطای {abs(need-supply):.0f} ppm)"
                })

        return result_doses, total_supply, warnings

    except Exception as e:
        warnings.append({
            "type": "fallback_used",
            "severity": "warning",
            "message": f"خطا در بهینه‌سازی ترکیبی: {str(e)}. از روش ساده استفاده می‌شود."
        })

        best_fert, best_dose, best_supply = select_best_fertilizer_for_macro(needs, macro_fertilizers)

        if not best_fert:
            return [], {e: 0.0 for e in macro_elements}, warnings

        is_ok, max_dose, sol_warning = check_solubility(best_fert, best_dose, temperature_c)
        if not is_ok:
            best_dose = max_dose
            warnings.append({
                "type": "solubility_limit",
                "severity": "warning",
                "message": sol_warning
            })
            best_supply = calculate_element_ppm(best_fert, best_dose)

        result_doses = [{
            "id": best_fert.id,
            "name": best_fert.name,
            "brand_name": best_fert.brand_name,
            "dose_g_per_liter": round(best_dose, 3),
            "chemical_formula": best_fert.chemical_formula,
            "layer": "macro"
        }]

        final_supply = {e: best_supply.get(e, 0.0) for e in macro_elements}

        return result_doses, final_supply, warnings


def solve_secondary_layer(
    needs: Dict[str, float],
    fertilizers: List,
    max_total_dose: float = 2.0
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    secondary_elements = ['Ca', 'Mg', 'S']
    warnings = []

    secondary_fertilizers = [f for f in fertilizers if f.fertilizer_type in ['تک عنصری', 'NPK']]

    if not secondary_fertilizers:
        warnings.append({
            "type": "missing_fertilizers",
            "severity": "warning",
            "message": "هیچ کود حاوی عناصر ثانویه (Ca, Mg, S) یافت نشد"
        })
        return [], {e: 0.0 for e in secondary_elements}, warnings

    selected = select_best_fertilizer_for_secondary(needs, secondary_fertilizers)

    result_doses = []
    final_supply = {e: 0.0 for e in secondary_elements}

    for fert, dose, supply in selected:
        result_doses.append({
            "id": fert.id,
            "name": fert.name,
            "brand_name": fert.brand_name,
            "dose_g_per_liter": round(dose, 3),
            "chemical_formula": fert.chemical_formula,
            "layer": "secondary"
        })
        for elem, val in supply.items():
            if elem in final_supply:
                final_supply[elem] += val

    return result_doses, final_supply, warnings


def solve_micro_layer(
    needs: Dict[str, float],
    fertilizers: List,
    max_dose: float = 0.5
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    micro_elements = ['Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']
    warnings = []

    micro_fertilizers = [f for f in fertilizers if f.fertilizer_type == 'ریزمغذی']

    if not micro_fertilizers:
        warnings.append({
            "type": "missing_fertilizers",
            "severity": "warning",
            "message": "هیچ کود ریز مغذی در دیتابیس یافت نشد"
        })
        return [], {e: 0.0 for e in micro_elements}, warnings

    micro_fert = micro_fertilizers[0]

    required_dose = 0
    for elem in micro_elements:
        need = needs.get(elem, 0)
        if need > 0:
            elem_percent = getattr(micro_fert, f"{elem.lower()}_percent", 0) or 0
            if elem_percent > 0:
                dose_for_elem = need / (elem_percent * 10)
                required_dose = max(required_dose, dose_for_elem)

    dose = min(required_dose, max_dose)
    if dose < 0.01:
        dose = 0.01

    content = calculate_element_ppm(micro_fert, dose)
    final_supply = {e: content.get(e, 0.0) for e in micro_elements}

    result_doses = [{
        "id": micro_fert.id,
        "name": micro_fert.name,
        "brand_name": micro_fert.brand_name,
        "dose_g_per_liter": round(dose, 3),
        "chemical_formula": micro_fert.chemical_formula,
        "layer": "micro"
    }]

    uncovered = []
    for elem in micro_elements:
        need = needs.get(elem, 0)
        supply = final_supply[elem]
        if need > 0.1 and supply < need * 0.5:
            uncovered.append(elem)

    if uncovered:
        warnings.append({
            "type": "partial_coverage",
            "severity": "warning",
            "message": f"عناصر ریز مغذی به طور کامل تامین نشدند: {', '.join(uncovered)}",
            "fertilizers": [micro_fert.name]
        })

    return result_doses, final_supply, warnings


def optimize_fertilizer_doses_professional(
    remaining_needs: Dict[str, float],
    fertilizers: List,
    brand_filter: Optional[str] = None,
    max_total_dose: float = 5.0,
    temperature_c: float = 20.0
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    """الگوریتم لایه‌به‌لایه - NPK → Secondary → Micro با پشتیبانی از دما"""

    final_supply = {elem: 0.0 for elem in SUPPORTED_ELEMENTS}

    if not fertilizers:
        return [], final_supply, []

    if brand_filter:
        fertilizers = [f for f in fertilizers if f.brand_name == brand_filter]
        if not fertilizers:
            return [], final_supply, [{
                "type": "brand_filter",
                "severity": "warning",
                "message": f"هیچ کودی برای برند {brand_filter} یافت نشد"
            }]

    all_warnings = []
    all_doses = []

    macro_needs = {elem: remaining_needs.get(elem, 0) for elem in ['N', 'P', 'K']}
    macro_doses, macro_supply, macro_warnings = solve_macro_layer(macro_needs, fertilizers, 3.0, temperature_c)
    all_doses.extend(macro_doses)
    all_warnings.extend(macro_warnings)

    for elem, value in macro_supply.items():
        if elem in final_supply:
            final_supply[elem] += value
        else:
            final_supply[elem] = value

    remaining = {}
    for elem in SUPPORTED_ELEMENTS:
        remaining[elem] = max(0, remaining_needs.get(elem, 0) - final_supply.get(elem, 0))

    secondary_needs = {elem: remaining.get(elem, 0) for elem in ['Ca', 'Mg', 'S']}
    secondary_doses, secondary_supply, secondary_warnings = solve_secondary_layer(secondary_needs, fertilizers, 2.0)
    all_doses.extend(secondary_doses)
    all_warnings.extend(secondary_warnings)

    for elem, value in secondary_supply.items():
        if elem in final_supply:
            final_supply[elem] += value
        else:
            final_supply[elem] = value

    for elem in ['Ca', 'Mg', 'S']:
        remaining[elem] = max(0, remaining.get(elem, 0) - secondary_supply.get(elem, 0))

    micro_needs = {elem: remaining.get(elem, 0) for elem in ['Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']}
    micro_doses, micro_supply, micro_warnings = solve_micro_layer(micro_needs, fertilizers, 0.5)
    all_doses.extend(micro_doses)
    all_warnings.extend(micro_warnings)

    for elem, value in micro_supply.items():
        if elem in final_supply:
            final_supply[elem] += value
        else:
            final_supply[elem] = value

    unique_doses = {}
    for dose in all_doses:
        name = dose['name']
        if name in unique_doses:
            unique_doses[name]['dose_g_per_liter'] += dose['dose_g_per_liter']
        else:
            unique_doses[name] = dose

    result_doses = list(unique_doses.values())
    result_doses.sort(key=lambda x: x['dose_g_per_liter'], reverse=True)

    for dose in result_doses:
        dose['dose_g_per_liter'] = round(dose['dose_g_per_liter'], 3)

    uncovered = []
    for elem in SUPPORTED_ELEMENTS:
        need = remaining_needs.get(elem, 0)
        supply = final_supply.get(elem, 0)
        if elem in ['N', 'P', 'K', 'Ca', 'Mg'] and need > 10.0 and supply < need * 0.5:
            uncovered.append(elem)

    if uncovered:
        all_warnings.append({
            "type": "partial_coverage",
            "severity": "info",
            "message": f"عناصر زیر به طور کامل تامین نشدند: {', '.join(uncovered)}. می‌توانید نیازها را به صورت دستی تنظیم کنید."
        })

    return result_doses, final_supply, all_warnings

```

---

## File 14: `backend/app/calculator/stock.py`

**Size:** 8.4 KB

```python
from typing import List, Dict, Tuple


def calculate_dose_kg_for_stock(
    dose_gpl: float,
    injector_ratio: float,
    stock_tank_volume_liters: float
) -> float:
    """
    محاسبه مقدار کود مورد نیاز برای ساخت استوک (کیلوگرم)

    فرمول: مقدار کود (کیلوگرم) = (دوز مصرف (گرم در لیتر) × نسبت تزریق (X) × حجم استوک (لیتر)) ÷ 1000
    """
    dose_kg = (dose_gpl * injector_ratio * stock_tank_volume_liters) / 1000
    return round(dose_kg, 2)


def calculate_stock_consumption(
    injector_ratio: float,
    main_tank_volume_liters: float
) -> Tuple[float, float]:
    """
    محاسبه مقدار مصرف استوک در مخزن اصلی
    """
    stock_liters_for_main_tank = round(main_tank_volume_liters / injector_ratio, 2)
    stock_ml_per_liter = round(1000 / injector_ratio, 1)
    return stock_liters_for_main_tank, stock_ml_per_liter


def get_injector_explanation(injector_ratio: float) -> str:
    """تولید توضیح ساده برای مفهوم نسبت تزریق"""
    water_ratio = injector_ratio - 1
    return f"""📖 نسبت تزریق 1:{int(injector_ratio)} یعنی:
   1 لیتر استوک + {int(water_ratio)} لیتر آب = {int(injector_ratio)} لیتر محلول نهایی

مثال با نسبت 1:{int(injector_ratio)}:
   1 لیتر استوک + {int(water_ratio)} لیتر آب = {int(injector_ratio)} لیتر محلول نهایی"""


def get_stock_mixing_instructions(fertilizer_names: List[str]) -> str:
    """تولید دستورالعمل گام به گام ساخت استوک"""
    instructions = """🔧 روش ساخت استوک:
1. مخزن تمیز با حجم مناسب آماده کنید
2. 70% حجم مخزن را آب بریزید
3. کودها را به ترتیب زیر اضافه کنید:\n"""

    for i, name in enumerate(fertilizer_names, 1):
        instructions += f"   {i}. {name}\n"

    instructions += """4. بعد از هر کود، 2 دقیقه هم بزنید
5. آب را به حجم نهایی برسانید
6. 5 دقیقه دیگر هم بزنید
7. برچسب بزنید: نام کودها، تاریخ ساخت، نسبت تزریق"""

    return instructions


def get_stock_usage_instructions(injector_ratio: float) -> str:
    """تولید دستورالعمل مصرف استوک در مخزن اصلی"""
    return f"""🔧 روش مصرف استوک در مخزن اصلی:

با نسبت تزریق 1:{int(injector_ratio)}:

1. قبل از مصرف، استوک را خوب تکان دهید
2. مقدار مورد نیاز را اندازه بگیرید
3. به آرامی به مخزن اصلی اضافه کنید
4. 5 دقیقه هم بزنید

⚠️ نکته: هیچگاه استوک حاوی کلسیم را با استوک حاوی سولفات/فسفات قبل از ورود به مخزن اصلی مخلوط نکنید."""


def get_storage_instructions() -> Tuple[str, str, str, str]:
    """تولید نکات نگهداری و ایمنی استوک"""
    storage_instructions = """⚠️ نکات نگهداری و ایمنی استوک:

• همیشه ظرف استوک را محکم ببندید
• دور از نور مستقیم خورشید و در جای خنک نگهداری کنید
• برچسب بزنید: نام کودها، تاریخ ساخت، نسبت تزریق
• دور از دسترس کودکان نگهداری شود"""

    shelf_life_fridge = "7 روز در یخچال (دمای 4 درجه)"
    shelf_life_room = "3 روز در دمای محیط (زیر 25 درجه)"
    warning_signs = "نشانه‌های خرابی: رسوب سفید، تغییر رنگ، بوی نامطبوع، باد کردگی ظرف"

    return storage_instructions, shelf_life_fridge, shelf_life_room, warning_signs


# ============================================================
# توابع جدید برای بررسی حلالیت در استوک (مرحله 2)
# ============================================================

def get_solubility_limit_stock(fertilizer, temperature_c: float = 20.0) -> float:
    """
    برگرداندن حد حلالیت برای محلول استوک
    """
    from .optimization import get_solubility_limit
    return get_solubility_limit(fertilizer, temperature_c)


def check_stock_solubility(
    fertilizer,
    dose_gpl: float,
    injector_ratio: int = 200,
    temperature_c: float = 20.0
) -> Tuple[bool, float, str]:
    """
    بررسی حلالیت در محلول استوک

    Returns:
        (is_ok, max_safe_dose_gpl, warning_message)
    """
    solubility_limit = get_solubility_limit_stock(fertilizer, temperature_c)

    stock_concentration = dose_gpl * injector_ratio

    if stock_concentration <= solubility_limit:
        return True, dose_gpl, ""

    max_safe_stock = solubility_limit * 0.95
    max_safe_dose_gpl = max_safe_stock / injector_ratio

    warning = (
        f"⚠️ غلظت استوک برای {fertilizer.name} ({stock_concentration:.0f} g/L) "
        f"بیشتر از حد حلالیت ({solubility_limit:.0f} g/L) است. "
        f"حداکثر دوز قابل استفاده در استوک: {max_safe_dose_gpl:.3f} g/L "
        f"(معادل {max_safe_stock:.0f} g/L در استوک)"
    )

    return False, max_safe_dose_gpl, warning


def validate_stock_doses(doses: List[Dict], injector_ratio: int = 200, temperature_c: float = 20.0) -> Tuple[List[Dict], List[Dict]]:
    """
    اعتبارسنجی دوزهای استوک از نظر حلالیت
    """
    adjusted_doses = []
    solubility_warnings = []

    for dose in doses:
        fert = dose.get('fertilizer')
        if not fert:
            adjusted_doses.append(dose)
            continue

        dose_gpl = dose.get('dose_g_per_liter', 0)
        is_ok, max_dose_gpl, warning = check_stock_solubility(
            fert, dose_gpl, injector_ratio, temperature_c
        )

        if is_ok:
            adjusted_doses.append(dose)
        else:
            adjusted_dose = dose.copy()
            adjusted_dose['dose_g_per_liter'] = round(max_dose_gpl, 3)
            adjusted_dose['original_dose_g_per_liter'] = round(dose_gpl, 3)
            adjusted_dose['solubility_limited_stock'] = True
            adjusted_doses.append(adjusted_dose)

            solubility_warnings.append({
                "type": "stock_solubility_limit",
                "severity": "warning",
                "fertilizer": fert.name,
                "message": warning,
                "original_dose": round(dose_gpl, 3),
                "adjusted_dose": round(max_dose_gpl, 3)
            })

    return adjusted_doses, solubility_warnings


def add_stock_calculations_to_doses(
    doses: List[Dict],
    tank_volume_liters: float,
    injector_ratio: float,
    stock_tank_volume_liters: float,
    temperature_c: float = 20.0
) -> List[Dict]:
    """
    اضافه کردن محاسبات استوک به لیست دوزها با بررسی حلالیت
    """
    from .optimization import get_solubility_limit

    result = []
    for dose in doses:
        dose_gpl = dose.get('dose_g_per_liter', 0)

        fert = dose.get('fertilizer')
        if fert:
            solubility_limit = get_solubility_limit(fert, temperature_c)
            stock_concentration = dose_gpl * injector_ratio

            if stock_concentration > solubility_limit:
                max_safe_stock = solubility_limit * 0.95
                max_safe_dose = max_safe_stock / injector_ratio

                dose['solubility_warning'] = True
                dose['original_dose_gpl'] = dose_gpl
                dose_gpl = max_safe_dose

        dose_kg_for_stock = calculate_dose_kg_for_stock(
            dose_gpl=dose_gpl,
            injector_ratio=injector_ratio,
            stock_tank_volume_liters=stock_tank_volume_liters
        )

        dose_g_for_stock_alternative = None
        if dose_kg_for_stock < 1 and dose_kg_for_stock > 0:
            dose_g_for_stock_alternative = round(dose_kg_for_stock * 1000, 0)

        new_dose = dose.copy()
        new_dose['dose_kg_for_stock'] = dose_kg_for_stock
        new_dose['dose_g_for_stock_alternative'] = dose_g_for_stock_alternative
        new_dose['dose_g_per_liter'] = round(dose_gpl, 3)

        result.append(new_dose)

    return result

```

---

## File 15: `backend/app/calculator/tank.py`

**Size:** 1.0 KB

```python
# backend/app/calculator/tank.py

from typing import List, Dict


def calculate_tank_doses(doses: List[Dict], tank_volume_liters: float) -> List[Dict]:
    """
    محاسبه دوز برای کل مخزن و استوک 200x
    
    Args:
        doses: لیست دوزهای محاسبه شده (هر دوز شامل dose_g_per_liter و name)
        tank_volume_liters: حجم مخزن به لیتر
    
    Returns:
        لیست دوزها با فیلدهای جدید:
        - dose_g_for_tank: دوز کل برای مخزن (گرم)
        - stock_200x_g_per_liter: دوز برای استوک 200x (گرم در لیتر آب)
    """
    result = []
    for dose in doses:
        dose_g_for_tank = dose['dose_g_per_liter'] * tank_volume_liters
        stock_200x = dose['dose_g_per_liter'] * 200

        result.append({
            **dose,
            "dose_g_for_tank": round(dose_g_for_tank, 1),
            "stock_200x_g_per_liter": round(stock_200x, 1)
        })

    return result
```

---

## File 16: `frontend/src/views/CalculatorView.vue`

**Size:** 53.5 KB

```vue
<template>
  <div class="min-h-screen bg-[var(--bg-primary)]">

    <!-- Header -->
    <header class="bg-[var(--bg-card)] border-b border-gray-100 sticky top-0 z-10 no-print">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 py-4">
        <div class="flex justify-between items-center">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-800">FarmTech</h1>
              <p class="text-xs text-gray-500">سیستم هوشمند نسخه‌دهی کود - دو مخزن</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <div :class="['w-2 h-2 rounded-full', connectionStatus === 'connected' ? 'bg-green-500' : 'bg-red-500']"></div>
            <span class="text-xs text-gray-500">{{ connectionStatus === 'connected' ? 'متصل به سرور' : 'قطع ارتباط با سرور' }}</span>
            <button @click="showFertilizerList = !showFertilizerList" class="px-3 py-1 text-sm text-gray-600 hover:text-green-600 border border-gray-200 rounded-lg transition">
              <svg class="w-4 h-4 inline ml-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              لیست کودها
            </button>
            <button v-if="result" @click="printResult" class="px-3 py-1 text-sm text-gray-600 hover:text-green-600 border border-gray-200 rounded-lg transition">
              <svg class="w-4 h-4 inline ml-1" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
              </svg>
              پرینت
            </button>
            <ThemeToggle />
          </div>
        </div>
      </div>
    </header>

    <!-- Modal لیست کودها -->
    <div v-if="showFertilizerList" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" @click.self="showFertilizerList = false">
      <div class="bg-[var(--bg-card)] rounded-2xl max-w-4xl w-full max-h-[80vh] overflow-hidden shadow-xl">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gradient-to-r from-green-600 to-teal-600">
          <h3 class="text-lg font-semibold text-white">📋 لیست کودهای موجود در دیتابیس</h3>
          <button @click="showFertilizerList = false" class="text-white hover:text-gray-200 text-xl">✕</button>
        </div>
        <div class="p-6 overflow-y-auto max-h-[calc(80vh-120px)]">
          <div v-if="isLoadingFertilizers" class="text-center py-8">
            <div class="inline-block w-8 h-8 border-2 border-green-500 border-t-transparent rounded-full animate-spin"></div>
            <p class="mt-2 text-gray-500">در حال بارگذاری...</p>
          </div>
          <div v-else-if="fertilizers.length === 0" class="text-center py-8 text-gray-500">
            هیچ کودی در دیتابیس یافت نشد
          </div>
          <div v-else class="space-y-3">
            <div v-for="fert in fertilizers" :key="fert.id" class="border border-gray-200 rounded-xl p-4 hover:shadow-md transition">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center gap-2 flex-wrap">
                    <h4 class="font-bold text-gray-800">{{ fert.persian_name || fert.name }}</h4>
                    <span class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">{{ fert.brand_name }}</span>
                    <span class="text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full">{{ fert.fertilizer_type }}</span>
                  </div>
                  <div class="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2 text-xs text-gray-500">
                    <span v-if="fert.n_percent">N: {{ fert.n_percent }}%</span>
                    <span v-if="fert.p_percent">P: {{ fert.p_percent }}%</span>
                    <span v-if="fert.k_percent">K: {{ fert.k_percent }}%</span>
                    <span v-if="fert.ca_percent">Ca: {{ fert.ca_percent }}%</span>
                    <span v-if="fert.mg_percent">Mg: {{ fert.mg_percent }}%</span>
                    <span v-if="fert.fe_percent">Fe: {{ fert.fe_percent }}%</span>
                    <span v-if="fert.zn_percent">Zn: {{ fert.zn_percent }}%</span>
                    <span v-if="fert.s_percent">S: {{ fert.s_percent }}%</span>
                  </div>
                  <p class="text-xs text-gray-400 mt-2">{{ getFertilizerDescription(fert.name) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
      <!-- Form Card -->
      <div class="bg-[var(--bg-card)] rounded-2xl shadow-card border border-gray-100 overflow-hidden">
        <div class="px-6 py-5 border-b border-gray-100">
          <h2 class="text-lg font-semibold text-gray-800">اطلاعات محاسبه</h2>
          <p class="text-sm text-gray-500 mt-0.5">لطفاً اطلاعات مورد نیاز را وارد کنید</p>
        </div>

        <div class="p-6 space-y-6">
          <!-- Crop and Variety and Cultivation Type -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                <svg class="w-4 h-4 inline ml-1 text-gray-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                </svg>
                محصول
              </label>
              <select v-model="selectedCrop" class="w-full px-3 py-2.5 bg-[var(--bg-primary)] border border-gray-200 rounded-xl" disabled>
                <option value="توت‌فرنگی">توت‌فرنگی</option>
              </select>
              <p class="text-xs text-gray-400 mt-1">محصول انتخابی - توت فرنگی</p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                <svg class="w-4 h-4 inline ml-1 text-gray-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2zM12 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z" />
                  <path d="M20 12c0-4.418-3.582-8-8-8s-8 3.582-8 8 3.582 8 8 8 8-3.582 8-8z" />
                </svg>
                رقم گیاه
              </label>
              <select v-model="selectedVariety" class="w-full px-3 py-2.5 bg-[var(--bg-primary)] border border-gray-200 rounded-xl focus:border-green-500 focus:ring-1 focus:ring-green-500 transition">
                <option value="">انتخاب کنید</option>
                <option value="سن اندرسا">سن اندرسا</option>
                <option value="کاماروسا">کاماروسا</option>
              </select>
              <p class="text-xs text-gray-400 mt-1">رقم مورد نظر خود را انتخاب کنید</p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                <svg class="w-4 h-4 inline ml-1 text-gray-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
                مرحله رشد
              </label>
              <select v-model="selectedStage" @change="onStageChange" class="w-full px-3 py-2.5 bg-[var(--bg-primary)] border border-gray-200 rounded-xl focus:border-green-500 focus:ring-1 focus:ring-green-500 transition">
                <option value="">انتخاب کنید</option>
                <option value="استقرار نشاء">استقرار نشاء</option>
                <option value="ریشه‌زایی">ریشه‌زایی</option>
                <option value="رشد رویشی">رشد رویشی</option>
                <option value="گلدهی">گلدهی</option>
                <option value="میوه‌دهی">میوه‌دهی</option>
              </select>
              <p class="text-xs text-gray-400 mt-1">مرحله رشدی گیاه را انتخاب کنید</p>
            </div>
          </div>

          <!-- Cultivation Type - New Field -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">
              <svg class="w-4 h-4 inline ml-1 text-gray-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              بستر کشت
            </label>
            <select v-model="cultivationType" class="w-full px-3 py-2.5 bg-[var(--bg-primary)] border border-gray-200 rounded-xl" disabled>
              <option value="هیدروپونیک">هیدروپونیک</option>
            </select>
            <p class="text-xs text-gray-400 mt-1">بستر کشت انتخابی - هیدروپونیک</p>
          </div>

          <!-- Brand Filter - Multi Select -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">
              <svg class="w-4 h-4 inline ml-1 text-gray-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2v16z" />
              </svg>
              فیلتر برند (اختیاری - چندگانه)
            </label>

            <!-- Multi-select dropdown -->
            <div class="relative">
              <button
                @click="brandDropdownOpen = !brandDropdownOpen"
                type="button"
                class="w-full px-3 py-2.5 bg-[var(--bg-primary)] border border-gray-200 rounded-xl text-right flex justify-between items-center focus:border-green-500 focus:ring-1 focus:ring-green-500 transition"
              >
                <span class="text-gray-700">
                  {{ selectedBrands.length === 0 ? 'همه برندها' : selectedBrands.length + ' برند انتخاب شده' }}
                </span>
                <svg class="w-4 h-4 text-gray-500" :class="{ 'rotate-180': brandDropdownOpen }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <div v-if="brandDropdownOpen" class="absolute z-20 mt-1 w-full bg-[var(--bg-card)] border border-gray-200 rounded-xl shadow-lg max-h-60 overflow-y-auto">
                <div class="p-2">
                  <label class="flex items-center gap-2 p-2 hover:bg-[var(--bg-primary)] rounded-lg cursor-pointer">
                    <input type="checkbox" v-model="selectAllBrands" @change="toggleAllBrands" class="w-4 h-4 text-green-600 rounded">
                    <span class="text-sm font-medium text-gray-700">انتخاب همه برندها</span>
                  </label>
                  <div class="border-t my-2"></div>
                  <div v-for="brand in allBrandsList" :key="brand" class="flex items-center gap-2 p-2 hover:bg-[var(--bg-primary)] rounded-lg cursor-pointer">
                    <input type="checkbox" v-model="selectedBrands" :value="brand" class="w-4 h-4 text-green-600 rounded">
                    <span class="text-sm text-gray-700">{{ brand }}</span>
                  </div>
                </div>
              </div>
            </div>
            <p class="text-xs text-gray-400 mt-1">می‌توانید یک یا چند برند را انتخاب کنید. در صورت عدم انتخاب، همه برندها در نظر گرفته می‌شوند.</p>
          </div>

          <!-- ============================================================ -->
          <!-- تنظیمات پیشرفته: ویرایش دستی نیازهای گیاه (منو کشویی) -->
          <!-- ============================================================ -->
          <div class="border border-gray-300 rounded-xl overflow-hidden">
            <button
              @click="advancedSettingsOpen = !advancedSettingsOpen"
              type="button"
              class="w-full px-4 py-3 bg-gray-100 hover:bg-gray-200 transition flex justify-between items-center text-right"
            >
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-gray-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span class="font-medium text-gray-700">⚙️ تنظیمات پیشرفته - ویرایش دستی نیازهای گیاه</span>
              </div>
              <svg class="w-5 h-5 text-gray-500 transition-transform" :class="{ 'rotate-180': advancedSettingsOpen }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <div v-if="advancedSettingsOpen" class="p-5 border-t border-gray-200">
              <p class="text-sm text-amber-600 mb-4 flex items-center gap-2">
                <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                ⚠️ توجه: تغییر این مقادیر فقط برای محاسبه فعلی اعمال می‌شود و در دیتابیس ذخیره نمی‌شود.
              </p>

              <div class="overflow-x-auto">
                <table class="w-full text-sm border-collapse">
                  <thead>
                    <tr class="bg-gray-100">
                      <th class="border border-gray-300 px-3 py-2 text-right">عنصر</th>
                      <th class="border border-gray-300 px-3 py-2 text-center">نیاز گیاه (ppm)</th>
                      <th class="border border-gray-300 px-3 py-2 text-center">واحد</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="nutrient in editableNutrients" :key="nutrient.element" class="hover:bg-[var(--bg-primary)]">
                      <td class="border border-gray-300 px-3 py-2 font-medium">{{ nutrient.name }} ({{ nutrient.element }})</td>
                      <td class="border border-gray-300 px-3 py-2 text-center">
                        <input
                          type="number"
                          v-model.number="nutrient.value"
                          class="w-24 px-2 py-1 text-center border border-gray-300 rounded focus:border-green-500 focus:ring-1 focus:ring-green-500"
                          step="1"
                          min="0"
                        >
                      </td>
                      <td class="border border-gray-300 px-3 py-2 text-center text-gray-500">ppm</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <button
                @click="resetNutrientsToDefault"
                type="button"
                class="mt-4 text-sm text-blue-600 hover:text-blue-800 transition flex items-center gap-1"
              >
                <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                بازنشانی به مقادیر پیش‌فرض مرحله رشد
              </button>
            </div>
          </div>

          <!-- ============================================================ -->
          <!-- 🆕 بخش آنالیز آب و پساب ترکیبی (نسخه 3.4.0) -->
          <!-- ============================================================ -->
          <div class="border border-teal-200 rounded-xl overflow-hidden">
            <button
              @click="waterAnalysisOpen = !waterAnalysisOpen"
              type="button"
              class="w-full px-4 py-3 bg-teal-50 hover:bg-teal-100 transition flex justify-between items-center text-right"
            >
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-teal-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
                <span class="font-medium text-teal-700">💧 آنالیز آب و پساب ترکیبی</span>
                <span class="text-xs text-teal-500">(اختیاری - برای محاسبه دقیق‌تر)</span>
              </div>
              <svg class="w-5 h-5 text-teal-500 transition-transform" :class="{ 'rotate-180': waterAnalysisOpen }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            <div v-if="waterAnalysisOpen" class="p-5 border-t border-teal-200">
              <p class="text-sm text-gray-600 mb-4 flex items-center gap-2">
                <svg class="w-5 h-5 text-teal-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                مقادیر آب و پساب خود را وارد کنید. نرم‌افزار به‌صورت خودکار مقادیر تامینی را محاسبه و از نیازهای گیاه کسر می‌کند.
              </p>

              <!-- درصدهای آب و پساب -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">
                    استفاده از آب (%)
                  </label>
                  <div class="flex items-center gap-3">
                    <input
                      type="range"
                      v-model.number="waterPercent"
                      min="0"
                      max="100"
                      class="flex-1 accent-teal-600"
                    >
                    <span class="w-16 text-center font-bold text-teal-700">{{ waterPercent }}%</span>
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">
                    استفاده از پساب (%)
                  </label>
                  <div class="flex items-center gap-3">
                    <input
                      type="range"
                      v-model.number="wastewaterPercent"
                      min="0"
                      max="100"
                      class="flex-1 accent-orange-600"
                    >
                    <span class="w-16 text-center font-bold text-orange-700">{{ wastewaterPercent }}%</span>
                  </div>
                  <p class="text-xs text-gray-400 mt-1">مجموع: {{ waterPercent + wastewaterPercent }}%</p>
                </div>
              </div>

              <!-- جداول آنالیز -->
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- آنالیز آب -->
                <div class="border border-blue-200 rounded-lg p-4 bg-blue-50/30">
                  <h4 class="font-semibold text-blue-700 mb-3 flex items-center gap-2">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                    </svg>
                    آنالیز آب
                  </h4>
                  <div class="grid grid-cols-2 gap-2">
                    <div v-for="(value, key) in waterAnalysis" :key="key" class="flex items-center gap-2">
                      <label class="text-xs text-gray-600 w-12">{{ getElementLabel(key) }}</label>
                      <input
                        type="number"
                        v-model.number="waterAnalysis[key]"
                        class="flex-1 px-2 py-1 text-xs border border-gray-200 rounded focus:border-blue-500 focus:ring-1 focus:ring-blue-500 bg-[var(--bg-primary)]"
                        step="0.1"
                        min="0"
                      >
                    </div>
                  </div>
                </div>

                <!-- آنالیز پساب -->
                <div class="border border-orange-200 rounded-lg p-4 bg-orange-50/30">
                  <h4 class="font-semibold text-orange-700 mb-3 flex items-center gap-2">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                    </svg>
                    آنالیز پساب
                  </h4>
                  <div class="grid grid-cols-2 gap-2">
                    <div v-for="(value, key) in wastewaterAnalysis" :key="key" class="flex items-center gap-2">
                      <label class="text-xs text-gray-600 w-12">{{ getElementLabel(key) }}</label>
                      <input
                        type="number"
                        v-model.number="wastewaterAnalysis[key]"
                        class="flex-1 px-2 py-1 text-xs border border-gray-200 rounded focus:border-orange-500 focus:ring-1 focus:ring-orange-500 bg-[var(--bg-primary)]"
                        step="0.1"
                        min="0"
                      >
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-4 text-xs text-gray-500 bg-gray-50 rounded-lg p-3 border border-gray-200">
                <span class="font-medium">💡 نکته:</span>
                عناصر با رنگ {{ waterPercent }}% آب و {{ wastewaterPercent }}% پساب ترکیب می‌شوند و از نیازهای گیاه کسر می‌گردند.
              </div>
            </div>
          </div>

          <!-- ============================================================ -->
          <!-- بخش آب (منبع مشترک) -->
          <!-- ============================================================ -->
          <div class="border border-green-200 rounded-xl overflow-hidden">
            <div class="bg-green-50 px-4 py-3 border-b border-green-200">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-green-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
                <h3 class="font-semibold text-green-800">اطلاعات آب (منبع مشترک)</h3>
              </div>
              <p class="text-xs text-green-600 mt-1">اطلاعات کیفیت آب - این مقادیر برای هر دو مخزن یکسان خواهد بود</p>
            </div>
            <div class="p-4">
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">

                <!-- EC Water -->
                <InputField
                  v-model.number="waterSource.water_ec_ms_cm"
                  label="EC آب (mS/cm)"
                  type="number"
                  placeholder="0.4"
                  icon="M13 10V3L4 14h7v7l9-11h-7z"
                  :step="0.1"
                  :min="0"
                  help-text="بازه ایده‌آل: 0.2 - 0.8 mS/cm - مقدار پیش‌فرض 0.4"
                />

                <!-- pH Water -->
                <InputField
                  v-model.number="waterSource.water_ph"
                  label="pH آب"
                  type="number"
                  placeholder="7.0"
                  icon="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 6.34l-1.41-1.41M17.66 6.34l1.41-1.41"
                  :step="0.1"
                  :min="0"
                  :max="14"
                  help-text="بازه ایده‌آل: 6.0 - 7.0 - مقدار پیش‌فرض 7.0"
                />

                <!-- Calcium Water -->
                <InputField
                  v-model.number="waterSource.water_ca_ppm"
                  label="کلسیم آب (ppm)"
                  type="number"
                  placeholder="50"
                  icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2zM12 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z"
                  :step="1"
                  :min="0"
                  help-text="بازه ایده‌آل: 40 - 80 ppm - مقدار پیش‌فرض 50"
                />

                <!-- Magnesium Water -->
                <InputField
                  v-model.number="waterSource.water_mg_ppm"
                  label="منیزیم آب (ppm)"
                  type="number"
                  placeholder="20"
                  icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2zM12 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z"
                  :step="1"
                  :min="0"
                  help-text="بازه ایده‌آل: 15 - 30 ppm - مقدار پیش‌فرض 20"
                />

                <!-- Bicarbonate Water -->
                <InputField
                  v-model.number="waterSource.water_hco3_ppm"
                  label="بیکربنات (ppm)"
                  type="number"
                  placeholder="0"
                  icon="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  :step="1"
                  :min="0"
                  help-text="بازه ایده‌آل: 0 - 100 ppm - مقدار پیش‌فرض 0"
                />

                <!-- Chlorine Water -->
                <InputField
                  v-model.number="waterSource.water_cl_ppm"
                  label="کلر آب (ppm)"
                  type="number"
                  placeholder="0"
                  icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2-1.343-2-3-2z"
                  :step="1"
                  :min="0"
                  help-text="بازه ایده‌آل: 0 - 50 ppm - مقدار پیش‌فرض 0"
                />

              </div>
            </div>
          </div>

          <!-- ============================================================ -->
          <!-- مخزن اصلی -->
          <!-- ============================================================ -->
          <div class="border border-blue-200 rounded-xl overflow-hidden">
            <div class="bg-blue-50 px-4 py-3 border-b border-blue-200">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-blue-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
                <h3 class="font-semibold text-blue-800">مخزن اصلی (کودهای غیر کلسیمی)</h3>
              </div>
              <p class="text-xs text-blue-600 mt-1">این مخزن برای کودهای NPK، سولفات‌ها و ریز مغذی‌ها استفاده می‌شود</p>
            </div>
            <div class="p-4">
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <InputField
                  v-model="tankMain.name"
                  label="نام مخزن"
                  placeholder="مثال: مخزن اصلی"
                  icon="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
                  :required="true"
                />
                <InputField
                  v-model.number="tankMain.volume_liters"
                  label="حجم مخزن (لیتر)"
                  type="number"
                  placeholder="100"
                  icon="M4 20h16a2 2 0 002-2V8a2 2 0 00-2-2h-7.93a2 2 0 01-1.66-.9l-.82-1.2A2 2 0 007.93 3H4a2 2 0 00-2 2v13a2 2 0 002 2z"
                  :step="1"
                  :min="1"
                  :required="true"
                  help-text="حجم مخزن بر حسب لیتر - مقدار پیش‌فرض 100 لیتر"
                />
              </div>
            </div>
          </div>

          <!-- ============================================================ -->
          <!-- مخزن کلسیم -->
          <!-- ============================================================ -->
          <div class="border border-amber-200 rounded-xl overflow-hidden">
            <div class="bg-amber-50 px-4 py-3 border-b border-amber-200">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-amber-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
                <h3 class="font-semibold text-amber-800">مخزن کلسیم (کودهای حاوی کلسیم)</h3>
              </div>
              <p class="text-xs text-amber-600 mt-1">این مخزن فقط برای کودهای حاوی کلسیم مانند نیترات کلسیم و کلات آهن استفاده می‌شود</p>
            </div>
            <div class="p-4">
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <InputField
                  v-model="tankCalcium.name"
                  label="نام مخزن"
                  placeholder="مثال: مخزن کلسیم"
                  icon="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
                  :required="true"
                />
                <InputField
                  v-model.number="tankCalcium.volume_liters"
                  label="حجم مخزن (لیتر)"
                  type="number"
                  placeholder="100"
                  icon="M4 20h16a2 2 0 002-2V8a2 2 0 00-2-2h-7.93a2 2 0 01-1.66-.9l-.82-1.2A2 2 0 007.93 3H4a2 2 0 00-2 2v13a2 2 0 002 2z"
                  :step="1"
                  :min="1"
                  :required="true"
                  help-text="حجم مخزن بر حسب لیتر - مقدار پیش‌فرض 100 لیتر"
                />
              </div>
            </div>
          </div>

          <!-- ============================================================ -->
          <!-- تنظیمات سیستم استوک -->
          <!-- ============================================================ -->
          <div class="border border-purple-200 rounded-xl overflow-hidden">
            <div class="bg-purple-50 px-4 py-3 border-b border-purple-200">
              <div class="flex items-center gap-2">
                <svg class="w-5 h-5 text-purple-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
                <h3 class="font-semibold text-purple-800">تنظیمات سیستم استوک (محلول مادر)</h3>
              </div>
              <p class="text-xs text-purple-600 mt-1">این تنظیمات برای محاسبه مقدار کود مورد نیاز برای ساخت استوک استفاده می‌شود</p>
            </div>
            <div class="p-4">
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <InputField
                  v-model.number="stockTankVolume"
                  label="حجم مخزن استوک (لیتر)"
                  type="number"
                  placeholder="20"
                  icon="M4 20h16a2 2 0 002-2V8a2 2 0 00-2-2h-7.93a2 2 0 01-1.66-.9l-.82-1.2A2 2 0 007.93 3H4a2 2 0 00-2 2v13a2 2 0 002 2z"
                  :step="1"
                  :min="1"
                  :max="500"
                  help-text="ظرفی که محلول استوک در آن ساخته می‌شود - پیش‌فرض 20 لیتر"
                />
                <InputField
                  v-model.number="injectorRatio"
                  label="نسبت تزریق (1 : X)"
                  type="number"
                  placeholder="200"
                  icon="M13 10V3L4 14h7v7l9-11h-7z"
                  :step="10"
                  :min="50"
                  :max="1000"
                  help-text="مثال: 200 یعنی 1 لیتر استوک + 199 لیتر آب = 200 لیتر محلول نهایی"
                />
              </div>
              <div class="mt-3 text-xs text-gray-500 bg-[var(--bg-primary)] rounded-lg p-2">
                <span class="font-medium">💡 مفهوم نسبت تزریق:</span>
                <span> به ازای هر 1 لیتر استوک، {{ injectorRatio - 1 }} لیتر آب اضافه می‌شود تا {{ injectorRatio }} لیتر محلول نهایی بدست آید.</span>
              </div>
            </div>
          </div>

          <!-- Calculate Button -->
          <button
            @click="calculateDualTank"
            :disabled="isLoading || !selectedVariety || !selectedStage"
            class="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium py-3 rounded-xl transition-all duration-200 flex items-center justify-center gap-2"
          >
            <svg v-if="isLoading" class="w-5 h-5 animate-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            {{ isLoading ? 'در حال محاسبه...' : 'محاسبه ترکیب بهینه دو مخزن' }}
          </button>
        </div>
      </div>

      <!-- Errors -->
      <div v-if="validationErrors.length > 0" class="mt-6 bg-red-50 border border-red-200 rounded-xl p-4">
        <div class="flex gap-3">
          <svg class="w-5 h-5 text-red-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div class="flex-1">
            <h4 class="text-sm font-bold text-red-800">خطاهای اعتبارسنجی</h4>
            <ul class="mt-1 text-sm text-red-700 list-disc list-inside">
              <li v-for="(err, idx) in validationErrors" :key="idx">{{ err }}</li>
            </ul>
          </div>
          <button @click="validationErrors = []" class="text-red-400 hover:text-red-600">✕</button>
        </div>
      </div>

      <div v-if="errorMessage" class="mt-6 bg-red-50 border border-red-200 rounded-xl p-4">
        <div class="flex gap-3">
          <svg class="w-5 h-5 text-red-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="text-sm text-red-700">{{ errorMessage }}</p>
          <button @click="errorMessage = ''" class="mr-auto text-red-400 hover:text-red-600">✕</button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="mt-8 flex justify-center">
        <div class="bg-[var(--bg-card)] rounded-xl shadow-card px-6 py-4 flex items-center gap-3">
          <div class="w-5 h-5 border-2 border-green-500 border-t-transparent rounded-full animate-spin"></div>
          <span class="text-gray-600">در حال محاسبه...</span>
        </div>
      </div>

      <!-- Results -->
      <div v-if="result" class="mt-8">
        <ResultsDisplay
          :result="result"
          :stock-tank-volume="stockTankVolume"
          :injector-ratio="injectorRatio"
        />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import ResultsDisplay from '../components/calculator/ResultsDisplay.vue'
import InputField from '../components/common/InputField.vue'
import ThemeToggle from '../components/common/ThemeToggle.vue'

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'

const connectionStatus = ref('checking')
const selectedCrop = ref('توت‌فرنگی')
const cultivationType = ref('هیدروپونیک')
const selectedVariety = ref('')
const selectedStage = ref('')
const isLoading = ref(false)
const isLoadingFertilizers = ref(false)
const result = ref<any>(null)
const errorMessage = ref('')
const validationErrors = ref<string[]>([])
const showFertilizerList = ref(false)
const fertilizers = ref<any[]>([])

// ============================================================
// فیلدهای جدید سیستم استوک
// ============================================================
const stockTankVolume = ref(20)
const injectorRatio = ref(200)

// ============================================================
// 🆕 Stateهای جدید برای آنالیز آب و پساب (نسخه 3.4.0)
// ============================================================

// درصدهای آب و پساب
const waterPercent = ref(80)
const wastewaterPercent = ref(20)

// آنالیز آب (14 عنصر + EC + pH)
const waterAnalysis = ref({
  n_no3: 10,
  p: 2,
  s: 5,
  n_nh4: 0,
  k: 8,
  ca: 50,
  mg: 20,
  na: 5,
  cl: 5,
  fe: 0.5,
  mn: 0.1,
  zn: 0.05,
  b: 0.2,
  cu: 0.02,
  mo: 0.01,
  ec: 0.4,
  ph: 7.0
})

// آنالیز پساب (14 عنصر + EC + pH)
const wastewaterAnalysis = ref({
  n_no3: 25,
  p: 5,
  s: 10,
  n_nh4: 2,
  k: 15,
  ca: 80,
  mg: 30,
  na: 10,
  cl: 15,
  fe: 1.0,
  mn: 0.3,
  zn: 0.1,
  b: 0.5,
  cu: 0.05,
  mo: 0.02,
  ec: 1.2,
  ph: 6.5
})

// وضعیت نمایش بخش آنالیز آب
const waterAnalysisOpen = ref(false)

// ============================================================
// تنظیمات پیشرفته - منو کشویی
// ============================================================
const advancedSettingsOpen = ref(false)

// لیست عناصر قابل ویرایش
const editableNutrients = ref([
  { element: 'N', name: 'نیتروژن', value: 0 },
  { element: 'P', name: 'فسفر', value: 0 },
  { element: 'K', name: 'پتاسیم', value: 0 },
  { element: 'Ca', name: 'کلسیم', value: 0 },
  { element: 'Mg', name: 'منیزیم', value: 0 },
  { element: 'S', name: 'گوگرد', value: 0 },
  { element: 'Fe', name: 'آهن', value: 0 },
  { element: 'Zn', name: 'روی', value: 0 },
  { element: 'Mn', name: 'منگنز', value: 0 },
  { element: 'Cu', name: 'مس', value: 0 },
  { element: 'B', name: 'بُر', value: 0 },
  { element: 'Mo', name: 'مولیبدن', value: 0 },
  { element: 'Cl', name: 'کلر', value: 0 }
])

// ذخیره مقادیر پیش‌فرض برای بازنشانی
let defaultNutrientValues: Record<string, number> = {}

// دریافت نیازهای گیاه از دیتابیس بر اساس مرحله رشد
const fetchNutrientNeeds = async (stageName: string) => {
  if (!stageName) return

  try {
    const response = await axios.get(`${API_BASE_URL}/growth-stages`)
    const stages = response.data

    // پیدا کردن مرحله رشد مناسب
    const stage = stages.find((s: any) => s.name === stageName)

    if (stage && stage.nutrient_needs) {
      const needs = stage.nutrient_needs

      // به‌روزرسانی مقادیر editableNutrients
      for (const nutrient of editableNutrients.value) {
        const value = needs[nutrient.element] || 0
        nutrient.value = value
        defaultNutrientValues[nutrient.element] = value
      }
    }
  } catch (err) {
    console.error('Error fetching nutrient needs:', err)
  }
}

// بازنشانی به مقادیر پیش‌فرض
const resetNutrientsToDefault = () => {
  for (const nutrient of editableNutrients.value) {
    nutrient.value = defaultNutrientValues[nutrient.element] || 0
  }
}

// دریافت نیازهای گیاه به صورت آبجکت برای ارسال به سرور
const getCustomNutrientNeeds = () => {
  const needs: Record<string, number> = {}
  for (const nutrient of editableNutrients.value) {
    needs[nutrient.element] = nutrient.value
  }
  return needs
}

// وقتی مرحله رشد تغییر می‌کند، نیازهای گیاه را از دیتابیس بگیر
const onStageChange = () => {
  if (selectedStage.value) {
    fetchNutrientNeeds(selectedStage.value)
  }
}

// ============================================================
// فیلدهای فیلتر برند (Multi-Select)
// ============================================================
const brandDropdownOpen = ref(false)
const allBrandsList = ref<string[]>([
  'گل سم گرگان',
  'رازاک شیمی',
  'گرین استار',
  'زاگرا استار',
  'اطلس',
  'ردسا'
])
const selectedBrands = ref<string[]>([])
const selectAllBrands = ref(false)

const toggleAllBrands = () => {
  if (selectAllBrands.value) {
    selectedBrands.value = [...allBrandsList.value]
  } else {
    selectedBrands.value = []
  }
}

// ============================================================
// فیلدهای منبع آب (یک منبع مشترک)
// ============================================================
const waterSource = ref({
  water_ec_ms_cm: 0.4,
  water_ph: 7.0,
  water_ca_ppm: 50,
  water_mg_ppm: 20,
  water_hco3_ppm: 0,
  water_cl_ppm: 0,
  water_na_ppm: 0,
  water_so4_ppm: 0,
  water_no3_ppm: 0,
  water_fe_ppm: 0
})

// مخزن اصلی
const tankMain = ref({
  name: 'مخزن اصلی',
  tank_type: 'main',
  volume_liters: 100
})

// مخزن کلسیم
const tankCalcium = ref({
  name: 'مخزن کلسیم',
  tank_type: 'calcium',
  volume_liters: 100
})

// ============================================================
// توابع کمکی
// ============================================================

const getElementLabel = (key: string): string => {
  const labels: Record<string, string> = {
    'n_no3': 'NO3',
    'p': 'P',
    's': 'S',
    'n_nh4': 'NH4',
    'k': 'K',
    'ca': 'Ca',
    'mg': 'Mg',
    'na': 'Na',
    'cl': 'Cl',
    'fe': 'Fe',
    'mn': 'Mn',
    'zn': 'Zn',
    'b': 'B',
    'cu': 'Cu',
    'mo': 'Mo',
    'ec': 'EC',
    'ph': 'pH'
  }
  return labels[key] || key
}

const getFertilizerDescription = (name: string) => {
  const descriptions: Record<string, string> = {
    'نیترات کلسیم': 'منبع کلسیم و نیتروژن - برای رشد ساختار گیاه و جلوگیری از پوسیدگی گلگاه',
    'سولفات منیزیم': 'منبع منیزیم و گوگرد - برای تولید کلروفیل و فعالسازی آنزیم‌ها',
    'سولفات پتاسیم': 'منبع پتاسیم و گوگرد - برای کیفیت میوه و مقاومت به تنش',
    'کلات آهن': 'منبع آهن - برای جلوگیری از زردی برگ‌ها (کلروز)',
    'فرتی‌گل 20-20-20': 'کود کامل NPK متعادل - مناسب برای رشد عمومی و مراحل اولیه',
    'فرتی‌گل 36-12-12': 'کود NPK با پتاسیم بالا - مناسب برای میوه‌دهی و افزایش کیفیت',
    'فرتی‌گل 10-50-10': 'کود NPK با فسفر بالا - مناسب برای ریشه‌زایی و گلدهی',
    'فرتی‌گل 30-5-15': 'کود NPK با نیتروژن بالا - مناسب برای رشد رویشی',
    'یونی کمپلکس پودری': 'کود کامل ریز مغذی‌ها - برای تامین عناصر کم مصرف',
    'NPK 20-20-20 گرین استار': 'کود NPK متعادل - مناسب برای رشد عمومی',
    'NPK 12-12-36 گرین استار': 'کود NPK با پتاسیم بالا - مناسب برای میوه‌دهی',
    'NPK 10-52-10 زاگرا استار': 'کود NPK با فسفر بالا - مناسب برای ریشه‌زایی',
    'کلرید پتاسیم': 'منبع پتاسیم و کلر - برای تغذیه عمومی (در آب با کلر پایین)'
  }
  return descriptions[name] || 'کود مغذی برای تامین عناصر مورد نیاز گیاه'
}

const fetchFertilizers = async () => {
  isLoadingFertilizers.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/fertilizers`)
    fertilizers.value = response.data
  } catch (err) {
    console.error('Error fetching fertilizers:', err)
  } finally {
    isLoadingFertilizers.value = false
  }
}

const checkConnection = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`)
    if (response.data && response.data.status === 'ok') {
      connectionStatus.value = 'connected'
      console.log('Connected to server')
      await fetchFertilizers()
    } else {
      connectionStatus.value = 'disconnected'
      errorMessage.value = 'خطا در اتصال به سرور'
    }
  } catch (err: any) {
    console.error('Connection error:', err.message)
    connectionStatus.value = 'disconnected'
    errorMessage.value = 'خطا در اتصال به سرور. لطفاً سرور بک‌اند را بررسی کنید.'
  }
}

const calculateDualTank = async () => {
  validationErrors.value = []

  if (!selectedVariety.value) {
    validationErrors.value.push('لطفاً رقم گیاه را انتخاب کنید')
  }
  if (!selectedStage.value) {
    validationErrors.value.push('لطفاً مرحله رشد را انتخاب کنید')
  }

  const mainVolume = Number(tankMain.value.volume_liters)
  if (isNaN(mainVolume) || mainVolume <= 0) {
    validationErrors.value.push('حجم مخزن اصلی معتبر نیست (باید عدد مثبت باشد)')
  }

  const calciumVolume = Number(tankCalcium.value.volume_liters)
  if (isNaN(calciumVolume) || calciumVolume <= 0) {
    validationErrors.value.push('حجم مخزن کلسیم معتبر نیست (باید عدد مثبت باشد)')
  }

  if (validationErrors.value.length > 0) {
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  result.value = null

  try {
    const payload = {
      crop_name: selectedCrop.value,
      variety_name: selectedVariety.value,
      stage_name: selectedStage.value,
      brand_filter: selectedBrands.value.length > 0 ? selectedBrands.value : null,
      custom_nutrient_needs: getCustomNutrientNeeds(),
      tank_main: {
        name: tankMain.value.name,
        tank_type: tankMain.value.tank_type,
        volume_liters: mainVolume,
        water_ec_ms_cm: waterSource.value.water_ec_ms_cm,
        water_ph: waterSource.value.water_ph,
        water_ca_ppm: waterSource.value.water_ca_ppm,
        water_mg_ppm: waterSource.value.water_mg_ppm,
        water_hco3_ppm: waterSource.value.water_hco3_ppm,
        water_cl_ppm: waterSource.value.water_cl_ppm,
        water_na_ppm: waterSource.value.water_na_ppm,
        water_so4_ppm: waterSource.value.water_so4_ppm,
        water_no3_ppm: waterSource.value.water_no3_ppm,
        water_fe_ppm: waterSource.value.water_fe_ppm
      },
      tank_calcium: {
        name: tankCalcium.value.name,
        tank_type: tankCalcium.value.tank_type,
        volume_liters: calciumVolume,
        water_ec_ms_cm: waterSource.value.water_ec_ms_cm,
        water_ph: waterSource.value.water_ph,
        water_ca_ppm: waterSource.value.water_ca_ppm,
        water_mg_ppm: waterSource.value.water_mg_ppm,
        water_hco3_ppm: waterSource.value.water_hco3_ppm,
        water_cl_ppm: waterSource.value.water_cl_ppm,
        water_na_ppm: waterSource.value.water_na_ppm,
        water_so4_ppm: waterSource.value.water_so4_ppm,
        water_no3_ppm: waterSource.value.water_no3_ppm,
        water_fe_ppm: waterSource.value.water_fe_ppm
      },
      stock_tank_volume_liters: stockTankVolume.value,
      injector_ratio: injectorRatio.value,
      // 🆕 فیلدهای جدید برای آنالیز آب و پساب
      water_percent: waterPercent.value,
      wastewater_percent: wastewaterPercent.value,
      water_analysis: waterAnalysis.value,
      wastewater_analysis: wastewaterAnalysis.value
    }

    console.log('Sending request with water analysis:', payload.water_analysis)
    const response = await axios.post(`${API_BASE_URL}/calculate-dual-tank`, payload)

    if (response.data.success) {
      result.value = response.data
      console.log('Calculation successful')
    } else {
      errorMessage.value = response.data.error_message || 'خطا در محاسبه'
    }
  } catch (err: any) {
    console.error('Calculation error:', err)
    if (err.response?.data?.detail) {
      if (typeof err.response.data.detail === 'string') {
        errorMessage.value = err.response.data.detail
      } else if (Array.isArray(err.response.data.detail)) {
        validationErrors.value = err.response.data.detail.map((e: any) => {
          if (e.msg === 'Input should be a valid number') {
            return 'لطفاً مقدار معتبر برای حجم مخزن وارد کنید'
          }
          return e.msg
        })
      } else {
        errorMessage.value = JSON.stringify(err.response.data.detail)
      }
    } else if (err.message === 'Network Error') {
      errorMessage.value = 'خطا در اتصال به سرور. لطفاً از اجرای سرور بک‌اند اطمینان حاصل کنید.'
    } else {
      errorMessage.value = 'خطا در محاسبه. لطفاً دوباره تلاش کنید.'
    }
  } finally {
    isLoading.value = false
  }
}

const printResult = () => {
  window.print()
}

onMounted(() => {
  checkConnection()
})
</script>

<style scoped>
@media print {
  .no-print {
    display: none !important;
  }

  header {
    display: none !important;
  }

  button {
    display: none !important;
  }
}
</style>

```

---

## File 17: `frontend/src/components/calculator/ResultsDisplay.vue`

**Size:** 42.4 KB

```vue
<template>
  <div class="space-y-6">
    <!-- Header -->
    <div
      class="bg-gradient-to-r from-green-600 to-teal-600 rounded-2xl p-5 text-white"
    >
      <h2 class="text-xl font-bold flex items-center gap-2">
        <svg
          class="w-6 h-6"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        نتیجه محاسبات
      </h2>
      <p class="text-green-100 text-sm mt-1">
        محصول: {{ result.crop_name }} | رقم: {{ result.variety_name }} | مرحله:
        {{ result.stage_name }}
      </p>
    </div>

    <!-- بخش 1: تنظیمات شما -->
    <div
      class="bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl p-5 border border-gray-200"
    >
      <h3 class="font-bold text-gray-700 mb-4 flex items-center gap-2">
        <svg
          class="w-5 h-5 text-gray-600"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
          />
          <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        تنظیمات شما
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white rounded-lg p-3 text-center shadow-sm">
          <svg
            class="w-6 h-6 mx-auto text-green-600 mb-1"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
            />
          </svg>
          <div class="text-xs text-gray-500">مرحله رشد</div>
          <div class="font-bold text-gray-800">{{ result.stage_name }}</div>
        </div>
        <div class="bg-white rounded-lg p-3 text-center shadow-sm">
          <svg
            class="w-6 h-6 mx-auto text-blue-600 mb-1"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M4 20h16a2 2 0 002-2V8a2 2 0 00-2-2h-7.93a2 2 0 01-1.66-.9l-.82-1.2A2 2 0 007.93 3H4a2 2 0 00-2 2v13a2 2 0 002 2z"
            />
          </svg>
          <div class="text-xs text-gray-500">حجم مخزن اصلی</div>
          <div class="font-bold text-gray-800">
            {{ formatNumber(result.tank_main_result?.tank_volume_liters || 0) }}
            <span class="text-sm font-normal">لیتر</span>
          </div>
        </div>
        <div class="bg-white rounded-lg p-3 text-center shadow-sm">
          <svg
            class="w-6 h-6 mx-auto text-amber-600 mb-1"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
            />
          </svg>
          <div class="text-xs text-gray-500">حجم مخزن کلسیم</div>
          <div class="font-bold text-gray-800">
            {{
              formatNumber(result.tank_calcium_result?.tank_volume_liters || 0)
            }}
            <span class="text-sm font-normal">لیتر</span>
          </div>
        </div>
        <div class="bg-white rounded-lg p-3 text-center shadow-sm">
          <svg
            class="w-6 h-6 mx-auto text-purple-600 mb-1"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
            />
          </svg>
          <div class="text-xs text-gray-500">حجم مخزن استوک</div>
          <div class="font-bold text-gray-800">
            {{ props.stockTankVolume || 20 }}
            <span class="text-sm font-normal">لیتر</span>
          </div>
        </div>
        <div class="bg-white rounded-lg p-3 text-center shadow-sm">
          <svg
            class="w-6 h-6 mx-auto text-indigo-600 mb-1"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          <div class="text-xs text-gray-500">نسبت تزریق</div>
          <div class="font-bold text-gray-800">
            1:{{ props.injectorRatio || 200 }}
          </div>
        </div>
        <div class="bg-white rounded-lg p-3 text-center shadow-sm">
          <svg
            class="w-6 h-6 mx-auto text-gray-600 mb-1"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
          </svg>
          <div class="text-xs text-gray-500">حجم کل محلول نهایی</div>
          <div class="font-bold text-gray-800">
            {{
              (
                (result.tank_main_result?.tank_volume_liters || 0) +
                (result.tank_calcium_result?.tank_volume_liters || 0)
              ).toLocaleString()
            }}
            <span class="text-sm font-normal">لیتر</span>
          </div>
        </div>
      </div>

      <div
        class="mt-4 bg-blue-50 rounded-lg p-3 text-sm border border-blue-200"
      >
        <p class="font-medium text-blue-800 mb-1 flex items-center gap-1">
          <svg
            class="w-4 h-4"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          مفهوم نسبت تزریق 1:{{ props.injectorRatio || 200 }}
        </p>
        <p class="text-blue-700">
          به ازای هر 1 لیتر استوک، {{ (props.injectorRatio || 200) - 1 }} لیتر
          آب اضافه می‌شود تا {{ props.injectorRatio || 200 }} لیتر محلول نهایی
          بدست آید.
        </p>
      </div>
    </div>

    <!-- جدول نیاز گیاه و عناصر تامین شده -->
    <div
      class="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden"
    >
      <div class="bg-gradient-to-r from-gray-600 to-gray-700 px-5 py-3">
        <h3 class="text-white font-bold flex items-center gap-2">
          <svg
            class="w-5 h-5"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
          </svg>
          مقایسه نیاز گیاه با عناصر تامین شده
        </h3>
      </div>
      <div class="p-5">
        <div class="overflow-x-auto">
          <table class="w-full text-sm border-collapse">
            <thead>
              <tr class="bg-gray-100">
                <th class="border border-gray-300 px-3 py-2 text-right">
                  عنصر
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  نیاز گیاه (ppm)
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  تامین شده (ppm)
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  وضعیت
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in nutrientComparison"
                :key="item.element"
                class="hover:bg-gray-50"
              >
                <td class="border border-gray-300 px-3 py-2 font-medium">
                  {{ getElementName(item.element) }}
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  {{ formatNumber(item.need) }}
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  {{ formatNumber(item.supplied) }}
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  <span
                    v-if="item.status === 'ok'"
                    class="text-green-600 font-medium"
                    >✓ کافی</span
                  >
                  <span
                    v-else-if="item.status === 'low'"
                    class="text-amber-600 font-medium"
                    >⚠️ کم</span
                  >
                  <span v-else class="text-red-600 font-medium"
                    >✗ بسیار کم</span
                  >
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- مخزن اصلی -->
    <div
      class="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden"
    >
      <div class="bg-gradient-to-r from-blue-600 to-indigo-600 px-5 py-3">
        <h3 class="text-white font-bold flex items-center justify-between">
          <span class="flex items-center gap-2">
            <svg
              class="w-5 h-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
              />
            </svg>
            مخزن اصلی (کودهای غیر کلسیمی)
          </span>
          <span class="text-xs bg-white/20 px-2 py-1 rounded-full">{{
            result.tank_main_result.tank_name
          }}</span>
        </h3>
      </div>

      <div class="p-5">
        <div class="overflow-x-auto mb-4">
          <table class="w-full text-sm border-collapse">
            <thead>
              <tr class="bg-gray-100">
                <th class="border border-gray-300 px-3 py-2 text-right">
                  نام کود
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  مصرف (g/L)
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  مجموع برای مخزن
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  مقدار برای استوک
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center"></th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="dose in result.tank_main_result.doses"
                :key="dose.name"
                class="hover:bg-gray-50"
              >
                <td class="border border-gray-300 px-3 py-2 font-medium">
                  {{ dose.persian_name || dose.name }}
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  {{ dose.dose_g_per_liter }} g/L
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  {{ formatNumber(dose.dose_g_for_tank) }} گرم
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  <span v-if="getStockAmount(dose) >= 1000"
                    >{{
                      (getStockAmount(dose) / 1000).toFixed(2)
                    }}
                    کیلوگرم</span
                  >
                  <span v-else-if="getStockAmount(dose) >= 1"
                    >{{ getStockAmount(dose).toFixed(0) }} گرم</span
                  >
                  <span v-else
                    >{{
                      (getStockAmount(dose) * 1000).toFixed(0)
                    }}
                    میلی‌گرم</span
                  >
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  <button
                    @click="showFertilizerDetail(dose.name)"
                    class="text-blue-600 hover:text-blue-800 transition"
                    title="مشاهده اطلاعات کامل کود"
                  >
                    <svg
                      class="w-5 h-5 inline"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <circle cx="12" cy="12" r="10" />
                      <path d="M12 16v-4M12 8h.01" />
                    </svg>
                    اطلاعات
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="grid grid-cols-2 gap-3 mb-4">
          <div class="bg-blue-50 rounded-lg p-3 text-center">
            <span class="font-bold text-blue-700">EC پیش‌بینی شده:</span>
            <span class="text-blue-700 font-bold mx-2"
              >{{ result.tank_main_result.target_ec || "---" }} mS/cm</span
            >
          </div>
          <div class="bg-blue-50 rounded-lg p-3 text-center">
            <span class="font-bold text-blue-700">pH هدف:</span>
            <span class="text-blue-700 font-bold mx-2">{{
              result.tank_main_result.target_ph || "5.8 - 6.2"
            }}</span>
          </div>
        </div>

        <div class="bg-purple-50 rounded-lg p-3 mb-3">
          <h4 class="font-medium text-purple-800 mb-2 flex items-center gap-1">
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
              />
            </svg>
            مرحله 1: ساخت استوک برای مخزن اصلی
          </h4>
          <p class="text-sm text-gray-700 mb-2">
            برای ساخت {{ props.stockTankVolume || 20 }} لیتر استوک با نسبت 1:{{
              props.injectorRatio || 200
            }}، مقادیر زیر را با دقت اندازه گیری کنید:
          </p>
          <div class="bg-white rounded-lg p-3">
            <div
              v-for="dose in result.tank_main_result.doses"
              :key="dose.name"
              class="flex justify-between items-center py-1 border-b border-gray-100 last:border-0"
            >
              <span class="text-sm font-medium">{{
                dose.persian_name || dose.name
              }}</span>
              <span class="text-sm text-gray-600">
                <span v-if="getStockAmount(dose) >= 1000"
                  >{{ (getStockAmount(dose) / 1000).toFixed(2) }} کیلوگرم</span
                >
                <span v-else-if="getStockAmount(dose) >= 1"
                  >{{ getStockAmount(dose).toFixed(0) }} گرم</span
                >
                <span v-else
                  >{{ (getStockAmount(dose) * 1000).toFixed(0) }} میلی‌گرم</span
                >
              </span>
            </div>
          </div>
        </div>

        <div class="bg-green-50 rounded-lg p-3 mb-3">
          <h4 class="font-medium text-green-800 mb-2 flex items-center gap-1">
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            مرحله 2: مصرف استوک در مخزن اصلی
          </h4>
          <div class="grid grid-cols-2 gap-3 mb-2">
            <div class="bg-white rounded-lg p-2 text-center">
              <p class="text-lg font-bold text-green-700">
                {{
                  (
                    (result.tank_main_result.tank_volume_liters || 0) /
                    (props.injectorRatio || 200)
                  ).toFixed(1)
                }}
                لیتر
              </p>
              <p class="text-xs text-gray-600">
                استوک برای مخزن
                {{
                  formatNumber(result.tank_main_result.tank_volume_liters || 0)
                }}
                لیتری
              </p>
            </div>
            <div class="bg-white rounded-lg p-2 text-center">
              <p class="text-lg font-bold text-green-700">
                {{ (1000 / (props.injectorRatio || 200)).toFixed(1) }} میلی‌لیتر
              </p>
              <p class="text-xs text-gray-600">استوک برای هر 1 لیتر آب</p>
            </div>
          </div>
        </div>

        <details class="mt-3">
          <summary
            class="cursor-pointer text-blue-600 hover:text-blue-700 font-medium text-sm inline-flex items-center gap-1"
          >
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            مشاهده دستورالعمل اختلاط مستقیم (بدون استوک)
          </summary>
          <div
            class="mt-3 p-4 bg-gray-100 rounded-lg text-sm whitespace-pre-line font-mono"
            v-html="
              formatInstructions(result.tank_main_result.mixing_instructions)
            "
          ></div>
        </details>
      </div>
    </div>

    <!-- مخزن کلسیم -->
    <div
      class="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden"
    >
      <div class="bg-gradient-to-r from-amber-600 to-orange-600 px-5 py-3">
        <h3 class="text-white font-bold flex items-center justify-between">
          <span class="flex items-center gap-2">
            <svg
              class="w-5 h-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
              />
            </svg>
            مخزن کلسیم (کودهای حاوی کلسیم)
          </span>
          <span class="text-xs bg-white/20 px-2 py-1 rounded-full">{{
            result.tank_calcium_result.tank_name
          }}</span>
        </h3>
      </div>

      <div class="p-5">
        <div class="overflow-x-auto mb-4">
          <table class="w-full text-sm border-collapse">
            <thead>
              <tr class="bg-gray-100">
                <th class="border border-gray-300 px-3 py-2 text-right">
                  نام کود
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  مصرف (g/L)
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  مجموع برای مخزن
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center">
                  مقدار برای استوک
                </th>
                <th class="border border-gray-300 px-3 py-2 text-center"></th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="dose in result.tank_calcium_result.doses"
                :key="dose.name"
                class="hover:bg-gray-50"
              >
                <td class="border border-gray-300 px-3 py-2 font-medium">
                  {{ dose.persian_name || dose.name }}
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  {{ dose.dose_g_per_liter }} g/L
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  {{ formatNumber(dose.dose_g_for_tank) }} گرم
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  <span v-if="getStockAmount(dose) >= 1000"
                    >{{
                      (getStockAmount(dose) / 1000).toFixed(2)
                    }}
                    کیلوگرم</span
                  >
                  <span v-else-if="getStockAmount(dose) >= 1"
                    >{{ getStockAmount(dose).toFixed(0) }} گرم</span
                  >
                  <span v-else
                    >{{
                      (getStockAmount(dose) * 1000).toFixed(0)
                    }}
                    میلی‌گرم</span
                  >
                </td>
                <td class="border border-gray-300 px-3 py-2 text-center">
                  <button
                    @click="showFertilizerDetail(dose.name)"
                    class="text-amber-600 hover:text-amber-800 transition"
                    title="مشاهده اطلاعات کامل کود"
                  >
                    <svg
                      class="w-5 h-5 inline"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <circle cx="12" cy="12" r="10" />
                      <path d="M12 16v-4M12 8h.01" />
                    </svg>
                    اطلاعات
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="grid grid-cols-2 gap-3 mb-4">
          <div class="bg-amber-50 rounded-lg p-3 text-center">
            <span class="font-bold text-amber-700">EC پیش‌بینی شده:</span>
            <span class="text-amber-700 font-bold mx-2"
              >{{ result.tank_calcium_result.target_ec || "---" }} mS/cm</span
            >
          </div>
          <div class="bg-amber-50 rounded-lg p-3 text-center">
            <span class="font-bold text-amber-700">pH هدف:</span>
            <span class="text-amber-700 font-bold mx-2">{{
              result.tank_calcium_result.target_ph || "6.0 - 6.5"
            }}</span>
          </div>
        </div>

        <div class="bg-purple-50 rounded-lg p-3 mb-3">
          <h4 class="font-medium text-purple-800 mb-2 flex items-center gap-1">
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
              />
            </svg>
            مرحله 1: ساخت استوک برای مخزن کلسیم
          </h4>
          <p class="text-sm text-gray-700 mb-2">
            برای ساخت {{ props.stockTankVolume || 20 }} لیتر استوک کلسیم با نسبت
            1:{{ props.injectorRatio || 200 }}، مقادیر زیر را با دقت اندازه گیری
            کنید:
          </p>
          <div class="bg-white rounded-lg p-3">
            <div
              v-for="dose in result.tank_calcium_result.doses"
              :key="dose.name"
              class="flex justify-between items-center py-1 border-b border-gray-100 last:border-0"
            >
              <span class="text-sm font-medium">{{
                dose.persian_name || dose.name
              }}</span>
              <span class="text-sm text-gray-600">
                <span v-if="getStockAmount(dose) >= 1000"
                  >{{ (getStockAmount(dose) / 1000).toFixed(2) }} کیلوگرم</span
                >
                <span v-else-if="getStockAmount(dose) >= 1"
                  >{{ getStockAmount(dose).toFixed(0) }} گرم</span
                >
                <span v-else
                  >{{ (getStockAmount(dose) * 1000).toFixed(0) }} میلی‌گرم</span
                >
              </span>
            </div>
          </div>
        </div>

        <div class="bg-green-50 rounded-lg p-3 mb-3">
          <h4 class="font-medium text-green-800 mb-2 flex items-center gap-1">
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            مرحله 2: مصرف استوک در مخزن کلسیم
          </h4>
          <div class="grid grid-cols-2 gap-3 mb-2">
            <div class="bg-white rounded-lg p-2 text-center">
              <p class="text-lg font-bold text-green-700">
                {{
                  (
                    (result.tank_calcium_result.tank_volume_liters || 0) /
                    (props.injectorRatio || 200)
                  ).toFixed(1)
                }}
                لیتر
              </p>
              <p class="text-xs text-gray-600">
                استوک برای مخزن
                {{
                  formatNumber(
                    result.tank_calcium_result.tank_volume_liters || 0,
                  )
                }}
                لیتری
              </p>
            </div>
            <div class="bg-white rounded-lg p-2 text-center">
              <p class="text-lg font-bold text-green-700">
                {{ (1000 / (props.injectorRatio || 200)).toFixed(1) }} میلی‌لیتر
              </p>
              <p class="text-xs text-gray-600">استوک برای هر 1 لیتر آب</p>
            </div>
          </div>
        </div>

        <div class="bg-red-50 rounded-lg p-3 mb-3">
          <p class="text-sm text-red-700 flex items-center gap-2">
            <svg
              class="w-5 h-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
            هیچگاه استوک مخزن کلسیم را با استوک مخزن اصلی قبل از ورود به مخزن
            اصلی مخلوط نکنید!
          </p>
        </div>

        <details class="mt-3">
          <summary
            class="cursor-pointer text-amber-600 hover:text-amber-700 font-medium text-sm inline-flex items-center gap-1"
          >
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            مشاهده دستورالعمل اختلاط مستقیم (بدون استوک) - مخزن کلسیم
          </summary>
          <div
            class="mt-3 p-4 bg-gray-100 rounded-lg text-sm whitespace-pre-line font-mono"
            v-html="
              formatInstructions(result.tank_calcium_result.mixing_instructions)
            "
          ></div>
        </details>
      </div>
    </div>

    <!-- نکات نگهداری و ایمنی استوک -->
    <div class="bg-yellow-50 rounded-xl p-4 border border-yellow-200">
      <h3 class="font-semibold text-yellow-800 mb-3 flex items-center gap-2">
        <svg
          class="w-5 h-5"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
          />
        </svg>
        نکات نگهداری و ایمنی استوک
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
        <div class="bg-white rounded-lg p-2">
          <span class="font-bold">ماندگاری در یخچال:</span> 7 روز (دمای 4 درجه)
        </div>
        <div class="bg-white rounded-lg p-2">
          <span class="font-bold">ماندگاری در دمای محیط:</span> 3 روز (دمای زیر
          25 درجه)
        </div>
        <div class="bg-white rounded-lg p-2 col-span-2">
          <span class="font-bold">نشانه‌های خرابی:</span> رسوب سفید رنگ، تغییر
          رنگ، بوی نامطبوع، باد کردگی ظرف
        </div>
      </div>
    </div>

    <!-- مودال اطلاعات کامل کود -->
    <div
      v-if="selectedFertilizer"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      @click.self="selectedFertilizer = null"
    >
      <div
        class="bg-white rounded-2xl max-w-2xl w-full max-h-[85vh] overflow-hidden shadow-xl"
      >
        <div
          class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gradient-to-r from-green-600 to-teal-600"
        >
          <h3 class="text-lg font-semibold text-white">اطلاعات کامل کود</h3>
          <button
            @click="selectedFertilizer = null"
            class="text-white hover:text-gray-200 text-xl"
          >
            ✕
          </button>
        </div>
        <div class="p-6 overflow-y-auto max-h-[calc(85vh-70px)]">
          <div v-if="isLoadingFertilizerDetail" class="text-center py-8">
            <div
              class="inline-block w-8 h-8 border-2 border-green-500 border-t-transparent rounded-full animate-spin"
            ></div>
            <p class="mt-2 text-gray-500">در حال بارگذاری...</p>
          </div>
          <div v-else-if="fertilizerDetail" class="space-y-4">
            <div>
              <h4 class="font-bold text-gray-800 text-lg">
                {{ fertilizerDetail.persian_name || fertilizerDetail.name }}
              </h4>
              <div class="flex gap-2 mt-1">
                <span
                  class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full"
                  >{{ fertilizerDetail.brand_name }}</span
                >
                <span
                  class="text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full"
                  >{{ fertilizerDetail.fertilizer_type }}</span
                >
              </div>
            </div>

            <div class="border-t pt-3">
              <h5 class="font-semibold text-gray-700 mb-2">توضیحات</h5>
              <p class="text-sm text-gray-600 whitespace-pre-line">
                {{
                  fertilizerDetail.description ||
                  "توضیحاتی برای این کود ثبت نشده است"
                }}
              </p>
            </div>

            <div class="border-t pt-3">
              <h5 class="font-semibold text-gray-700 mb-2">ترکیبات شیمیایی</h5>
              <div class="grid grid-cols-2 md:grid-cols-3 gap-2 text-sm">
                <div v-if="fertilizerDetail.n_percent">
                  N:
                  <span class="font-medium"
                    >{{ fertilizerDetail.n_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.p_percent">
                  P:
                  <span class="font-medium"
                    >{{ fertilizerDetail.p_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.k_percent">
                  K:
                  <span class="font-medium"
                    >{{ fertilizerDetail.k_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.ca_percent">
                  Ca:
                  <span class="font-medium"
                    >{{ fertilizerDetail.ca_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.mg_percent">
                  Mg:
                  <span class="font-medium"
                    >{{ fertilizerDetail.mg_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.s_percent">
                  S:
                  <span class="font-medium"
                    >{{ fertilizerDetail.s_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.fe_percent">
                  Fe:
                  <span class="font-medium"
                    >{{ fertilizerDetail.fe_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.zn_percent">
                  Zn:
                  <span class="font-medium"
                    >{{ fertilizerDetail.zn_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.mn_percent">
                  Mn:
                  <span class="font-medium"
                    >{{ fertilizerDetail.mn_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.cu_percent">
                  Cu:
                  <span class="font-medium"
                    >{{ fertilizerDetail.cu_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.b_percent">
                  B:
                  <span class="font-medium"
                    >{{ fertilizerDetail.b_percent }}%</span
                  >
                </div>
                <div v-if="fertilizerDetail.mo_percent">
                  Mo:
                  <span class="font-medium"
                    >{{ fertilizerDetail.mo_percent }}%</span
                  >
                </div>
              </div>
            </div>

            <div class="border-t pt-3">
              <h5 class="font-semibold text-gray-700 mb-2">اطلاعات مصرف</h5>
              <div class="grid grid-cols-2 gap-2 text-sm">
                <div>
                  حداقل دوز:
                  <span class="font-medium"
                    >{{
                      fertilizerDetail.min_dose_g_per_liter || "نامشخص"
                    }}
                    g/L</span
                  >
                </div>
                <div>
                  حداکثر دوز:
                  <span class="font-medium"
                    >{{
                      fertilizerDetail.max_dose_g_per_liter || "نامشخص"
                    }}
                    g/L</span
                  >
                </div>
                <div v-if="fertilizerDetail.solubility_g_per_l">
                  حلالیت:
                  <span class="font-medium"
                    >{{ fertilizerDetail.solubility_g_per_l }} g/L</span
                  >
                </div>
                <div v-if="fertilizerDetail.ph_effect">
                  اثر بر pH:
                  <span class="font-medium">{{
                    fertilizerDetail.ph_effect
                  }}</span>
                </div>
              </div>
            </div>

            <div
              v-if="fertilizerDetail.registration_code"
              class="border-t pt-3"
            >
              <h5 class="font-semibold text-gray-700 mb-2">اطلاعات ثبتی</h5>
              <div class="text-sm">
                کد ثبت:
                <span class="font-mono">{{
                  fertilizerDetail.registration_code
                }}</span>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-500">
            اطلاعاتی برای این کود یافت نشد
          </div>
        </div>
      </div>
    </div>

    <!-- زمان محاسبه -->
    <div
      class="text-center text-xs text-gray-400 pt-4 border-t border-gray-100"
    >
      <svg
        class="w-4 h-4 inline ml-1"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      زمان محاسبه:
      {{ result.calculation_time_ms?.toFixed(0) || "0" }} میلی‌ثانیه
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import axios from "axios";

const props = defineProps<{
  result: any;
  stockTankVolume?: number;
  injectorRatio?: number;
}>();

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";

const selectedFertilizer = ref<any>(null);
const fertilizerDetail = ref<any>(null);
const isLoadingFertilizerDetail = ref(false);
const allFertilizers = ref<any[]>([]);

const fetchAllFertilizers = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/fertilizers`);
    allFertilizers.value = response.data;
  } catch (err) {
    console.error("Error fetching fertilizers:", err);
  }
};

const showFertilizerDetail = async (fertilizerName: string) => {
  isLoadingFertilizerDetail.value = true;
  selectedFertilizer.value = { name: fertilizerName };
  fertilizerDetail.value = null;

  try {
    const found = allFertilizers.value.find(
      (f: any) => f.name === fertilizerName,
    );
    if (found) {
      fertilizerDetail.value = found;
    }
  } catch (err) {
    console.error("Error fetching fertilizer detail:", err);
  } finally {
    isLoadingFertilizerDetail.value = false;
  }
};

const getStockAmount = (dose: any) => {
  const doseGpl = dose.dose_g_per_liter || 0;
  const injectorRatio = props.injectorRatio || 200;
  const stockVolume = props.stockTankVolume || 20;
  const amountGram = doseGpl * injectorRatio * stockVolume;
  return amountGram;
};

const formatNumber = (num: number) => {
  if (!num && num !== 0) return "0";
  return new Intl.NumberFormat("fa-IR").format(Math.round(num));
};

const formatInstructions = (text: string) => {
  if (!text) return "";
  return text.replace(/\n/g, "<br>").replace(/\*/g, "•");
};

const getElementName = (element: string) => {
  const names: Record<string, string> = {
    N: "نیتروژن (N)",
    P: "فسفر (P)",
    K: "پتاسیم (K)",
    Ca: "کلسیم (Ca)",
    Mg: "منیزیم (Mg)",
    S: "گوگرد (S)",
    Fe: "آهن (Fe)",
    Zn: "روی (Zn)",
    Mn: "منگنز (Mn)",
    Cu: "مس (Cu)",
    B: "بُر (B)",
    Mo: "مولیبدن (Mo)",
    Cl: "کلر (Cl)",
  };
  return names[element] || element;
};

const nutrientComparison = computed(() => {
  const elements = ["N", "P", "K", "Ca", "Mg", "Fe", "Zn", "Mn", "B"];

  const needs = props.result.custom_needs || props.result.target_needs || {};

  const suppliedMain = props.result.tank_main_result?.supplied_ppm || {};
  const suppliedCalcium = props.result.tank_calcium_result?.supplied_ppm || {};

  return elements.map((elem) => {
    const need = needs[elem] || 0;
    const supplied = (suppliedMain[elem] || 0) + (suppliedCalcium[elem] || 0);
    let status = "ok";
    if (need > 0) {
      const ratio = supplied / need;
      if (ratio < 0.7) status = "critical";
      else if (ratio < 0.9) status = "low";
      else status = "ok";
    }
    return { element: elem, need, supplied, status };
  });
});

onMounted(() => {
  fetchAllFertilizers();
});
</script>

<style scoped>
details summary {
  list-style: none;
  cursor: pointer;
}

details summary::-webkit-details-marker {
  display: none;
}

details summary::before {
  content: "📂 ";
  font-size: 14px;
}

details[open] summary::before {
  content: "📁 ";
}

@media print {
  .bg-white {
    break-inside: avoid;
    page-break-inside: avoid;
  }

  details {
    display: block !important;
  }

  details summary {
    display: block !important;
  }

  details[open] summary::before {
    content: "📁 ";
  }

  .fixed {
    display: none !important;
  }
}
</style>

```

---

## File 18: `frontend/src/components/common/InputField.vue`

**Size:** 2.0 KB

```vue
<!-- Platform-v3\frontend\src\components\common\InputField.vue -->

<template>
  <div class="w-full">
    <label class="block text-xs font-medium text-gray-700 mb-1">
      <svg v-if="icon" class="w-3 h-3 inline ml-1 text-gray-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path :d="icon" />
      </svg>
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    
    <input
      :type="type"
      :value="modelValue"
      @input="updateValue"
      :placeholder="placeholder"
      :step="step"
      :min="min"
      :max="max"
      class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:border-green-500 focus:ring-1 focus:ring-green-500 transition outline-none"
      :class="{ 'border-red-300 bg-red-50': error }"
    />
    
    <p v-if="helpText" class="text-[10px] text-gray-400 mt-1 flex items-start gap-1">
      <svg class="w-3 h-3 inline mt-0.5 flex-shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      {{ helpText }}
    </p>
    
    <p v-if="error" class="text-[10px] text-red-500 mt-1">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  modelValue: string | number | null
  label: string
  type?: string
  placeholder?: string
  icon?: string
  required?: boolean
  step?: string | number
  min?: string | number
  max?: string | number
  helpText?: string
  error?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number | null): void
}>()

const updateValue = (event: Event) => {
  const target = event.target as HTMLInputElement
  let value: string | number | null = target.value
  
  if (props.type === 'number') {
    value = value === '' ? null : Number(value)
  }
  
  emit('update:modelValue', value)
}
</script>
```

---

## File 19: `frontend/src/components/common/ThemeToggle.vue`

**Size:** 969 B

```vue
<template>
  <button 
    @click="toggleTheme" 
    class="px-3 py-1 rounded-lg border transition-colors duration-200"
    :class="isDark ? 'bg-gray-700 border-gray-600 text-yellow-400' : 'bg-gray-100 border-gray-300 text-gray-700'"
    :title="isDark ? 'حالت روشن' : 'حالت تاریک'"
  >
    {{ isDark ? '☀️' : '🌙' }}
  </button>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isDark = ref(false)

const toggleTheme = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
})
</script>
```

---

## File 20: `frontend/src/App.vue`

**Size:** 194 B

```vue
<!-- Platform-v3\frontend\src\App.vue -->

<template>
  <div class="min-h-screen bg-gray-50 font-vazirmatn">
    <router-view />
  </div>
</template>

<script setup lang="ts">
</script>
```

---

## File 21: `frontend/src/main.ts`

**Size:** 315 B

```typescript
// Platform-v3\frontend\src\main.ts

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'  // <-- این خط مهم است

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.mount('#app')
```

---

## File 22: `frontend/src/style.css`

**Size:** 7.3 KB

```css
/* ============================================
   Platform-v3\frontend\src\style.css
   نرم‌افزار تغذیه سبز - Green Nutrition Software
   ============================================ */

/* ============================================
   Tailwind Directives
   ============================================ */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* ============================================
   Font Definitions
   ============================================ */

@font-face {
  font-family: 'Vazirmatn';
  src: url('/fonts/Vazirmatn-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Vazirmatn';
  src: url('/fonts/Vazirmatn-Bold.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Sahel';
  src: url('/fonts/Sahel.ttf') format('truetype');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Sahel';
  src: url('/fonts/Sahel-Bold.ttf') format('truetype');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Samim';
  src: url('/fonts/Samim.ttf') format('truetype');
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

@font-face {
  font-family: 'Samim';
  src: url('/fonts/Samim-Bold.ttf') format('truetype');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}

/* ============================================
   Dark/Light Theme Variables
   ============================================ */

:root {
  --bg-primary: #f8fafc;
  --bg-card: #ffffff;
  --text-primary: #1e293b;
  --text-secondary: #475569;
  --border: #e2e8f0;
}

.dark {
  --bg-primary: #0f172a;
  --bg-card: #1e293b;
  --text-primary: #f1f5f9;
  --text-secondary: #94a3b8;
  --border: #334155;
}

/* ============================================
   Global Styles
   ============================================ */

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: 'Vazirmatn', 'Sahel', 'Samim', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg-primary);
  direction: rtl;
  color: var(--text-primary);
  line-height: 1.5;
  transition: background-color 0.3s, color 0.3s;
}

/* ============================================
   Force Dark Mode
   ============================================ */

html.dark,
html.dark body {
  background-color: #0f172a !important;
}

/* ============================================
   Custom Scrollbar
   ============================================ */

::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* ============================================
   Animations
   ============================================ */

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-out forwards;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 0.8s linear infinite;
}

/* ============================================
   Form Elements
   ============================================ */

input, select, textarea {
  transition: all 0.2s ease;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #10b981;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.1);
}

/* ============================================
   Dark Mode - General Text
   ============================================ */

html.dark,
html.dark * {
  color: #f1f5f9 !important;
}

html.dark .text-gray-500,
html.dark .text-gray-600,
html.dark .text-gray-700,
html.dark .text-gray-800,
html.dark .text-gray-900 {
  color: #cbd5e1 !important;
}

/* ============================================
   Dark Mode - Form Elements
   ============================================ */

html.dark input,
html.dark select,
html.dark textarea {
  background-color: #1e293b !important;
  color: #f1f5f9 !important;
  border-color: #475569 !important;
}

html.dark input::placeholder,
html.dark textarea::placeholder {
  color: #94a3b8 !important;
}

/* ============================================
   Dark Mode - Buttons
   ============================================ */

html.dark button:not(.theme-toggle) {
  background-color: #334155 !important;
  color: #f1f5f9 !important;
}

/* ============================================
   Dark Mode - Backgrounds
   ============================================ */

html.dark .bg-white,
html.dark .bg-gray-50,
html.dark .bg-gray-100,
html.dark .bg-gray-200 {
  background-color: #1e293b !important;
}

/* ============================================
   Dark Mode - Borders
   ============================================ */

html.dark .border,
html.dark .border-gray-100,
html.dark .border-gray-200,
html.dark .border-gray-300 {
  border-color: #475569 !important;
}

/* ============================================
   Dark Mode - Tank Headers (مخزن کلسیم و سایر مخازن)
   ============================================ */

/* پس‌زمینه هدرها */
html.dark .bg-amber-50,
html.dark .bg-green-50,
html.dark .bg-blue-50,
html.dark .bg-purple-50,
html.dark .bg-amber-100,
html.dark .bg-green-100,
html.dark .bg-blue-100,
html.dark .bg-purple-100 {
  background-color: #1e293b !important;
}

/* رنگ عنوان هدرها */
html.dark .text-amber-800,
html.dark .text-green-800,
html.dark .text-blue-800,
html.dark .text-purple-800,
html.dark .text-amber-700,
html.dark .text-green-700,
html.dark .text-blue-700,
html.dark .text-purple-700 {
  color: #94a3b8 !important;
}

/* رنگ توضیحات هدرها */
html.dark .text-amber-600,
html.dark .text-green-600,
html.dark .text-blue-600,
html.dark .text-purple-600 {
  color: #64748b !important;
}

/* حاشیه هدرها */
html.dark .border-amber-200,
html.dark .border-green-200,
html.dark .border-blue-200,
html.dark .border-purple-200,
html.dark .border-amber-100,
html.dark .border-green-100,
html.dark .border-blue-100,
html.dark .border-purple-100 {
  border-color: #334155 !important;
}

/* آیکون هدرها */
html.dark svg.text-amber-600,
html.dark svg.text-green-600,
html.dark svg.text-blue-600,
html.dark svg.text-purple-600 {
  color: #64748b !important;
}

/* ============================================
   RTL Number Input
   ============================================ */

input[type="number"] {
  text-align: left;
  direction: ltr;
}

/* ============================================
   Print Styles
   ============================================ */

@media print {
  body {
    background: white;
    padding: 0;
    margin: 0;
  }

  .no-print {
    display: none !important;
  }

  .print-friendly {
    box-shadow: none !important;
    border: 1px solid #e5e7eb !important;
  }
}

```

---

## File 23: `frontend/package.json`

**Size:** 633 B

```json
{
  "name": "frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc -b && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.17.0",
    "pinia": "^3.0.4",
    "vue": "^3.5.34",
    "vue-router": "^4.6.4"
  },
  "devDependencies": {
    "@types/node": "^24.12.3",
    "@vitejs/plugin-vue": "^6.0.6",
    "@vue/tsconfig": "^0.9.1",
    "autoprefixer": "^10.5.0",
    "postcss": "^8.5.15",
    "tailwindcss": "^3.4.19",
    "typescript": "~6.0.2",
    "vite": "^8.0.12",
    "vue-tsc": "^3.2.8"
  }
}

```

---

## 📊 Summary

- **Total Core Files:** 23
- **Found:** 22 ✅

### 🚀 What's Included:

1. **Backend API** - FastAPI routes, models, schemas
2. **Calculator Engine** - Core optimization algorithm
3. **Dual Tank System** - Calcium/Main tank separation logic
4. **Stock Solution** - Injector ratio calculations
5. **Frontend UI** - Main calculator view and results

### ❌ What's Excluded (Not needed for understanding):

- Database files
- Seed data
- Config files (tailwind, vite, tsconfig)
- Simple UI components (Button, Card, Input, etc.)
- Router files
- Admin components
- Test files
- Project management files

**Generated:** 2026-06-16 18:36:37