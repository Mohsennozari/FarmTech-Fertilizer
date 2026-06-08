# 🌱 FarmTech Core Context

**Generated:** 2026-06-07 18:01:52
**Project:** FarmTech Fertilizer System

---

## 🔧 Backend Core

### 📄 `backend/app/calculator.py`

```python
# Platform-v3\backend\app\calculator.py

import numpy as np
from typing import List, Dict, Tuple, Optional

# اضافه شدن import برای scipy
try:
    from scipy.optimize import minimize, Bounds
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("Warning: scipy not installed. Using fallback method.")

SUPPORTED_ELEMENTS = ['N', 'P', 'K', 'Ca', 'Mg', 'S', 'Fe', 'Zn', 'Mn', 'Cu', 'B', 'Mo', 'Cl']


def calculate_element_ppm(fertilizer, dose_g_per_liter: float) -> Dict[str, float]:
    """محاسبه ppm هر عنصر از یک کود با دوز مشخص"""
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
    """محاسبه سهم عناصر از آب مخزن"""
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
    """محاسبه سهم عناصر از اسید مصرفی"""
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


def optimize_fertilizer_doses_professional(
    remaining_needs: Dict[str, float],
    fertilizers: List,
    brand_filter: Optional[str] = None,
    max_total_dose: float = 5.0
) -> Tuple[List[Dict], Dict[str, float], List[Dict]]:
    """
    بهینه‌سازی دوز کودها با استفاده از روش SLSQP (مقید)

    این نسخه بهبود یافته از الگوریتم قبلی است و:
    1. از محدودیت‌های min/max دوز هر کود استفاده می‌کند
    2. مجموع دوزها را محدود می‌کند
    3. پایدارتر از روش least squares است
    """

    if not fertilizers:
        return [], {elem: 0.0 for elem in SUPPORTED_ELEMENTS}, []

    # فیلتر برند
    if brand_filter:
        fertilizers = [f for f in fertilizers if f.brand_name == brand_filter]
        if not fertilizers:
            return [], {elem: 0.0 for elem in SUPPORTED_ELEMENTS}, [{
                "type": "brand_filter",
                "severity": "warning",
                "message": f"No fertilizers found for brand {brand_filter}"
            }]

    # حذف عناصر با نیاز بسیار کم (بهبود پایداری عددی)
    active_needs = {}
    for elem, value in remaining_needs.items():
        if value > 0.5:  # فقط عناصر با نیاز > 0.5 ppm
            active_needs[elem] = value

    # اگر تعداد عناصر فعال خیلی زیاد است، اولویت‌بندی کن
    if len(active_needs) > len(fertilizers) * 2:
        priority_elements = ['N', 'P', 'K', 'Ca', 'Mg', 'Fe']
        active_needs = {k: v for k, v in active_needs.items() if k in priority_elements}

    elem_list = list(active_needs.keys())

    # ساخت ماتریس A (m عنصر × n کود)
    A = []
    for fert in fertilizers:
        purity = (fert.purity_percent or 100) / 100.0
        factor = 10 * purity
        row = []
        for elem in elem_list:
            attr_name = f"{elem.lower()}_percent"
            value = getattr(fert, attr_name, 0) or 0
            row.append(value * factor)
        A.append(row)

    A = np.array(A).T  # transpose برای شکل (m × n)
    b = np.array([active_needs[e] for e in elem_list])

    # تنظیم محدوده دوز برای هر کود
    bounds = []
    for fert in fertilizers:
        min_dose = fert.min_dose_g_per_liter or 0.01
        max_dose = fert.max_dose_g_per_liter or 5.0
        bounds.append((min_dose, max_dose))

    # تابع هدف: minimize squared error
    def objective(x):
        return np.sum((A @ x - b) ** 2)

    # محدودیت مجموع دوز
    def total_dose_constraint(x):
        return max_total_dose - np.sum(x)

    constraints = {'type': 'ineq', 'fun': total_dose_constraint}

    # حدس اولیه (دوز متوسط)
    x0 = np.ones(len(fertilizers)) * 0.5

    # بهینه‌سازی با روش مناسب
    if SCIPY_AVAILABLE and len(elem_list) <= len(fertilizers) * 2:
        try:
            result = minimize(
                objective,
                x0,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints,
                options={'maxiter': 500, 'ftol': 1e-6, 'disp': False}
            )
            doses = result.x
            success = result.success
        except Exception as e:
            print(f"Optimization error: {e}")
            doses = x0
            success = False
    else:
        # Fallback: روش least squares ساده
        try:
            doses, _, _, _ = np.linalg.lstsq(A, b, rcond=1e-4)
            doses = np.maximum(doses, 0)
            doses = np.nan_to_num(doses, 0)
            success = True
        except Exception as e:
            print(f"Least squares error: {e}")
            doses = x0
            success = False

        # اعمال محدودیت‌ها
        for i, (low, high) in enumerate(bounds):
            doses[i] = np.clip(doses[i], low, high)

        total_dose = np.sum(doses)
        if total_dose > max_total_dose:
            doses = doses * (max_total_dose / total_dose)

    # ساخت خروجی
    final_supply = {elem: 0.0 for elem in SUPPORTED_ELEMENTS}
    result_doses = []
    warnings = []

    for i, fert in enumerate(fertilizers):
        if doses[i] > 0.01:
            content = calculate_element_ppm(fert, doses[i])
            for elem in SUPPORTED_ELEMENTS:
                final_supply[elem] += content[elem]

            # بررسی هشدار حداکثر دوز
            max_dose = fert.max_dose_g_per_liter
            if max_dose and doses[i] > max_dose * 0.95:
                warnings.append({
                    "type": "max_dose_approaching",
                    "severity": "warning",
                    "fertilizer": fert.name,
                    "message": f"Dose for {fert.name} ({round(doses[i], 3)} g/L) is near maximum ({max_dose} g/L)"
                })

            result_doses.append({
                "id": fert.id,
                "name": fert.name,
                "brand_name": fert.brand_name,
                "dose_g_per_liter": round(float(doses[i]), 3),
                "chemical_formula": fert.chemical_formula
            })

    # شناسایی عناصر پوشش داده نشده
    uncovered = []
    for elem in SUPPORTED_ELEMENTS:
        need = remaining_needs.get(elem, 0)
        supply = final_supply[elem]
        if need > 1.0 and supply < need * 0.7:
            uncovered.append(elem)

    if uncovered:
        warnings.append({
            "type": "partial_coverage",
            "severity": "warning",
            "message": f"Elements not fully supplied: {', '.join(uncovered)}",
            "fertilizers": []
        })

    if not success:
        warnings.append({
            "type": "optimization",
            "severity": "warning",
            "message": "Optimization did not fully converge. Results may be suboptimal.",
            "fertilizers": []
        })

    result_doses.sort(key=lambda x: x['dose_g_per_liter'], reverse=True)
    return result_doses, final_supply, warnings


def calculate_tank_doses(doses: List[Dict], tank_volume_liters: float) -> List[Dict]:
    """محاسبه دوز برای کل مخزن و استوک 200x"""
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


def generate_professional_mixing_instructions(doses: List[Dict], warnings: List[Dict], tank_volume: float) -> str:
    """تولید دستورالعمل اختلاط حرفه‌ای"""
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
    instructions.append("2. Add fertilizers in this order (avoid mixing incompatible ones):")
    instructions.append("")

    # تفکیک کودهای کلسیمی و فسفری (برای جلوگیری از رسوب)
    calcium_fertilizers = []
    phosphorus_fertilizers = []
    other_fertilizers = []

    for dose in doses:
        if 'calcium' in dose['name'].lower() or 'کلسیم' in dose['name']:
            calcium_fertilizers.append(dose)
        elif 'phosphate' in dose['name'].lower() or 'فسفر' in dose['name'] or '10-52' in dose['name']:
            phosphorus_fertilizers.append(dose)
        else:
            other_fertilizers.append(dose)

    step_num = 1
    for dose in other_fertilizers:
        instructions.append(f"   {step_num}. {dose['name']}: {dose['dose_g_per_liter']} g/L")
        instructions.append(f"      Total for tank: {dose['dose_g_for_tank']} g")
        step_num += 1

    if calcium_fertilizers:
        instructions.append("")
        instructions.append("   ⚠️ Add calcium fertilizers separately:")
        for dose in calcium_fertilizers:
            instructions.append(f"   {step_num}. {dose['name']}: {dose['dose_g_per_liter']} g/L")
            instructions.append(f"      Total for tank: {dose['dose_g_for_tank']} g")
            step_num += 1

    if phosphorus_fertilizers:
        instructions.append("")
        instructions.append("   ⚠️ Add phosphorus fertilizers last:")
        for dose in phosphorus_fertilizers:
            instructions.append(f"   {step_num}. {dose['name']}: {dose['dose_g_per_liter']} g/L")
            instructions.append(f"      Total for tank: {dose['dose_g_for_tank']} g")
            step_num += 1

    instructions.append("")
    instructions.append(f"{step_num}. After adding each fertilizer, mix well for 2 minutes")
    instructions.append("")
    instructions.append(f"{step_num+1}. Fill to final volume and mix for 5 more minutes")
    instructions.append("")
    instructions.append(f"{step_num+2}. Measure and adjust EC and pH")
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
        seen_messages = set()
        for warn in warnings:
            msg = warn.get('description', warn.get('message', ''))
            if msg not in seen_messages:
                instructions.append(f"   ⚠️ {msg}")
                seen_messages.add(msg)

    return "\n".join(instructions)

```

### 📄 `backend/app/models.py`

```python
# Platform-v3\backend\app\models.py

from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, Table, DateTime, Boolean
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
    notes = Column(String, nullable=True)

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
    description = Column(String, nullable=True)
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

    fertilizer_form = Column(String, default="powder")
    chemical_formula = Column(String, nullable=True)
    molecular_weight = Column(Float, nullable=True)
    purity_percent = Column(Float, default=100.0)
    fertilizer_type = Column(String, nullable=True)

    max_dose_g_per_liter = Column(Float, nullable=True)
    max_dose_ml_per_liter = Column(Float, nullable=True)
    min_dose_g_per_liter = Column(Float, nullable=True, default=0.01)
    density_g_per_ml = Column(Float, nullable=True)

    n_percent = Column(Float, default=0)
    p_percent = Column(Float, default=0)
    k_percent = Column(Float, default=0)
    ca_percent = Column(Float, default=0)
    mg_percent = Column(Float, default=0)
    s_percent = Column(Float, default=0)

    fe_percent = Column(Float, default=0)
    zn_percent = Column(Float, default=0)
    mn_percent = Column(Float, default=0)
    cu_percent = Column(Float, default=0)
    b_percent = Column(Float, default=0)
    mo_percent = Column(Float, default=0)
    cl_percent = Column(Float, default=0)

    solubility_g_per_l = Column(Float, nullable=True)
    ph_effect = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    # روابط
    brand = relationship("Brand", back_populates="fertilizers", lazy="select")
    growth_stages = relationship("GrowthStage", secondary=growth_stage_fertilizer, back_populates="fertilizers", lazy="select")


class GrowthStage(Base):
    __tablename__ = "growth_stages"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    variety_id = Column(Integer, ForeignKey("varieties.id"), nullable=True)
    name = Column(String, nullable=False)
    stage_order = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    nutrient_needs = Column(JSON, nullable=True)
    target_ec_min = Column(Float, nullable=True)
    target_ec_max = Column(Float, nullable=True)
    target_ph_min = Column(Float, nullable=True)
    target_ph_max = Column(Float, nullable=True)
    priority = Column(String, nullable=True)

    # روابط
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
    description = Column(String, nullable=True)

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
    notes = Column(String, nullable=True)


class Tank(Base):
    __tablename__ = "tanks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    volume_liters = Column(Float, nullable=False)

    water_ec_ms_cm = Column(Float, nullable=True)
    water_ph = Column(Float, nullable=True)
    water_hco3_ppm = Column(Float, default=0)
    water_ca_ppm = Column(Float, default=0)
    water_mg_ppm = Column(Float, default=0)
    water_na_ppm = Column(Float, default=0)
    water_cl_ppm = Column(Float, default=0)
    water_so4_ppm = Column(Float, default=0)
    water_no3_ppm = Column(Float, default=0)
    water_fe_ppm = Column(Float, default=0)

    notes = Column(String, nullable=True)

    calculations = relationship("CalculationHistory", back_populates="tank", lazy="select")


class CalculationHistory(Base):
    __tablename__ = "calculation_history"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    crop_name = Column(String, nullable=False)
    variety_name = Column(String, nullable=False)
    stage_name = Column(String, nullable=False)
    brand_filter = Column(String, nullable=True)
    tank_id = Column(Integer, ForeignKey("tanks.id"), nullable=False)
    tank_name = Column(String, nullable=False)
    tank_volume_liters = Column(Float, nullable=False)
    water_ec_ms_cm = Column(Float, nullable=True)
    water_ph = Column(Float, nullable=True)
    water_hco3_ppm = Column(Float, default=0)
    target_needs_ppm = Column(JSON, nullable=False)
    water_contribution_ppm = Column(JSON, nullable=False)
    remaining_needs_ppm = Column(JSON, nullable=False)
    calculated_supply_ppm = Column(JSON, nullable=False)
    doses = Column(JSON, nullable=False)
    warnings = Column(JSON, nullable=False)
    ec_ph_targets = Column(JSON, nullable=False)
    mixing_instructions = Column(String, nullable=True)
    acid_adjustment = Column(JSON, nullable=True)
    success = Column(Integer, default=1)
    error_message = Column(String, nullable=True)

    tank = relationship("Tank", back_populates="calculations", lazy="select")
```

### 📄 `backend/app/routes.py`

```python
# Platform-v3\backend\app\routes.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from .database import get_db
from .models import (
    Crop, Variety, GrowthStage, Fertilizer, Brand,
    Tank, CalculationHistory, Interaction, Acid
)
from .schemas import (
    FertilizerResponse, GrowthStageResponse, VarietyResponse, CropResponse,
    BrandResponse, TankCreate, TankResponse, CalculationHistoryResponse,
    CalculationRequest, CalculationResponse, DoseResponse, WarningResponse,
    AcidResponse, InteractionResponse
)
from .calculator import (
    SUPPORTED_ELEMENTS,
    calculate_water_contribution,
    calculate_acid_contribution,
    optimize_fertilizer_doses_professional,
    calculate_tank_doses,
    generate_professional_mixing_instructions
)

router = APIRouter()


# ============================================================
# Helper function for checking fertilizer interactions
# ============================================================

def check_fertilizer_interactions(fertilizer_ids: List[int], db: Session) -> List[Dict]:
    """
    بررسی تداخلات شیمیایی بین کودهای انتخاب شده
    Returns list of warnings for incompatible fertilizer pairs
    """
    warnings = []

    if len(fertilizer_ids) < 2:
        return warnings

    # دریافت اطلاعات کودها از دیتابیس
    fertilizers = {f.id: f for f in db.query(Fertilizer).filter(Fertilizer.id.in_(fertilizer_ids)).all()}

    for i in range(len(fertilizer_ids)):
        for j in range(i + 1, len(fertilizer_ids)):
            fert_a_id = fertilizer_ids[i]
            fert_b_id = fertilizer_ids[j]

            # بررسی تداخل در هر دو جهت
            interaction = db.query(Interaction).filter(
                ((Interaction.fertilizer_a_id == fert_a_id) &
                 (Interaction.fertilizer_b_id == fert_b_id)) |
                ((Interaction.fertilizer_a_id == fert_b_id) &
                 (Interaction.fertilizer_b_id == fert_a_id))
            ).first()

            if interaction:
                fert_a = fertilizers.get(fert_a_id)
                fert_b = fertilizers.get(fert_b_id)

                warnings.append({
                    "type": interaction.reaction_type,
                    "severity": interaction.severity,
                    "product": interaction.precipitate_product,
                    "description": interaction.description,
                    "fertilizers": [fert_a.name if fert_a else str(fert_a_id),
                                   fert_b.name if fert_b else str(fert_b_id)]
                })

    return warnings


# ============================================================
# API Endpoints
# ============================================================

@router.get("/health")
def health_check():
    return {"status": "ok", "message": "FarmTech API is running"}


@router.get("/crops", response_model=List[CropResponse])
def get_crops(db: Session = Depends(get_db)):
    return db.query(Crop).all()


@router.get("/varieties", response_model=List[VarietyResponse])
def get_varieties(
    crop_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Variety)
    if crop_id:
        query = query.filter(Variety.crop_id == crop_id)
    return query.all()


@router.get("/brands", response_model=List[BrandResponse])
def get_brands(db: Session = Depends(get_db)):
    return db.query(Brand).all()


@router.get("/fertilizers", response_model=List[FertilizerResponse])
def get_fertilizers(
    brand_id: Optional[int] = Query(None),
    brand_name: Optional[str] = Query(None),
    fertilizer_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Fertilizer)
    if brand_id:
        query = query.filter(Fertilizer.brand_id == brand_id)
    if brand_name:
        query = query.filter(Fertilizer.brand_name == brand_name)
    if fertilizer_type:
        query = query.filter(Fertilizer.fertilizer_type == fertilizer_type)
    return query.all()


@router.get("/growth-stages", response_model=List[GrowthStageResponse])
def get_growth_stages(
    crop_id: Optional[int] = Query(None),
    variety_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(GrowthStage)
    if crop_id:
        query = query.filter(GrowthStage.crop_id == crop_id)
    if variety_id:
        query = query.filter(GrowthStage.variety_id == variety_id)
    return query.order_by(GrowthStage.stage_order).all()


@router.get("/acids", response_model=List[AcidResponse])
def get_acids(db: Session = Depends(get_db)):
    return db.query(Acid).all()


@router.get("/interactions", response_model=List[InteractionResponse])
def get_interactions(db: Session = Depends(get_db)):
    return db.query(Interaction).all()


@router.post("/tanks", response_model=TankResponse, status_code=201)
def create_tank(tank: TankCreate, db: Session = Depends(get_db)):
    try:
        tank_data = tank.model_dump()
        db_tank = Tank(**tank_data)
        db.add(db_tank)
        db.commit()
        db.refresh(db_tank)
        return db_tank
    except Exception as e:
        db.rollback()
        print(f"Error creating tank: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error creating tank: {str(e)}")


@router.get("/tanks", response_model=List[TankResponse])
def get_tanks(db: Session = Depends(get_db)):
    try:
        return db.query(Tank).all()
    except Exception as e:
        print(f"Error getting tanks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tanks/{tank_id}")
def delete_tank(tank_id: int, db: Session = Depends(get_db)):
    tank = db.query(Tank).filter(Tank.id == tank_id).first()
    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")
    db.delete(tank)
    db.commit()
    return {"message": "Tank deleted successfully"}


@router.get("/history", response_model=List[CalculationHistoryResponse])
def get_calculation_history(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    return db.query(CalculationHistory).order_by(
        CalculationHistory.created_at.desc()
    ).limit(limit).all()
    # ============================================================
# Main Calculation Endpoint (ادامه از بخش قبلی)
# ============================================================

@router.post("/calculate", response_model=CalculationResponse)
def calculate_fertilizer(
    request: CalculationRequest,
    db: Session = Depends(get_db)
):
    try:
        # 1. پیدا کردن رقم گیاه
        variety = db.query(Variety).filter(Variety.name == request.variety_name).first()
        if not variety:
            raise HTTPException(status_code=404, detail=f"Variety '{request.variety_name}' not found")

        # 2. پیدا کردن مرحله رشد
        stage = db.query(GrowthStage).filter(
            GrowthStage.name == request.stage_name,
            GrowthStage.variety_id == variety.id
        ).first()

        if not stage:
            stage = db.query(GrowthStage).filter(
                GrowthStage.name == request.stage_name,
                GrowthStage.variety_id.is_(None)
            ).first()

        if not stage:
            raise HTTPException(status_code=404, detail=f"Growth stage '{request.stage_name}' not found")

        # 3. ایجاد مخزن موقت
        tank_data = request.tank.model_dump()
        tank = Tank(**tank_data)
        db.add(tank)
        db.flush()

        # 4. نیازهای هدف گیاه
        target_needs = stage.nutrient_needs or {}
        for elem in SUPPORTED_ELEMENTS:
            if elem not in target_needs:
                target_needs[elem] = 0

        # 5. محاسبه سهم آب
        water_contribution = calculate_water_contribution(tank)

        # 6. محاسبه سهم اسید (در صورت وجود)
        acid_contribution = {elem: 0.0 for elem in SUPPORTED_ELEMENTS}
        if request.acid_id and request.acid_dose_ml_per_liter:
            acid = db.query(Acid).filter(Acid.id == request.acid_id).first()
            if acid:
                acid_contribution = calculate_acid_contribution(acid, request.acid_dose_ml_per_liter)

        # 7. محاسبه نیاز باقیمانده پس از کسر سهم آب و اسید
        remaining_needs = {}
        for elem in SUPPORTED_ELEMENTS:
            remaining_needs[elem] = max(0, target_needs[elem] - water_contribution[elem] - acid_contribution[elem])

        # 8. دریافت لیست کودها (با فیلتر برند در صورت وجود)
        query = db.query(Fertilizer)
        if request.brand_filter:
            query = query.filter(Fertilizer.brand_name == request.brand_filter)

        all_fertilizers = query.all()

        if not all_fertilizers:
            raise HTTPException(status_code=404, detail="No fertilizers found")

        # 9. بهینه‌سازی دوز کودها (نسخه بهبود یافته)
        doses, calculated_supply, optimization_warnings = optimize_fertilizer_doses_professional(
            remaining_needs, all_fertilizers, request.brand_filter, max_total_dose=5.0
        )

        # 10. محاسبه دوز برای حجم مخزن و استوک 200x
        doses_with_tank = calculate_tank_doses(doses, tank.volume_liters)

        # 11. بررسی تداخلات شیمیایی بین کودهای انتخاب شده
        selected_fertilizer_ids = [d['id'] for d in doses_with_tank]
        interaction_warnings = check_fertilizer_interactions(selected_fertilizer_ids, db)

        # 12. ترکیب همه هشدارها
        all_warnings = []

        # هشدارهای بهینه‌سازی
        for warn in optimization_warnings:
            all_warnings.append(WarningResponse(
                type=warn.get('type', 'unknown'),
                severity=warn.get('severity', 'warning'),
                product=None,
                description=warn.get('message', ''),
                fertilizers=[warn.get('fertilizer', '')] if warn.get('fertilizer') else []
            ))

        # هشدارهای تداخلات شیمیایی
        for warn in interaction_warnings:
            all_warnings.append(WarningResponse(
                type=warn.get('type', 'interaction'),
                severity=warn.get('severity', 'warning'),
                product=warn.get('product'),
                description=warn.get('description', ''),
                fertilizers=warn.get('fertilizers', [])
            ))

        # 13. تولید دستورالعمل اختلاط
        mixing_instructions = generate_professional_mixing_instructions(
            doses_with_tank, [w.model_dump() for w in all_warnings], tank.volume_liters
        )

        # 14. ذخیره در تاریخچه
        history = CalculationHistory(
            crop_name=request.crop_name,
            variety_name=request.variety_name,
            stage_name=request.stage_name,
            brand_filter=request.brand_filter,
            tank_id=tank.id,
            tank_name=tank.name,
            tank_volume_liters=tank.volume_liters,
            water_ec_ms_cm=tank.water_ec_ms_cm,
            water_ph=tank.water_ph,
            target_needs_ppm=target_needs,
            water_contribution_ppm=water_contribution,
            remaining_needs_ppm=remaining_needs,
            calculated_supply_ppm={k: round(v, 2) for k, v in calculated_supply.items()},
            doses=[d for d in doses_with_tank],
            warnings=[w.model_dump() for w in all_warnings],
            ec_ph_targets={
                "ec_min": stage.target_ec_min,
                "ec_max": stage.target_ec_max,
                "ph_min": stage.target_ph_min,
                "ph_max": stage.target_ph_max
            },
            mixing_instructions=mixing_instructions,
            success=1
        )
        db.add(history)
        db.commit()

        # 15. بازگشت پاسخ
        return CalculationResponse(
            success=True,
            created_at=datetime.now(),
            stage_name=stage.name,
            variety_name=variety.name,
            tank_name=tank.name,
            tank_volume_liters=tank.volume_liters,
            target_needs_ppm=target_needs,
            water_contribution_ppm=water_contribution,
            remaining_needs_ppm=remaining_needs,
            calculated_supply_ppm={k: round(v, 2) for k, v in calculated_supply.items()},
            doses=[DoseResponse(**d) for d in doses_with_tank],
            warnings=all_warnings,
            ec_ph_targets={
                "ec_min": stage.target_ec_min,
                "ec_max": stage.target_ec_max,
                "ph_min": stage.target_ph_min,
                "ph_max": stage.target_ph_max
            },
            mixing_instructions=mixing_instructions,
            message="Calculation completed successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Calculation error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/debug/stages")
def debug_stages(db: Session = Depends(get_db)):
    """Debug endpoint برای بررسی مراحل رشد"""
    stages = db.query(GrowthStage).all()
    return {
        "total": len(stages),
        "stages": [
            {
                "id": s.id,
                "name": s.name,
                "variety_id": s.variety_id,
                "variety_name": s.variety.name if s.variety else None,
                "stage_order": s.stage_order
            }
            for s in stages
        ]
    }

```

### 📄 `backend/app/schemas.py`

```python
# Platform-v3\backend\app\schemas.py

from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime


class BrandBase(BaseModel):
    name: str
    country: Optional[str] = None
    website: Optional[str] = None
    notes: Optional[str] = None

class BrandResponse(BrandBase):
    id: int
    class Config:
        from_attributes = True


class CropBase(BaseModel):
    name: str
    scientific_name: Optional[str] = None
    cultivation_type: Optional[str] = None

class CropResponse(CropBase):
    id: int
    class Config:
        from_attributes = True


class VarietyBase(BaseModel):
    crop_id: int
    name: str
    description: Optional[str] = None
    growth_days: Optional[int] = None
    yield_potential: Optional[str] = None

class VarietyResponse(VarietyBase):
    id: int
    class Config:
        from_attributes = True


class FertilizerBase(BaseModel):
    name: str
    brand_id: Optional[int] = None
    brand_name: Optional[str] = None
    fertilizer_form: str = "power"  # powder, liquid
    chemical_formula: Optional[str] = None
    molecular_weight: Optional[float] = None
    purity_percent: float = 100.0
    fertilizer_type: Optional[str] = None
    max_dose_g_per_liter: Optional[float] = None
    max_dose_ml_per_liter: Optional[float] = None
    min_dose_g_per_liter: Optional[float] = 0.01
    density_g_per_ml: Optional[float] = None

    n_percent: float = 0
    p_percent: float = 0
    k_percent: float = 0
    ca_percent: float = 0
    mg_percent: float = 0
    s_percent: float = 0

    fe_percent: float = 0
    zn_percent: float = 0
    mn_percent: float = 0
    cu_percent: float = 0
    b_percent: float = 0
    mo_percent: float = 0
    cl_percent: float = 0

    solubility_g_per_l: Optional[float] = None
    ph_effect: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True

class FertilizerResponse(FertilizerBase):
    id: int
    class Config:
        from_attributes = True


class GrowthStageBase(BaseModel):
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

class GrowthStageResponse(GrowthStageBase):
    id: int
    class Config:
        from_attributes = True


class InteractionBase(BaseModel):
    fertilizer_a_id: int
    fertilizer_b_id: int
    reaction_type: str
    severity: str
    precipitate_product: Optional[str] = None
    description: Optional[str] = None

class InteractionResponse(InteractionBase):
    id: int
    class Config:
        from_attributes = True


class AcidBase(BaseModel):
    name: str
    chemical_formula: Optional[str] = None
    concentration_percent: float
    density_g_per_ml: Optional[float] = None
    supplies_element: Optional[str] = None
    element_percent: Optional[float] = None
    ml_per_1000L_per_ph_point: Optional[float] = None
    notes: Optional[str] = None

class AcidResponse(AcidBase):
    id: int
    class Config:
        from_attributes = True


class TankBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    volume_liters: float = Field(..., gt=0, le=100000)
    water_ec_ms_cm: Optional[float] = Field(None, ge=0, le=10)
    water_ph: Optional[float] = Field(None, ge=0, le=14)
    water_hco3_ppm: Optional[float] = Field(0, ge=0, le=500)
    water_ca_ppm: Optional[float] = Field(0, ge=0)
    water_mg_ppm: Optional[float] = Field(0, ge=0)
    water_na_ppm: Optional[float] = Field(0, ge=0)
    water_cl_ppm: Optional[float] = Field(0, ge=0)
    water_so4_ppm: Optional[float] = Field(0, ge=0)
    water_no3_ppm: Optional[float] = Field(0, ge=0)
    water_fe_ppm: Optional[float] = Field(0, ge=0)
    notes: Optional[str] = None

class TankCreate(TankBase):
    pass

class TankResponse(TankBase):
    id: int
    class Config:
        from_attributes = True


class CalculationRequest(BaseModel):
    crop_name: str = "توت‌فرنگی"
    variety_name: str
    stage_name: str
    brand_filter: Optional[str] = None
    tank: TankCreate
    acid_id: Optional[int] = None
    acid_dose_ml_per_liter: Optional[float] = None


class DoseResponse(BaseModel):
    id: int
    name: str
    brand_name: Optional[str]
    fertilizer_form: str = "powder"
    dose_g_per_liter: float
    dose_ml_per_liter: Optional[float] = None
    dose_g_for_tank: float
    dose_ml_for_tank: Optional[float] = None
    stock_200x_g_per_liter: float
    stock_200x_ml_per_liter: Optional[float] = None
    chemical_formula: Optional[str]
    max_dose_warning: Optional[str] = None


class WarningResponse(BaseModel):
    type: str
    severity: str
    product: Optional[str]
    description: str
    fertilizers: List[str]


class CalculationResponse(BaseModel):
    success: bool
    created_at: datetime
    stage_name: str
    variety_name: str
    tank_name: str
    tank_volume_liters: float
    target_needs_ppm: Dict[str, float]
    water_contribution_ppm: Dict[str, float]
    acid_contribution_ppm: Dict[str, float]
    remaining_needs_ppm: Dict[str, float]
    calculated_supply_ppm: Dict[str, float]
    doses: List[DoseResponse]
    warnings: List[WarningResponse]
    ec_ph_targets: Dict[str, Optional[float]]
    mixing_instructions: str
    message: Optional[str] = None
    acid_adjustment: Optional[Dict[str, float]] = None


class CalculationHistoryResponse(BaseModel):
    id: int
    created_at: datetime
    crop_name: str
    variety_name: str
    stage_name: str
    tank_name: str
    tank_volume_liters: float
    success: int
    error_message: Optional[str]

    class Config:
        from_attributes = True
```

### 📄 `backend/app/seed.py`

```python
# Platform-v3\backend\app\seed.py

import json
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import (
    Crop, Variety, GrowthStage, Brand, Fertilizer,
    Interaction, Acid, Tank, CalculationHistory
)

# ضرایب تبدیل اکسید به عنصر خالص (مقادیر دقیق علمی)
P2O5_TO_P = 0.4364   # 61.9475 / 141.9445
K2O_TO_K = 0.8301    # 78.1966 / 94.196
CaO_TO_Ca = 0.7147   # 40.078 / 56.0774
MgO_TO_Mg = 0.603    # 24.305 / 40.3044


def convert_p2o5_to_p(p2o5_percent: float) -> float:
    return round(p2o5_percent * P2O5_TO_P, 2)


def convert_k2o_to_k(k2o_percent: float) -> float:
    return round(k2o_percent * K2O_TO_K, 2)


def convert_cao_to_ca(cao_percent: float) -> float:
    return round(cao_percent * CaO_TO_Ca, 2)


def convert_mgo_to_mg(mgo_percent: float) -> float:
    return round(mgo_percent * MgO_TO_Mg, 2)


def seed_database():
    db = SessionLocal()

    try:
        print("Clearing existing data...")
        db.query(CalculationHistory).delete()
        db.query(Tank).delete()
        db.query(Interaction).delete()
        db.query(GrowthStage).delete()
        db.query(Fertilizer).delete()
        db.query(Variety).delete()
        db.query(Brand).delete()
        db.query(Crop).delete()
        db.query(Acid).delete()
        db.commit()
        print("Previous data cleared")

        print("\nCreating crops...")
        strawberry = Crop(
            name="توت‌فرنگی",
            scientific_name="Fragaria × ananassa",
            cultivation_type="هیدروپونیک"
        )
        db.add(strawberry)
        db.flush()
        print(f"   Crop: {strawberry.name}")

        print("\nCreating varieties...")
        san_andreas = Variety(
            crop_id=strawberry.id,
            name="سن اندرسا",
            description="High yield variety suitable for hydroponics",
            growth_days=90,
            yield_potential="High"
        )
        db.add(san_andreas)

        camarosa = Variety(
            crop_id=strawberry.id,
            name="کاماروسا",
            description="Early ripening with large fruits",
            growth_days=80,
            yield_potential="Very High"
        )
        db.add(camarosa)
        db.flush()
        print(f"   Variety: {san_andreas.name}")
        print(f"   Variety: {camarosa.name}")

        print("\nCreating brands...")
        gol_sam = Brand(
            name="گل سم گرگان",
            country="Iran",
            website="www.golsam.com",
            notes="Fertilizer manufacturer"
        )
        db.add(gol_sam)

        razak = Brand(
            name="رازاک شیمی",
            country="Iran",
            website="www.razakshimi.com",
            notes="NPK and sulfate fertilizer manufacturer"
        )
        db.add(razak)
        db.flush()
        print(f"   Brand: {gol_sam.name}")
        print(f"   Brand: {razak.name}")

        print("\nCreating fertilizers...")

        fertilizers_data = [
            {
                "name": "یونی کمپلکس پودری",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_type": "ریزمغذی",
                "chemical_formula": "Complete Micro",
                "purity_percent": 100,
                "max_dose_g_per_liter": 5.0,
                "min_dose_g_per_liter": 0.5,
                "fe_percent": 5.0,
                "zn_percent": 5.0,
                "mn_percent": 4.0,
                "cu_percent": 4.0,
                "b_percent": 1.5,
                "mo_percent": 0.07,
                "mg_percent": convert_mgo_to_mg(1.2),
                "s_percent": 25.0,
            },
            {
                "name": "فرتی‌گل 36-12-12",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 12-12-36",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 12.0,
                "p_percent": convert_p2o5_to_p(12.0),
                "k_percent": convert_k2o_to_k(36.0),
                "mg_percent": convert_mgo_to_mg(1.0),
                "fe_percent": 0.016,
                "zn_percent": 0.037,
                "mn_percent": 0.006,
                "cu_percent": 0.0015,
            },
            {
                "name": "فرتی‌گل 10-50-10",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 10-50-10",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 10.0,
                "p_percent": convert_p2o5_to_p(50.0),
                "k_percent": convert_k2o_to_k(10.0),
            },
            {
                "name": "فرتی‌گل 30-5-15",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 15-5-30",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 15.0,
                "p_percent": convert_p2o5_to_p(5.0),
                "k_percent": convert_k2o_to_k(30.0),
                "mg_percent": convert_mgo_to_mg(1.0),
            },
            {
                "name": "فرتی‌گل 20-20-20",
                "brand_id": gol_sam.id,
                "brand_name": gol_sam.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 20-20-20",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 20.0,
                "p_percent": convert_p2o5_to_p(20.0),
                "k_percent": convert_k2o_to_k(20.0),
                "mg_percent": convert_mgo_to_mg(1.0),
            },
            {
                "name": "NPK 20-20-20 گرین استار",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 20-20-20",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 20.0,
                "p_percent": convert_p2o5_to_p(20.0),
                "k_percent": convert_k2o_to_k(20.0),
            },
            {
                "name": "NPK 12-12-36 گرین استار",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 12-12-36",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 12.0,
                "p_percent": convert_p2o5_to_p(12.0),
                "k_percent": convert_k2o_to_k(36.0),
            },
            {
                "name": "NPK 10-52-10 زاگرا استار",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "NPK",
                "chemical_formula": "NPK 10-52-10",
                "purity_percent": 100,
                "max_dose_g_per_liter": 3.0,
                "min_dose_g_per_liter": 0.5,
                "n_percent": 10.0,
                "p_percent": convert_p2o5_to_p(52.0),
                "k_percent": convert_k2o_to_k(10.0),
            },
            {
                "name": "سولفات پتاسیم",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "K2SO4",
                "purity_percent": 100,
                "max_dose_g_per_liter": 2.0,
                "min_dose_g_per_liter": 0.2,
                "k_percent": 51.0,
                "s_percent": 18.0,
            },
            {
                "name": "نیترات کلسیم",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "Ca(NO3)2",
                "purity_percent": 100,
                "max_dose_g_per_liter": 2.0,
                "min_dose_g_per_liter": 0.2,
                "n_percent": 15.5,
                "ca_percent": 19.0,
            },
            {
                "name": "کلرید پتاسیم",
                "brand_id": razak.id,
                "brand_name": razak.name,
                "fertilizer_type": "تک عنصری",
                "chemical_formula": "KCl",
                "purity_percent": 100,
                "max_dose_g_per_liter": 1.0,
                "min_dose_g_per_liter": 0.1,
                "k_percent": 52.0,
                "cl_percent": 47.0,
            },
        ]

        fertilizers = []
        for fert_data in fertilizers_data:
            fert = Fertilizer(**fert_data)
            db.add(fert)
            fertilizers.append(fert)

        db.flush()
        print(f"   {len(fertilizers)} fertilizers created")

        print("\nCreating growth stages...")

        # ============================================================
        # نیازهای تغذیه‌ای اصلاح شده با نسبت K/Ca مناسب
        # نسبت استاندارد: K/Ca ≤ 1.2 برای توت‌فرنگی
        # ============================================================

        san_andreas_needs = {
            "استقرار نشاء": {"N": 50, "P": 30, "K": 55, "Ca": 50, "Mg": 20, "S": 15, "Fe": 2, "Zn": 0.5, "Mn": 0.5, "Cu": 0.1, "B": 0.2, "Mo": 0.05, "Cl": 0},
            "ریشه‌زایی": {"N": 70, "P": 40, "K": 75, "Ca": 65, "Mg": 25, "S": 18, "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0},
            "رشد رویشی": {"N": 120, "P": 50, "K": 120, "Ca": 105, "Mg": 40, "S": 25, "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.4, "Mo": 0.05, "Cl": 0},
            "گلدهی": {"N": 100, "P": 60, "K": 130, "Ca": 105, "Mg": 35, "S": 22, "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.5, "Mo": 0.05, "Cl": 0},
            "میوه‌دهی": {"N": 80, "P": 40, "K": 140, "Ca": 115, "Mg": 30, "S": 20, "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0}
        }

        camarosa_needs = {
            "استقرار نشاء": {"N": 55, "P": 28, "K": 55, "Ca": 50, "Mg": 19, "S": 14, "Fe": 2, "Zn": 0.5, "Mn": 0.5, "Cu": 0.1, "B": 0.2, "Mo": 0.05, "Cl": 0},
            "ریشه‌زایی": {"N": 75, "P": 38, "K": 70, "Ca": 60, "Mg": 24, "S": 17, "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0},
            "رشد رویشی": {"N": 110, "P": 48, "K": 115, "Ca": 100, "Mg": 39, "S": 24, "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.4, "Mo": 0.05, "Cl": 0},
            "گلدهی": {"N": 95, "P": 58, "K": 125, "Ca": 100, "Mg": 34, "S": 21, "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.5, "Mo": 0.05, "Cl": 0},
            "میوه‌دهی": {"N": 75, "P": 38, "K": 135, "Ca": 105, "Mg": 29, "S": 19, "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0}
        }

        stage_names = ["استقرار نشاء", "ریشه‌زایی", "رشد رویشی", "گلدهی", "میوه‌دهی"]
        stage_orders = [0, 1, 2, 3, 4]

        ec_ph_targets = {
            "استقرار نشاء": (0.8, 1.2, 5.5, 6.0),
            "ریشه‌زایی": (1.0, 1.4, 5.6, 6.1),
            "رشد رویشی": (1.2, 1.6, 5.8, 6.2),
            "گلدهی": (1.4, 1.8, 5.8, 6.2),
            "میوه‌دهی": (1.6, 2.0, 5.8, 6.2)
        }

        priorities = {
            "استقرار نشاء": "high",
            "ریشه‌زایی": "high",
            "رشد رویشی": "medium",
            "گلدهی": "high",
            "میوه‌دهی": "critical"
        }

        stages = []

        # مراحل رشد برای سن اندرسا
        for i, name in enumerate(stage_names):
            ec_min, ec_max, ph_min, ph_max = ec_ph_targets[name]
            stage = GrowthStage(
                crop_id=strawberry.id,
                variety_id=san_andreas.id,
                name=name,
                stage_order=stage_orders[i],
                description=f"Stage {name} for San Andreas",
                nutrient_needs=san_andreas_needs[name],
                target_ec_min=ec_min,
                target_ec_max=ec_max,
                target_ph_min=ph_min,
                target_ph_max=ph_max,
                priority=priorities[name]
            )
            db.add(stage)
            stages.append(stage)

        # مراحل رشد برای کاماروسا
        for i, name in enumerate(stage_names):
            ec_min, ec_max, ph_min, ph_max = ec_ph_targets[name]
            stage = GrowthStage(
                crop_id=strawberry.id,
                variety_id=camarosa.id,
                name=name,
                stage_order=stage_orders[i],
                description=f"Stage {name} for Camarosa",
                nutrient_needs=camarosa_needs[name],
                target_ec_min=ec_min,
                target_ec_max=ec_max,
                target_ph_min=ph_min,
                target_ph_max=ph_max,
                priority=priorities[name]
            )
            db.add(stage)
            stages.append(stage)

        # مراحل رشد عمومی (بدون رقم خاص)
        for i, name in enumerate(stage_names):
            ec_min, ec_max, ph_min, ph_max = ec_ph_targets[name]
            stage = GrowthStage(
                crop_id=strawberry.id,
                variety_id=None,
                name=name,
                stage_order=stage_orders[i],
                description=f"General stage {name} for Strawberry",
                nutrient_needs=san_andreas_needs[name],
                target_ec_min=ec_min,
                target_ec_max=ec_max,
                target_ph_min=ph_min,
                target_ph_max=ph_max,
                priority=priorities[name]
            )
            db.add(stage)
            stages.append(stage)

        db.flush()
        print(f"   {len(stages)} growth stages created")

        print("\nCreating interactions...")

        # تداخل نیترات کلسیم با کودهای فسفری
        calcium_nitrate = db.query(Fertilizer).filter(Fertilizer.name == "نیترات کلسیم").first()
        high_phosphorus = db.query(Fertilizer).filter(Fertilizer.name.ilike("%10-52-10%")).first()

        if calcium_nitrate and high_phosphorus:
            interaction = Interaction(
                fertilizer_a_id=calcium_nitrate.id,
                fertilizer_b_id=high_phosphorus.id,
                reaction_type="precipitation",
                severity="critical",
                precipitate_product="Calcium Phosphate",
                description="⚠️ خطر رسوب کلسیم فسفات! این دو کود را هرگز با هم مخلوط نکنید. ابتدا یکی را حل کنید، سپس دیگری را اضافه کنید."
            )
            db.add(interaction)

        # تداخل نیترات کلسیم با سولفات پتاسیم
        potassium_sulfate = db.query(Fertilizer).filter(Fertilizer.name == "سولفات پتاسیم").first()
        if calcium_nitrate and potassium_sulfate:
            interaction2 = Interaction(
                fertilizer_a_id=calcium_nitrate.id,
                fertilizer_b_id=potassium_sulfate.id,
                reaction_type="precipitation",
                severity="high",
                precipitate_product="Calcium Sulfate",
                description="⚠️ خطر رسوب کلسیم سولفات (گچ). در غلظت‌های بالا ممکن است باعث گرفتگی شود."
            )
            db.add(interaction2)

        db.flush()

        print("\nCreating acids...")
        acids_data = [
            {
                "name": "Phosphoric Acid",
                "chemical_formula": "H3PO4",
                "concentration_percent": 85.0,
                "density_g_per_ml": 1.685,
                "supplies_element": "P",
                "element_percent": 27.0,
                "ml_per_1000L_per_ph_point": 50
            },
            {
                "name": "Nitric Acid",
                "chemical_formula": "HNO3",
                "concentration_percent": 68.0,
                "density_g_per_ml": 1.41,
                "supplies_element": "N",
                "element_percent": 15.0,
                "ml_per_1000L_per_ph_point": 30
            },
            {
                "name": "Sulfuric Acid",
                "chemical_formula": "H2SO4",
                "concentration_percent": 98.0,
                "density_g_per_ml": 1.84,
                "supplies_element": "S",
                "element_percent": 32.7,
                "ml_per_1000L_per_ph_point": 25
            },
        ]

        for acid_data in acids_data:
            acid = Acid(**acid_data)
            db.add(acid)

        db.flush()
        print(f"   {len(acids_data)} acids created")

        db.commit()

        print("\n" + "="*50)
        print("Database seeded successfully!")
        print("="*50)
        print(f"\nStatistics:")
        print(f"   Crops: 1")
        print(f"   Varieties: 2")
        print(f"   Brands: 2")
        print(f"   Fertilizers: {len(fertilizers)}")
        print(f"   Growth Stages: {len(stages)}")
        print(f"   Acids: {len(acids_data)}")
        print(f"   Interactions: 2")

        # نمایش نسبت‌های K/Ca برای تأیید
        print("\n📊 K/Ca Ratios (San Andreas - corrected):")
        for stage, needs in san_andreas_needs.items():
            k_ca = needs['K'] / needs['Ca']
            status = "✅" if k_ca <= 1.3 else "⚠️"
            print(f"   {status} {stage}: K/Ca = {k_ca:.2f}")

    except Exception as e:
        db.rollback()
        print(f"\nError seeding database: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def init_db():
    print("Initializing FarmTech Database...")
    print("="*50)
    Base.metadata.create_all(bind=engine)
    print("Database tables created")
    seed_database()


if __name__ == "__main__":
    init_db()

```

### 📄 `backend/requirements.txt`

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

## 🎨 Frontend Core

### 📄 `frontend/src/views/CalculatorView.vue`

```vue
<!-- Platform-v3\frontend\src\views\CalculatorView.vue -->

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b border-gray-100 sticky top-0 z-10 no-print">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 py-4">
        <div class="flex justify-between items-center">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-800">FarmTech</h1>
              <p class="text-xs text-gray-500">سیستم هوشمند نسخه‌دهی کود</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <div :class="['w-2 h-2 rounded-full', connectionStatus === 'connected' ? 'bg-green-500' : 'bg-red-500']"></div>
            <span class="text-xs text-gray-500">{{ connectionStatus === 'connected' ? 'متصل به سرور' : 'قطع ارتباط با سرور' }}</span>
            <button v-if="result" @click="printResult" class="px-3 py-1 text-sm text-gray-600 hover:text-green-600 border border-gray-200 rounded-lg transition">
              🖨️ پرینت
            </button>
            <!-- اضافه کنید بعد از دکمه پرینت -->
            <router-link
              to="/admin/fertilizers"
              class="px-3 py-1 text-sm text-gray-600 hover:text-green-600 border border-gray-200 rounded-lg transition"
            >
              📋 کودها
            </router-link>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
      <!-- Form Card -->
      <div class="bg-white rounded-2xl shadow-card border border-gray-100 overflow-hidden">
        <div class="px-6 py-5 border-b border-gray-100">
          <h2 class="text-lg font-semibold text-gray-800">📊 اطلاعات محاسبه</h2>
          <p class="text-sm text-gray-500 mt-0.5">لطفاً اطلاعات مورد نیاز را وارد کنید</p>
        </div>

        <div class="p-6 space-y-6">
          <!-- Row 1: Variety, Stage -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                🌾 محصول
                <span class="text-xs text-gray-400 cursor-help ml-1" title="نوع گیاه مورد نظر">ⓘ</span>
              </label>
              <select v-model="selectedCrop" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl" disabled>
                <option value="توت‌فرنگی">🍓 توت‌فرنگی</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                🍓 رقم گیاه
                <span class="text-xs text-gray-400 cursor-help ml-1" title="واریته توت‌فرنگی - نیازهای غذایی متفاوتی دارند">ⓘ</span>
              </label>
              <select v-model="selectedVariety" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:border-green-500 focus:ring-1 focus:ring-green-500 transition">
                <option value="">انتخاب کنید</option>
                <option value="سن اندرسا">سن اندرسا (San Andreas)</option>
                <option value="کاماروسا">کاماروسا (Camarosa)</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                📈 مرحله رشد
                <span class="text-xs text-gray-400 cursor-help ml-1" title="هر مرحله نیاز مغذی متفاوتی دارد">ⓘ</span>
              </label>
              <select v-model="selectedStage" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:border-green-500 focus:ring-1 focus:ring-green-500 transition">
                <option value="">انتخاب کنید</option>
                <option value="استقرار نشاء">🌱 استقرار نشاء (روزهای 1-15)</option>
                <option value="ریشه‌زایی">🌿 ریشه‌زایی (روزهای 15-30)</option>
                <option value="رشد رویشی">🍃 رشد رویشی (روزهای 30-50)</option>
                <option value="گلدهی">🌸 گلدهی (روزهای 50-65)</option>
                <option value="میوه‌دهی">🍓 میوه‌دهی (روزهای 65-90)</option>
              </select>
            </div>
          </div>

          <!-- Brand Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">
              🏭 فیلتر برند
              <span class="text-xs text-gray-400 cursor-help ml-1" title="اختیاری - سیستم فقط از کودهای برند انتخاب شده استفاده می‌کند">ⓘ</span>
            </label>
            <select v-model="selectedBrand" class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:border-green-500 focus:ring-1 focus:ring-green-500 transition">
              <option value="">همه برندها</option>
              <option value="گل سم گرگان">🌾 گل سم گرگان</option>
              <option value="رازاک شیمی">🧪 رازاک شیمی</option>
            </select>
          </div>

          <!-- Tanks Section -->
          <div>
            <div class="flex justify-between items-center mb-3">
              <label class="text-sm font-medium text-gray-700">🗄️ مخازن</label>
              <button @click="openTankModal" class="text-sm text-green-600 hover:text-green-700 flex items-center gap-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                افزودن مخزن
              </button>
            </div>

            <div v-if="tanks.length === 0" class="bg-gray-50 rounded-xl p-8 text-center border border-dashed border-gray-200">
              <svg class="w-12 h-12 mx-auto text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M6 14h12M5 6h14a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2z" />
              </svg>
              <p class="text-gray-500 text-sm">هیچ مخزنی تعریف نشده است</p>
              <button @click="openTankModal" class="mt-3 text-green-600 text-sm">+ افزودن مخزن جدید</button>
            </div>

            <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              <div
                v-for="tank in tanks"
                :key="tank.id"
                @click="selectTank(tank)"
                :class="[
                  'border rounded-xl p-4 cursor-pointer transition-all',
                  selectedTank?.id === tank.id
                    ? 'border-green-500 bg-green-50 ring-2 ring-green-200'
                    : 'border-gray-200 hover:border-gray-300 hover:shadow-soft bg-white'
                ]"
              >
                <div class="flex justify-between items-start">
                  <div>
                    <h4 class="font-medium text-gray-800">{{ tank.name }}</h4>
                    <p class="text-xs text-gray-500 mt-1">{{ tank.volume_liters }} لیتر</p>
                  </div>
                  <button @click.stop="deleteTank(tank.id)" class="text-gray-400 hover:text-red-500 transition">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
                <div class="mt-2 text-xs text-gray-400">
                  <span v-if="tank.water_ec_ms_cm !== null && tank.water_ec_ms_cm !== undefined">EC: {{ tank.water_ec_ms_cm }} | </span>
                  <span v-if="tank.water_ph !== null && tank.water_ph !== undefined">pH: {{ tank.water_ph }}</span>
                  <span v-if="(!tank.water_ec_ms_cm && tank.water_ec_ms_cm !== 0) && (!tank.water_ph && tank.water_ph !== 0)">پارامترها در محاسبه وارد می‌شوند</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Water Parameters for Selected Tank -->
          <div v-if="selectedTank" class="p-4 bg-blue-50 rounded-xl border border-blue-100">
            <h4 class="text-sm font-medium text-blue-800 mb-3 flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.414 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
              </svg>
              💧 پارامترهای آب مخزن {{ selectedTank.name }}
            </h4>
            <p class="text-xs text-blue-600 mb-3">لطفاً مقادیر اندازه‌گیری شده با دستگاه EC و pH متر را وارد کنید</p>

            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              <div class="relative">
                <label class="block text-xs font-medium text-gray-700 mb-1">
                  EC آب (mS/cm)
                  <span class="text-xs text-gray-400 cursor-help ml-1" title="هدایت الکتریکی آب - با EC متر اندازه‌گیری کنید. محدوده مجاز: 0 تا 10">ⓘ</span>
                </label>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  max="10"
                  v-model.number="tempWaterEc"
                  class="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:border-blue-500"
                  placeholder="0.8"
                >
              </div>

              <div class="relative">
                <label class="block text-xs font-medium text-gray-700 mb-1">
                  pH آب
                  <span class="text-xs text-gray-400 cursor-help ml-1" title="اسیدیته آب - با pH متر اندازه‌گیری کنید. محدوده مجاز: 0 تا 14">ⓘ</span>
                </label>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  max="14"
                  v-model.number="tempWaterPh"
                  class="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:border-blue-500"
                  placeholder="7.0"
                >
              </div>

              <div class="relative">
                <label class="block text-xs font-medium text-gray-700 mb-1">
                  بیکربنات HCO₃ (ppm)
                  <span class="text-xs text-gray-400 cursor-help ml-1" title="بیکربنات آب - در صورت بالا بودن نیاز به اسید بیشتری برای تنظیم pH دارد">ⓘ</span>
                </label>
                <input
                  type="number"
                  min="0"
                  max="500"
                  v-model.number="tempWaterHco3"
                  class="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:border-blue-500"
                  placeholder="120"
                >
              </div>

              <div class="relative">
                <label class="block text-xs font-medium text-gray-700 mb-1">
                  کلسیم (ppm)
                  <span class="text-xs text-gray-400 cursor-help ml-1" title="کلسیم موجود در آب - اختیاری">ⓘ</span>
                </label>
                <input
                  type="number"
                  min="0"
                  v-model.number="tempWaterCa"
                  class="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:border-blue-500"
                  placeholder="40"
                >
              </div>

              <div class="relative">
                <label class="block text-xs font-medium text-gray-700 mb-1">
                  منیزیم (ppm)
                  <span class="text-xs text-gray-400 cursor-help ml-1" title="منیزیم موجود در آب - اختیاری">ⓘ</span>
                </label>
                <input
                  type="number"
                  min="0"
                  v-model.number="tempWaterMg"
                  class="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:border-blue-500"
                  placeholder="15"
                >
              </div>
            </div>
          </div>

          <!-- Calculate Button -->
          <button
            @click="calculate"
            :disabled="isLoading || !selectedVariety || !selectedStage || !selectedTank"
            class="w-full bg-green-600 hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium py-3 rounded-xl transition-all duration-200 flex items-center justify-center gap-2"
          >
            <svg v-if="isLoading" class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            {{ isLoading ? 'در حال محاسبه...' : '🚀 محاسبه ترکیب بهینه' }}
          </button>
        </div>
      </div>

      <!-- Validation Errors -->
      <div v-if="validationErrors.length > 0" class="mt-6 bg-red-50 border border-red-200 rounded-xl p-4">
        <div class="flex gap-3">
          <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div class="flex-1">
            <h4 class="text-sm font-bold text-red-800">❌ خطاهای اعتبارسنجی</h4>
            <ul class="mt-1 text-sm text-red-700 list-disc list-inside">
              <li v-for="(err, idx) in validationErrors" :key="idx">{{ err }}</li>
            </ul>
          </div>
          <button @click="validationErrors = []" class="text-red-400 hover:text-red-600">✕</button>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="errorMessage" class="mt-6 bg-red-50 border border-red-200 rounded-xl p-4">
        <div class="flex gap-3">
          <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="text-sm text-red-700">{{ errorMessage }}</p>
          <button @click="errorMessage = ''" class="mr-auto text-red-400 hover:text-red-600">✕</button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="mt-8 flex justify-center">
        <div class="bg-white rounded-xl shadow-card px-6 py-4 flex items-center gap-3">
          <div class="w-5 h-5 border-2 border-green-500 border-t-transparent rounded-full animate-spin"></div>
          <span class="text-gray-600">در حال محاسبه...</span>
        </div>
      </div>

      <!-- Results -->
      <div v-if="result" class="mt-8">
        <ResultsDisplay :result="result" />
      </div>
    </main>

    <!-- Tank Modal -->
    <div v-if="showTankModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" @click.self="showTankModal = false">
      <div class="bg-white rounded-2xl max-w-md w-full shadow-xl">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
          <h3 class="text-lg font-semibold text-gray-800">➕ افزودن مخزن جدید</h3>
          <button @click="showTankModal = false" class="text-gray-400 hover:text-gray-600">✕</button>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">نام مخزن</label>
            <input v-model="newTankName" placeholder="مثال: مخزن A" class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:border-green-500">
            <p class="text-xs text-gray-400 mt-1">یک نام مشخص برای این مخزن انتخاب کنید</p>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">حجم (لیتر)</label>
            <input type="number" min="1" v-model.number="newTankVolume" placeholder="1000" class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:border-green-500">
            <p class="text-xs text-gray-400 mt-1">ظرفیت مخزن بر حسب لیتر</p>
          </div>
          <p class="text-xs text-blue-600 mt-2">ℹ️ پارامترهای EC، pH، بیکربنات و سایر عناصر آب را بعد از انتخاب مخزن می‌توانید وارد کنید</p>
        </div>
        <div class="px-6 py-4 bg-gray-50 rounded-b-2xl flex gap-3">
          <button @click="addTank" class="flex-1 bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg transition">افزودن</button>
          <button @click="showTankModal = false" class="flex-1 border border-gray-200 hover:bg-gray-50 py-2 rounded-lg transition">انصراف</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Platform-v3\frontend\src\views\CalculatorView.vue

import { ref, onMounted } from 'vue'
import axios from 'axios'
import ResultsDisplay from '../components/calculator/ResultsDisplay.vue'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  timeout: 60000
})

// Connection Status
const connectionStatus = ref('checking')

// Form State
const selectedCrop = ref('توت‌فرنگی')
const selectedVariety = ref('')
const selectedStage = ref('')
const selectedBrand = ref('')

// Tanks
const tanks = ref<any[]>([])
const selectedTank = ref<any>(null)
const showTankModal = ref(false)
const isLoading = ref(false)
const result = ref<any>(null)
const errorMessage = ref('')
const validationErrors = ref<string[]>([])

// Temporary water parameters for selected tank
const tempWaterEc = ref<number | null>(null)
const tempWaterPh = ref<number | null>(null)
const tempWaterHco3 = ref<number>(0)
const tempWaterCa = ref<number>(0)
const tempWaterMg = ref<number>(0)

// New tank data
const newTankName = ref('')
const newTankVolume = ref(1000)

// Check connection on mount
onMounted(async () => {
  await checkConnection()
  await loadTanks()
})

const checkConnection = async () => {
  try {
    await api.get('/health')
    connectionStatus.value = 'connected'
  } catch (err) {
    connectionStatus.value = 'disconnected'
    errorMessage.value = '❌ خطا در اتصال به سرور. لطفاً سرور بک‌اند را بررسی کنید.'
  }
}

const loadTanks = async () => {
  try {
    const response = await api.get('/tanks')
    tanks.value = response.data
  } catch (err) {
    console.error('Error loading tanks:', err)
  }
}

const openTankModal = () => {
  newTankName.value = ''
  newTankVolume.value = 1000
  showTankModal.value = true
}

const addTank = async () => {
  validationErrors.value = []

  if (!newTankName.value || newTankName.value.trim() === '') {
    validationErrors.value.push('نام مخزن اجباری است')
    return
  }

  if (!newTankVolume.value || newTankVolume.value <= 0) {
    validationErrors.value.push('حجم مخزن باید بزرگتر از 0 باشد')
    return
  }

  try {
    const response = await api.post('/tanks', {
      name: newTankName.value,
      volume_liters: newTankVolume.value,
      water_ec_ms_cm: null,
      water_ph: null,
      water_hco3_ppm: 0,
      water_ca_ppm: 0,
      water_mg_ppm: 0,
      water_na_ppm: 0,
      water_cl_ppm: 0,
      water_so4_ppm: 0,
      water_no3_ppm: 0,
      water_fe_ppm: 0
    })
    tanks.value.push(response.data)
    showTankModal.value = false
    errorMessage.value = ''
    validationErrors.value = []
  } catch (err: any) {
    console.error('Error creating tank:', err)
    if (err.response?.data?.detail) {
      if (typeof err.response.data.detail === 'string') {
        errorMessage.value = err.response.data.detail
      } else if (Array.isArray(err.response.data.detail)) {
        validationErrors.value = err.response.data.detail.map((e: any) => `${e.loc.join('.')}: ${e.msg}`)
      } else {
        errorMessage.value = 'خطا در ایجاد مخزن'
      }
    } else {
      errorMessage.value = 'خطا در ارتباط با سرور'
    }
  }
}

const deleteTank = async (tankId: number) => {
  try {
    await api.delete(`/tanks/${tankId}`)
    tanks.value = tanks.value.filter(t => t.id !== tankId)
    if (selectedTank.value?.id === tankId) {
      selectedTank.value = null
      resetTempParams()
    }
  } catch (err) {
    errorMessage.value = 'خطا در حذف مخزن'
  }
}

const selectTank = (tank: any) => {
  selectedTank.value = tank
  resetTempParams()
}

const resetTempParams = () => {
  tempWaterEc.value = selectedTank.value?.water_ec_ms_cm ?? null
  tempWaterPh.value = selectedTank.value?.water_ph ?? null
  tempWaterHco3.value = selectedTank.value?.water_hco3_ppm ?? 0
  tempWaterCa.value = selectedTank.value?.water_ca_ppm ?? 0
  tempWaterMg.value = selectedTank.value?.water_mg_ppm ?? 0
}

const calculate = async () => {
  validationErrors.value = []

  if (!selectedVariety.value) {
    validationErrors.value.push('لطفاً رقم گیاه را انتخاب کنید')
  }
  if (!selectedStage.value) {
    validationErrors.value.push('لطفاً مرحله رشد را انتخاب کنید')
  }
  if (!selectedTank.value) {
    validationErrors.value.push('لطفاً یک مخزن را انتخاب کنید')
  }

  if (validationErrors.value.length > 0) {
    return
  }

  // Validate EC and PH
  if (tempWaterEc.value !== null && tempWaterEc.value !== undefined) {
    if (tempWaterEc.value < 0) {
      validationErrors.value.push('EC آب نمی‌تواند منفی باشد')
    }
    if (tempWaterEc.value > 10) {
      validationErrors.value.push(`EC آب باید کمتر یا مساوی 10 باشد (مقدار وارد شده: ${tempWaterEc.value})`)
    }
  }

  if (tempWaterPh.value !== null && tempWaterPh.value !== undefined) {
    if (tempWaterPh.value < 0) {
      validationErrors.value.push('pH آب نمی‌تواند منفی باشد')
    }
    if (tempWaterPh.value > 14) {
      validationErrors.value.push(`pH آب باید بین 0 تا 14 باشد (مقدار وارد شده: ${tempWaterPh.value})`)
    }
  }

  if (tempWaterHco3.value < 0) {
    validationErrors.value.push('بیکربنات آب نمی‌تواند منفی باشد')
  }
  if (tempWaterHco3.value > 500) {
    validationErrors.value.push(`بیکربنات آب باید کمتر یا مساوی 500 ppm باشد (مقدار وارد شده: ${tempWaterHco3.value})`)
  }

  if (validationErrors.value.length > 0) {
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  result.value = null

  try {
    const response = await api.post('/calculate', {
      crop_name: selectedCrop.value,
      variety_name: selectedVariety.value,
      stage_name: selectedStage.value,
      brand_filter: selectedBrand.value || null,
      tank: {
        name: selectedTank.value.name,
        volume_liters: selectedTank.value.volume_liters,
        water_ec_ms_cm: tempWaterEc.value,
        water_ph: tempWaterPh.value,
        water_hco3_ppm: tempWaterHco3.value || 0,
        water_ca_ppm: tempWaterCa.value || 0,
        water_mg_ppm: tempWaterMg.value || 0,
        water_na_ppm: 0,
        water_cl_ppm: 0,
        water_so4_ppm: 0,
        water_no3_ppm: 0,
        water_fe_ppm: 0
      }
    })
    result.value = response.data
    errorMessage.value = ''
  } catch (err: any) {
    console.error('Calculation error:', err)
    if (err.response?.data?.detail) {
      if (typeof err.response.data.detail === 'string') {
        errorMessage.value = err.response.data.detail
      } else if (Array.isArray(err.response.data.detail)) {
        validationErrors.value = err.response.data.detail.map((e: any) => {
          if (e.msg === 'Input should be less than or equal to 10') {
            return `مقدار ${e.loc.join('.')} باید کمتر یا مساوی 10 باشد`
          }
          if (e.msg === 'Input should be less than or equal to 14') {
            return `مقدار ${e.loc.join('.')} باید کمتر یا مساوی 14 باشد`
          }
          return `${e.loc.join('.')}: ${e.msg}`
        })
      } else {
        errorMessage.value = JSON.stringify(err.response.data.detail)
      }
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
</script>
```

### 📄 `frontend/src/components/calculator/ResultsDisplay.vue`

```vue
<!-- Platform-v3\frontend\src\components\calculator\ResultsDisplay.vue -->

<template>
  <div class="space-y-6 print-friendly">
    <!-- Header Info -->
    <div class="bg-white rounded-xl shadow-card border border-gray-100 p-5">
      <div class="flex flex-wrap justify-between gap-4">
        <div>
          <p class="text-xs text-gray-500 mb-1">📅 تاریخ محاسبه</p>
          <p class="text-sm font-medium text-gray-800">{{ formatDate(result.created_at) }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 mb-1">🌱 مرحله رشد</p>
          <p class="text-sm font-medium text-gray-800">{{ result.stage_name }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 mb-1">🍓 رقم</p>
          <p class="text-sm font-medium text-gray-800">{{ result.variety_name }}</p>
        </div>
        <div>
          <p class="text-xs text-gray-500 mb-1">🗄️ مخزن</p>
          <p class="text-sm font-medium text-gray-800">{{ result.tank_name }} ({{ result.tank_volume_liters }} L)</p>
        </div>
      </div>
    </div>

    <!-- Acid Adjustment Info -->
    <div v-if="result.acid_adjustment && result.acid_adjustment.ml_per_1000L > 0" class="bg-blue-50 border border-blue-200 rounded-xl p-5">
      <div class="flex gap-3">
        <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        <div class="flex-1">
          <h3 class="font-semibold text-blue-800 mb-2">⚗️ تنظیم pH اولیه آب</h3>
          <p class="text-sm text-blue-700">
            به دلیل وجود {{ result.acid_adjustment.hco3_neutralized || 0 }} ppm بیکربنات در آب،
            ابتدا <strong class="font-bold">{{ result.acid_adjustment.ml_per_1000L }}</strong> میلی‌لیتر اسید فسفریک 85% را به ازای هر 1000 لیتر آب اضافه کنید.
          </p>
          <p class="text-xs text-blue-600 mt-2">⚠️ همیشه اسید را به آب اضافه کنید، نه آب را به اسید.</p>
        </div>
      </div>
    </div>

    <!-- Warnings -->
    <div v-if="result.warnings && result.warnings.length > 0" class="bg-amber-50 border border-amber-200 rounded-xl p-5">
      <div class="flex gap-3">
        <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <div class="flex-1">
          <h3 class="font-semibold text-amber-800 mb-2">⚠️ هشدارهای ایمنی</h3>
          <div v-for="(warn, idx) in result.warnings" :key="idx" class="text-sm text-amber-700 mb-2">
            <span class="font-medium">{{ warn.fertilizers?.join(' + ') || '' }}</span>
            <span> - {{ warn.description }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Doses Table -->
    <div class="bg-white rounded-xl shadow-card border border-gray-100 overflow-hidden">
      <div class="px-5 py-4 border-b border-gray-100 bg-gray-50">
        <h3 class="font-semibold text-gray-800 flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          📋 دستور تهیه محلول
        </h3>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">نام کود</th>
              <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">🧪 دوز (g/L)</th>
              <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">🗄️ برای مخزن (g)</th>
              <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">🏺 استوک 200x (g/L)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="dose in result.doses" :key="dose.id" class="hover:bg-gray-50 transition">
              <td class="px-4 py-3 text-sm text-gray-800">{{ dose.name }} <span v-if="dose.brand_name" class="text-xs text-gray-400">({{ dose.brand_name }})</span></td>
              <td class="px-4 py-3 text-sm text-center font-mono font-medium text-green-700">{{ dose.dose_g_per_liter }}</td>
              <td class="px-4 py-3 text-sm text-center text-gray-600">{{ dose.dose_g_for_tank }}</td>
              <td class="px-4 py-3 text-sm text-center text-gray-600">{{ dose.stock_200x_g_per_liter }}</td>
            </tr>
            <tr v-if="result.doses.length === 0">
              <td colspan="4" class="px-4 py-8 text-center text-gray-500">
                ⚠️ هیچ ترکیب بهینه‌ای با کودهای موجود یافت نشد. لطفاً کودهای بیشتری را به دیتابیس اضافه کنید.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="px-5 py-3 bg-gray-50 text-xs text-gray-500 border-t border-gray-100">
        💡 <strong>نکته:</strong> برای ساخت استوک 200 برابر، مقدار ذکر شده را در 1 لیتر آب حل کنید. سپس به ازای هر 1 لیتر آب نهایی، 5 میلی‌لیتر از استوک را اضافه کنید.
      </div>
    </div>

    <!-- Nutrient Comparison -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white rounded-xl shadow-card border border-gray-100 p-5">
        <h4 class="font-semibold text-gray-800 mb-3 flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          🎯 نیاز گیاه (ppm)
        </h4>
        <div class="space-y-2">
          <div v-for="(val, key) in result.target_needs_ppm" :key="key" class="flex justify-between items-center text-sm border-b border-gray-100 pb-1.5">
            <span class="text-gray-600">{{ getElementName(String(key)) }}</span>
            <span class="font-medium text-gray-800">{{ val }}</span>
          </div>
        </div>
        <div class="mt-3 pt-2 text-xs text-gray-400 border-t border-gray-100">
          💡 مقادیر بر اساس رقم {{ result.variety_name }} و مرحله {{ result.stage_name }} تنظیم شده است
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-card border border-gray-100 p-5">
        <h4 class="font-semibold text-gray-800 mb-3 flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          ✅ تامین شده (ppm)
        </h4>
        <div class="space-y-2">
          <div v-for="(val, key) in result.calculated_supply_ppm" :key="key" class="flex justify-between items-center text-sm border-b border-gray-100 pb-1.5">
            <span class="text-gray-600">{{ getElementName(String(key)) }}</span>
            <span class="font-medium text-green-700">{{ val }}</span>
          </div>
        </div>
        <div class="mt-3 pt-2 text-xs text-gray-400 border-t border-gray-100">
          💡 مقادیر تامین شده با استفاده از الگوریتم بهینه‌سازی Least Squares محاسبه شده است
        </div>
      </div>
    </div>

    <!-- EC & pH Targets -->
    <div class="bg-white rounded-xl shadow-card border border-gray-100 p-5 flex flex-col sm:flex-row justify-between items-center gap-4">
      <div class="text-center sm:text-right">
        <p class="text-xs text-gray-500 mb-1">📊 محدوده EC هدف</p>
        <p class="text-xl font-semibold text-gray-800">
          {{ result.ec_ph_targets?.ec_min || 0 }} - {{ result.ec_ph_targets?.ec_max || 0 }} <span class="text-sm font-normal text-gray-500">mS/cm</span>
        </p>
        <p class="text-xs text-gray-400 mt-1">برای این مرحله رشد</p>
      </div>
      <div class="w-px h-8 bg-gray-200 hidden sm:block"></div>
      <div class="text-center sm:text-right">
        <p class="text-xs text-gray-500 mb-1">🔬 محدوده pH هدف</p>
        <p class="text-xl font-semibold text-gray-800">
          {{ result.ec_ph_targets?.ph_min || 0 }} - {{ result.ec_ph_targets?.ph_max || 0 }}
        </p>
        <p class="text-xs text-gray-400 mt-1">برای جذب بهینه عناصر</p>
      </div>
    </div>

    <!-- Mixing Instructions -->
    <div class="bg-white rounded-xl shadow-card border border-gray-100 p-5">
      <h4 class="font-semibold text-gray-800 mb-3 flex items-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        📋 دستورالعمل اختلاط
      </h4>
      <div class="text-sm text-gray-600 whitespace-pre-line font-mono text-xs bg-gray-50 p-4 rounded-lg">
        {{ result.mixing_instructions }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Platform-v3\frontend\src\components\calculator\ResultsDisplay.vue

defineProps<{
  result: any
}>()

const getElementName = (key: string): string => {
  const names: Record<string, string> = {
    N: 'نیتروژن (N)',
    P: 'فسفر (P)',
    K: 'پتاسیم (K)',
    Ca: 'کلسیم (Ca)',
    Mg: 'منیزیم (Mg)',
    S: 'گوگرد (S)',
    Fe: 'آهن (Fe)',
    Zn: 'روی (Zn)',
    Mn: 'منگنز (Mn)',
    Cu: 'مس (Cu)',
    B: 'بور (B)',
    Mo: 'مولیبدن (Mo)',
    Cl: 'کلر (Cl)'
  }
  return names[key] || key
}

const formatDate = (dateStr: string): string => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('fa-IR') + ' - ' + date.toLocaleTimeString('fa-IR')
}
</script>
```

### 📄 `frontend/package.json`

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

## 📁 Project Structure

```
├── backend
│   ├── __init__.py
│   ├── app
│   │   ├── __init__.py
│   │   ├── calculator.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── seed.py
│   ├── farmtech.db
│   ├── requirements.txt
│   └── run.py
├── backup.py
├── CORE_CONTEXT.md
├── frontend
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── public
│   │   ├── favicon.svg
│   │   ├── fonts
│   │   └── icons.svg
│   ├── README.md
│   ├── src
│   │   ├── App.vue
│   │   ├── components
│   │   ├── main.ts
│   │   ├── router
│   │   ├── style.css
│   │   └── views
│   ├── tailwind.config.js
│   ├── test
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
└── README.md
```

---

## 📊 Summary

- **Backend Files:** 6
- **Frontend Files:** 3
- **Generated:** 2026-06-07 18:01:52
