"""
About Page: Project Vision, Analytical Scope, Technology & Roadmap
Pakistan Climate Opportunity Mapper — Module 1
"""
import streamlit as st
import config.settings as config

st.set_page_config(
    page_title="About | Pakistan Climate Opportunity Mapper",
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
    .about-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    }
    .module-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        height: 100%;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
        position: relative;
    }
    .module-card.active-module {
        border-top: 3px solid #0284C7;
    }
    .module-card.planned-module {
        border-top: 3px solid #94A3B8;
    }
    .module-status {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        margin-bottom: 0.5rem;
    }
    .status-active {
        background-color: #E0F2FE;
        color: #0369A1;
        border: 1px solid #BAE6FD;
    }
    .status-planned {
        background-color: #F1F5F9;
        color: #475569;
        border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="inst-header-bar">
    <div>
        <div class="inst-title">About Pakistan Climate Opportunity Mapper</div>
        <div class="inst-subtitle">Spatial Decision Support for Climate Vulnerability & Resilience Programming</div>
    </div>
    <div>
        <span class="inst-badge">Project Profile</span>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="about-card">
        <h3 style="margin-top:0; font-size:1.15rem; color:#0F172A;">Project Purpose</h3>
        <p style="font-size:0.9rem; color:#334155; line-height:1.55;">
            The <strong>Pakistan Climate Opportunity Mapper</strong> is an open analytical platform and decision-support prototype developed by an environmental science professional with environmental consultancy and project development experience.
        </p>
        <p style="font-size:0.9rem; color:#334155; line-height:1.55;">
            It demonstrates how <strong>environmental data, Python, GIS, and climate-risk analytics</strong> can be synthesized into a transparent, reproducible spatial decision-support system to inform early-stage climate resilience programming, community adaptation planning, and climate-finance pipeline development.
        </p>
        <hr style="border:none; border-top:1px solid #E2E8F0; margin:1rem 0;">
        <h4 style="font-size:1rem; color:#0F172A; margin-bottom:0.5rem;">Analytical Use Case</h4>
        <p style="font-size:0.88rem; color:#475569; line-height:1.55;">
            The prototype is designed around an early-stage climate-programming use case: bringing together empirical climate, geographic, and socioeconomic evidence to support further investigation of potential areas of climate vulnerability. It is intended as a demonstration of how quantitative data tools can complement field knowledge, stakeholder consultations, and formal project identification processes.
        </p>
        <hr style="border:none; border-top:1px solid #E2E8F0; margin:1rem 0;">
        <h4 style="font-size:1rem; color:#0F172A; margin-bottom:0.5rem;">Analytical Disclaimer</h4>
        <p style="font-size:0.82rem; color:#64748B; line-height:1.5;">
            <strong>This is an independent analytical prototype created solely for technical demonstration, research, and portfolio evaluation.</strong> It does <strong>not</strong> claim to be an official Government of Pakistan, Green Climate Fund (GCF), or international climate-finance assessment, and does not imply institutional endorsement.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="about-card">
        <h3 style="margin-top:0; font-size:1.15rem; color:#0F172A;">Technical Stack</h3>
        <ul style="font-size:0.85rem; color:#334155; padding-left:1.2rem; line-height:1.6;">
            <li><strong>Core Language:</strong> Python 3.14</li>
            <li><strong>Application Framework:</strong> Streamlit</li>
            <li><strong>Data Engineering:</strong> Pandas, NumPy</li>
            <li><strong>Spatial Analysis:</strong> Shapely, GeoJSON</li>
            <li><strong>Interactive GIS:</strong> Plotly Express (<code>px.choropleth_map</code>)</li>
            <li><strong>Administrative Standard:</strong> UN OCHA COD-AB Pakistan (Sept 2022)</li>
            <li><strong>Authoritative Data:</strong> PBS, NDMA, PMD, UNDP, World Bank CCKP</li>
        </ul>
        <hr style="border:none; border-top:1px solid #E2E8F0; margin:0.75rem 0;">
        <div style="font-size:0.78rem; color:#64748B; line-height:1.45;">
            <strong>Engineering Standards:</strong> Zero fabricated data, transparent min-max normalization, automated geographic name harmonization, and 95% geometry optimization for instant web rendering.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### Multi-Module Architecture & Programmatic Roadmap")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown("""
    <div class="module-card active-module">
        <span class="module-status status-active">Module 1 (Active)</span>
        <h4 style="font-size:0.95rem; font-weight:700; color:#0F172A; margin:0.3rem 0;">Pakistan Climate & Vulnerability Explorer</h4>
        <ul style="font-size:0.8rem; color:#475569; padding-left:1rem; line-height:1.45; margin-top:0.5rem;">
            <li>160-district spatial mapping</li>
            <li>Multi-hazard exposure proxies</li>
            <li>Socioeconomic sensitivity metrics</li>
            <li>Transparent composite scoring</li>
            <li>Analytical quadrant positioning</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="module-card planned-module">
        <span class="module-status status-planned">Module 2 (Planned)</span>
        <h4 style="font-size:0.95rem; font-weight:700; color:#0F172A; margin:0.3rem 0;">Climate Project Opportunity Screening</h4>
        <ul style="font-size:0.8rem; color:#475569; padding-left:1rem; line-height:1.45; margin-top:0.5rem;">
            <li>Sectoral vulnerability matching</li>
            <li>Water & irrigation resilience</li>
            <li>Agrarian adaptation interventions</li>
            <li>Community priority alignment</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="module-card planned-module">
        <span class="module-status status-planned">Module 3 (Planned)</span>
        <h4 style="font-size:0.95rem; font-weight:700; color:#0F172A; margin:0.3rem 0;">Safeguards & Risk Screening</h4>
        <ul style="font-size:0.8rem; color:#475569; padding-left:1rem; line-height:1.45; margin-top:0.5rem;">
            <li>GCF Environmental & Social Safeguards</li>
            <li>Gender action & social inclusion</li>
            <li>Biodiversity & ecological constraints</li>
            <li>Grievance & accountability screening</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown("""
    <div class="module-card planned-module">
        <span class="module-status status-planned">Module 4 (Planned)</span>
        <h4 style="font-size:0.95rem; font-weight:700; color:#0F172A; margin:0.3rem 0;">Climate-Finance Pipeline Structuring</h4>
        <ul style="font-size:0.8rem; color:#475569; padding-left:1rem; line-height:1.45; margin-top:0.5rem;">
            <li>GCF concept note outline generation</li>
            <li>Empirical climate rationale synthesis</li>
            <li>Theory of Change (ToC) framework</li>
            <li>Indicative budget & co-financing matrices</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
