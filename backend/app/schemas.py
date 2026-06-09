# Platform-v3\backend\app\schemas.py

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============================================================
# مدل‌های مربوط به Brand
# ============================================================
class BrandBase(BaseModel):
    name: str
    country: Optional[str] = None
    website: Optional[str] = None
    notes: Optional[str] = None


class BrandCreate(BrandBase):
    pass


class Brand(BrandBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# مدل‌های مربوط به Crop
# ============================================================
class CropBase(BaseModel):
    name: str
    scientific_name: Optional[str] = None
    cultivation_type: Optional[str] = None


class CropCreate(CropBase):
    pass


class Crop(CropBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# مدل‌های مربوط به Variety
# ============================================================
class VarietyBase(BaseModel):
    crop_id: int
    name: str
    description: Optional[str] = None
    growth_days: Optional[int] = None
    yield_potential: Optional[str] = None


class VarietyCreate(VarietyBase):
    pass


class Variety(VarietyBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# مدل‌های مربوط به Fertilizer
# ============================================================
class FertilizerBase(BaseModel):
    name: str
    brand_id: Optional[int] = None
    brand_name: Optional[str] = None
    fertilizer_form: Optional[str] = "powder"
    chemical_formula: Optional[str] = None
    molecular_weight: Optional[float] = None
    purity_percent: Optional[float] = 100.0
    fertilizer_type: Optional[str] = None
    max_dose_g_per_liter: Optional[float] = None
    max_dose_ml_per_liter: Optional[float] = None
    min_dose_g_per_liter: Optional[float] = 0.01
    density_g_per_ml: Optional[float] = None
    n_percent: Optional[float] = 0
    p_percent: Optional[float] = 0
    k_percent: Optional[float] = 0
    ca_percent: Optional[float] = 0
    mg_percent: Optional[float] = 0
    s_percent: Optional[float] = 0
    fe_percent: Optional[float] = 0
    zn_percent: Optional[float] = 0
    mn_percent: Optional[float] = 0
    cu_percent: Optional[float] = 0
    b_percent: Optional[float] = 0
    mo_percent: Optional[float] = 0
    cl_percent: Optional[float] = 0
    solubility_g_per_l: Optional[float] = None
    ph_effect: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = True


class FertilizerCreate(FertilizerBase):
    pass


class Fertilizer(FertilizerBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# مدل‌های مربوط به GrowthStage
# ============================================================
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


class GrowthStageCreate(GrowthStageBase):
    pass


class GrowthStage(GrowthStageBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# مدل‌های مربوط به Interaction
# ============================================================
class InteractionBase(BaseModel):
    fertilizer_a_id: int
    fertilizer_b_id: int
    reaction_type: str
    severity: str
    precipitate_product: Optional[str] = None
    description: Optional[str] = None


class InteractionCreate(InteractionBase):
    pass


class Interaction(InteractionBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# مدل‌های مربوط به Acid
# ============================================================
class AcidBase(BaseModel):
    name: str
    chemical_formula: Optional[str] = None
    concentration_percent: float
    density_g_per_ml: Optional[float] = None
    supplies_element: Optional[str] = None
    element_percent: Optional[float] = None
    ml_per_1000L_per_ph_point: Optional[float] = None
    notes: Optional[str] = None


class AcidCreate(AcidBase):
    pass


class Acid(AcidBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# مدل‌های مربوط به Tank
# ============================================================
class TankBase(BaseModel):
    name: str
    tank_type: Optional[str] = "main"
    volume_liters: float
    water_ec_ms_cm: Optional[float] = None
    water_ph: Optional[float] = None
    water_ca_ppm: Optional[float] = 0
    water_mg_ppm: Optional[float] = 0
    water_na_ppm: Optional[float] = 0
    water_cl_ppm: Optional[float] = 0
    water_so4_ppm: Optional[float] = 0
    water_hco3_ppm: Optional[float] = 0
    water_no3_ppm: Optional[float] = 0
    water_fe_ppm: Optional[float] = 0
    notes: Optional[str] = None


class TankCreate(TankBase):
    pass


class Tank(TankBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# مدل‌های مربوط به دوز کود
# ============================================================
class DoseItem(BaseModel):
    name: str
    persian_name: Optional[str] = None
    brand_name: Optional[str] = None
    dose_g_per_liter: float
    dose_g_for_tank: float
    dose_ml_per_liter: Optional[float] = None
    dose_ml_for_tank: Optional[float] = None
    stock_200x_g_per_liter: Optional[float] = None
    stock_200x_ml_per_liter: Optional[float] = None
    fertilizer_type: Optional[str] = None
    caution: Optional[str] = None


# ============================================================
# مدل‌های مربوط به درخواست و پاسخ دو مخزن
# ============================================================
class DualTankRequest(BaseModel):
    """درخواست محاسبه با دو مخزن - کشاورز باید هر دو مخزن را وارد کند"""
    crop_name: str
    variety_name: str
    stage_name: str
    brand_filter: Optional[str] = None
    tank_main: TankBase
    tank_calcium: TankBase

    @validator('tank_calcium')
    def validate_calcium_tank(cls, v):
        v.tank_type = "calcium"
        return v

    @validator('tank_main')
    def validate_main_tank(cls, v):
        v.tank_type = "main"
        return v


class SingleTankResult(BaseModel):
    """نتیجه محاسبه برای یک مخزن"""
    tank_name: str
    tank_type: str
    tank_volume_liters: float
    doses: List[DoseItem]
    water_contribution_ppm: Dict[str, float]
    remaining_needs_ppm: Dict[str, float]
    supplied_ppm: Dict[str, float]
    warnings: List[str]
    mixing_instructions: str
    acid_adjustment: Optional[Dict[str, Any]] = None
    target_ec: Optional[float] = None
    target_ph: Optional[float] = None


class DualTankResponse(BaseModel):
    """پاسخ نهایی محاسبات با دو مخزن"""
    success: bool
    crop_name: str
    variety_name: str
    stage_name: str
    tank_main_result: SingleTankResult
    tank_calcium_result: SingleTankResult
    combined_warnings: List[str]
    general_mixing_instructions: str
    calculation_time_ms: Optional[float] = None
    error_message: Optional[str] = None


# ============================================================
# مدل‌های قبلی برای سازگاری با عقب (Backward Compatible)
# ============================================================
class CalculateRequest(BaseModel):
    """درخواست محاسبه با یک مخزن (برای سازگاری با نسخه‌های قبل)"""
    crop_name: str
    variety_name: str
    stage_name: str
    brand_filter: Optional[str] = None
    tank: TankBase


class CalculateResponse(BaseModel):
    """پاسخ محاسبه با یک مخزن (برای سازگاری با نسخه‌های قبل)"""
    success: bool
    stage_name: str
    variety_name: str
    tank_name: str
    tank_volume_liters: float
    doses: List[DoseItem]
    warnings: List[str]
    mixing_instructions: str
    target_nutrients: Optional[Dict[str, float]] = None
    supplied_nutrients: Optional[Dict[str, float]] = None
    acid_adjustment: Optional[Dict[str, Any]] = None


# ============================================================
# مدل‌های مربوط به History
# ============================================================
class CalculationHistoryResponse(BaseModel):
    id: int
    created_at: datetime
    crop_name: str
    variety_name: str
    stage_name: str
    brand_filter: Optional[str] = None
    tank_main_name: str
    tank_calcium_name: str
    doses_main: List[DoseItem]
    doses_calcium: List[DoseItem]
    combined_warnings: List[str]
    success: int

    class Config:
        from_attributes = True