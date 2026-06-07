# Platform-v3\backend\app\routes.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
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
