# backend/app/calculator/__init__.py

"""
FarmTech Calculator Module
Version: 3.3.1
Date: 1405/03/21

This module contains all calculation logic for fertilizer optimization:
- Core calculations (element ppm, water contribution, acid contribution)
- EC calculations and warnings
- Layer-by-layer optimization algorithm (NPK -> Secondary -> Micro)
- Stock solution calculations (kg, injector ratio, instructions)
- Dual tank separation and calculations
- Professional mixing instructions (Persian & English)
"""

from .core import (
    SUPPORTED_ELEMENTS,
    calculate_element_ppm,
    calculate_water_contribution,
    calculate_acid_contribution
)

from .ec import (
    EC_COEFFICIENTS,
    calculate_final_ec,
    get_ec_warning
)

from .optimization import (
    select_best_fertilizer_for_macro,
    select_best_fertilizer_for_secondary,
    solve_macro_layer,
    solve_secondary_layer,
    solve_micro_layer,
    optimize_fertilizer_doses_professional
)

from .stock import (
    calculate_dose_kg_for_stock,
    calculate_stock_consumption,
    get_injector_explanation,
    get_stock_mixing_instructions,
    get_stock_usage_instructions,
    get_storage_instructions,
    add_stock_calculations_to_doses
)

from .tank import (
    calculate_tank_doses
)

from .dual_tank import (
    separate_into_tanks_professional,
    separate_into_tanks,
    calculate_dual_tank_professional
)

from .instructions import (
    generate_professional_mixing_instructions,
    generate_persian_mixing_instructions,
    generate_persian_general_instructions
)


__version__ = "3.3.1"
__author__ = "FarmTech Team"

__all__ = [
    "SUPPORTED_ELEMENTS",
    "calculate_element_ppm",
    "calculate_water_contribution",
    "calculate_acid_contribution",
    "EC_COEFFICIENTS",
    "calculate_final_ec",
    "get_ec_warning",
    "select_best_fertilizer_for_macro",
    "select_best_fertilizer_for_secondary",
    "solve_macro_layer",
    "solve_secondary_layer",
    "solve_micro_layer",
    "optimize_fertilizer_doses_professional",
    "calculate_dose_kg_for_stock",
    "calculate_stock_consumption",
    "get_injector_explanation",
    "get_stock_mixing_instructions",
    "get_stock_usage_instructions",
    "get_storage_instructions",
    "add_stock_calculations_to_doses",
    "calculate_tank_doses",
    "separate_into_tanks_professional",
    "separate_into_tanks",
    "calculate_dual_tank_professional",
    "generate_professional_mixing_instructions",
    "generate_persian_mixing_instructions",
    "generate_persian_general_instructions"
]