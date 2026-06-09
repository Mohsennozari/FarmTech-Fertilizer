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