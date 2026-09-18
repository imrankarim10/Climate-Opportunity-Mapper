"""
Analytical visualization components for Pakistan Climate Opportunity Mapper.
Includes district indicator profiles (horizontal bar comparison) and
the Climate Hazard vs Socioeconomic Vulnerability analytical positioning scatter plot.
"""
from typing import Optional, List
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import config.settings as config


def create_indicator_profile_chart(
    df: pd.DataFrame,
    selected_district: str,
    selected_province: Optional[str] = None
) -> go.Figure:
    """
    Creates a grouped horizontal bar chart comparing the selected district's normalized indicators
    against the Provincial Average and the National Average.
    """
    dist_row = df[df["district"] == selected_district]
    if dist_row.empty:
        # Fallback empty figure
        fig = go.Figure()
        fig.update_layout(title="Select a district to view indicator profile")
        return fig

    dist_series = dist_row.iloc[0]
    prov_name = dist_series["province"]
    prov_df = df[df["province"] == prov_name]

    indicator_keys = list(config.INDICATORS.keys())
    labels = [config.INDICATORS[k]["short_name"] for k in indicator_keys]
    categories = [config.INDICATORS[k]["category"] for k in indicator_keys]
    norm_cols = [config.INDICATORS[k]["norm_col"] for k in indicator_keys]

    dist_vals = [dist_series[col] for col in norm_cols]
    prov_vals = [prov_df[col].mean() for col in norm_cols]
    nat_vals = [df[col].mean() for col in norm_cols]

    fig = go.Figure()

    # National Benchmark
    fig.add_trace(
        go.Bar(
            name="Pakistan National Average",
            y=labels,
            x=nat_vals,
            orientation="h",
            marker=dict(color="#94A3B8"),  # Slate-400
            opacity=0.75,
            hovertemplate="%{y}<br>National Avg: %{x:.1f}/100<extra></extra>"
        )
    )

    # Provincial Benchmark
    fig.add_trace(
        go.Bar(
            name=f"{prov_name} Average",
            y=labels,
            x=prov_vals,
            orientation="h",
            marker=dict(color="#0284C7"),  # Sky-600
            opacity=0.85,
            hovertemplate=f"%{{y}}<br>{prov_name} Avg: %{{x:.1f}}/100<extra></extra>"
        )
    )

    # District Values
    # Use distinct color depending on whether it belongs to Climate Hazard or Socioeconomic
    district_colors = [
        "#EA580C" if cat == "climate_hazard" else "#7C3AED"  # Orange-600 vs Violet-600
        for cat in categories
    ]
    
    fig.add_trace(
        go.Bar(
            name=f"{selected_district} (District Score)",
            y=labels,
            x=dist_vals,
            orientation="h",
            marker=dict(
                color=district_colors,
                line=dict(color="#0F172A", width=1.5)
            ),
            hovertemplate=f"<b>{selected_district}</b><br>%{{y}}: %{{x:.1f}}/100<extra></extra>"
        )
    )

    fig.update_layout(
        barmode="group",
        xaxis=dict(
            title=dict(
                text="Normalized Score (0–100)",
                font=dict(size=11, color="#475569")
            ),
            range=[0, 105],
            gridcolor="#E2E8F0",
            zeroline=False
        ),
        yaxis=dict(
            autorange="reversed",
            automargin=True,
            tickfont=dict(size=11, color="#1E293B")
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0.0,
            font=dict(size=10, color="#334155"),
            itemsizing="constant"
        ),
        margin=dict(l=145, r=20, t=30, b=45),
        height=410,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF"
    )

    return fig


def create_analytical_positioning_scatter(
    df: pd.DataFrame,
    selected_district: Optional[str] = None,
    selected_province: Optional[str] = None
) -> go.Figure:
    """
    Creates the Climate Hazard vs. Socioeconomic Vulnerability scatter plot:
    - X-axis: Climate Hazard Score
    - Y-axis: Socioeconomic Vulnerability Score
    - Quadrants divided by national medians
    - Selected district prominently highlighted
    - Tooltip shows district details
    """
    fig = go.Figure()

    # Median thresholds for analytical quadrants
    median_hazard = float(df["climate_hazard_score"].median())
    median_socio = float(df["socioeconomic_vulnerability_score"].median())

    # Add quadrant reference zones (shaded rectangles)
    fig.add_shape(
        type="rect",
        x0=median_hazard, y0=median_socio, x1=100, y1=100,
        fillcolor="rgba(239, 68, 68, 0.07)",  # Soft red for compound quadrant
        line=dict(width=0),
        layer="below"
    )
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=median_hazard, y1=median_socio,
        fillcolor="rgba(34, 197, 94, 0.06)",  # Soft green for lower quadrant
        line=dict(width=0),
        layer="below"
    )

    # Reference median lines
    fig.add_hline(
        y=median_socio,
        line_dash="dot",
        line_color="#94A3B8",
        line_width=1.2,
        annotation_text=f"Median Socioeconomic ({median_socio:.1f})",
        annotation_position="bottom right",
        annotation_font=dict(size=9, color="#475569"),
        annotation_bgcolor="rgba(255, 255, 255, 0.85)"
    )
    fig.add_vline(
        x=median_hazard,
        line_dash="dot",
        line_color="#94A3B8",
        line_width=1.2,
        annotation_text=f"Median Hazard ({median_hazard:.1f})",
        annotation_position="top left",
        annotation_font=dict(size=9, color="#475569"),
        annotation_bgcolor="rgba(255, 255, 255, 0.85)"
    )

    # Province color palette
    province_colors = {
        "Punjab": "#2563EB",
        "Sindh": "#16A34A",
        "Balochistan": "#D97706",
        "Khyber Pakhtunkhwa": "#7C3AED",
        "Gilgit Baltistan": "#0891B2",
        "Azad Kashmir": "#DB2777",
        "Islamabad": "#475569"
    }

    provinces = sorted(df["province"].unique().tolist())
    for prov in provinces:
        prov_data = df[df["province"] == prov]
        is_highlighted_prov = (selected_province == "All Pakistan" or selected_province is None or selected_province == prov)
        base_opacity = 0.85 if is_highlighted_prov else 0.25

        fig.add_trace(
            go.Scatter(
                x=prov_data["climate_hazard_score"],
                y=prov_data["socioeconomic_vulnerability_score"],
                mode="markers",
                name=prov,
                marker=dict(
                    size=9,
                    color=province_colors.get(prov, "#64748B"),
                    opacity=base_opacity,
                    line=dict(width=0.5, color="#FFFFFF")
                ),
                text=prov_data["district"],
                customdata=np.stack((
                    prov_data["province"],
                    prov_data["preliminary_vulnerability_score"],
                    prov_data["vulnerability_category"]
                ), axis=-1),
                hovertemplate=(
                    "<b>%{text}</b> (%{customdata[0]})<br>"
                    "Climate Hazard: %{x:.1f}<br>"
                    "Socioeconomic Vuln: %{y:.1f}<br>"
                    "Preliminary Index: %{customdata[1]:.1f}<br>"
                    "Classification: %{customdata[2]}<extra></extra>"
                )
            )
        )

    # Highlight selected district if one is chosen
    if selected_district and selected_district != "All districts":
        sel_row = df[df["district"] == selected_district]
        if not sel_row.empty:
            x_val = float(sel_row["climate_hazard_score"].iloc[0])
            y_val = float(sel_row["socioeconomic_vulnerability_score"].iloc[0])
            pvi_val = float(sel_row["preliminary_vulnerability_score"].iloc[0])

            fig.add_trace(
                go.Scatter(
                    x=[x_val],
                    y=[y_val],
                    mode="markers+text",
                    name="Selected District",
                    marker=dict(
                        size=16,
                        color="#DC2626",  # Red-600
                        symbol="star",
                        line=dict(color="#0F172A", width=1.5)
                    ),
                    text=[f"<b>{selected_district}</b> ({pvi_val:.1f})"],
                    textposition="top right",
                    textfont=dict(size=10, color="#0F172A"),
                    hoverinfo="skip",
                    showlegend=True
                )
            )

    fig.update_layout(
        xaxis=dict(
            title=dict(
                text="Climate Hazard Score (0–100)",
                font=dict(size=11, color="#475569")
            ),
            range=[0, 103],
            gridcolor="#F1F5F9",
            zeroline=False
        ),
        yaxis=dict(
            title=dict(
                text="Socioeconomic Vulnerability Score (0–100)",
                font=dict(size=11, color="#475569")
            ),
            range=[0, 103],
            gridcolor="#F1F5F9",
            zeroline=False
        ),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1.0,
            xanchor="left",
            x=1.02,
            font=dict(size=9.5, color="#334155")
        ),
        margin=dict(l=55, r=135, t=20, b=45),
        height=410,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF"
    )

    return fig
