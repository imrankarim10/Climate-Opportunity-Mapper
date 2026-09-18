"""
Methodology and Analytical Framework
Pakistan Climate Opportunity Mapper — Module 1
"""
import streamlit as st
import pandas as pd

import config.settings as config

st.set_page_config(
    page_title="Methodology | Pakistan Climate Opportunity Mapper",
    layout="wide"
)

# Institutional Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    .inst-header-bar {
        background: linear-gradient(90deg, #0F172A 0%, #1E293B 100%);
        color: #F8FAFC;
        padding: 0.75rem 1.25rem;
        border-radius: 8px;
        margin-bottom: 1.25rem;
        border-left: 5px solid #0284C7;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .inst-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0;
    }
    .inst-subtitle {
        font-size: 0.85rem;
        color: #94A3B8;
        margin-top: 0.15rem;
    }
    .inst-badge {
        background-color: rgba(2, 132, 199, 0.2);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.4);
        padding: 0.3rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .method-callout {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #0284C7;
        padding: 0.85rem 1.1rem;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #334155;
        margin: 1rem 0;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="inst-header-bar">
    <div>
        <div class="inst-title">Analytical Methodology & Index Framework</div>
        <div class="inst-subtitle">Pakistan Climate Opportunity Mapper — Module 1 Technical Architecture</div>
    </div>
    <div>
        <span class="inst-badge">Scientific Framework</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
This document details the scientific, mathematical, and data-engineering foundations of the **Preliminary Vulnerability Index (PVI)** and its constituent hazard and socioeconomic pillars.

As an analytical decision-support prototype, this tool provides **relative spatial screening** across Pakistan's 160 administrative districts to support early-stage climate project identification and research.
""")

# Table of Contents tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Data Pipeline & Harmonization",
    "2. Normalization & Scoring",
    "3. Scientific Distinctions (Hazard vs Risk)",
    "4. Limitations & Quality Guardrails"
])

with tab1:
    st.subheader("1. Data Collection & Geographic Harmonization")
    st.markdown("""
    ### Geographic Foundation
    * **Administrative Boundary Standard:** United Nations Office for the Coordination of Humanitarian Affairs (UN OCHA) / Humanitarian Data Exchange (HDX) **Common Operational Dataset for Administrative Boundaries (COD-AB) Pakistan**, published September 2022.
    * **Spatial Hierarchy:** National (`ADM0`, Pakistan) to Province/Region (`ADM1`, 7 units) to District (`ADM2`, 160 units).
    * **Standardized District Identifier (`district_id`):** To eliminate spelling and administrative discrepancies across varied government and multilateral agencies, every district is assigned its official UN P-Code (e.g., `PK101`, `PK201`, `PK729`).
    
    ### Programmatic Naming Harmonization
    Administrative entities in Pakistan frequently vary in spelling, transliteration, or historic nomenclature across different databases. The automated ingestion pipeline (`src/preprocessing.py`) implements a programmatic harmonization engine:
    """)

    sample_harmonization = [
        {"Agency Variant": "Chaghi", "Official UN OCHA Standard": "Chagai", "Standardized P-Code": "PK203", "Province": "Balochistan"},
        {"Agency Variant": "Hattian / Hattian Bala", "Official UN OCHA Standard": "Jhelum Valley", "Standardized P-Code": "PK103", "Province": "Azad Kashmir"},
        {"Agency Variant": "Surab", "Official UN OCHA Standard": "Shaheed Sikandarabad", "Standardized P-Code": "PK233", "Province": "Balochistan"},
        {"Agency Variant": "Layyah", "Official UN OCHA Standard": "Leiah", "Standardized P-Code": "PK618", "Province": "Punjab"},
        {"Agency Variant": "Dera Ismail Khan", "Official UN OCHA Standard": "D. I. Khan", "Standardized P-Code": "PK509", "Province": "Khyber Pakhtunkhwa"},
        {"Agency Variant": "Karachi Central / East / South", "Official UN OCHA Standard": "Central / East / South Karachi", "Standardized P-Code": "PK702 / 704 / 721", "Province": "Sindh"},
        {"Agency Variant": "Ex-FATA Agencies (Bajaur, Khyber, Kurram)", "Official UN OCHA Standard": "Post-25th Amendment Districts", "Standardized P-Code": "PK502, PK513, etc.", "Province": "Khyber Pakhtunkhwa"}
    ]
    st.dataframe(pd.DataFrame(sample_harmonization), hide_index=True, use_container_width=True)


with tab2:
    st.subheader("2. Indicator Normalization & Composite Scoring")
    
    st.markdown("""
    ### Indicator Directionality & Min-Max Scaling
    Environmental and socioeconomic indicators possess differing physical units (e.g., temperature in °C, population density in persons/km², poverty in %, rainfall variance in CV %).
    To aggregate these indicators into a rigorous composite metric, all raw indicators are normalized onto a consistent **0–100 scale** using min-max scaling:

    $$\\text{Normalized Score} = \\frac{x - x_{\\min}}{x_{\\max} - x_{\\min}} \\times 100$$
    
    Where:
    * **$x$** is the observed raw metric for a given district.
    * **$x_{\\min}$** and **$x_{\\max}$** are the empirical minimum and maximum observed values across the national dataset.
    * All 7 indicators in Module 1 are directionally aligned:
      $$\\text{Score} = 100 \\longrightarrow \\text{Highest Relative Exposure or Vulnerability}$$
      $$\\text{Score} = 0 \\longrightarrow \\text{Lowest Relative Exposure or Vulnerability}$$
    
    <div class="method-callout">
        <strong>Logarithmic Transformation for Population Density:</strong><br>
        Population density spans five orders of magnitude—from 4.1 persons/km² in Awaran to over 43,000 persons/km² in Karachi Central. A standard linear scaling would compress 95% of districts into values near zero. Therefore, population density is transformed logarithmically: $\\ln(1 + \\text{density})$ prior to min-max scaling.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### Composite Formulation
    The **Preliminary Vulnerability Index (PVI)** aggregates two equal thematic pillars:
    
    $$PVI = (W_{\\text{hazard}} \\times \\text{Climate Hazard Score}) + (W_{\\text{socio}} \\times \\text{Socioeconomic Vulnerability Score})$$
    
    Where by default:
    * **Climate Hazard Score (50% Weight)**:
      $$\\text{CHS} = 0.25 \\times \\text{Flood} + 0.25 \\times \\text{Drought} + 0.25 \\times \\text{Heat} + 0.25 \\times \\text{Rainfall CV}$$
    * **Socioeconomic Vulnerability Score (50% Weight)**:
      $$\\text{SVS} = 0.30 \\times \\text{Density} + 0.40 \\times \\text{Multidimensional Poverty} + 0.30 \\times \\text{Rural Agri Dependence}$$
    """)


with tab3:
    st.subheader("3. Scientific Distinctions: Hazard, Exposure, Vulnerability, and Risk")
    
    st.markdown("""
    In accordance with the Intergovernmental Panel on Climate Change (IPCC AR6 WGII) conceptual framework, this tool maintains strict terminological discipline:
    
    * **Hazard**: The potential occurrence of a natural or human-induced physical event or trend (e.g., flash flooding, heatwave duration, meteorological aridity) that may cause physical damage or loss.
    * **Exposure**: The presence of people, livelihoods, infrastructure, or environmental services in areas that could be adversely affected by a hazard event.
    * **Vulnerability**: The predisposition or susceptibility of a population or system to experience harm, driven by poverty, lack of asset diversification, and inadequate coping capacity.
    * **Risk**: The resulting potential for adverse consequences resulting from the compounding interaction between climate hazards, exposed assets, and vulnerable human systems.
    
    <div class="method-callout">
        <strong>Methodological Rationale for the "Proxy" Designation:</strong><br>
        National-level public statistics provide proxy representations of physical exposure and social sensitivity; they do not replace hydrodynamic 2D floodplain modeling or primary household socio-economic surveys. Therefore, variables are explicitly designated as <strong>proxies</strong> (e.g., <em>Flood Exposure Proxy</em>, <em>Drought & Water Stress Proxy</em>) to avoid misleading precision.
    </div>
    """, unsafe_allow_html=True)


with tab4:
    st.subheader("4. Limitations, Missing Data Treatment & Quality Guardrails")
    
    st.markdown("""
    ### Minimum Data Coverage Guardrail
    To prevent false precision and skewed rankings:
    * **Threshold Rule:** If an administrative unit has fewer than **60% of required indicators** available, the composite score is suppressed, and the system reports:  
      *`"Insufficient data for composite score."`*
    * In the current baseline master dataset, all 160 districts achieve **100% data completeness** across the core indicator suite.
    
    ### Analytical Positioning vs Operational Mandates
    * The **Climate Hazard vs Socioeconomic Vulnerability scatter plot** visualizes the analytical positioning of districts across national median lines.
    * **Placement in the upper-right quadrant does not constitute an automated investment mandate.** Practical climate-finance project development requires:
      1. Primary field validation and community stakeholder consultation.
      2. Verification of local water tenure, land rights, and existing irrigation infrastructure.
      3. Alignment with provincial Climate Change Action Plans and national climate programming guidelines.
      4. Detailed Environmental and Social Safeguards (ESS) screening against international standards.
    """)
