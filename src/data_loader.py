"""
Data loading, caching, and querying utilities for the Pakistan Climate Opportunity Mapper.
"""
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import pandas as pd
import streamlit as st

import config.settings as config
from src.preprocessing import run_preprocessing_pipeline


@st.cache_data(show_spinner="Loading district climate and vulnerability data...")
def load_processed_data() -> pd.DataFrame:
    """
    Loads the processed master dataset from disk. If missing, triggers the preprocessing pipeline.
    """
    data_path = config.PROCESSED_DATA_PATH
    if not data_path.exists():
        print("Processed data missing. Running preprocessing pipeline...")
        return run_preprocessing_pipeline()
    
    df = pd.read_csv(data_path)
    return df


@st.cache_data(show_spinner="Loading Pakistan district boundary GeoJSON...")
def load_geojson() -> Dict[str, Any]:
    """
    Loads the simplified GeoJSON boundaries for rapid interactive mapping.
    Falls back to raw GeoJSON if simplified version is not present.
    """
    target_path = config.SIMPLIFIED_GEOJSON_PATH
    if not target_path.exists():
        target_path = config.RAW_GEOJSON_PATH

    if not target_path.exists():
        raise FileNotFoundError(f"GeoJSON file not found at {target_path}")

    with open(target_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    return geojson_data


def get_available_provinces(df: pd.DataFrame) -> List[str]:
    """Returns a sorted list of unique provinces present in the dataset."""
    provinces = sorted(df["province"].dropna().unique().tolist())
    return provinces


def get_districts_for_province(df: pd.DataFrame, province: Optional[str] = None) -> List[str]:
    """
    Returns sorted list of districts for a given province.
    If province is None or 'All Pakistan', returns all districts.
    """
    if not province or province == "All Pakistan":
        return sorted(df["district"].dropna().unique().tolist())
    
    filtered = df[df["province"] == province]
    return sorted(filtered["district"].dropna().unique().tolist())


def get_district_record(df: pd.DataFrame, district_name: str) -> Optional[pd.Series]:
    """Retrieves single district row as a Series."""
    matches = df[df["district"] == district_name]
    if matches.empty:
        return None
    return matches.iloc[0]


def format_district_export(df: pd.DataFrame, district_name: Optional[str] = None) -> pd.DataFrame:
    """
    Prepares a clean, human-readable export DataFrame for CSV/JSON download.
    """
    target_df = df if (not district_name or district_name == "All districts") else df[df["district"] == district_name]
    
    # Rename columns for external reporting
    rename_cols = {
        "district_id": "District P-Code",
        "district": "District Name",
        "province": "Province",
        "area_sqkm": "Area (sq km)",
        "flood_exposure_raw": "Flood Exposure Proxy (Observed 0-100)",
        "flood_exposure_norm": "Flood Exposure (Normalized 0-100)",
        "drought_stress_raw": "Drought & Water Stress Proxy (Observed 0-100)",
        "drought_stress_norm": "Drought & Water Stress (Normalized 0-100)",
        "heat_stress_raw": "Extreme Heat Proxy (Mean Max °C)",
        "heat_stress_norm": "Extreme Heat (Normalized 0-100)",
        "rainfall_variability_raw": "Rainfall Variability Proxy (CV %)",
        "rainfall_variability_norm": "Rainfall Variability (Normalized 0-100)",
        "population_density_raw": "Population Density (Persons / sq km)",
        "population_density_norm": "Population Density (Normalized 0-100)",
        "poverty_headcount_raw": "Multidimensional Poverty Headcount (%)",
        "poverty_headcount_norm": "Multidimensional Poverty (Normalized 0-100)",
        "rural_agri_share_raw": "Rural Population Share (%)",
        "rural_agri_share_norm": "Rural / Agri Dependence (Normalized 0-100)",
        "data_coverage_pct": "Data Coverage (%)",
        "climate_hazard_score": "Climate Hazard Score (0-100)",
        "socioeconomic_vulnerability_score": "Socioeconomic Vulnerability Score (0-100)",
        "preliminary_vulnerability_score": "Preliminary Vulnerability Score (0-100)",
        "vulnerability_category": "Vulnerability Classification"
    }
    
    available_cols = [c for c in rename_cols.keys() if c in target_df.columns]
    exported = target_df[available_cols].rename(columns=rename_cols)
    return exported
