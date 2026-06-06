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
    calculate_acid_for_hco3,
    optimize_fertilizer_doses_professional_v2,
    calculate_tank_doses,
    generate_scientific_mixing_instructions
)

router = APIRouter()


# ============================================================
# Health Check
# ============================================================
@router.get("/health")
def health_check():
    return {"status": "ok", "message": "FarmTech API is running"}


# ============================================================
# Crops (محصولات)
# ============================================================
@router.get("/crops", response_model=List[CropResponse])
def get_crops(db: Session = Depends(get_db)):
    """دریافت لیست تمام محصولات"""
    return db.query(Crop).all()


# ============================================================
# Varieties (ارقام)
# ============================================================
@router.get("/varieties", response_model=List[VarietyResponse])
def get_varieties(
    crop_id: Optional[int] = Query(None, description="فیلتر بر اساس محصول"),
    db: Session = Depends(get_db)
):
    """دریافت لیست ارقام گیاهی"""
    query = db.query(Variety)
    if crop_id:
        query = query.filter(Variety.crop_id == crop_id)
    return query.all()


# ============================================================
# Brands (برندها)
# ============================================================
@router.get("/brands", response_model=List[BrandResponse])
def get_brands(db: Session = Depends(get_db)):
    """دریافت لیست برندهای کود"""
    return db.query(Brand).all()


# ============================================================
# Fertilizers (کودها)
# ============================================================
@router.get("/fertilizers", response_model=List[FertilizerResponse])
def get_fertilizers(
    brand_id: Optional[int] = Query(None, description="فیلتر بر اساس آیدی برند"),
    brand_name: Optional[str] = Query(None, description="فیلتر بر اساس نام برند"),
    fertilizer_type: Optional[str] = Query(None, description="فیلتر بر اساس نوع کود (NPK, تک عنصری, ریزمغذی, آلی)"),
    is_active: Optional[bool] = Query(True, description="فقط کودهای فعال"),
    db: Session = Depends(get_db)
):
    """دریافت لیست کودها با قابلیت فیلتر"""
    query = db.query(Fertilizer).filter(Fertilizer.is_active == is_active)
    if brand_id:
        query = query.filter(Fertilizer.brand_id == brand_id)
    if brand_name:
        query = query.filter(Fertilizer.brand_name == brand_name)
    if fertilizer_type:
        query = query.filter(Fertilizer.fertilizer_type == fertilizer_type)
    return query.all()


# ============================================================
# Growth Stages (مراحل رشد)
# ============================================================
@router.get("/growth-stages", response_model=List[GrowthStageResponse])
def get_growth_stages(
    crop_id: Optional[int] = Query(None, description="فیلتر بر اساس محصول"),
    variety_id: Optional[int] = Query(None, description="فیلتر بر اساس رقم"),
    db: Session = Depends(get_db)
):
    """دریافت لیست مراحل رشد گیاه"""
    query = db.query(GrowthStage)
    if crop_id:
        query = query.filter(GrowthStage.crop_id == crop_id)
    if variety_id:
        query = query.filter(GrowthStage.variety_id == variety_id)
    return query.order_by(GrowthStage.stage_order).all()


# ============================================================
# Acids (اسیدها)
# ============================================================
@router.get("/acids", response_model=List[AcidResponse])
def get_acids(db: Session = Depends(get_db)):
    """دریافت لیست اسیدهای قابل استفاده برای تنظیم pH"""
    return db.query(Acid).all()


# ============================================================
# Interactions (تداخلات شیمیایی)
# ============================================================
@router.get("/interactions", response_model=List[InteractionResponse])
def get_interactions(db: Session = Depends(get_db)):
    """دریافت لیست تداخلات شیمیایی بین کودها"""
    return db.query(Interaction).all()


# ============================================================
# Tanks (مخازن) - CRUD
# ============================================================
@router.post("/tanks", response_model=TankResponse, status_code=201)
def create_tank(tank: TankCreate, db: Session = Depends(get_db)):
    """ایجاد مخزن جدید"""
    try:
        tank_data = tank.model_dump()
        for key, value in tank_data.items():
            if value is None:
                if key in ['water_ec_ms_cm', 'water_ph']:
                    tank_data[key] = None
                else:
                    tank_data[key] = 0
        
        db_tank = Tank(**tank_data)
        db.add(db_tank)
        db.commit()
        db.refresh(db_tank)
        return db_tank
    except Exception as e:
        db.rollback()
        print(f"Error creating tank: {str(e)}")
        raise HTTPException(status_code=400, detail=f"خطا در ایجاد مخزن: {str(e)}")


@router.get("/tanks", response_model=List[TankResponse])
def get_tanks(db: Session = Depends(get_db)):
    """دریافت لیست تمام مخازن"""
    try:
        return db.query(Tank).all()
    except Exception as e:
        print(f"Error getting tanks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tanks/{tank_id}", response_model=TankResponse)
def get_tank(tank_id: int, db: Session = Depends(get_db)):
    """دریافت اطلاعات یک مخزن مشخص"""
    tank = db.query(Tank).filter(Tank.id == tank_id).first()
    if not tank:
        raise HTTPException(status_code=404, detail="مخزن یافت نشد")
    return tank


@router.put("/tanks/{tank_id}", response_model=TankResponse)
def update_tank(tank_id: int, tank: TankCreate, db: Session = Depends(get_db)):
    """ویرایش اطلاعات مخزن"""
    db_tank = db.query(Tank).filter(Tank.id == tank_id).first()
    if not db_tank:
        raise HTTPException(status_code=404, detail="مخزن یافت نشد")
    
    tank_data = tank.model_dump()
    for key, value in tank_data.items():
        if value is None:
            if key in ['water_ec_ms_cm', 'water_ph']:
                value = None
            else:
                value = 0
        setattr(db_tank, key, value)
    
    db.commit()
    db.refresh(db_tank)
    return db_tank


@router.delete("/tanks/{tank_id}")
def delete_tank(tank_id: int, db: Session = Depends(get_db)):
    """حذف مخزن"""
    tank = db.query(Tank).filter(Tank.id == tank_id).first()
    if not tank:
        raise HTTPException(status_code=404, detail="مخزن یافت نشد")
    db.delete(tank)
    db.commit()
    return {"message": "مخزن با موفقیت حذف شد"}


# ============================================================
# Calculation History (تاریخچه محاسبات)
# ============================================================
@router.get("/history", response_model=List[CalculationHistoryResponse])
def get_calculation_history(
    limit: int = Query(50, ge=1, le=200, description="تعداد رکوردهای برگشتی"),
    db: Session = Depends(get_db)
):
    """دریافت تاریخچه محاسبات اخیر"""
    return db.query(CalculationHistory).order_by(
        CalculationHistory.created_at.desc()
    ).limit(limit).all()


@router.get("/history/{history_id}", response_model=CalculationHistoryResponse)
def get_calculation_by_id(history_id: int, db: Session = Depends(get_db)):
    """دریافت یک محاسبه مشخص از تاریخچه"""
    history = db.query(CalculationHistory).filter(CalculationHistory.id == history_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="رکورد مورد نظر یافت نشد")
    return history


# ============================================================
# Main Calculation Endpoint (محاسبه اصلی)
# ============================================================
@router.post("/calculate", response_model=CalculationResponse)
def calculate_fertilizer(
    request: CalculationRequest,
    db: Session = Depends(get_db)
):
    """
    محاسبه بهترین ترکیب کود با الگوریتم حرفه‌ای دو مرحله‌ای
    
    ویژگی‌های الگوریتم:
    - وزن دهی به عناصر بر اساس اهمیت (فسفر مهم‌ترین)
    - محدودیت‌های ایمنی و سمیت بر اساس استانداردهای علمی
    - بازه خطای مجاز (تحمل 15% برای عناصر اصلی)
    - اولویت کودهای تخصصی برای ریزمغذی‌ها
    - هشدارهای کیفی برای کمبود یا بیش‌بود عناصر
    """
    try:
        # ============================================================
        # 1. پیدا کردن رقم (Variety)
        # ============================================================
        variety = db.query(Variety).filter(Variety.name == request.variety_name).first()
        if not variety:
            raise HTTPException(
                status_code=404, 
                detail=f"رقم '{request.variety_name}' یافت نشد. ارقام موجود: سن اندرسا, کاماروسا"
            )
        
        # ============================================================
        # 2. پیدا کردن مرحله رشد
        # ============================================================
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
            raise HTTPException(
                status_code=404,
                detail=f"مرحله رشد '{request.stage_name}' برای رقم '{request.variety_name}' یافت نشد"
            )
        
        # ============================================================
        # 3. ایجاد مخزن در دیتابیس
        # ============================================================
        tank_data = request.tank.model_dump()
        for key, value in tank_data.items():
            if value is None:
                if key in ['water_ec_ms_cm', 'water_ph']:
                    tank_data[key] = None
                else:
                    tank_data[key] = 0
        
        tank = Tank(**tank_data)
        db.add(tank)
        db.flush()
        
        # ============================================================
        # 4. نیازهای تغذیه‌ای گیاه
        # ============================================================
        target_needs = stage.nutrient_needs or {}
        for elem in SUPPORTED_ELEMENTS:
            if elem not in target_needs:
                target_needs[elem] = 0
        
        # ============================================================
        # 5. سهم عناصر تامین شده توسط آب مخزن
        # ============================================================
        water_contribution = calculate_water_contribution(tank)
        
        # ============================================================
        # 6. محاسبه اسید مورد نیاز برای خنثی‌سازی بیکربنات
        # ============================================================
        acid_adjustment = None
        if tank.water_hco3_ppm and tank.water_hco3_ppm > 0:
            acid_adjustment = calculate_acid_for_hco3(tank.water_hco3_ppm)
        
        # ============================================================
        # 7. سهم اسید (اختیاری - از درخواست کاربر)
        # ============================================================
        acid_contribution = {elem: 0.0 for elem in SUPPORTED_ELEMENTS}
        
        # ============================================================
        # 8. محاسبه نیاز باقیمانده (پس از کسر سهم آب و اسید)
        # ============================================================
        remaining_needs = {}
        for elem in SUPPORTED_ELEMENTS:
            remaining_needs[elem] = max(0, target_needs[elem] - water_contribution[elem] - acid_contribution[elem])
        
        # ============================================================
        # 9. دریافت کودهای فعال از دیتابیس
        # ============================================================
        query = db.query(Fertilizer).filter(Fertilizer.is_active == True)
        if request.brand_filter:
            query = query.filter(Fertilizer.brand_name == request.brand_filter)
        
        all_fertilizers = query.all()
        
        if not all_fertilizers:
            raise HTTPException(
                status_code=404, 
                detail=f"هیچ کودی یافت نشد. لطفاً دیتابیس را بررسی کنید."
            )
        
        # ============================================================
        # 10. اجرای الگوریتم حرفه‌ای بهینه‌سازی (نسخه 2)
        # ============================================================
        doses, calculated_supply, optimization_warnings, supply_quality = optimize_fertilizer_doses_professional_v2(
            remaining_needs, all_fertilizers, request.brand_filter, 10.0
        )
        
        # ============================================================
        # 11. محاسبه دوز برای حجم مخزن و استوک 200 برابر
        # ============================================================
        doses_with_tank = calculate_tank_doses(doses, tank.volume_liters)
        
        # ============================================================
        # 12. تبدیل هشدارها به فرمت استاندارد
        # ============================================================
        warnings = []
        
        for warn in optimization_warnings:
            warnings.append(WarningResponse(
                type=warn.get('type', 'unknown'),
                severity=warn.get('severity', 'warning'),
                product=None,
                description=warn.get('message', ''),
                fertilizers=[warn.get('fertilizer', '')] if warn.get('fertilizer') else []
            ))
        
        for sq in supply_quality:
            warnings.append(WarningResponse(
                type=sq.get('type', 'supply_quality'),
                severity=sq.get('severity', 'warning'),
                product=sq.get('element', None),
                description=sq.get('message', ''),
                fertilizers=[]
            ))
        
        # ============================================================
        # 13. تولید دستورالعمل اختلاط علمی
        # ============================================================
        mixing_instructions = generate_scientific_mixing_instructions(
            doses_with_tank, 
            [w.model_dump() for w in warnings], 
            tank.volume_liters,
            {
                "hco3_ppm": tank.water_hco3_ppm or 0,
                "ml_per_1000L": acid_adjustment.get("ml_per_1000L", 0) if acid_adjustment else 0
            } if acid_adjustment and acid_adjustment.get("ml_per_1000L", 0) > 0 else None,
            supply_quality
        )
        
        # ============================================================
        # 14. ذخیره در تاریخچه محاسبات
        # ============================================================
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
            water_hco3_ppm=tank.water_hco3_ppm or 0,
            target_needs_ppm=target_needs,
            water_contribution_ppm=water_contribution,
            remaining_needs_ppm=remaining_needs,
            calculated_supply_ppm={k: round(v, 2) for k, v in calculated_supply.items()},
            doses=[d for d in doses_with_tank],
            warnings=[w.model_dump() for w in warnings],
            ec_ph_targets={
                "ec_min": stage.target_ec_min,
                "ec_max": stage.target_ec_max,
                "ph_min": stage.target_ph_min,
                "ph_max": stage.target_ph_max
            },
            mixing_instructions=mixing_instructions,
            acid_adjustment={
                "ml_per_1000L": acid_adjustment.get("ml_per_1000L", 0),
                "element_added_ppm": acid_adjustment.get("element_added_ppm", 0)
            } if acid_adjustment else None,
            success=1
        )
        db.add(history)
        db.commit()
        
        # ============================================================
        # 15. ساخت پاسخ نهایی
        # ============================================================
        return CalculationResponse(
            success=True,
            created_at=datetime.now(),
            stage_name=stage.name,
            variety_name=variety.name,
            tank_name=tank.name,
            tank_volume_liters=tank.volume_liters,
            target_needs_ppm=target_needs,
            water_contribution_ppm=water_contribution,
            acid_contribution_ppm=acid_contribution,
            remaining_needs_ppm=remaining_needs,
            calculated_supply_ppm={k: round(v, 2) for k, v in calculated_supply.items()},
            doses=[DoseResponse(**d) for d in doses_with_tank],
            warnings=warnings,
            ec_ph_targets={
                "ec_min": stage.target_ec_min,
                "ec_max": stage.target_ec_max,
                "ph_min": stage.target_ph_min,
                "ph_max": stage.target_ph_max
            },
            mixing_instructions=mixing_instructions,
            message="محاسبه با موفقیت انجام شد",
            acid_adjustment={
                "ml_per_1000L": acid_adjustment.get("ml_per_1000L", 0),
                "hco3_neutralized": tank.water_hco3_ppm or 0
            } if acid_adjustment and acid_adjustment.get("ml_per_1000L", 0) > 0 else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Calculation error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"خطا در محاسبه: {str(e)}")


# ============================================================
# Debug Endpoint (برای عیب‌یابی)
# ============================================================
@router.get("/debug/stages")
def debug_stages(db: Session = Depends(get_db)):
    """نمایش اطلاعات دیباگ مراحل رشد"""
    stages = db.query(GrowthStage).all()
    return {
        "total": len(stages),
        "stages": [
            {
                "id": s.id,
                "name": s.name,
                "variety_id": s.variety_id,
                "variety_name": s.variety.name if s.variety else None,
                "stage_order": s.stage_order,
                "nutrient_needs": s.nutrient_needs
            }
            for s in stages
        ]
    }


@router.get("/debug/fertilizers")
def debug_fertilizers(db: Session = Depends(get_db)):
    """نمایش اطلاعات دیباگ کودها"""
    fertilizers = db.query(Fertilizer).filter(Fertilizer.is_active == True).all()
    return {
        "total": len(fertilizers),
        "fertilizers": [
            {
                "id": f.id,
                "name": f.name,
                "brand_name": f.brand_name,
                "fertilizer_type": f.fertilizer_type,
                "n_percent": f.n_percent,
                "p_percent": f.p_percent,
                "k_percent": f.k_percent,
                "ca_percent": f.ca_percent,
                "mg_percent": f.mg_percent,
                "s_percent": f.s_percent,
                "max_dose_g_per_liter": f.max_dose_g_per_liter
            }
            for f in fertilizers
        ]
    }