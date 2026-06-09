from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============================================================
# Tank Schemas
# ============================================================
class TankBase(BaseModel):
    name: str
    volume_liters: float = Field(..., gt=0, description="حجم مخزن به لیتر")
    water_ec_ms_cm: Optional[float] = Field(None, ge=0, le=10, description="EC آب به میلی‌زیمنس بر سانتی‌متر")
    water_ph: Optional[float] = Field(None, ge=0, le=14, description="pH آب")
    water_ca_ppm: float = Field(0, ge=0, description="کلسیم آب به ppm")
    water_mg_ppm: float = Field(0, ge=0, description="منیزیم آب به ppm")
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
                    "water_ec_ms_cm": 0.8,
                    "water_ph": 7.0,
                    "water_ca_ppm": 40,
                    "water_mg_ppm": 15
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


class DualTankRequest(BaseModel):
    crop_name: str
    variety_name: str
    stage_name: str
    brand_filter: Optional[str] = None
    tank_main: TankCreate
    tank_calcium: TankCreate
    stock_tank_volume_liters: float = 20.0
    injector_ratio: float = 200.0


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