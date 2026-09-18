"""
Scoring and Normalization Engine for Pakistan Climate Opportunity Mapper.
Implements transparent min-max normalization, sub-index aggregation,
data coverage checks, and relative categorical ranking.
"""
from typing import Dict, Any, Tuple, Optional
import pandas as pd
import numpy as np

import config.settings as config


def normalize_series(
    series: pd.Series,
    direction: str = "higher_is_worse",
    custom_min: Optional[float] = None,
    custom_max: Optional[float] = None
) -> pd.Series:
    """
    Normalizes a numerical Pandas Series onto a standard 0 to 100 scale.
    
    Parameters:
        series: Raw numerical data series
        direction: 'higher_is_worse' (higher value -> higher vulnerability score)
                   or 'lower_is_worse' (lower value -> higher vulnerability score)
        custom_min: Optional pre-defined lower bound
        custom_max: Optional pre-defined upper bound
        
    Returns:
        pd.Series with values normalized to [0, 100], preserving NaN for missing entries.
    """
    valid_series = series.dropna()
    if valid_series.empty:
        return pd.Series(np.nan, index=series.index)

    min_val = custom_min if custom_min is not None else valid_series.min()
    max_val = custom_max if custom_max is not None else valid_series.max()

    if max_val == min_val:
        # Avoid division by zero when all values are identical
        return pd.Series(50.0, index=series.index)

    if direction == "higher_is_worse":
        norm = ((series - min_val) / (max_val - min_val)) * 100.0
    elif direction == "lower_is_worse":
        norm = ((max_val - series) / (max_val - min_val)) * 100.0
    else:
        raise ValueError(f"Unknown normalization direction: {direction}")

    # Clip to [0, 100] bounds to prevent numerical overshoot from outliers
    return norm.clip(0.0, 100.0)


def calculate_data_coverage(df: pd.DataFrame) -> pd.Series:
    """
    Calculates the percentage of available (non-null) indicators for each district.
    
    Returns:
        pd.Series of coverage percentages [0.0 to 100.0].
    """
    raw_cols = [meta["raw_col"] for meta in config.INDICATORS.values() if meta["raw_col"] in df.columns]
    total_indicators = len(raw_cols)
    if total_indicators == 0:
        return pd.Series(0.0, index=df.index)

    available_count = df[raw_cols].notna().sum(axis=1)
    coverage_pct = (available_count / total_indicators) * 100.0
    return coverage_pct.round(1)


def compute_composite_scores(
    df: pd.DataFrame,
    climate_weights: Optional[Dict[str, float]] = None,
    socio_weights: Optional[Dict[str, float]] = None,
    category_weights: Optional[Dict[str, float]] = None
) -> pd.DataFrame:
    """
    Computes normalized indicators, Climate Hazard Score, Socioeconomic Vulnerability Score,
    and Overall Preliminary Vulnerability Score.
    
    Handles missing data transparently by re-weighting remaining indicators and enforcing
    the minimum coverage guardrail.
    """
    df_scored = df.copy()

    # 1. Normalize each indicator
    for ind_key, meta in config.INDICATORS.items():
        raw_col = meta["raw_col"]
        norm_col = meta["norm_col"]
        direction = meta.get("direction", "higher_is_worse")

        if raw_col in df_scored.columns:
            # Special treatment: population density is logarithmic-scaled before min-max
            # to prevent mega-cities (e.g. Karachi, Lahore) from compressing all rural districts to near zero
            if ind_key == "population_density":
                log_vals = np.log1p(df_scored[raw_col].fillna(0).clip(lower=0))
                df_scored[norm_col] = normalize_series(log_vals, direction=direction)
            else:
                df_scored[norm_col] = normalize_series(df_scored[raw_col], direction=direction)
        else:
            df_scored[norm_col] = np.nan

    # 2. Calculate data coverage %
    df_scored["data_coverage_pct"] = calculate_data_coverage(df_scored)

    # 3. Aggregate Climate Hazard Score
    hazard_indicators = [
        k for k, v in config.INDICATORS.items() if v["category"] == "climate_hazard"
    ]
    hazard_norm_cols = [config.INDICATORS[k]["norm_col"] for k in hazard_indicators]

    if climate_weights is None:
        # Default equal weights across available hazard indicators
        hazard_weight_vals = [config.INDICATORS[k].get("default_weight", 1.0) for k in hazard_indicators]
    else:
        hazard_weight_vals = [climate_weights.get(k, 1.0) for k in hazard_indicators]

    # Normalize weights so they sum to 1
    total_hw = sum(hazard_weight_vals)
    norm_hw = [w / total_hw for w in hazard_weight_vals]

    # Weighted mean of normalized hazard columns
    hazard_matrix = df_scored[hazard_norm_cols].values
    hazard_w = np.array(norm_hw)
    df_scored["climate_hazard_score"] = np.nanmean(hazard_matrix * hazard_w * len(hazard_norm_cols), axis=1)

    # 4. Aggregate Socioeconomic Vulnerability Score
    socio_indicators = [
        k for k, v in config.INDICATORS.items() if v["category"] == "socioeconomic_vulnerability"
    ]
    socio_norm_cols = [config.INDICATORS[k]["norm_col"] for k in socio_indicators]

    if socio_weights is None:
        socio_weight_vals = [config.INDICATORS[k].get("default_weight", 1.0) for k in socio_indicators]
    else:
        socio_weight_vals = [socio_weights.get(k, 1.0) for k in socio_indicators]

    total_sw = sum(socio_weight_vals)
    norm_sw = [w / total_sw for w in socio_weight_vals]

    socio_matrix = df_scored[socio_norm_cols].values
    socio_w = np.array(norm_sw)
    df_scored["socioeconomic_vulnerability_score"] = np.nanmean(socio_matrix * socio_w * len(socio_norm_cols), axis=1)

    # 5. Composite Preliminary Vulnerability Score
    cat_weights = category_weights or config.DEFAULT_CATEGORY_WEIGHTS
    w_hazard = cat_weights.get("climate_hazard", 0.50)
    w_socio = cat_weights.get("socioeconomic_vulnerability", 0.50)

    # Composite = w_hazard * CHS + w_socio * SVS
    df_scored["preliminary_vulnerability_score"] = (
        (w_hazard * df_scored["climate_hazard_score"]) +
        (w_socio * df_scored["socioeconomic_vulnerability_score"])
    )

    # 6. Apply Data Coverage Guardrail
    low_coverage_mask = df_scored["data_coverage_pct"] < config.MIN_DATA_COVERAGE_PCT
    df_scored.loc[low_coverage_mask, "preliminary_vulnerability_score"] = np.nan

    # Round scores for clean presentation
    df_scored["climate_hazard_score"] = df_scored["climate_hazard_score"].round(1)
    df_scored["socioeconomic_vulnerability_score"] = df_scored["socioeconomic_vulnerability_score"].round(1)
    df_scored["preliminary_vulnerability_score"] = df_scored["preliminary_vulnerability_score"].round(1)

    # 7. Categorical Relative Classification
    def classify_vulnerability(val: float) -> str:
        if pd.isna(val):
            return "Insufficient Data"
        if val <= config.VULNERABILITY_THRESHOLDS["low_max"]:
            return config.CATEGORY_LABELS["low"]
        elif val <= config.VULNERABILITY_THRESHOLDS["mod_max"]:
            return config.CATEGORY_LABELS["moderate"]
        else:
            return config.CATEGORY_LABELS["high"]

    df_scored["vulnerability_category"] = df_scored["preliminary_vulnerability_score"].apply(classify_vulnerability)

    return df_scored
