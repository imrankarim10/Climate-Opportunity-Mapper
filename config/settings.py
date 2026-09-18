"""
Configuration settings and indicator definitions for the Pakistan Climate Opportunity Mapper.
Module 1: Pakistan Climate & Vulnerability Explorer.
"""
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = BASE_DIR / "outputs"

RAW_GEOJSON_PATH = RAW_DATA_DIR / "pak_admin2.geojson"
SIMPLIFIED_GEOJSON_PATH = PROCESSED_DATA_DIR / "pak_admin2_simplified.geojson"
PROCESSED_DATA_PATH = PROCESSED_DATA_DIR / "district_climate_vulnerability.csv"
MASTER_DISTRICTS_PATH = RAW_DATA_DIR / "districts_master_list.csv"

# Application Branding & Metadata
APP_TITLE = "Pakistan Climate Opportunity Mapper"
APP_SUBTITLE = "Module 1 — Pakistan Climate & Vulnerability Explorer"
APP_DISCLAIMER = (
    "Prototype analytical tool for decision-support and screening. "
    "Not an official government, GCF, or international climate-finance assessment."
)

# Geographic defaults
PAKISTAN_CENTER_LAT = 30.3753
PAKISTAN_CENTER_LON = 69.3451
DEFAULT_MAP_ZOOM = 4.8

# Categorical Classification Labels
CATEGORY_LABELS = {
    "low": "Lower relative exposure/vulnerability",
    "moderate": "Moderate relative exposure/vulnerability",
    "high": "Higher relative exposure/vulnerability"
}

VULNERABILITY_THRESHOLDS = {
    "low_max": 35.0,
    "mod_max": 65.0
}

# Data Coverage Guardrail
# If a district has fewer than this percentage of indicators, do not calculate composite score
MIN_DATA_COVERAGE_PCT = 60.0

# Default Composite Weights (Must sum to 1.0)
DEFAULT_CATEGORY_WEIGHTS = {
    "climate_hazard": 0.50,
    "socioeconomic_vulnerability": 0.50
}

# Indicator Suite Metadata & Data Dictionary
INDICATORS = {
    # ---------------- Climate Hazard Proxies ----------------
    "flood_exposure_proxy": {
        "name": "Flood Exposure Proxy",
        "short_name": "Flood Exposure",
        "category": "climate_hazard",
        "raw_col": "flood_exposure_raw",
        "norm_col": "flood_exposure_norm",
        "unit": "Exposure Index (0–100)",
        "direction": "higher_is_worse",
        "default_weight": 0.25,
        "source": "NDMA & PDNA 2022 Floods",
        "dataset_title": "Pakistan 2022 Floods: Calamity-Hit Districts & Damage Assessment",
        "year": "2022",
        "resolution": "District (ADM2)",
        "processing": (
            "Synthesized from NDMA official calamity declarations, Post-Disaster Needs Assessment (PDNA) "
            "flood severity tiers (Severe, Moderate, Low, Non-Calamity), and inundated cropland percentage."
        ),
        "limitations": (
            "Reflects 2022 historic monsoon flood inundation and official calamity designation; does not replace "
            "hydrodynamic modeling of return periods."
        ),
        "url": "https://www.ndma.gov.pk/"
    },
    "drought_water_stress_proxy": {
        "name": "Drought & Water Stress Proxy",
        "short_name": "Drought / Aridity",
        "category": "climate_hazard",
        "raw_col": "drought_stress_raw",
        "norm_col": "drought_stress_norm",
        "unit": "Stress Index (0–100)",
        "direction": "higher_is_worse",
        "default_weight": 0.25,
        "source": "PMD & WRI Aqueduct",
        "dataset_title": "National Drought Monitoring Centre (NDMC) Aridity & Baseline Water Stress",
        "year": "2021–2023",
        "resolution": "District (ADM2)",
        "processing": (
            "Composite of PMD aridity classification (hyper-arid, arid, semi-arid, sub-humid) "
            "and WRI baseline water stress ratios."
        ),
        "limitations": (
            "Represents baseline climatic dryness and recurring seasonal drought pressure; "
            "canal irrigation infrastructure mitigates local surface availability in canal commands."
        ),
        "url": "https://ndmc.pmd.gov.pk/"
    },
    "heat_stress_indicator": {
        "name": "Extreme Heat & Temperature Indicator",
        "short_name": "Extreme Heat",
        "category": "climate_hazard",
        "raw_col": "heat_stress_raw",
        "norm_col": "heat_stress_norm",
        "unit": "Mean Max Temp (°C)",
        "direction": "higher_is_worse",
        "default_weight": 0.25,
        "source": "PMD & World Bank CCKP",
        "dataset_title": "Pakistan Climate Normals (1991–2020) & Extreme Temperature Climatology",
        "year": "1991–2020 Normal",
        "resolution": "District (ADM2)",
        "processing": (
            "Mean annual daily maximum temperature (°C) alongside recorded incidence of extreme "
            "heatwave conditions (>40°C summer days)."
        ),
        "limitations": (
            "Based on climatological station observations interpolated across administrative boundaries; "
            "microclimates in high-relief mountainous districts may have localized variation."
        ),
        "url": "https://climateknowledgeportal.worldbank.org/country/pakistan"
    },
    "rainfall_variability_proxy": {
        "name": "Precipitation Variability Proxy",
        "short_name": "Rainfall Variability",
        "category": "climate_hazard",
        "raw_col": "rainfall_variability_raw",
        "norm_col": "rainfall_variability_norm",
        "unit": "Interannual CV (%)",
        "direction": "higher_is_worse",
        "default_weight": 0.25,
        "source": "PMD & CHIRPS / World Bank",
        "dataset_title": "Historical Rainfall Variability & Monsoon Anomaly Index",
        "year": "1991–2020",
        "resolution": "District (ADM2)",
        "processing": (
            "Coefficient of Variation (CV %) of annual rainfall. Arid and low-rainfall zones "
            "exhibit high percentage variability indicating erratic monsoon/winter precipitation regimes."
        ),
        "limitations": (
            "Variability highlights unpredictability rather than total flood volume; "
            "rain-shadow alpine valleys may show high variability with low absolute precipitation."
        ),
        "url": "https://pmd.gov.pk/"
    },

    # ------------ Socioeconomic Vulnerability Proxies ------------
    "population_density": {
        "name": "Population Density Proxy",
        "short_name": "Population Density",
        "category": "socioeconomic_vulnerability",
        "raw_col": "population_density_raw",
        "norm_col": "population_density_norm",
        "unit": "Persons / sq km",
        "direction": "higher_is_worse",
        "default_weight": 0.30,
        "source": "Pakistan Bureau of Statistics (PBS)",
        "dataset_title": "Digital Census of Pakistan (2017 & 2023 Population Tables)",
        "year": "2017 / 2023",
        "resolution": "District (ADM2)",
        "processing": "Total district population divided by official land area in square kilometers.",
        "limitations": (
            "High population density increases human exposure to acute hazard events; however, "
            "dense urban hubs may also possess greater disaster-response infrastructure than sparse rural areas."
        ),
        "url": "https://www.pbs.gov.pk/"
    },
    "multidimensional_poverty": {
        "name": "Multidimensional Poverty Headcount Proxy",
        "short_name": "Multidimensional Poverty",
        "category": "socioeconomic_vulnerability",
        "raw_col": "poverty_headcount_raw",
        "norm_col": "poverty_headcount_norm",
        "unit": "Poverty Headcount (%)",
        "direction": "higher_is_worse",
        "default_weight": 0.40,
        "source": "Planning Commission of Pakistan, UNDP & OPHI",
        "dataset_title": "Multidimensional Poverty in Pakistan (National MPI Report)",
        "year": "2019–2020",
        "resolution": "District (ADM2)",
        "processing": (
            "Headcount ratio H (%) of population experiencing acute multidimensional poverty "
            "across education, health, and living standards dimensions (Alkire-Foster method)."
        ),
        "limitations": (
            "Survey-based estimates at district level; some newly split districts inherit their parent "
            "district baseline rate in public reporting."
        ),
        "url": "https://www.undp.org/pakistan/publications/multidimensional-poverty-pakistan"
    },
    "rural_agriculture_dependence": {
        "name": "Rural & Agricultural Livelihood Dependence Proxy",
        "short_name": "Rural / Agri Dependence",
        "category": "socioeconomic_vulnerability",
        "raw_col": "rural_agri_share_raw",
        "norm_col": "rural_agri_share_norm",
        "unit": "Rural Population (%)",
        "direction": "higher_is_worse",
        "default_weight": 0.30,
        "source": "Pakistan Bureau of Statistics (PBS)",
        "dataset_title": "Pakistan Census & Labour Force Survey: Rural Population & Primary Livelihoods",
        "year": "2017 / 2021",
        "resolution": "District (ADM2)",
        "processing": (
            "Percentage of district population residing in rural administrative areas "
            "coupled with agricultural / agrarian livelihood dependence."
        ),
        "limitations": (
            "Rural population is a proxy for agrarian climate sensitivity; does not capture off-farm remittance "
            "income or diversified rural enterprise."
        ),
        "url": "https://www.pbs.gov.pk/"
    }
}

# Color palettes for map layers (Plotly continuous color scales)
MAP_COLOR_SCALES = {
    "preliminary_vulnerability": "YlOrRd",
    "climate_hazard": "Oranges",
    "socioeconomic_vulnerability": "Purples",
    "flood_exposure_proxy": "Blues",
    "drought_water_stress_proxy": "YlOrBr",
    "heat_stress_indicator": "Inferno",
    "rainfall_variability_proxy": "Tealrose",
    "population_density": "YlGnBu",
    "multidimensional_poverty": "Reds",
    "rural_agriculture_dependence": "Greens"
}
