# backend/app/seed/base.py
"""
Base utilities for all seed files
Contains common conversion functions and helper methods
Date: 1405/03/14
"""

from sqlalchemy.orm import Session
from app.models import Brand, Fertilizer


# ============================================================
# Conversion Coefficients (Oxide to Pure Element)
# Scientific exact values
# ============================================================

P2O5_TO_P = 0.4364      # 61.9475 / 141.9445
K2O_TO_K = 0.8301       # 78.1966 / 94.196
CaO_TO_Ca = 0.7147      # 40.078 / 56.0774
MgO_TO_Mg = 0.603       # 24.305 / 40.3044


def convert_p2o5_to_p(p2o5_percent: float) -> float:
    """
    Convert P2O5 percentage to pure P percentage
    
    Args:
        p2o5_percent: Percentage of P2O5
        
    Returns:
        Pure P percentage rounded to 2 decimal places
    """
    return round(p2o5_percent * P2O5_TO_P, 2)


def convert_k2o_to_k(k2o_percent: float) -> float:
    """
    Convert K2O percentage to pure K percentage
    
    Args:
        k2o_percent: Percentage of K2O
        
    Returns:
        Pure K percentage rounded to 2 decimal places
    """
    return round(k2o_percent * K2O_TO_K, 2)


def convert_cao_to_ca(cao_percent: float) -> float:
    """
    Convert CaO percentage to pure Ca percentage
    
    Args:
        cao_percent: Percentage of CaO
        
    Returns:
        Pure Ca percentage rounded to 2 decimal places
    """
    return round(cao_percent * CaO_TO_Ca, 2)


def convert_mgo_to_mg(mgo_percent: float) -> float:
    """
    Convert MgO percentage to pure Mg percentage
    
    Args:
        mgo_percent: Percentage of MgO
        
    Returns:
        Pure Mg percentage rounded to 2 decimal places
    """
    return round(mgo_percent * MgO_TO_Mg, 2)


def get_brand_id(db: Session, brand_name: str) -> int:
    """
    Get brand ID by brand name
    
    Args:
        db: Database session
        brand_name: Name of the brand in Persian
        
    Returns:
        Brand ID
        
    Raises:
        ValueError: If brand not found
    """
    brand = db.query(Brand).filter(Brand.name == brand_name).first()
    if not brand:
        raise ValueError(f"برند '{brand_name}' در دیتابیس وجود ندارد. لطفا ابتدا برند را ایجاد کنید.")
    return brand.id


def get_or_create_brand(db: Session, brand_data: dict) -> Brand:
    """
    Get existing brand or create new one
    
    Args:
        db: Database session
        brand_data: Dictionary containing brand information
        
    Returns:
        Brand object
    """
    brand = db.query(Brand).filter(Brand.name == brand_data["name"]).first()
    if not brand:
        brand = Brand(**brand_data)
        db.add(brand)
        db.flush()
        print(f"   ✅ Brand created: {brand.name}")
    else:
        print(f"   ⏭️  Brand already exists: {brand.name}")
    return brand


def fertilizer_exists(db: Session, name: str, brand_id: int) -> bool:
    """
    Check if a fertilizer already exists in database
    
    Args:
        db: Database session
        name: Fertilizer name
        brand_id: Brand ID
        
    Returns:
        True if exists, False otherwise
    """
    return db.query(Fertilizer).filter(
        Fertilizer.name == name,
        Fertilizer.brand_id == brand_id
    ).first() is not None