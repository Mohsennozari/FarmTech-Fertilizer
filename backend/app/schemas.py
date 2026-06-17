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
    water_ec_ms_cm: Optional[float] = Field(0.4, ge=0, le=10, description="EC آب به میلی‌زیمنس بر سانتی‌متر")
    water_ph: Optional[float] = Field(7.0, ge=0, le=14, description="pH آب")
    water_ca_ppm: float = Field(50, ge=0, description="کلسیم آب به ppm")
    water_mg_ppm: float = Field(20, ge=0, description="منیزیم آب به ppm")
    water_hco3_ppm: float = Field(0, ge=0, description="بیکربنات آب به ppm")
    water_cl_ppm: float = Field(0, ge=0, description="کلر آب به ppm")
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
    crop_name: str = Field(..., description="نام محصول")
    variety_name: str = Field(..., description="نام رقم")
    stage_name: str = Field(..., description="مرحله رشد")
    brand_filter: Optional[str] = Field(None, description="فیلتر برند")
    tank: TankCreate = Field(..., description="اطلاعات مخزن اصلی")
    stock_tank_volume_liters: float = Field(20.0, ge=1.0, le=500.0, description="حجم مخزن استوک")
    injector_ratio: float = Field(200.0, ge=50, le=1000, description="نسبت تزریق")

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
# Calculation Response Schemas
# ============================================================
class FertilizerDose(BaseModel):
    name: str
    dose_g_per_liter: float
    dose_g_for_tank: float
    dose_kg_for_stock: float
    dose_g_for_stock_alternative: Optional[float] = None


class StockInstructions(BaseModel):
    stock_tank_volume_liters: float
    injector_ratio: float
    main_tank_volume_liters: float
    injector_explanation: str
    fertilizers_for_stock: List[Dict[str, Any]]
    mixing_instructions: str
    stock_liters_for_main_tank: float
    stock_ml_per_liter: float
    usage_instructions: str
    storage_instructions: str
    shelf_life_fridge: str
    shelf_life_room: str
    warning_signs: str


class NutrientComparison(BaseModel):
    element: str
    required_ppm: float
    supplied_ppm: float
    difference_ppm: float
    status: str


class CalculationResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    crop_name: str
    variety_name: str
    stage_name: str
    tank_name: str
    tank_volume_liters: float
    doses: List[FertilizerDose]
    stock_instructions: StockInstructions
    warnings: List[str] = []
    interactions: List[Dict[str, str]] = []
    nutrient_comparison: Optional[List[NutrientComparison]] = None
    custom_needs: Optional[Dict[str, float]] = None
    target_ec: Optional[float] = None
    target_ph: Optional[float] = None
    calculation_time: datetime = Field(default_factory=datetime.now)


# ============================================================
# Create Schemas
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
# 🆕 DualTankRequest با پشتیبانی از عناصر هدف ۱۶ گانه
# ============================================================
class DualTankRequest(BaseModel):
    """درخواست محاسبه دو مخزن - نسخه 3.4.0 با پشتیبانی از عناصر هدف ۱۶ گانه"""

    # اطلاعات محصول و مرحله رشد
    crop_name: str = Field(..., description="نام محصول")
    variety_name: str = Field(..., description="نام رقم")
    stage_name: str = Field(..., description="مرحله رشد")

    # فیلتر برند (چندگانه)
    brand_filter: Optional[List[str]] = Field(None, description="لیست برندهای انتخاب شده")

    # اطلاعات مخازن
    tank_main: TankCreate = Field(..., description="اطلاعات مخزن اصلی")
    tank_calcium: TankCreate = Field(..., description="اطلاعات مخزن کلسیم")

    # تنظیمات سیستم استوک
    stock_tank_volume_liters: float = Field(20.0, ge=1.0, le=500.0, description="حجم مخزن استوک")
    injector_ratio: float = Field(200.0, ge=50, le=1000, description="نسبت تزریق")

    # ============================================================
    # 🆕 عناصر هدف ۱۶ گانه
    # ============================================================
    target_elements_16: Optional[Dict[str, float]] = Field(
        None,
        description="عناصر هدف ۱۶ گانه (N-NO3, P, S, N-NH4, K, Ca, Mg, Na, Cl, Fe, Mn, Zn, B, Cu, Mo)"
    )

    # نیازهای سفارشی کاربر (فرمت قدیمی - برای سازگاری)
    custom_nutrient_needs: Optional[Dict[str, float]] = Field(
        None,
        description="نیازهای تغذیه‌ای سفارشی (فرمت قدیمی)"
    )

    # ============================================================
    # آنالیز آب و پساب ترکیبی
    # ============================================================
    water_percent: float = Field(80.0, ge=0, le=100, description="درصد آب تامینی")
    wastewater_percent: float = Field(20.0, ge=0, le=100, description="درصد پساب تامینی")
    water_analysis: Dict[str, float] = Field(
        default_factory=dict,
        description="آنالیز آب (N-NO3, P, S, N-NH4, K, Ca, Fe, Mn, Zn, B, Cu, Mo, EC, pH)"
    )
    wastewater_analysis: Dict[str, float] = Field(
        default_factory=dict,
        description="آنالیز پساب (N-NO3, P, S, N-NH4, K, Ca, Fe, Mn, Zn, B, Cu, Mo, EC, pH)"
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
                "target_elements_16": {
                    "N-NO3": 150,
                    "P": 30,
                    "S": 50,
                    "N-NH4": 10,
                    "K": 200,
                    "Ca": 180,
                    "Mg": 40,
                    "Na": 0,
                    "Cl": 0,
                    "Fe": 2.5,
                    "Mn": 0.5,
                    "Zn": 0.3,
                    "B": 0.2,
                    "Cu": 0.05,
                    "Mo": 0.02
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

    @validator('target_elements_16')
    def validate_target_elements_16(cls, v):
        if v is None:
            return v
        valid_elements = ['N-NO3', 'P', 'S', 'N-NH4', 'K', 'Ca', 'Mg', 'Na', 'Cl', 'Fe', 'Mn', 'Zn', 'B', 'Cu', 'Mo']
        for key in v.keys():
            if key not in valid_elements:
                raise ValueError(f"عنصر نامعتبر: {key}. عناصر مجاز: {', '.join(valid_elements)}")
        for key, value in v.items():
            if value < 0:
                raise ValueError(f"مقدار عنصر {key} نمی‌تواند منفی باشد: {value}")
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
    confirm: bool
    password: Optional[str] = None


class ResetResponse(BaseModel):
    success: bool
    message: str
    tables_dropped: Optional[List[str]] = None
    tables_created: Optional[List[str]] = None
