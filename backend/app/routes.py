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
        "version": "3.3.1",
        "dual_tank_support": True,
        "stock_system": True,
        "custom_needs_support": True,
        "multi_brand_support": True
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
# محاسبه با دو مخزن (نسخه 3.3.1)
# ============================================================
# ============================================================
@router.post("/calculate-dual-tank")
async def calculate_dual_tank(
    request: schemas.DualTankRequest,
    db: Session = Depends(get_db)
):
    """
    محاسبه دوز بهینه کودها برای دو مخزن جداگانه - نسخه 3.3.1
    
    قابلیت‌های جدید:
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
        # مرحله 2: اولویت با نیازهای سفارشی کاربر (Custom Nutrient Needs)
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
        # مرحله 3: فیلتر برند (Multi Brand Filter - پشتیبانی از لیست)
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
        # مرحله 4: انجام محاسبات حرفه‌ای دو مخزن
        # ============================================================
        
        result_main, result_calcium, combined_warnings, general_instructions = calculate_dual_tank_professional(
            remaining_needs=plant_needs,
            all_fertilizers=all_fertilizers,
            tank_main=request.tank_main,
            tank_calcium=request.tank_calcium,
            brand_filter=brand_filter_str
        )
        
        # ============================================================
        # مرحله 5: اضافه کردن محاسبات استوک به دوزها
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
        # مرحله 6: محاسبه مصرف استوک
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
        # مرحله 7: ساخت دستورالعمل استوک
        # ============================================================
        
        injector_explanation = get_injector_explanation(request.injector_ratio)
        usage_instructions = get_stock_usage_instructions(request.injector_ratio)
        storage_instructions, shelf_life_fridge, shelf_life_room, warning_signs = get_storage_instructions()
        
        main_fertilizer_names = [d.get("name", "") for d in result_main.get("doses", [])]
        main_mixing_instructions = get_stock_mixing_instructions(main_fertilizer_names)
        
        calcium_fertilizer_names = [d.get("name", "") for d in result_calcium.get("doses", [])]
        calcium_mixing_instructions = get_stock_mixing_instructions(calcium_fertilizer_names)
        
        # ============================================================
        # مرحله 8: محاسبه زمان و آماده‌سازی پاسخ
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