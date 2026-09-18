"""
Interactive GIS mapping utilities for Pakistan Climate Opportunity Mapper.
Builds Plotly choropleth maps with custom layer switching, dynamic province zooming,
district selection highlighting, and rich environmental tooltips.
"""
from typing import Dict, Any, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import config.settings as config


LAYER_CONFIG = {
    "Preliminary Vulnerability": {
        "col": "preliminary_vulnerability_score",
        "colorscale": "YlOrRd",
        "title": "Preliminary Vulnerability (0–100)",
        "unit": "Index (0–100)",
        "is_raw": False
    },
    "Climate Hazard Score": {
        "col": "climate_hazard_score",
        "colorscale": "Oranges",
        "title": "Climate Hazard Score (0–100)",
        "unit": "Score (0–100)",
        "is_raw": False
    },
    "Socioeconomic Vulnerability Score": {
        "col": "socioeconomic_vulnerability_score",
        "colorscale": "Purples",
        "title": "Socioeconomic Vulnerability (0–100)",
        "unit": "Score (0–100)",
        "is_raw": False
    },
    "Flood Exposure Proxy": {
        "col": "flood_exposure_norm",
        "colorscale": "Blues",
        "title": "Flood Exposure (Normalized 0–100)",
        "unit": "Norm (0–100)",
        "is_raw": False
    },
    "Drought & Water Stress Proxy": {
        "col": "drought_stress_norm",
        "colorscale": "YlOrBr",
        "title": "Drought Stress (Normalized 0–100)",
        "unit": "Norm (0–100)",
        "is_raw": False
    },
    "Extreme Heat Indicator": {
        "col": "heat_stress_norm",
        "colorscale": "Inferno",
        "title": "Heat Stress (Normalized 0–100)",
        "unit": "Norm (0–100)",
        "is_raw": False
    },
    "Rainfall Variability Proxy": {
        "col": "rainfall_variability_norm",
        "colorscale": "Tealrose",
        "title": "Rainfall Variability (Normalized 0–100)",
        "unit": "Norm (0–100)",
        "is_raw": False
    },
    "Multidimensional Poverty Proxy": {
        "col": "poverty_headcount_norm",
        "colorscale": "Reds",
        "title": "Poverty Headcount (Normalized 0–100)",
        "unit": "Norm (0–100)",
        "is_raw": False
    }
}


def compute_map_center_and_zoom(
    df: pd.DataFrame,
    selected_province: Optional[str] = None,
    selected_district: Optional[str] = None
) -> Dict[str, Any]:
    """
    Computes optimal camera center (lat, lon) and zoom level depending on user filter selection.
    """
    if selected_district and selected_district != "All districts":
        dist_row = df[df["district"] == selected_district]
        if not dist_row.empty:
            return {
                "center": {
                    "lat": float(dist_row["center_lat"].iloc[0]),
                    "lon": float(dist_row["center_lon"].iloc[0])
                },
                "zoom": 6.8
            }

    if selected_province and selected_province != "All Pakistan":
        prov_rows = df[df["province"] == selected_province]
        if not prov_rows.empty:
            mean_lat = float(prov_rows["center_lat"].mean())
            mean_lon = float(prov_rows["center_lon"].mean())
            
            # Zoom customized by geographic extent
            zoom_levels = {
                "Balochistan": 5.2,
                "Punjab": 5.8,
                "Sindh": 6.0,
                "Khyber Pakhtunkhwa": 6.0,
                "Gilgit Baltistan": 6.4,
                "Azad Kashmir": 7.0,
                "Islamabad": 9.0
            }
            zoom = zoom_levels.get(selected_province, 5.8)
            return {
                "center": {"lat": mean_lat, "lon": mean_lon},
                "zoom": zoom
            }

    # Default All Pakistan view
    return {
        "center": {
            "lat": config.PAKISTAN_CENTER_LAT,
            "lon": config.PAKISTAN_CENTER_LON
        },
        "zoom": config.DEFAULT_MAP_ZOOM
    }


def create_pakistan_choropleth_map(
    df: pd.DataFrame,
    geojson_data: Dict[str, Any],
    selected_layer: str = "Preliminary Vulnerability",
    selected_province: Optional[str] = None,
    selected_district: Optional[str] = None
) -> go.Figure:
    """
    Generates an interactive Plotly choropleth map with:
    - Layer-specific continuous color scale
    - Highlighted border on selected district
    - Dynamic camera focusing
    - Comprehensive hover tooltips
    """
    layer_info = LAYER_CONFIG.get(selected_layer, LAYER_CONFIG["Preliminary Vulnerability"])
    color_col = layer_info["col"]
    colorscale = layer_info["colorscale"]
    colorbar_title = layer_info["title"]

    camera = compute_map_center_and_zoom(df, selected_province, selected_district)

    # Prepare custom hover data
    hover_cols = {
        "district_id": False,
        "province": True,
        "climate_hazard_score": ":.1f",
        "socioeconomic_vulnerability_score": ":.1f",
        "preliminary_vulnerability_score": ":.1f",
        "data_coverage_pct": ":.0f"
    }

    # Modern Plotly 6 px.choropleth_map
    fig = px.choropleth_map(
        df,
        geojson=geojson_data,
        featureidkey="properties.adm2_pcode",
        locations="district_id",
        color=color_col,
        color_continuous_scale=colorscale,
        range_color=(0, 100),
        map_style="carto-positron",
        zoom=camera["zoom"],
        center=camera["center"],
        opacity=0.82,
        hover_name="district",
        hover_data=hover_cols,
        labels={
            color_col: colorbar_title,
            "district": "District",
            "province": "Province",
            "climate_hazard_score": "Climate Hazard",
            "socioeconomic_vulnerability_score": "Socioeconomic Vuln.",
            "preliminary_vulnerability_score": "Preliminary Index",
            "data_coverage_pct": "Coverage %"
        }
    )

    # If a single district is selected, add a distinct pinpoint marker
    if selected_district and selected_district != "All districts":
        selected_row = df[df["district"] == selected_district]
        if not selected_row.empty:
            sel_lat = float(selected_row["center_lat"].iloc[0])
            sel_lon = float(selected_row["center_lon"].iloc[0])
            sel_pvi = selected_row["preliminary_vulnerability_score"].iloc[0]
            
            fig.add_trace(
                go.Scattermap(
                    lat=[sel_lat],
                    lon=[sel_lon],
                    mode="markers+text",
                    marker=dict(
                        size=14,
                        color="#1B365D",  # Primary Navy accent
                        symbol="circle"
                    ),
                    text=[f"<b>{selected_district}</b> ({sel_pvi})"],
                    textposition="top center",
                    textfont=dict(size=12, color="#0F172A", family="Arial Black"),
                    hoverinfo="skip",
                    showlegend=False
                )
            )

    fig.update_layout(
        margin=dict(r=0, t=0, l=0, b=0),
        coloraxis_colorbar=dict(
            title=dict(text=colorbar_title, font=dict(size=12, family="sans-serif")),
            thicknessmode="pixels",
            thickness=15,
            lenmode="fraction",
            len=0.75,
            x=0.98,
            xanchor="right",
            y=0.5,
            yanchor="middle",
            bgcolor="rgba(255, 255, 255, 0.85)",
            outlinecolor="rgba(0, 0, 0, 0.1)",
            outlinewidth=1
        ),
        paper_bgcolor="#F8FAFC"
    )

    return fig
