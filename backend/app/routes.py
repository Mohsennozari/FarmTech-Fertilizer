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
    # ============================================================
    # توابع جدید نسخه 3.3.0
    # ============================================================
    calculate_dose_kg_for_stock,
    calculate_stock_consumption,
    get_injector_explanation,
    get_stock_mixing_instructions,
    get_stock_usage_instructions,
    get_storage_instructions,
    add_stock_calculations_to_doses
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["FarmTech API"])


# ============================================================
# Health Check
# ============================================================
@router.get("/health")
def health_check():
    return {"status": "ok", "version": "3.3.0", "dual_tank_support": True, "stock_system": True}


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
# محاسبه با یک مخزن - نسخه 3.3.0 با پشتیبانی از سیستم استوک
# ============================================================
# ============================================================
@router.post("/calculate", response_model=schemas.CalculationResponse)
def calculate(request: schemas.CalculationRequest, db: Session = Depends(get_db)):
    """
    محاسبه دوز بهینه کودها برای یک مخزن - نسخه 3.3.0
    
    این endpoint با پشتیبانی از سیستم استوک به‌روزرسانی شده است:
    - محاسبه مقدار کود مورد نیاز برای ساخت استوک (کیلوگرم)
    - محاسبه مقدار مصرف استوک در مخزن اصلی
    - توضیح مفهوم نسبت تزریق برای کاربر
    - دستورالعمل گام به گام ساخت و مصرف استوک
    """
    try:
        # دریافت مرحله رشد
        growth_stage = db.query(models.GrowthStage).join(models.Crop).join(models.Variety).filter(
            models.Crop.name == request.crop_name,
            models.Variety.name == request.variety_name,
            models.GrowthStage.name == request.stage_name
        ).first()
        
        if not growth_stage:
            raise HTTPException(status_code=404, detail="Growth stage not found")
        
        # دریافت کودها با فیلتر برند
        query = db.query(models.Fertilizer).filter(models.Fertilizer.is_active == True)
        if request.brand_filter:
            query = query.filter(models.Fertilizer.brand_name == request.brand_filter)
        
        fertilizers = query.all()
        
        if not fertilizers:
            # ایجاد پاسخ خطا با ساختار کامل StockInstructions
            empty_stock_instructions = schemas.StockInstructions(
                stock_tank_volume_liters=request.stock_tank_volume_liters,
                injector_ratio=request.injector_ratio,
                main_tank_volume_liters=request.tank.volume_liters,
                injector_explanation=get_injector_explanation(request.injector_ratio),
                fertilizers_for_stock=[],
                mixing_instructions=get_stock_mixing_instructions([]),
                stock_liters_for_main_tank=0,
                stock_ml_per_liter=0,
                usage_instructions=get_stock_usage_instructions(request.injector_ratio),
                storage_instructions=get_storage_instructions()[0],
                shelf_life_fridge=get_storage_instructions()[1],
                shelf_life_room=get_storage_instructions()[2],
                warning_signs=get_storage_instructions()[3]
            )
            
            return schemas.CalculationResponse(
                success=False,
                crop_name=request.crop_name,
                variety_name=request.variety_name,
                stage_name=request.stage_name,
                tank_name=request.tank.name,
                tank_volume_liters=request.tank.volume_liters,
                doses=[],
                stock_instructions=empty_stock_instructions,
                warnings=["هیچ کود فعالی برای محاسبه وجود ندارد"]
            )
        
        # محاسبه سهم عناصر از آب
        water_contribution = calculate_water_contribution(request.tank)
        
        # محاسبه نیاز باقیمانده پس از کسر سهم آب
        remaining_needs = {}
        for elem, need in (growth_stage.nutrient_needs or {}).items():
            water = water_contribution.get(elem, 0)
            remaining_needs[elem] = max(0, need - water)
        
        # بهینه‌سازی دوز کودها
        doses_raw, final_supply, warnings = optimize_fertilizer_doses_professional(
            remaining_needs=remaining_needs,
            fertilizers=fertilizers,
            brand_filter=request.brand_filter
        )
        
        # محاسبه دوز برای کل مخزن
        doses = calculate_tank_doses(doses_raw, request.tank.volume_liters)
        
        # ============================================================
        # بخش جدید: اضافه کردن محاسبات استوک به دوزها
        # ============================================================
        doses_with_stock = add_stock_calculations_to_doses(
            doses=doses,
            tank_volume_liters=request.tank.volume_liters,
            injector_ratio=request.injector_ratio,
            stock_tank_volume_liters=request.stock_tank_volume_liters
        )
        
        # محاسبه مصرف استوک در مخزن اصلی
        stock_liters_for_main_tank, stock_ml_per_liter = calculate_stock_consumption(
            injector_ratio=request.injector_ratio,
            main_tank_volume_liters=request.tank.volume_liters
        )
        
        # آماده سازی لیست کودها برای دستورالعمل ساخت استوک
        fertilizers_for_stock = []
        for dose in doses_with_stock:
            fertilizers_for_stock.append({
                "name": dose.get("name", ""),
                "kg": dose.get("dose_kg_for_stock", 0),
                "g_alternative": dose.get("dose_g_for_stock_alternative")
            })
        
        # دریافت دستورالعمل‌های استوک
        fertilizer_names = [d.get("name", "") for d in doses_with_stock]
        mixing_instructions = get_stock_mixing_instructions(fertilizer_names)
        usage_instructions = get_stock_usage_instructions(request.injector_ratio)
        storage_instructions, shelf_life_fridge, shelf_life_room, warning_signs = get_storage_instructions()
        injector_explanation = get_injector_explanation(request.injector_ratio)
        
        # ساخت دستورالعمل استوک کامل
        stock_instructions = schemas.StockInstructions(
            stock_tank_volume_liters=request.stock_tank_volume_liters,
            injector_ratio=request.injector_ratio,
            main_tank_volume_liters=request.tank.volume_liters,
            injector_explanation=injector_explanation,
            fertilizers_for_stock=fertilizers_for_stock,
            mixing_instructions=mixing_instructions,
            stock_liters_for_main_tank=stock_liters_for_main_tank,
            stock_ml_per_liter=stock_ml_per_liter,
            usage_instructions=usage_instructions,
            storage_instructions=storage_instructions,
            shelf_life_fridge=shelf_life_fridge,
            shelf_life_room=shelf_life_room,
            warning_signs=warning_signs
        )
        
        # محاسبه EC پیش‌بینی شده
        ec_predicted = calculate_final_ec(request.tank.water_ec_ms_cm or 0, doses)
        
        # هشدار EC
        ec_warning = get_ec_warning(
            predicted_ec=ec_predicted,
            target_ec_min=growth_stage.target_ec_min,
            target_ec_max=growth_stage.target_ec_max
        )
        if ec_warning:
            warnings.append({
                "type": "ec_warning",
                "severity": "warning",
                "message": ec_warning
            })
        
        # تبدیل هشدارها به لیست رشته‌ها
        warnings_list = [w.get('message', str(w)) for w in warnings]
        
        # ساخت پاسخ نهایی
        return schemas.CalculationResponse(
            success=True,
            crop_name=request.crop_name,
            variety_name=request.variety_name,
            stage_name=request.stage_name,
            tank_name=request.tank.name,
            tank_volume_liters=request.tank.volume_liters,
            doses=doses_with_stock,
            stock_instructions=stock_instructions,
            warnings=warnings_list,
            interactions=[],
            nutrient_comparison=None,
            target_ec=growth_stage.target_ec_max,
            target_ph=growth_stage.target_ph_max
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Calculation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# ============================================================
# محاسبه با دو مخزن (Endpoint نسخه 3.3.0)
# ============================================================
# ============================================================
@router.post("/calculate-dual-tank")
async def calculate_dual_tank(
    request: schemas.DualTankRequest,
    db: Session = Depends(get_db)
):
    """
    محاسبه دوز بهینه کودها برای دو مخزن جداگانه - نسخه 3.3.0
    
    مخزن اصلی (Main): برای کودهای غیر کلسیمی (NPK، سولفات‌ها، ریز مغذی‌ها)
    مخزن کلسیم (Calcium): برای کودهای حاوی کلسیم (نیترات کلسیم، کلات آهن)
    
    کشاورز باید اطلاعات هر دو مخزن را وارد کند تا سیستم دستورالعمل ساخت جداگانه بدهد.
    """
    start_time = time.time()
    
    try:
        # دریافت نیازهای تغذیه‌ای بر اساس محصول، رقم و مرحله رشدی
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
        
        # دریافت لیست کودهای فعال
        query = db.query(models.Fertilizer).filter(models.Fertilizer.is_active == True)
        if request.brand_filter:
            query = query.filter(models.Fertilizer.brand_name == request.brand_filter)
        
        all_fertilizers = query.all()
        
        if not all_fertilizers:
            return {
                "success": False,
                "error_message": "هیچ کود فعالی در دیتابیس یافت نشد"
            }
        
        # دریافت نیازهای گیاه - این مهم است که به فرانت ارسال شود
        plant_needs = growth_stage.nutrient_needs or {}
        
        # انجام محاسبات حرفه‌ای دو مخزن
        result_main, result_calcium, combined_warnings, general_instructions = calculate_dual_tank_professional(
            remaining_needs=plant_needs,
            all_fertilizers=all_fertilizers,
            tank_main=request.tank_main,
            tank_calcium=request.tank_calcium,
            brand_filter=request.brand_filter
        )
        
        calculation_time = (time.time() - start_time) * 1000
        
        # تبدیل هشدارها به فرمت مناسب
        warnings_main_list = [w.get('message', str(w)) for w in result_main.get('warnings', [])]
        warnings_calcium_list = [w.get('message', str(w)) for w in result_calcium.get('warnings', [])]
        combined_warnings_list = [w.get('message', str(w)) for w in combined_warnings]
        
        # ساخت پاسخ با target_needs
        return {
            "success": True,
            "crop_name": request.crop_name,
            "variety_name": request.variety_name,
            "stage_name": request.stage_name,
            "target_needs": plant_needs,
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
                "target_ph": growth_stage.target_ph_max
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
                "target_ph": growth_stage.target_ph_min
            },
            "combined_warnings": combined_warnings_list,
            "general_mixing_instructions": general_instructions,
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