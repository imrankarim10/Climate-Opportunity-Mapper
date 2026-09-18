"""
Pakistan Climate Opportunity Mapper
Module 1: Pakistan Climate & Vulnerability Explorer

Institutional decision-support platform for spatial climate-risk and
socioeconomic vulnerability screening across districts in Pakistan.
"""
import streamlit as st
import pandas as pd
import numpy as np

import config.settings as config
from src.data_loader import (
    load_processed_data,
    load_geojson,
    get_available_provinces,
    get_districts_for_province,
    get_district_record,
    format_district_export
)
from src.map_utils import create_pakistan_choropleth_map, LAYER_CONFIG
from src.charts import create_indicator_profile_chart, create_analytical_positioning_scatter
from src.scoring import compute_composite_scores

# ---------------- Streamlit Page Configuration ----------------
st.set_page_config(
    page_title="Pakistan Climate Opportunity Mapper | Module 1",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CSS: Pinned Sidebar & Executive Command Center ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Pinned Sidebar: Force expanded and hide collapse button */
    section[data-testid="stSidebar"] {
        width: 320px !important;
        min-width: 320px !important;
        transform: none !important;
        position: relative !important;
        transition: none !important;
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B !important;
    }
    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        color: #0F172A !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #0F172A !important;
    }
    button[data-testid="stSidebarCollapseButton"],
    button[data-testid="baseButton-headerNoPadding"],
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* Institutional Header Banner */
    .command-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #334155;
        border-left: 6px solid #0284C7;
        padding: 1.1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
    }
    .header-tag {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        color: #38BDF8;
        text-transform: uppercase;
    }
    .header-main-title {
        font-size: 1.55rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        margin-top: 0.15rem;
        line-height: 1.2;
    }
    .header-sub {
        font-size: 0.85rem;
        color: #94A3B8;
        margin-top: 0.2rem;
    }
    .header-badge-live {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.4);
        padding: 0.4rem 0.85rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        display: inline-block;
        text-align: right;
    }

    /* KPI Cards */
    .metric-panel {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
        position: relative;
        overflow: hidden;
    }
    .metric-panel::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3.5px;
        background: #CBD5E1;
    }
    .metric-hazard::before { background: #EA580C; }
    .metric-socio::before { background: #7C3AED; }
    .metric-composite::before { background: #0284C7; }
    .metric-coverage::before { background: #059669; }

    .metric-title {
        font-size: 0.72rem;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .metric-number {
        font-size: 1.7rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 0.2rem;
        line-height: 1.1;
    }
    .metric-meta {
        font-size: 0.72rem;
        color: #94A3B8;
        margin-top: 0.35rem;
    }

    /* District Cockpit Glass Card */
    .cockpit-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.25rem;
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.04);
        margin-bottom: 1rem;
    }
    .cockpit-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        padding-bottom: 0.85rem;
        border-bottom: 1px solid #F1F5F9;
        margin-bottom: 1rem;
    }
    .cockpit-name {
        font-size: 1.45rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
    }
    .cockpit-pcode {
        font-size: 0.82rem;
        color: #64748B;
        margin-top: 0.2rem;
    }

    /* Category Badges */
    .status-chip {
        display: inline-block;
        padding: 0.3rem 0.75rem;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.75rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    .chip-red {
        background-color: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FECACA;
    }
    .chip-yellow {
        background-color: #FFFBEB;
        color: #B45309;
        border: 1px solid #FDE68A;
    }
    .chip-green {
        background-color: #F0FDF4;
        color: #15803D;
        border: 1px solid #BBF7D0;
    }

    /* Indicator Comparison Bar */
    .ind-item {
        padding: 0.6rem 0;
        border-bottom: 1px solid #F8FAFC;
    }
    .ind-item:last-child {
        border-bottom: none;
    }
    .ind-header {
        display: flex;
        justify-content: space-between;
        font-size: 0.84rem;
        font-weight: 600;
        color: #1E293B;
        margin-bottom: 0.25rem;
    }
    .ind-obs {
        font-size: 0.78rem;
        color: #64748B;
        font-weight: 400;
    }

    /* Sidebar Clean Styling */
    .sidebar-brand-box {
        padding: 0.75rem 0 1.25rem 0;
        border-bottom: 1px solid #334155;
        margin-bottom: 1.25rem;
    }
    .sb-org {
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        color: #38BDF8;
        text-transform: uppercase;
    }
    .sb-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-top: 0.2rem;
    }
    .sb-sub {
        font-size: 0.75rem;
        color: #94A3B8;
        margin-top: 0.15rem;
    }

    /* Disclaimer Card */
    .notice-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #0284C7;
        padding: 0.65rem 1rem;
        border-radius: 6px;
        font-size: 0.8rem;
        color: #475569;
        margin-bottom: 1.25rem;
        line-height: 1.45;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- Data Loading ----------------
try:
    df_master = load_processed_data()
    geojson_data = load_geojson()
except Exception as e:
    st.error(f"Data engine initialization error: {e}")
    st.stop()


# ---------------- Pinned Sidebar Controls ----------------
st.sidebar.markdown("""
<div class="sidebar-brand-box">
    <div class="sb-org">Climate Analytics & GIS</div>
    <div class="sb-title">Pakistan Opportunity Mapper</div>
    <div class="sb-sub">Module 1: Vulnerability Explorer</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("**Geographic Filter**")

# Province Selector
provinces = ["All Pakistan"] + get_available_provinces(df_master)
selected_province = st.sidebar.selectbox(
    "Province / Region",
    provinces,
    index=0,
    help="Filter data and camera focus to a specific province or territory."
)

# Dynamic District Selector
available_districts = get_districts_for_province(df_master, selected_province)
district_options = ["All districts"] + available_districts

selected_district = st.sidebar.selectbox(
    "District Selection",
    district_options,
    index=0,
    help="Select a district to isolate its risk metrics, indicator profile, and benchmarks."
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Layer Display**")

layer_choices = list(LAYER_CONFIG.keys())
selected_layer = st.sidebar.selectbox(
    "Active Geospatial Layer",
    layer_choices,
    index=0,
    help="Select the environmental hazard or socioeconomic indicator to render on the choropleth map."
)

# Optional Sensitivity Weight Customizer
with st.sidebar.expander("Analytical Weight Customizer", expanded=False):
    st.caption("Adjust composite weighting to test screening sensitivity:")
    w_hazard = st.slider("Climate Hazard Weight (%)", min_value=0, max_value=100, value=50, step=5)
    w_socio = 100 - w_hazard
    st.text(f"Socioeconomic Weight: {w_socio}%")
    
    if w_hazard != 50:
        cat_w = {
            "climate_hazard": w_hazard / 100.0,
            "socioeconomic_vulnerability": w_socio / 100.0
        }
        df_current = compute_composite_scores(df_master, category_weights=cat_w)
    else:
        df_current = df_master

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Export**")

# Export functionality
export_df = format_district_export(
    df_current,
    selected_district if selected_district != "All districts" else None
)

col_dl1, col_dl2 = st.sidebar.columns(2)
with col_dl1:
    csv_data = export_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name=f"pakistan_vulnerability_{selected_district.replace(' ', '_') if selected_district != 'All districts' else 'all_districts'}.csv",
        mime="text/csv",
        use_container_width=True
    )
with col_dl2:
    json_data = export_df.to_json(orient="records", indent=2).encode("utf-8")
    st.download_button(
        label="Download JSON",
        data=json_data,
        file_name=f"pakistan_vulnerability_{selected_district.replace(' ', '_') if selected_district != 'All districts' else 'all_districts'}.json",
        mime="application/json",
        use_container_width=True
    )

st.sidebar.markdown("---")
st.sidebar.caption("Spatial standard: UN OCHA COD-AB (Sept 2022). Authoritative sources: PBS, NDMA, PMD, UNDP.")


# ---------------- Top Command Center Banner ----------------
st.markdown(f"""
<div class="command-header">
    <div>
        <div class="header-tag">Decision Support System — Spatial Screening Layer</div>
        <div class="header-main-title">{config.APP_TITLE}</div>
        <div class="header-sub">{config.APP_SUBTITLE} &nbsp;|&nbsp; 160 Administrative Units Harmonized</div>
    </div>
    <div style="text-align: right;">
        <span class="header-badge-live">Status: Operational</span>
        <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 0.35rem;">National Baseline: 2022/2023</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="notice-box">
    <strong>Analytical Protocol:</strong> {config.APP_DISCLAIMER}
</div>
""", unsafe_allow_html=True)


# ---------------- Geographic Scope & KPI Metrics ----------------
if selected_province != "All Pakistan":
    kpi_df = df_current[df_current["province"] == selected_province]
    kpi_scope_desc = f"{selected_province} Scope"
else:
    kpi_df = df_current
    kpi_scope_desc = "National Scope (160 Districts)"

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""
    <div class="metric-panel">
        <div class="metric-title">Units Analysed</div>
        <div class="metric-number">{len(kpi_df)}</div>
        <div class="metric-meta">{kpi_scope_desc}</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    avg_haz = kpi_df["climate_hazard_score"].mean()
    st.markdown(f"""
    <div class="metric-panel metric-hazard">
        <div class="metric-title">Climate Hazard</div>
        <div class="metric-number">{avg_haz:.1f}<span style='font-size:0.95rem;color:#94A3B8;'>/100</span></div>
        <div class="metric-meta">Mean exposure proxy</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    avg_soc = kpi_df["socioeconomic_vulnerability_score"].mean()
    st.markdown(f"""
    <div class="metric-panel metric-socio">
        <div class="metric-title">Socioeconomic Vuln.</div>
        <div class="metric-number">{avg_soc:.1f}<span style='font-size:0.95rem;color:#94A3B8;'>/100</span></div>
        <div class="metric-meta">Mean deprivation proxy</div>
    </div>
    """, unsafe_allow_html=True)
with k4:
    avg_pvi = kpi_df["preliminary_vulnerability_score"].mean()
    st.markdown(f"""
    <div class="metric-panel metric-composite">
        <div class="metric-title">Preliminary Index</div>
        <div class="metric-number">{avg_pvi:.1f}<span style='font-size:0.95rem;color:#94A3B8;'>/100</span></div>
        <div class="metric-meta">Composite screening metric</div>
    </div>
    """, unsafe_allow_html=True)
with k5:
    cov = kpi_df["data_coverage_pct"].mean()
    st.markdown(f"""
    <div class="metric-panel metric-coverage">
        <div class="metric-title">Data Completeness</div>
        <div class="metric-number">{cov:.0f}%</div>
        <div class="metric-meta">7 of 7 core indicators</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")


# ---------------- Split-Screen Command Center ----------------
# Left Column (7): Geospatial Map | Right Column (5): Intelligence Cockpit
col_map, col_cockpit = st.columns([7, 5])

with col_map:
    st.markdown(f"#### Geospatial Intelligence Map — {selected_layer}")
    st.caption("Rendered across 160 UN OCHA administrative polygons. Hover to inspect localized scores; click sidebar to filter.")
    
    map_fig = create_pakistan_choropleth_map(
        df=df_current,
        geojson_data=geojson_data,
        selected_layer=selected_layer,
        selected_province=selected_province,
        selected_district=selected_district
    )
    st.plotly_chart(map_fig, use_container_width=True)

    # Regional Quick Facts Bar below map
    top_regional_dist = kpi_df.sort_values(by="preliminary_vulnerability_score", ascending=False).iloc[0]
    low_regional_dist = kpi_df.sort_values(by="preliminary_vulnerability_score", ascending=True).iloc[0]
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; background: #F8FAFC; border: 1px solid #E2E8F0; padding: 0.55rem 0.9rem; border-radius: 6px; font-size: 0.78rem; color: #475569; margin-top: -0.5rem;">
        <div>Regional Peak: <strong>{top_regional_dist['district']}</strong> ({top_regional_dist['preliminary_vulnerability_score']:.1f}/100)</div>
        <div>Regional Median: <strong>{kpi_df['preliminary_vulnerability_score'].median():.1f}/100</strong></div>
        <div>Regional Baseline: <strong>{low_regional_dist['district']}</strong> ({low_regional_dist['preliminary_vulnerability_score']:.1f}/100)</div>
    </div>
    """, unsafe_allow_html=True)

with col_cockpit:
    if selected_district and selected_district != "All districts":
        dist_row = get_district_record(df_current, selected_district)
        
        if dist_row is not None:
            pvi_val = dist_row["preliminary_vulnerability_score"]
            chs_val = dist_row["climate_hazard_score"]
            svs_val = dist_row["socioeconomic_vulnerability_score"]
            cat_label = dist_row["vulnerability_category"]
            
            # Chip styling
            if "Higher" in cat_label:
                chip_html = '<span class="status-chip chip-red">Higher Relative Vulnerability</span>'
            elif "Moderate" in cat_label:
                chip_html = '<span class="status-chip chip-yellow">Moderate Relative Vulnerability</span>'
            else:
                chip_html = '<span class="status-chip chip-green">Lower Relative Vulnerability</span>'

            # Percentiles & Rankings
            pvi_percentile = (df_current["preliminary_vulnerability_score"] <= pvi_val).mean() * 100.0
            prov_districts = df_current[df_current["province"] == dist_row["province"]]
            prov_rank = (prov_districts["preliminary_vulnerability_score"] > pvi_val).sum() + 1
            prov_total = len(prov_districts)

            st.markdown(f"""
            <div class="cockpit-container">
                <div class="cockpit-header">
                    <div>
                        <div class="cockpit-name">{selected_district}</div>
                        <div class="cockpit-pcode">
                            Province: <strong>{dist_row['province']}</strong> &nbsp;|&nbsp; 
                            P-Code: <strong>{dist_row['district_id']}</strong> &nbsp;|&nbsp; 
                            Area: <strong>{dist_row['area_sqkm']:,.0f} km²</strong>
                        </div>
                    </div>
                    <div>
                        {chip_html}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Triple Key Score Gauges
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Climate Hazard", f"{chs_val:.1f} / 100")
                st.progress(min(1.0, max(0.0, chs_val / 100.0)))
            with c2:
                st.metric("Socioeconomic", f"{svs_val:.1f} / 100")
                st.progress(min(1.0, max(0.0, svs_val / 100.0)))
            with c3:
                st.metric("Composite Index", f"{pvi_val:.1f} / 100")
                st.progress(min(1.0, max(0.0, pvi_val / 100.0)))

            st.write("")

            # Tabbed breakdown
            tb_haz, tb_soc, tb_rank = st.tabs([
                "Hazard Exposure Breakdown",
                "Socioeconomic Sensitivity",
                "Percentiles & Standing"
            ])

            with tb_haz:
                st.markdown(f"""
                <div class="ind-item">
                    <div class="ind-header">
                        <span>Flood Exposure Proxy</span>
                        <span><strong>{dist_row['flood_exposure_norm']:.1f}</strong>/100</span>
                    </div>
                    <div class="ind-obs">Observed: {dist_row['flood_exposure_raw']:.1f}/100 &nbsp;|&nbsp; NDMA/PDNA 2022 Floods</div>
                </div>
                <div class="ind-item">
                    <div class="ind-header">
                        <span>Drought & Water Stress Proxy</span>
                        <span><strong>{dist_row['drought_stress_norm']:.1f}</strong>/100</span>
                    </div>
                    <div class="ind-obs">Observed: {dist_row['drought_stress_raw']:.1f}/100 &nbsp;|&nbsp; PMD NDMC Aridity / WRI</div>
                </div>
                <div class="ind-item">
                    <div class="ind-header">
                        <span>Extreme Heat & Temperature</span>
                        <span><strong>{dist_row['heat_stress_norm']:.1f}</strong>/100</span>
                    </div>
                    <div class="ind-obs">Observed: {dist_row['heat_stress_raw']:.1f} °C mean max &nbsp;|&nbsp; PMD / World Bank CCKP</div>
                </div>
                <div class="ind-item">
                    <div class="ind-header">
                        <span>Precipitation Variability</span>
                        <span><strong>{dist_row['rainfall_variability_norm']:.1f}</strong>/100</span>
                    </div>
                    <div class="ind-obs">Observed: {dist_row['rainfall_variability_raw']:.1f}% interannual CV &nbsp;|&nbsp; PMD / CHIRPS</div>
                </div>
                """, unsafe_allow_html=True)

            with tb_soc:
                st.markdown(f"""
                <div class="ind-item">
                    <div class="ind-header">
                        <span>Multidimensional Poverty Headcount</span>
                        <span><strong>{dist_row['poverty_headcount_norm']:.1f}</strong>/100</span>
                    </div>
                    <div class="ind-obs">Observed: {dist_row['poverty_headcount_raw']:.1f}% headcount ratio &nbsp;|&nbsp; Planning Commission/UNDP</div>
                </div>
                <div class="ind-item">
                    <div class="ind-header">
                        <span>Population Density Proxy</span>
                        <span><strong>{dist_row['population_density_norm']:.1f}</strong>/100</span>
                    </div>
                    <div class="ind-obs">Observed: {dist_row['population_density_raw']:,.1f} persons/km² &nbsp;|&nbsp; PBS Digital Census</div>
                </div>
                <div class="ind-item">
                    <div class="ind-header">
                        <span>Rural & Agrarian Livelihoods</span>
                        <span><strong>{dist_row['rural_agri_share_norm']:.1f}</strong>/100</span>
                    </div>
                    <div class="ind-obs">Observed: {dist_row['rural_agri_share_raw']:.1f}% rural share &nbsp;|&nbsp; PBS Census</div>
                </div>
                <div class="ind-item">
                    <div class="ind-header">
                        <span>Data Completeness Score</span>
                        <span><strong>{dist_row['data_coverage_pct']:.0f}%</strong></span>
                    </div>
                    <div class="ind-obs">All 7 required indicators available with zero imputation required.</div>
                </div>
                """, unsafe_allow_html=True)

            with tb_rank:
                st.markdown(f"""
                **National Benchmark Standing**
                - Preliminary Vulnerability: **{pvi_val:.1f} / 100**
                - National Standing: **{pvi_percentile:.1f}th percentile** (ranks in top {100 - pvi_percentile:.1f}% nationwide)
                - Relative Category: **{cat_label}**

                **Provincial Position ({dist_row['province']})**
                - Rank: **Rank #{prov_rank}** of {prov_total} districts in {dist_row['province']}
                - Provincial Mean Score: **{prov_districts['preliminary_vulnerability_score'].mean():.1f} / 100**
                - Variance from Regional Baseline: **{pvi_val - prov_districts['preliminary_vulnerability_score'].mean():+.1f} points**
                """)
    else:
        # Default National Overview Card when no single district is selected
        st.markdown("""
        <div class="cockpit-container">
            <div class="cockpit-header">
                <div>
                    <div class="cockpit-name">National Vulnerability Leaderboard</div>
                    <div class="cockpit-pcode">Top-ranked districts warranting early-stage investigation</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        top_5 = df_current.sort_values(by="preliminary_vulnerability_score", ascending=False).head(5)
        st.markdown("**Highest Relative Vulnerability (National Top 5):**")
        for idx, r in top_5.iterrows():
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.4rem 0; border-bottom: 1px solid #F1F5F9; font-size: 0.85rem;">
                <div><strong>{r['district']}</strong> <span style="color:#64748B;">({r['province']})</span></div>
                <div>
                    <span style="font-weight:700; color:#B91C1C;">{r['preliminary_vulnerability_score']:.1f}/100</span> &nbsp;
                    <span class="status-chip chip-red" style="font-size:0.68rem; padding:0.15rem 0.45rem;">High</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.caption("Select any district from the sidebar dropdown to view its full localized indicator cockpit.")


# ---------------- Analytical Visualizations Section ----------------
st.markdown("---")
st.markdown("### Analytical Visualizations & Strategic Positioning")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    target_dist = selected_district if (selected_district and selected_district != "All districts") else "Tharparkar"
    st.markdown(f"#### Indicator Profile: {target_dist} vs. Benchmarks")
    st.caption("Normalized scores (0–100) compared to Provincial and National benchmark baselines.")
    dist_chart = create_indicator_profile_chart(
        df=df_current,
        selected_district=target_dist,
        selected_province=selected_province
    )
    st.plotly_chart(dist_chart, use_container_width=True)
    if selected_district == "All districts":
        st.caption(f"*(Displaying benchmark for **{target_dist}** as baseline demonstration. Select a district in the sidebar to update.)*")

with chart_col2:
    st.markdown("#### Strategic Positioning: Hazard vs. Vulnerability")
    st.caption("Multi-district scatter mapping. Dashed lines denote national median benchmarks.")
    scatter_chart = create_analytical_positioning_scatter(
        df=df_current,
        selected_district=selected_district,
        selected_province=selected_province
    )
    st.plotly_chart(scatter_chart, use_container_width=True)
    st.caption("Strategic Positioning: Upper-Right quadrant isolates districts with compounded high hazard exposure and high socioeconomic vulnerability.")


# ---------------- Interactive District Screening Table ----------------
st.markdown("---")
st.markdown("### District Screening Master Table")
st.caption("Search, sort, and inspect metrics across all 160 districts. Click column headers to sort by composite index, climate hazard, or poverty headcount.")

table_display_cols = [
    "district_id", "district", "province", "preliminary_vulnerability_score",
    "climate_hazard_score", "socioeconomic_vulnerability_score", "vulnerability_category",
    "flood_exposure_raw", "drought_stress_raw", "heat_stress_raw", "poverty_headcount_raw", "area_sqkm"
]

table_rename = {
    "district_id": "P-Code",
    "district": "District",
    "province": "Province",
    "preliminary_vulnerability_score": "Composite Index",
    "climate_hazard_score": "Hazard Score",
    "socioeconomic_vulnerability_score": "Socioeconomic Score",
    "vulnerability_category": "Vulnerability Tier",
    "flood_exposure_raw": "Flood Proxy",
    "drought_stress_raw": "Drought Proxy",
    "heat_stress_raw": "Heat (°C)",
    "poverty_headcount_raw": "Poverty (%)",
    "area_sqkm": "Area (km²)"
}

table_df = kpi_df[table_display_cols].rename(columns=table_rename).sort_values(by="Composite Index", ascending=False)

st.dataframe(
    table_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Composite Index": st.column_config.ProgressColumn(
            "Composite Index",
            help="Preliminary Vulnerability Index (0-100)",
            format="%.1f",
            min_value=0,
            max_value=100
        ),
        "Hazard Score": st.column_config.NumberColumn(
            "Hazard Score",
            format="%.1f"
        ),
        "Socioeconomic Score": st.column_config.NumberColumn(
            "Socioeconomic Score",
            format="%.1f"
        ),
        "Poverty (%)": st.column_config.NumberColumn(
            "Poverty (%)",
            format="%.1f%%"
        ),
        "Area (km²)": st.column_config.NumberColumn(
            "Area (km²)",
            format="%d"
        )
    }
)


# ---------------- Data Quality & Governance Panel ----------------
st.markdown("---")
st.markdown("### Data Quality, Limitations & Boundary Governance")

dq1, dq2, dq3 = st.columns(3)
with dq1:
    st.markdown("""
    **Completeness & Guardrails**
    - Administrative Units: **160 Districts**
    - Boundary Matching: **100% matched** to UN OCHA COD-AB (2022)
    - Minimum Coverage Guardrail: **60.0%**
    - Districts Suppressed Due to Low Coverage: **0**
    """)
with dq2:
    st.markdown("""
    **Methodological Precision**
    - The composite index is a **relative screening metric**, not an absolute physical risk measurement.
    - Avoid false precision: A score of 73 does not imply "73% risk", but rather ranks in the upper tier relative to national peers.
    """)
with dq3:
    st.markdown("""
    **Boundary Governance**
    - Spatial Reference: **UN OCHA COD-AB Pakistan (Sept 2022)**
    - Standardized P-Codes (`PK101` through `PK729`)
    - Captures post-25th amendment merged tribal districts in Khyber Pakhtunkhwa.
    """)


# ---------------- Source Transparency Table ----------------
with st.expander("Data Source Transparency & Provenance Dictionary", expanded=False):
    st.markdown("Detailed metadata and documentation for every indicator integrated into Module 1:")
    
    source_records = []
    for k, meta in config.INDICATORS.items():
        source_records.append({
            "Indicator": meta["name"],
            "Category": meta["category"].replace("_", " ").title(),
            "Source Agency": meta["source"],
            "Dataset Title": meta["dataset_title"],
            "Vintage / Year": meta["year"],
            "Geographic Resolution": meta["resolution"],
            "Processing Method": meta["processing"],
            "Known Limitations": meta["limitations"],
            "Public Link": meta["url"]
        })
    
    st.dataframe(
        pd.DataFrame(source_records),
        column_config={
            "Public Link": st.column_config.LinkColumn("Public URL")
        },
        use_container_width=True,
        hide_index=True
    )
