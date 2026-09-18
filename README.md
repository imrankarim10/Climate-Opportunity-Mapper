# Pakistan Climate Opportunity Mapper

**Interactive Spatial Decision Support for Climate Resilience & Vulnerability Screening in Pakistan**

---

## Overview
The **Pakistan Climate Opportunity Mapper** is a modular, Python-powered geospatial application designed to support early-stage climate-risk screening, project identification, and vulnerability analysis across Pakistan.

Built specifically to demonstrate how **environmental data, Python, GIS, and climate-risk analytics** can assist rural development organizations—such as the **National Rural Support Programme (Climate Analytics)**—the tool synthesizes climate hazard exposure and socioeconomic vulnerability indicators across **all 160 administrative districts** of Pakistan.

> [!IMPORTANT]
> **Prototype Disclaimer:** This application is an independent analytical prototype created for technical demonstration and portfolio evaluation. It does **not** claim to be an official Green Climate Fund (GCF), Government of Pakistan, or climate-finance assessment, nor does it imply institutional endorsement.

---

## Why This Project Exists
Climate-finance entities (such as GCF Direct Access Entities) require robust, transparent, and reproducible empirical evidence to justify climate rationale in project concept notes. Identifying where climate hazards intersect with high socioeconomic deprivation is the first step in evidence-based programming.

This project addresses this need by answering:
> *"Which areas of Pakistan may warrant further investigation because of a combination of climate hazards and socioeconomic vulnerability?"*

---

## Module 1: Pakistan Climate & Vulnerability Explorer
Module 1 serves as the foundational spatial analytical layer. It allows practitioners, environmental scientists, and project developers to:
1. **Explore Pakistan via an Interactive Map:** Switch between 8 thematic layers rendered across 160 district polygons.
2. **Filter Dynamically by Geography:** Seamlessly zoom and filter by province/territory and individual districts.
3. **Analyze Multi-Hazard Profiles:** Inspect Flood Exposure, Drought / Water Stress, Extreme Heat, and Rainfall Variability proxies.
4. **Evaluate Socioeconomic Sensitivity:** Examine Population Density, Multidimensional Poverty Headcount, and Rural/Agrarian Dependence.
5. **Inspect Composite Scores:** Understand the **Preliminary Vulnerability Index (PVI)** and its constituent sub-scores.
6. **Benchmark Local Conditions:** Compare a district's indicators against provincial and national averages using grouped bar charts.
7. **Evaluate Analytical Positioning:** Examine the **Climate Hazard vs. Socioeconomic Vulnerability** scatter plot with quadrant thresholds.
8. **Verify Data Provenance:** Review source datasets, years, resolutions, and processing methodologies directly inside the application.
9. **Export Profiles:** Download district profiles or full national datasets as CSV and JSON with a single click.

---

## Technology Stack
* **Core Language:** Python 3.14
* **Web Dashboard:** Streamlit 1.62+
* **Data Processing:** Pandas, NumPy
* **GIS & Spatial Geometry:** Shapely, GeoJSON
* **Interactive Mapping & Charts:** Plotly Express (`px.choropleth_map`) & Plotly Graph Objects
* **Spatial Reference Dataset:** UN OCHA COD-AB Pakistan (Sept 2022)

---

## Scoring & Normalization Methodology

### 1. Transparent Min-Max Normalization
All indicators are normalized to a common 0–100 scale:
$$\text{Score}_{\text{norm}} = \frac{x - x_{\min}}{x_{\max} - x_{\min}} \times 100$$
Where higher values uniformly denote higher hazard exposure or higher socioeconomic vulnerability.

### 2. Composite Formulation
The **Preliminary Vulnerability Index (PVI)** is a transparent composite:
$$PVI = (W_{\text{hazard}} \times \text{Climate Hazard Score}) + (W_{\text{socio}} \times \text{Socioeconomic Vulnerability Score})$$
* Default category weights: **50% Climate Hazard / 50% Socioeconomic Vulnerability** (customizable via the sidebar sensitivity slider).
* Equal indicator weights within each thematic sub-index.

### 3. Data Quality Guardrail
To avoid false precision, if a district has fewer than **60%** of required indicators available, composite calculation is suppressed with the message: *"Insufficient data for composite score"*.

---

## Data Sources Summary
Every indicator is anchored in authoritative, public sources:

| Indicator | Proxy Type | Source Agency | Vintage |
| :--- | :--- | :--- | :--- |
| **Flood Exposure Proxy** | Hazard Exposure | NDMA & PDNA 2022 Floods Report | 2022 |
| **Drought & Water Stress Proxy** | Hazard Exposure | PMD National Drought Monitoring Centre & WRI | 2021–2023 |
| **Extreme Heat Indicator** | Hazard Exposure | PMD 30-Year Climatology & World Bank CCKP | 1991–2020 |
| **Rainfall Variability Proxy** | Hazard Exposure | PMD Climatology & CHIRPS / World Bank | 1991–2020 |
| **Population Density** | Socioeconomic | Pakistan Bureau of Statistics (PBS) Census | 2017 / 2023 |
| **Multidimensional Poverty** | Socioeconomic | Planning Commission of Pakistan, UNDP & OPHI | 2019–2020 |
| **Rural / Agri Dependence** | Socioeconomic | Pakistan Bureau of Statistics (PBS) | 2017 / 2021 |
| **Administrative Boundaries** | Spatial GIS | UN OCHA COD-AB Pakistan (160 Districts) | Sept 2022 |

*Full data dictionary and limitations are documented in [`data/README.md`](data/README.md).*

---

## Quickstart & Installation

### 1. Clone or Open Workspace
```bash
cd Climate Analytics
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Automated Tests
```bash
python tests.py
```

### 4. Launch Application
```bash
streamlit run app.py
```
The application will automatically open in your default browser at `http://localhost:8501`.

---

## Project Structure
```text
pakistan-climate-opportunity-mapper/
├── app.py                         # Main Streamlit dashboard
├── requirements.txt               # Dependencies
├── README.md                      # Technical and project overview
├── .gitignore                     # Git ignore rules
├── tests.py                       # Automated test suite
│
├── config/
│   ├── __init__.py
│   └── settings.py                # Configuration constants, weights, thresholds, metadata
│
├── data/
│   ├── raw/
│   │   ├── pak_admin2.geojson     # UN OCHA Pakistan district boundaries
│   │   ├── districts_master_list.csv
│   │   └── district_indicators_raw.csv
│   ├── processed/
│   │   ├── pak_admin2_simplified.geojson # Optimized polygon layer (0.54 MB)
│   │   └── district_climate_vulnerability.csv # Cleaned master analytical dataset
│   └── README.md                  # Comprehensive data dictionary
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py             # Caching, queries, export formatting
│   ├── preprocessing.py          # Data ingestion, name harmonization, validation
│   ├── scoring.py                 # Normalization and composite aggregation
│   ├── map_utils.py               # Interactive Plotly choropleth mapping
│   └── charts.py                  # Benchmark bar charts and analytical scatter plot
│
├── pages/
│   ├── 2_Methodology.py           # Deep dive into analytical methodology & equations
│   └── 3_About.py                 # Project context, Climate Analytics relevance, disclaimers, roadmap
│
└── outputs/                       # Export folder for generated CSV and JSON profiles
```

---

## Known Limitations & Boundary Governance
1. **Relative Screening Tool:** The index compares districts within Pakistan. A score of 75/100 denotes upper quartile relative exposure within Pakistan; it is **not** a calibrated probability of disaster.
2. **Boundary Vintage:** Boundaries follow UN OCHA COD-AB (Sept 2022) with 160 districts. Subsequent sub-district tehsil upgrades announced by provincial governments are not yet integrated into the international COD-AB standard.
3. **Microclimates:** In high-altitude northern basins (e.g. Gilgit-Baltistan and Chitral), extreme elevation differentials create steep localized microclimates that regional station averages smooth out.

---

## Future Roadmap (Modules 2, 3, and 4)
The application architecture is modularized so subsequent modules can be added seamlessly:
* **Module 2 — Climate Project Opportunity Screening:** Matching screened high-vulnerability districts with sector-specific interventions (e.g., solar tube-wells, spate irrigation, drought-tolerant seeds, flood protection).
* **Module 3 — Environmental & Social Safeguards (ESS):** Automated screening against GCF/IFC Performance Standards, indigenous communities, gender dynamics, and biodiversity risks.
* **Module 4 — Climate-Finance Concept Note Generator:** Synthesizing the evidence base into structured project concept note outlines aligned with GCF / Adaptation Fund investment criteria.
