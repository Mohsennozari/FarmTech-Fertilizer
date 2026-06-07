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
    chemical_formula: Optional[str] = None
    molecular_weight: Optional[float] = None
    purity_percent: float = 100.0
    fertilizer_type: Optional[str] = None
    max_dose_g_per_liter: Optional[float] = None
    min_dose_g_per_liter: Optional[float] = 0.01

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

class AcidResponse(AcidBase):
    id: int
    class Config:
        from_attributes = True


class TankBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    volume_liters: float = Field(..., gt=0, le=100000)
    water_ec_ms_cm: Optional[float] = Field(None, ge=0, le=10)
    water_ph: Optional[float] = Field(None, ge=0, le=14)
    water_ca_ppm: float = 0
    water_mg_ppm: float = 0
    water_na_ppm: float = 0
    water_cl_ppm: float = 0
    water_so4_ppm: float = 0
    water_hco3_ppm: float = 0
    water_no3_ppm: float = 0
    water_fe_ppm: float = 0
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
    dose_g_per_liter: float
    dose_g_for_tank: float
    stock_200x_g_per_liter: float
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
    acid_contribution_ppm: Optional[Dict[str, float]] = None  # ← آپشنال شد
    remaining_needs_ppm: Dict[str, float]
    calculated_supply_ppm: Dict[str, float]
    doses: List[DoseResponse]
    warnings: List[WarningResponse]
    ec_ph_targets: Dict[str, Optional[float]]
    mixing_instructions: str
    message: Optional[str] = None


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
