# Platform-v3\backend\test_algorithm.py

"""
FarmTech Algorithm Test Suite
تست جامع و حرفه‌ای الگوریتم محاسبه کود

این فایل تمام سناریوهای ممکن را تست می‌کند:
1. مراحل مختلف رشد (استقرار نشاء تا میوه‌دهی)
2. ارقام مختلف (سن اندرسا و کاماروسا)
3. کیفیت‌های مختلف آب (EC و pH و عناصر)
4. دقت تامین نیازهای گیاه
5. تحلیل خطاها و هشدارها
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from datetime import datetime
from typing import Dict, List, Tuple
import numpy as np

# ایمپورت ماژول‌های پروژه
from app.database import SessionLocal, engine, Base
from app.models import (
    Crop, Variety, GrowthStage, Brand, Fertilizer,
    Interaction, Acid, Tank, CalculationHistory
)
from app.calculator import (
    calculate_water_contribution,
    optimize_fertilizer_doses_professional,
    calculate_tank_doses,
    calculate_dual_tank_professional,
    EC_COEFFICIENTS
)


class AlgorithmTester:
    """کلاس تست الگوریتم FarmTech"""
    
    def __init__(self):
        self.db = SessionLocal()
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
        
    def print_header(self, text: str):
        """چاپ هدر"""
        print("\n" + "="*80)
        print(f"  {text}")
        print("="*80)
    
    def print_section(self, text: str):
        """چاپ بخش"""
        print("\n" + "-"*60)
        print(f"  {text}")
        print("-"*60)
    
    def print_result(self, success: bool, message: str):
        """چاپ نتیجه تست"""
        if success:
            print(f"  ✅ {message}")
            self.passed_tests += 1
        else:
            print(f"  ❌ {message}")
            self.failed_tests += 1
    
    def analyze_accuracy(self, target: Dict[str, float], supplied: Dict[str, float], tolerance: float = 0.2) -> Dict:
        """
        تحلیل دقت تامین نیازها
        
        Args:
            target: نیازهای هدف گیاه (ppm)
            supplied: عناصر تامین شده (ppm)
            tolerance: مقدار خطای مجاز (20% پیش‌فرض)
        
        Returns:
            دیکشنری شامل نتایج تحلیل
        """
        analysis = {
            "total_elements": 0,
            "perfect": 0,
            "good": 0,
            "low": 0,
            "high": 0,
            "missing": 0,
            "details": []
        }
        
        for elem, need in target.items():
            if need < 0.5:  # نیاز ناچیز
                continue
                
            supply = supplied.get(elem, 0)
            analysis["total_elements"] += 1
            
            if supply == 0:
                analysis["missing"] += 1
                analysis["details"].append({
                    "element": elem,
                    "need": need,
                    "supply": supply,
                    "status": "missing",
                    "accuracy": 0,
                    "message": f"⚠️ {elem}: تامین نشده! (نیاز: {need:.1f})"
                })
            else:
                ratio = supply / need
                accuracy = min(ratio, 1/ratio) if ratio > 0 else 0
                
                if 0.95 <= ratio <= 1.05:
                    status = "perfect"
                    analysis["perfect"] += 1
                    msg = f"✅ {elem}: عالی (نیاز: {need:.1f} - تامین: {supply:.1f} - دقت: {accuracy:.0%})"
                elif 0.85 <= ratio <= 1.15:
                    status = "good"
                    analysis["good"] += 1
                    msg = f"👍 {elem}: خوب (نیاز: {need:.1f} - تامین: {supply:.1f} - دقت: {accuracy:.0%})"
                elif ratio < 0.7:
                    status = "low"
                    analysis["low"] += 1
                    msg = f"⚠️ {elem}: کمبود جدی (نیاز: {need:.1f} - تامین: {supply:.1f} - دقت: {accuracy:.0%})"
                elif ratio > 1.3:
                    status = "high"
                    analysis["high"] += 1
                    msg = f"⚠️ {elem}: اضافی (نیاز: {need:.1f} - تامین: {supply:.1f})"
                else:
                    status = "acceptable"
                    msg = f"📊 {elem}: قابل قبول (نیاز: {need:.1f} - تامین: {supply:.1f} - دقت: {accuracy:.0%})"
                
                analysis["details"].append({
                    "element": elem,
                    "need": need,
                    "supply": supply,
                    "status": status,
                    "accuracy": accuracy,
                    "message": msg
                })
        
        # محاسبه امتیاز کلی (0-100)
        if analysis["total_elements"] > 0:
            weighted_score = (
                analysis["perfect"] * 100 +
                analysis["good"] * 80 +
                (analysis["total_elements"] - analysis["perfect"] - analysis["good"] - analysis["low"] - analysis["high"] - analysis["missing"]) * 60
            ) / analysis["total_elements"]
            analysis["overall_score"] = round(weighted_score, 1)
        else:
            analysis["overall_score"] = 0
            
        return analysis
    
    def get_all_growth_stages(self):
        """دریافت تمام مراحل رشد از دیتابیس"""
        stages = self.db.query(GrowthStage).all()
        return stages
    
    def get_all_fertilizers(self):
        """دریافت تمام کودها از دیتابیس"""
        fertilizers = self.db.query(Fertilizer).filter(Fertilizer.is_active == True).all()
        return fertilizers
    
    def test_single_tank_scenarios(self):
        """تست سناریوهای مختلف با یک مخزن"""
        self.print_header("📊 تست سناریوهای مختلف با یک مخزن")
        
        fertilizers = self.get_all_fertilizers()
        if not fertilizers:
            self.print_result(False, "هیچ کودی در دیتابیس یافت نشد")
            return
        
        stages = self.get_all_growth_stages()
        
        # سناریوهای مختلف کیفیت آب
        water_scenarios = [
            {"name": "آب معمولی", "ec": 0.4, "ph": 7.0, "ca": 40, "mg": 15, "hco3": 0},
            {"name": "آب با کیفیت خوب", "ec": 0.2, "ph": 6.5, "ca": 20, "mg": 8, "hco3": 0},
            {"name": "آب با کیفیت ضعیف", "ec": 0.8, "ph": 7.5, "ca": 80, "mg": 30, "hco3": 150},
            {"name": "آب با بیکربنات بالا", "ec": 0.6, "ph": 7.8, "ca": 60, "mg": 20, "hco3": 250},
            {"name": "آب با کلسیم بالا", "ec": 0.7, "ph": 7.2, "ca": 120, "mg": 25, "hco3": 100}
        ]
        
        for stage in stages[:5]:  # تست 5 مرحله اول
            if not stage.variety_id:
                continue
                
            self.print_section(f"تست مرحله: {stage.name} - رقم: {stage.variety.name if stage.variety else 'عمومی'}")
            
            for water in water_scenarios:
                # ایجاد مخزن تست
                tank = Tank(
                    name="تست",
                    tank_type="main",
                    volume_liters=1000,
                    water_ec_ms_cm=water["ec"],
                    water_ph=water["ph"],
                    water_ca_ppm=water["ca"],
                    water_mg_ppm=water["mg"],
                    water_hco3_ppm=water["hco3"]
                )
                
                # محاسبه سهم آب
                water_contribution = calculate_water_contribution(tank)
                
                # محاسبه نیاز خالص
                remaining_needs = {}
                for elem, need in (stage.nutrient_needs or {}).items():
                    water_val = water_contribution.get(elem, 0)
                    remaining_needs[elem] = max(0, need - water_val)
                
                # بهینه‌سازی
                doses_raw, supply, warnings = optimize_fertilizer_doses_professional(
                    remaining_needs=remaining_needs,
                    fertilizers=fertilizers,
                    brand_filter=None
                )
                
                doses = calculate_tank_doses(doses_raw, 1000)
                
                # تحلیل دقت
                analysis = self.analyze_accuracy(stage.nutrient_needs or {}, supply)
                
                print(f"\n  💧 {water['name']}: EC={water['ec']}, Ca={water['ca']}, Mg={water['mg']}")
                print(f"     تعداد کودها: {len(doses)}")
                print(f"     امتیاز دقت: {analysis['overall_score']}%")
                print(f"     تامین شده: {analysis['perfect']} عالی, {analysis['good']} خوب, {analysis['low']} کمبود")
                
                for detail in analysis["details"][:3]:  # نمایش 3 مورد اول
                    print(f"     {detail['message']}")
                
                # ذخیره نتیجه تست
                self.test_results.append({
                    "type": "single_tank",
                    "stage": stage.name,
                    "variety": stage.variety.name if stage.variety else "general",
                    "water_quality": water["name"],
                    "fertilizers_used": len(doses),
                    "accuracy_score": analysis["overall_score"],
                    "perfect_count": analysis["perfect"],
                    "good_count": analysis["good"],
                    "low_count": analysis["low"]
                })
    
    def test_dual_tank_scenarios(self):
        """تست سناریوهای مختلف با دو مخزن"""
        self.print_header("📊 تست سناریوهای مختلف با دو مخزن")
        
        fertilizers = self.get_all_fertilizers()
        if not fertilizers:
            self.print_result(False, "هیچ کودی در دیتابیس یافت نشد")
            return
        
        stages = self.get_all_growth_stages()
        
        # سناریوهای مختلف
        test_scenarios = [
            {
                "name": "حالت استاندارد",
                "main_volume": 1000,
                "calcium_volume": 1000,
                "water_ec": 0.4,
                "water_ph": 7.0,
                "water_ca": 40,
                "water_mg": 15
            },
            {
                "name": "حالت با آب سبک",
                "main_volume": 1000,
                "calcium_volume": 1000,
                "water_ec": 0.2,
                "water_ph": 6.8,
                "water_ca": 20,
                "water_mg": 8
            },
            {
                "name": "حالت با آب سنگین",
                "main_volume": 1000,
                "calcium_volume": 1000,
                "water_ec": 0.8,
                "water_ph": 7.4,
                "water_ca": 80,
                "water_mg": 30
            },
            {
                "name": "حالت با مخازن کوچک",
                "main_volume": 200,
                "calcium_volume": 200,
                "water_ec": 0.4,
                "water_ph": 7.0,
                "water_ca": 40,
                "water_mg": 15
            }
        ]
        
        for stage in stages[:10]:  # تست 10 مرحله اول
            if not stage.variety_id:
                continue
                
            self.print_section(f"تست مرحله: {stage.name} - رقم: {stage.variety.name if stage.variety else 'عمومی'}")
            
            for scenario in test_scenarios:
                # ایجاد مخازن تست
                tank_main = Tank(
                    name="مخزن اصلی تست",
                    tank_type="main",
                    volume_liters=scenario["main_volume"],
                    water_ec_ms_cm=scenario["water_ec"],
                    water_ph=scenario["water_ph"],
                    water_ca_ppm=scenario["water_ca"],
                    water_mg_ppm=scenario["water_mg"]
                )
                
                tank_calcium = Tank(
                    name="مخزن کلسیم تست",
                    tank_type="calcium",
                    volume_liters=scenario["calcium_volume"],
                    water_ec_ms_cm=scenario["water_ec"],
                    water_ph=scenario["water_ph"],
                    water_ca_ppm=scenario["water_ca"],
                    water_mg_ppm=scenario["water_mg"]
                )
                
                # محاسبات دو مخزن
                result_main, result_calcium, warnings, instructions = calculate_dual_tank_professional(
                    remaining_needs=stage.nutrient_needs or {},
                    all_fertilizers=fertilizers,
                    tank_main=tank_main,
                    tank_calcium=tank_calcium,
                    brand_filter=None
                )
                
                # جمع عناصر تامین شده از هر دو مخزن
                total_supply = {}
                for elem, val in result_main.get("supplied_ppm", {}).items():
                    total_supply[elem] = total_supply.get(elem, 0) + val
                for elem, val in result_calcium.get("supplied_ppm", {}).items():
                    total_supply[elem] = total_supply.get(elem, 0) + val
                
                # تحلیل دقت
                analysis = self.analyze_accuracy(stage.nutrient_needs or {}, total_supply)
                
                print(f"\n  📦 {scenario['name']}:")
                print(f"     کودهای مخزن اصلی: {len(result_main.get('doses', []))}")
                print(f"     کودهای مخزن کلسیم: {len(result_calcium.get('doses', []))}")
                print(f"     امتیاز دقت: {analysis['overall_score']}%")
                print(f"     هشدارها: {len(warnings)}")
                
                for detail in analysis["details"][:3]:
                    print(f"     {detail['message']}")
                
                # ذخیره نتیجه تست
                self.test_results.append({
                    "type": "dual_tank",
                    "stage": stage.name,
                    "variety": stage.variety.name if stage.variety else "general",
                    "scenario": scenario["name"],
                    "main_fertilizers": len(result_main.get("doses", [])),
                    "calcium_fertilizers": len(result_calcium.get("doses", [])),
                    "accuracy_score": analysis["overall_score"],
                    "warnings_count": len(warnings)
                })
    
    def analyze_fertilizer_usage(self):
        """تحلیل الگوی استفاده از کودها"""
        self.print_header("📊 تحلیل الگوی استفاده از کودها")
        
        fertilizers = self.get_all_fertilizers()
        stages = self.get_all_growth_stages()
        
        fertilizer_usage = {}
        
        for stage in stages[:10]:
            if not stage.variety_id:
                continue
                
            tank_main = Tank(
                name="تست",
                tank_type="main",
                volume_liters=1000,
                water_ec_ms_cm=0.4,
                water_ph=7.0,
                water_ca_ppm=40,
                water_mg_ppm=15
            )
            
            tank_calcium = Tank(
                name="تست",
                tank_type="calcium",
                volume_liters=1000,
                water_ec_ms_cm=0.4,
                water_ph=7.0,
                water_ca_ppm=40,
                water_mg_ppm=15
            )
            
            result_main, result_calcium, warnings, _ = calculate_dual_tank_professional(
                remaining_needs=stage.nutrient_needs or {},
                all_fertilizers=fertilizers,
                tank_main=tank_main,
                tank_calcium=tank_calcium,
                brand_filter=None
            )
            
            all_doses = result_main.get("doses", []) + result_calcium.get("doses", [])
            
            for dose in all_doses:
                name = dose.get("name", "unknown")
                if name not in fertilizer_usage:
                    fertilizer_usage[name] = 0
                fertilizer_usage[name] += 1
        
        print("\n  کودهای پرکاربرد (به ترتیب):")
        sorted_usage = sorted(fertilizer_usage.items(), key=lambda x: x[1], reverse=True)
        for name, count in sorted_usage:
            print(f"     {name}: {count} بار استفاده")
    
    def check_element_coverage(self):
        """بررسی پوشش عناصر مختلف توسط کودها"""
        self.print_header("📊 بررسی پوشش عناصر توسط کودها")
        
        fertilizers = self.get_all_fertilizers()
        
        element_coverage = {
            'N': {'supplied': 0, 'fertilizers': []},
            'P': {'supplied': 0, 'fertilizers': []},
            'K': {'supplied': 0, 'fertilizers': []},
            'Ca': {'supplied': 0, 'fertilizers': []},
            'Mg': {'supplied': 0, 'fertilizers': []},
            'Fe': {'supplied': 0, 'fertilizers': []},
            'Zn': {'supplied': 0, 'fertilizers': []},
            'Mn': {'supplied': 0, 'fertilizers': []}
        }
        
        for fert in fertilizers:
            if fert.n_percent and fert.n_percent > 0:
                element_coverage['N']['supplied'] += 1
                element_coverage['N']['fertilizers'].append(fert.name)
            if fert.p_percent and fert.p_percent > 0:
                element_coverage['P']['supplied'] += 1
                element_coverage['P']['fertilizers'].append(fert.name)
            if fert.k_percent and fert.k_percent > 0:
                element_coverage['K']['supplied'] += 1
                element_coverage['K']['fertilizers'].append(fert.name)
            if fert.ca_percent and fert.ca_percent > 0:
                element_coverage['Ca']['supplied'] += 1
                element_coverage['Ca']['fertilizers'].append(fert.name)
            if fert.mg_percent and fert.mg_percent > 0:
                element_coverage['Mg']['supplied'] += 1
                element_coverage['Mg']['fertilizers'].append(fert.name)
            if fert.fe_percent and fert.fe_percent > 0:
                element_coverage['Fe']['supplied'] += 1
                element_coverage['Fe']['fertilizers'].append(fert.name)
            if fert.zn_percent and fert.zn_percent > 0:
                element_coverage['Zn']['supplied'] += 1
                element_coverage['Zn']['fertilizers'].append(fert.name)
            if fert.mn_percent and fert.mn_percent > 0:
                element_coverage['Mn']['supplied'] += 1
                element_coverage['Mn']['fertilizers'].append(fert.name)
        
        print("\n  پوشش هر عنصر توسط کودها:")
        for elem, data in element_coverage.items():
            status = "✅" if data['supplied'] > 0 else "❌"
            print(f"     {status} {elem}: {data['supplied']} کود")
            if data['fertilizers']:
                print(f"        └─ {', '.join(data['fertilizers'][:3])}")
    
    def run_all_tests(self):
        """اجرای تمام تست‌ها"""
        self.print_header("🚀 FarmTech Algorithm Test Suite")
        print(f"\n⏰ زمان شروع: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # بررسی دیتابیس
        fertilizers = self.get_all_fertilizers()
        print(f"\n📊 وضعیت دیتابیس:")
        print(f"   تعداد کودها: {len(fertilizers)}")
        
        stages = self.get_all_growth_stages()
        print(f"   تعداد مراحل رشد: {len(stages)}")
        
        # اجرای تست‌ها
        self.test_single_tank_scenarios()
        self.test_dual_tank_scenarios()
        self.analyze_fertilizer_usage()
        self.check_element_coverage()
        
        # گزارش نهایی
        self.print_header("📊 گزارش نهایی تست‌ها")
        
        print(f"\n  ✅ تست‌های موفق: {self.passed_tests}")
        print(f"  ❌ تست‌های ناموفق: {self.failed_tests}")
        
        total_tests = self.passed_tests + self.failed_tests
        success_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"  📊 نرخ موفقیت: {success_rate:.1f}%")
        
        # تحلیل نتایج
        if self.test_results:
            dual_tank_results = [r for r in self.test_results if r.get("type") == "dual_tank"]
            if dual_tank_results:
                avg_accuracy = sum(r.get("accuracy_score", 0) for r in dual_tank_results) / len(dual_tank_results)
                print(f"\n  🎯 میانگین دقت الگوریتم دو مخزن: {avg_accuracy:.1f}%")
            
            single_tank_results = [r for r in self.test_results if r.get("type") == "single_tank"]
            if single_tank_results:
                avg_accuracy_single = sum(r.get("accuracy_score", 0) for r in single_tank_results) / len(single_tank_results)
                print(f"  🎯 میانگین دقت الگوریتم یک مخزن: {avg_accuracy_single:.1f}%")
        
        print(f"\n⏰ زمان پایان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\n" + "="*80)
        
        # توصیه‌ها
        self.print_header("💡 توصیه‌ها و پیشنهادات")
        
        if len(fertilizers) < 10:
            print("\n  ⚠️ تعداد کودهای موجود در دیتابیس کم است.")
            print("     پیشنهاد: حداقل 10-15 کود مختلف (NPK، تک عنصری، میکرو) اضافه کنید")
        
        if len([f for f in fertilizers if f.fertilizer_type == 'NPK']) < 3:
            print("\n  ⚠️ تعداد کودهای NPK کافی نیست.")
            print("     پیشنهاد: کودهای NPK با نسبت‌های مختلف اضافه کنید (20-20-20، 36-12-12، 10-50-10)")
        
        if len([f for f in fertilizers if f.fertilizer_type == 'ریزمغذی']) == 0:
            print("\n  ⚠️ هیچ کود ریز مغذی در دیتابیس وجود ندارد.")
            print("     پیشنهاد: کود یونی کمپلکس یا کود ریز مغذی مشابه اضافه کنید")
        
        print("\n  ✅ برای بهبود دقت الگوریتم:")
        print("     1. کودهای متنوع‌تری به دیتابیس اضافه کنید")
        print("     2. دوز مجاز کودها (max_dose_g_per_liter) را بر اساس حلالیت تنظیم کنید")
        print("     3. از برندهای مختلف کود استفاده کنید تا الگوریتم گزینه بیشتری داشته باشد")


def main():
    """تابع اصلی"""
    tester = AlgorithmTester()
    try:
        tester.run_all_tests()
    except Exception as e:
        print(f"\n❌ خطا در اجرای تست‌ها: {e}")
        import traceback
        traceback.print_exc()
    finally:
        tester.db.close()


if __name__ == "__main__":
    main()