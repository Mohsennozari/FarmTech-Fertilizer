# backend/test_comprehensive.py

import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Tuple

# تنظیم مسیر دیتابیس
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "farmtech.db")
os.environ['DATABASE_URL'] = f'sqlite:///{DB_PATH.replace(os.sep, "/")}'

sys.path.insert(0, BASE_DIR)

from app.database import SessionLocal
from app import models
from app.calculator import calculate_dual_tank_professional
from app.schemas import TankCreate

# ============================================================
# تنظیمات رنگ برای خروجی کنسول
# ============================================================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    print(f"\n{Colors.HEADER}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^80}{Colors.END}")
    print(f"{Colors.HEADER}{'='*80}{Colors.END}")


def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_warning(text: str):
    print(f"{Colors.YELLOW}⚠️ {text}{Colors.END}")


def print_error(text: str):
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_info(text: str):
    print(f"{Colors.BLUE}ℹ️ {text}{Colors.END}")


# ============================================================
# سناریوهای تست
# ============================================================

# سناریوهای کیفیت آب
WATER_QUALITY_SCENARIOS = {
    "آب عالی (اسمز معکوس)": {
        "ec": 0.1,
        "ph": 6.5,
        "ca": 10,
        "mg": 5,
        "hco3": 0,
        "cl": 0
    },
    "آب معمولی (چاه/شهر)": {
        "ec": 0.4,
        "ph": 7.0,
        "ca": 50,
        "mg": 20,
        "hco3": 50,
        "cl": 20
    },
    "آب سخت (قلیایی)": {
        "ec": 0.8,
        "ph": 7.8,
        "ca": 100,
        "mg": 40,
        "hco3": 200,
        "cl": 50
    },
    "آب شور (نامناسب)": {
        "ec": 1.5,
        "ph": 8.0,
        "ca": 150,
        "mg": 80,
        "hco3": 300,
        "cl": 150
    }
}

# مراحل رشد توت فرنگی با نیازهای ppm
GROWTH_STAGES = {
    "استقرار نشاء": {
        "N": 50, "P": 30, "K": 55, "Ca": 50, "Mg": 20, "S": 15,
        "Fe": 2, "Zn": 0.5, "Mn": 0.5, "Cu": 0.1, "B": 0.2, "Mo": 0.05, "Cl": 0
    },
    "ریشه‌زایی": {
        "N": 70, "P": 40, "K": 75, "Ca": 65, "Mg": 25, "S": 18,
        "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0
    },
    "رشد رویشی": {
        "N": 120, "P": 50, "K": 120, "Ca": 105, "Mg": 40, "S": 25,
        "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.4, "Mo": 0.05, "Cl": 0
    },
    "گلدهی": {
        "N": 100, "P": 60, "K": 130, "Ca": 105, "Mg": 35, "S": 22,
        "Fe": 3, "Zn": 0.8, "Mn": 0.8, "Cu": 0.15, "B": 0.5, "Mo": 0.05, "Cl": 0
    },
    "میوه‌دهی": {
        "N": 80, "P": 40, "K": 140, "Ca": 115, "Mg": 30, "S": 20,
        "Fe": 2.5, "Zn": 0.6, "Mn": 0.6, "Cu": 0.1, "B": 0.3, "Mo": 0.05, "Cl": 0
    }
}

# ارقام توت فرنگی
VARIETIES = ["سن اندرسا", "کاماروسا"]

# سناریوهای فیلتر برند
BRAND_FILTERS = [
    None,  # همه برندها
    ["گل سم گرگان"],
    ["ردسا"],
    ["اطلس"],
    ["گل سم گرگان", "ردسا"],
    ["رازاک شیمی", "اطلس"]
]


def get_fertilizers(db, brand_filter=None):
    """دریافت کودها با فیلتر برند"""
    query = db.query(models.Fertilizer).filter(models.Fertilizer.is_active == True)
    if brand_filter:
        query = query.filter(models.Fertilizer.brand_name.in_(brand_filter))
    return query.all()


def calculate_supply_percentage(needs: Dict, supplied: Dict) -> Dict[str, float]:
    """محاسبه درصد تامین هر عنصر"""
    result = {}
    for elem, need in needs.items():
        if need > 0:
            supply = supplied.get(elem, 0)
            result[elem] = round((supply / need) * 100, 1)
        else:
            result[elem] = 100.0
    return result


def evaluate_results(needs: Dict, supplied: Dict) -> Dict:
    """ارزیابی نتایج محاسبات"""
    evaluation = {
        "perfect": [],      # 95-105%
        "good": [],         # 85-95% یا 105-115%
        "acceptable": [],   # 70-85% یا 115-130%
        "poor": [],         # 50-70% یا 130-150%
        "critical": [],     # زیر 50% یا بالای 150%
        "total_need": 0,
        "total_supply": 0
    }
    
    for elem, need in needs.items():
        if need == 0:
            continue
        
        supply = supplied.get(elem, 0)
        evaluation["total_need"] += need
        evaluation["total_supply"] += supply
        
        if need > 0:
            percentage = (supply / need) * 100
            
            if 95 <= percentage <= 105:
                evaluation["perfect"].append(elem)
            elif 85 <= percentage < 95 or 105 < percentage <= 115:
                evaluation["good"].append(elem)
            elif 70 <= percentage < 85 or 115 < percentage <= 130:
                evaluation["acceptable"].append(elem)
            elif 50 <= percentage < 70 or 130 < percentage <= 150:
                evaluation["poor"].append(elem)
            else:
                evaluation["critical"].append(elem)
    
    # محاسبه امتیاز کلی (0-100)
    total_elements = len([e for e in needs if needs[e] > 0])
    if total_elements > 0:
        perfect_score = len(evaluation["perfect"]) * 100
        good_score = len(evaluation["good"]) * 70
        acceptable_score = len(evaluation["acceptable"]) * 40
        poor_score = len(evaluation["poor"]) * 10
        critical_score = len(evaluation["critical"]) * 0
        
        evaluation["overall_score"] = (perfect_score + good_score + acceptable_score + poor_score + critical_score) / total_elements
    else:
        evaluation["overall_score"] = 0
    
    return evaluation


def test_database_connection(db) -> bool:
    """تست 1: اتصال به دیتابیس و بررسی داده‌ها"""
    print_header("تست 1: اتصال به دیتابیس و بررسی داده‌ها")
    
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.bind)
        tables = inspector.get_table_names()
        print_info(f"تعداد جداول: {len(tables)}")
        
        brands_count = db.query(models.Brand).count()
        print_info(f"تعداد برندها: {brands_count}")
        
        fertilizers_count = db.query(models.Fertilizer).count()
        print_info(f"تعداد کل کودها: {fertilizers_count}")
        
        active_fertilizers = db.query(models.Fertilizer).filter(models.Fertilizer.is_active == True).count()
        print_info(f"تعداد کودهای فعال: {active_fertilizers}")
        
        npk_count = db.query(models.Fertilizer).filter(models.Fertilizer.fertilizer_type == "NPK").count()
        micro_count = db.query(models.Fertilizer).filter(models.Fertilizer.fertilizer_type == "ریزمغذی").count()
        single_count = db.query(models.Fertilizer).filter(models.Fertilizer.fertilizer_type == "تک عنصری").count()
        stimulant_count = db.query(models.Fertilizer).filter(models.Fertilizer.fertilizer_type == "محرک رشد").count()
        
        print_info(f"   - NPK: {npk_count}")
        print_info(f"   - ریزمغذی: {micro_count}")
        print_info(f"   - تک عنصری: {single_count}")
        print_info(f"   - محرک رشد: {stimulant_count}")
        
        if active_fertilizers == 0:
            print_error("هیچ کود فعالی در دیتابیس وجود ندارد!")
            return False
        
        print_success("اتصال به دیتابیس و بررسی داده‌ها با موفقیت انجام شد")
        return True
        
    except Exception as e:
        print_error(f"خطا در اتصال به دیتابیس: {e}")
        return False


def test_variety_and_stage_combinations(db) -> Dict:
    """تست 2: ترکیب ارقام و مراحل رشد مختلف"""
    print_header("تست 2: ترکیب ارقام و مراحل رشد مختلف")
    
    results = {}
    tank_volume = 100
    stock_volume = 20
    injector_ratio = 200
    
    tank_main = TankCreate(
        name="مخزن اصلی",
        volume_liters=tank_volume,
        water_ec_ms_cm=0.4,
        water_ph=7.0,
        water_ca_ppm=50,
        water_mg_ppm=20,
        water_hco3_ppm=0,
        water_cl_ppm=0,
        water_na_ppm=0,
        water_so4_ppm=0,
        water_no3_ppm=0,
        water_fe_ppm=0
    )
    
    tank_calcium = TankCreate(
        name="مخزن کلسیم",
        volume_liters=tank_volume,
        water_ec_ms_cm=0.4,
        water_ph=7.0,
        water_ca_ppm=50,
        water_mg_ppm=20,
        water_hco3_ppm=0,
        water_cl_ppm=0,
        water_na_ppm=0,
        water_so4_ppm=0,
        water_no3_ppm=0,
        water_fe_ppm=0
    )
    
    all_fertilizers = get_fertilizers(db)
    
    for variety in VARIETIES:
        results[variety] = {}
        for stage_name, stage_needs in GROWTH_STAGES.items():
            start_time = time.time()
            
            try:
                result_main, result_calcium, warnings, instructions = calculate_dual_tank_professional(
                    remaining_needs=stage_needs,
                    all_fertilizers=all_fertilizers,
                    tank_main=tank_main,
                    tank_calcium=tank_calcium,
                    brand_filter=None
                )
                
                calc_time = (time.time() - start_time) * 1000
                
                evaluation = evaluate_results(stage_needs, result_main.get("supplied_ppm", {}))
                
                results[variety][stage_name] = {
                    "time_ms": round(calc_time, 2),
                    "main_doses": len(result_main.get("doses", [])),
                    "calcium_doses": len(result_calcium.get("doses", [])),
                    "ec_main": result_main.get("ec_predicted", 0),
                    "ec_calcium": result_calcium.get("ec_predicted", 0),
                    "warnings_count": len(warnings),
                    "overall_score": evaluation["overall_score"],
                    "perfect": evaluation["perfect"],
                    "good": evaluation["good"],
                    "acceptable": evaluation["acceptable"],
                    "poor": evaluation["poor"],
                    "critical": evaluation["critical"]
                }
                
                status_icon = Colors.GREEN + "✓" if evaluation["overall_score"] >= 70 else Colors.YELLOW + "⚠️" if evaluation["overall_score"] >= 50 else Colors.RED + "✗"
                print(f"   {status_icon} {Colors.END}{variety} - {stage_name}: امتیاز={evaluation['overall_score']:.0f}%, زمان={calc_time:.0f}ms")
                
            except Exception as e:
                print_error(f"خطا در {variety} - {stage_name}: {e}")
                results[variety][stage_name] = {"error": str(e)}
    
    return results


def test_water_quality_scenarios(db) -> Dict:
    """تست 3: سناریوهای مختلف کیفیت آب"""
    print_header("تست 3: سناریوهای مختلف کیفیت آب")
    
    results = {}
    stage_name = "رشد رویشی"
    stage_needs = GROWTH_STAGES[stage_name]
    tank_volume = 100
    stock_volume = 20
    injector_ratio = 200
    
    all_fertilizers = get_fertilizers(db)
    
    for scenario_name, water_params in WATER_QUALITY_SCENARIOS.items():
        print_info(f"در حال تست: {scenario_name}")
        
        tank_main = TankCreate(
            name="مخزن اصلی",
            volume_liters=tank_volume,
            water_ec_ms_cm=water_params["ec"],
            water_ph=water_params["ph"],
            water_ca_ppm=water_params["ca"],
            water_mg_ppm=water_params["mg"],
            water_hco3_ppm=water_params["hco3"],
            water_cl_ppm=water_params["cl"],
            water_na_ppm=0,
            water_so4_ppm=0,
            water_no3_ppm=0,
            water_fe_ppm=0
        )
        
        tank_calcium = TankCreate(
            name="مخزن کلسیم",
            volume_liters=tank_volume,
            water_ec_ms_cm=water_params["ec"],
            water_ph=water_params["ph"],
            water_ca_ppm=water_params["ca"],
            water_mg_ppm=water_params["mg"],
            water_hco3_ppm=water_params["hco3"],
            water_cl_ppm=water_params["cl"],
            water_na_ppm=0,
            water_so4_ppm=0,
            water_no3_ppm=0,
            water_fe_ppm=0
        )
        
        start_time = time.time()
        
        try:
            result_main, result_calcium, warnings, instructions = calculate_dual_tank_professional(
                remaining_needs=stage_needs,
                all_fertilizers=all_fertilizers,
                tank_main=tank_main,
                tank_calcium=tank_calcium,
                brand_filter=None
            )
            
            calc_time = (time.time() - start_time) * 1000
            
            evaluation = evaluate_results(stage_needs, result_main.get("supplied_ppm", {}))
            
            results[scenario_name] = {
                "time_ms": round(calc_time, 2),
                "main_doses": len(result_main.get("doses", [])),
                "calcium_doses": len(result_calcium.get("doses", [])),
                "ec_main": result_main.get("ec_predicted", 0),
                "ec_calcium": result_calcium.get("ec_predicted", 0),
                "overall_score": evaluation["overall_score"],
                "warnings_count": len(warnings)
            }
            
            status_icon = Colors.GREEN + "✓" if evaluation["overall_score"] >= 70 else Colors.YELLOW + "⚠️" if evaluation["overall_score"] >= 50 else Colors.RED + "✗"
            print(f"   {status_icon} {Colors.END}امتیاز={evaluation['overall_score']:.0f}%, EC={result_main.get('ec_predicted', 0)} mS/cm")
            
        except Exception as e:
            print_error(f"خطا در {scenario_name}: {e}")
            results[scenario_name] = {"error": str(e)}
    
    return results


def test_brand_filters(db) -> Dict:
    """تست 4: فیلترهای مختلف برند"""
    print_header("تست 4: فیلترهای مختلف برند")
    
    results = {}
    stage_name = "رشد رویشی"
    stage_needs = GROWTH_STAGES[stage_name]
    tank_volume = 100
    stock_volume = 20
    injector_ratio = 200
    
    tank_main = TankCreate(
        name="مخزن اصلی",
        volume_liters=tank_volume,
        water_ec_ms_cm=0.4,
        water_ph=7.0,
        water_ca_ppm=50,
        water_mg_ppm=20,
        water_hco3_ppm=0,
        water_cl_ppm=0,
        water_na_ppm=0,
        water_so4_ppm=0,
        water_no3_ppm=0,
        water_fe_ppm=0
    )
    
    tank_calcium = TankCreate(
        name="مخزن کلسیم",
        volume_liters=tank_volume,
        water_ec_ms_cm=0.4,
        water_ph=7.0,
        water_ca_ppm=50,
        water_mg_ppm=20,
        water_hco3_ppm=0,
        water_cl_ppm=0,
        water_na_ppm=0,
        water_so4_ppm=0,
        water_no3_ppm=0,
        water_fe_ppm=0
    )
    
    for brand_filter in BRAND_FILTERS:
        filter_name = str(brand_filter) if brand_filter else "همه برندها"
        if isinstance(brand_filter, list):
            filter_name = " + ".join(brand_filter)
        
        fertilizers = get_fertilizers(db, brand_filter)
        print_info(f"در حال تست: {filter_name} ({len(fertilizers)} کود)")
        
        if len(fertilizers) == 0:
            print_warning(f"هیچ کودی برای {filter_name} یافت نشد")
            results[filter_name] = {"error": "No fertilizers found"}
            continue
        
        start_time = time.time()
        
        try:
            result_main, result_calcium, warnings, instructions = calculate_dual_tank_professional(
                remaining_needs=stage_needs,
                all_fertilizers=fertilizers,
                tank_main=tank_main,
                tank_calcium=tank_calcium,
                brand_filter=brand_filter[0] if brand_filter and len(brand_filter) == 1 else None
            )
            
            calc_time = (time.time() - start_time) * 1000
            
            evaluation = evaluate_results(stage_needs, result_main.get("supplied_ppm", {}))
            
            results[filter_name] = {
                "fertilizers_count": len(fertilizers),
                "time_ms": round(calc_time, 2),
                "main_doses": len(result_main.get("doses", [])),
                "calcium_doses": len(result_calcium.get("doses", [])),
                "ec_main": result_main.get("ec_predicted", 0),
                "overall_score": evaluation["overall_score"]
            }
            
            status_icon = Colors.GREEN + "✓" if evaluation["overall_score"] >= 70 else Colors.YELLOW + "⚠️" if evaluation["overall_score"] >= 50 else Colors.RED + "✗"
            print(f"   {status_icon} {Colors.END}امتیاز={evaluation['overall_score']:.0f}%, کودهای انتخاب شده={len(result_main.get('doses', [])) + len(result_calcium.get('doses', []))}")
            
        except Exception as e:
            print_error(f"خطا در {filter_name}: {e}")
            results[filter_name] = {"error": str(e)}
    
    return results


def test_custom_nutrient_needs(db) -> Dict:
    """تست 5: نیازهای سفارشی گیاه (Custom Nutrient Needs)"""
    print_header("تست 5: نیازهای سفارشی گیاه")
    
    results = {}
    stage_name = "رشد رویشی"
    original_needs = GROWTH_STAGES[stage_name]
    tank_volume = 100
    
    tank_main = TankCreate(
        name="مخزن اصلی",
        volume_liters=tank_volume,
        water_ec_ms_cm=0.4,
        water_ph=7.0,
        water_ca_ppm=50,
        water_mg_ppm=20,
        water_hco3_ppm=0,
        water_cl_ppm=0,
        water_na_ppm=0,
        water_so4_ppm=0,
        water_no3_ppm=0,
        water_fe_ppm=0
    )
    
    tank_calcium = TankCreate(
        name="مخزن کلسیم",
        volume_liters=tank_volume,
        water_ec_ms_cm=0.4,
        water_ph=7.0,
        water_ca_ppm=50,
        water_mg_ppm=20,
        water_hco3_ppm=0,
        water_cl_ppm=0,
        water_na_ppm=0,
        water_so4_ppm=0,
        water_no3_ppm=0,
        water_fe_ppm=0
    )
    
    all_fertilizers = get_fertilizers(db)
    
    custom_scenarios = {
        "نیاز استاندارد": original_needs,
        "نیتروژن بالا (N=180)": {**original_needs, "N": 180},
        "پتاسیم بالا (K=200)": {**original_needs, "K": 200},
        "کلسیم بالا (Ca=200)": {**original_needs, "Ca": 200},
        "فسفر بالا (P=100)": {**original_needs, "P": 100},
        "همه عناصر دوبرابر": {k: v*2 for k, v in original_needs.items() if v > 0},
        "همه عناصر نصف": {k: v/2 for k, v in original_needs.items() if v > 0}
    }
    
    for scenario_name, custom_needs in custom_scenarios.items():
        print_info(f"در حال تست: {scenario_name}")
        
        start_time = time.time()
        
        try:
            result_main, result_calcium, warnings, instructions = calculate_dual_tank_professional(
                remaining_needs=custom_needs,
                all_fertilizers=all_fertilizers,
                tank_main=tank_main,
                tank_calcium=tank_calcium,
                brand_filter=None
            )
            
            calc_time = (time.time() - start_time) * 1000
            
            evaluation = evaluate_results(custom_needs, result_main.get("supplied_ppm", {}))
            
            results[scenario_name] = {
                "time_ms": round(calc_time, 2),
                "main_doses": len(result_main.get("doses", [])),
                "calcium_doses": len(result_calcium.get("doses", [])),
                "ec_main": result_main.get("ec_predicted", 0),
                "overall_score": evaluation["overall_score"],
                "perfect": evaluation["perfect"],
                "good": evaluation["good"],
                "acceptable": evaluation["acceptable"],
                "poor": evaluation["poor"],
                "critical": evaluation["critical"]
            }
            
            status_icon = Colors.GREEN + "✓" if evaluation["overall_score"] >= 70 else Colors.YELLOW + "⚠️" if evaluation["overall_score"] >= 50 else Colors.RED + "✗"
            print(f"   {status_icon} {Colors.END}امتیاز={evaluation['overall_score']:.0f}%, زمان={calc_time:.0f}ms")
            
        except Exception as e:
            print_error(f"خطا در {scenario_name}: {e}")
            results[scenario_name] = {"error": str(e)}
    
    return results


def test_performance_benchmark(db, iterations: int = 10) -> Dict:
    """تست 6: بنچمارک عملکرد و زمان اجرا"""
    print_header(f"تست 6: بنچمارک عملکرد ({iterations} بار اجرا)")
    
    stage_name = "رشد رویشی"
    stage_needs = GROWTH_STAGES[stage_name]
    tank_volume = 100
    
    tank_main = TankCreate(
        name="مخزن اصلی",
        volume_liters=tank_volume,
        water_ec_ms_cm=0.4,
        water_ph=7.0,
        water_ca_ppm=50,
        water_mg_ppm=20,
        water_hco3_ppm=0,
        water_cl_ppm=0,
        water_na_ppm=0,
        water_so4_ppm=0,
        water_no3_ppm=0,
        water_fe_ppm=0
    )
    
    tank_calcium = TankCreate(
        name="مخزن کلسیم",
        volume_liters=tank_volume,
        water_ec_ms_cm=0.4,
        water_ph=7.0,
        water_ca_ppm=50,
        water_mg_ppm=20,
        water_hco3_ppm=0,
        water_cl_ppm=0,
        water_na_ppm=0,
        water_so4_ppm=0,
        water_no3_ppm=0,
        water_fe_ppm=0
    )
    
    all_fertilizers = get_fertilizers(db)
    
    times = []
    scores = []
    
    for i in range(iterations):
        start_time = time.time()
        
        result_main, result_calcium, warnings, instructions = calculate_dual_tank_professional(
            remaining_needs=stage_needs,
            all_fertilizers=all_fertilizers,
            tank_main=tank_main,
            tank_calcium=tank_calcium,
            brand_filter=None
        )
        
        calc_time = (time.time() - start_time) * 1000
        times.append(calc_time)
        
        evaluation = evaluate_results(stage_needs, result_main.get("supplied_ppm", {}))
        scores.append(evaluation["overall_score"])
        
        if (i + 1) % 5 == 0 or i == iterations - 1:
            print_info(f"اجرای {i+1}/{iterations} - زمان: {calc_time:.0f}ms - امتیاز: {evaluation['overall_score']:.0f}%")
    
    avg_time = sum(times) / len(times)
    
    results = {
        "avg_time_ms": round(avg_time, 2),
        "min_time_ms": round(min(times), 2),
        "max_time_ms": round(max(times), 2),
        "avg_score": round(sum(scores) / len(scores), 2),
        "min_score": round(min(scores), 2),
        "max_score": round(max(scores), 2),
        "stability": round(100 - ((max(times) - min(times)) / avg_time * 100), 1) if avg_time > 0 else 0
    }
    
    print_info(f"میانگین زمان اجرا: {results['avg_time_ms']}ms")
    print_info(f"کمترین زمان: {results['min_time_ms']}ms")
    print_info(f"بیشترین زمان: {results['max_time_ms']}ms")
    print_info(f"میانگین امتیاز: {results['avg_score']}%")
    print_info(f"پایداری عملکرد: {results['stability']}%")
    
    return results


def main():
    """اجرای تمام تست‌ها و جمع‌آوری نتایج"""
    print_header("شروع تست جامع FarmTech Calculator")
    print_info(f"زمان شروع: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_results = {}
    
    with SessionLocal() as db:
        all_results["database"] = test_database_connection(db)
        
        if not all_results["database"]:
            print_error("تست دیتابیس با شکست مواجه شد. لطفاً ابتدا دیتابیس را سید کنید.")
            print_info("دستور سید کردن: python -c 'from app.seed import init_db; init_db()'")
            return
        
        all_results["variety_stage"] = test_variety_and_stage_combinations(db)
        all_results["water_quality"] = test_water_quality_scenarios(db)
        all_results["brand_filters"] = test_brand_filters(db)
        all_results["custom_needs"] = test_custom_nutrient_needs(db)
        all_results["performance"] = test_performance_benchmark(db)
    
    print_header("جمع‌بندی نهایی نتایج تست")
    print_info(f"زمان پایان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    output_file = os.path.join(BASE_DIR, "test_results.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print_success(f"نتایج تست در فایل {output_file} ذخیره شد")
    
    return all_results


if __name__ == "__main__":
    results = main()