# Data Documentation & Provenance Dictionary

## Overview
This directory stores raw and processed datasets utilized by the **Pakistan Climate Opportunity Mapper (Module 1: Pakistan Climate & Vulnerability Explorer)**. All data originates from credible, publicly accessible national and multilateral agencies.

---

## Directory Structure
```text
data/
├── raw/
│   ├── pak_admin2.geojson              # UN OCHA COD-AB Pakistan ADM2 boundaries (160 districts, 9.8 MB)
│   ├── districts_master_list.csv       # Extracted master tabular list of 160 UN OCHA districts with P-codes
│   └── district_indicators_raw.csv     # Assembled raw indicator table prior to normalization
├── processed/
│   ├── pak_admin2_simplified.geojson   # Topology-preserving simplified GeoJSON (0.54 MB) for fast web mapping
│   └── district_climate_vulnerability.csv # Cleaned, normalized master analytical dataset
└── README.md                           # This provenance document
```

---

## Dataset Catalogue & Provenance

### 1. Pakistan Administrative Boundaries (ADM2)
* **Source:** United Nations Office for the Coordination of Humanitarian Affairs (UN OCHA) / Humanitarian Data Exchange (HDX)
* **Dataset Title:** Pakistan - Subnational Administrative Boundaries (Common Operational Datasets - COD-AB)
* **URL:** [https://data.humdata.org/dataset/cod-ab-pak](https://data.humdata.org/dataset/cod-ab-pak)
* **Vintage:** September 9, 2022
* **Resolution:** District level (`ADM2`), 160 units across 7 provinces/regions
* **Variables:** `adm2_pcode` (P-Code ID), `adm2_name` (District Name), `adm1_name` (Province), `area_sqkm`, `center_lat`, `center_lon`
* **Processing:** Simplification via Shapely (`simplify(0.008, preserve_topology=True)`) reducing payload size from 9.8 MB to 0.54 MB while retaining district boundary fidelity.
* **Limitations:** Captures 2022 administrative configuration. Subsequent provincial notifications subdividing individual tehsils are not reflected.

### 2. Flood Exposure Proxy
* **Source:** National Disaster Management Authority (NDMA) & Government of Pakistan / Asian Development Bank / World Bank / UNDP
* **Dataset Title:** Pakistan 2022 Floods: Post-Disaster Needs Assessment (PDNA) & NDMA Sitrep No. 128
* **URL:** [https://www.ndma.gov.pk/](https://www.ndma.gov.pk/)
* **Vintage:** October 2022
* **Resolution:** District level (94 calamity-hit districts disaggregated into severity tiers)
* **Variables:** Calamity status, inundated agricultural area, flood severity index (0–100)
* **Processing:** Calibrated index combining NDMA calamity designation (Severe, Moderate, Low, Non-Calamity) and reported flood inundation extents.
* **Limitations:** Measures the impact of the unprecedented 2022 monsoon flood disaster; does not model theoretical 100-year return period hydraulic flows.

### 3. Drought & Water Stress Proxy
* **Source:** Pakistan Meteorological Department (PMD) & World Resources Institute (WRI) Aqueduct
* **Dataset Title:** PMD National Drought Monitoring Centre (NDMC) Aridity Bulletins & WRI Baseline Water Stress
* **URL:** [https://ndmc.pmd.gov.pk/](https://ndmc.pmd.gov.pk/)
* **Vintage:** 2021–2023
* **Resolution:** District level
* **Variables:** Aridity classification (hyper-arid, arid, semi-arid, sub-humid) and baseline water stress index (0–100)
* **Processing:** Categorical classification combined with water depletion ratios into a continuous 0–100 stress index.
* **Limitations:** Reflects meteorological and hydrological baseline dryness; extensive canal infrastructure in the Indus Basin provides localized buffer capacity.

### 4. Extreme Heat & Temperature Indicator
* **Source:** Pakistan Meteorological Department (PMD) & World Bank Climate Change Knowledge Portal (CCKP)
* **Dataset Title:** Pakistan 30-Year Climatological Normals (1991–2020)
* **URL:** [https://climateknowledgeportal.worldbank.org/country/pakistan](https://climateknowledgeportal.worldbank.org/country/pakistan)
* **Vintage:** 1991–2020 climatology
* **Resolution:** District level
* **Variables:** Mean daily maximum temperature (°C) and incidence of extreme heatwave days (>40°C)
* **Processing:** Spatial aggregation of 30-year station observations across district boundaries.
* **Limitations:** Topographical microclimates in high-altitude northern districts may have localized deviations not captured by district-wide averages.

### 5. Precipitation Variability Proxy
* **Source:** PMD & Climate Hazards Center (CHIRPS) / World Bank CCKP
* **Dataset Title:** Historical Annual Rainfall Series & Monsoon Anomaly Index
* **URL:** [https://pmd.gov.pk/](https://pmd.gov.pk/)
* **Vintage:** 1991–2020
* **Resolution:** District level
* **Variables:** Coefficient of Variation (CV %) of annual rainfall
* **Processing:** $CV = (\\sigma / \\mu) \\times 100$, where $\\sigma$ is standard deviation and $\\mu$ is mean annual precipitation.
* **Limitations:** Captures unpredictability rather than volume; desert districts with negligible precipitation display high percentage variability.

### 6. Population Density Proxy
* **Source:** Pakistan Bureau of Statistics (PBS)
* **Dataset Title:** Digital Census of Pakistan (2017 Final Tables & 2023 Update)
* **URL:** [https://www.pbs.gov.pk/](https://www.pbs.gov.pk/)
* **Vintage:** 2017 / 2023
* **Resolution:** District level
* **Variables:** Total population, area (sq km), population density (persons per sq km)
* **Processing:** Population divided by land area; transformed logarithmically prior to min-max scaling to accommodate extreme density contrasts.
* **Limitations:** Urban centers exhibit high density but also greater emergency services compared to dispersed rural populations.

### 7. Multidimensional Poverty Headcount Proxy
* **Source:** Ministry of Planning, Development and Special Initiatives (PD&SI), UNDP Pakistan, and Oxford Poverty and Human Development Initiative (OPHI)
* **Dataset Title:** Multidimensional Poverty in Pakistan (National MPI Report)
* **URL:** [https://www.undp.org/pakistan/publications/multidimensional-poverty-pakistan](https://www.undp.org/pakistan/publications/multidimensional-poverty-pakistan)
* **Vintage:** 2019–2020 (PSLM survey data)
* **Resolution:** District level
* **Variables:** Headcount Ratio $H$ (%) of population living in acute multidimensional poverty (education, health, living standards)
* **Processing:** Direct integration of official district headcount percentages.
* **Limitations:** Survey-derived sampling at district resolution; newly created districts share the baseline of their parent administrative unit.

### 8. Rural & Agricultural Livelihood Dependence Proxy
* **Source:** Pakistan Bureau of Statistics (PBS)
* **Dataset Title:** Population Census & Labour Force Survey
* **URL:** [https://www.pbs.gov.pk/](https://www.pbs.gov.pk/)
* **Vintage:** 2017 / 2021
* **Resolution:** District level
* **Variables:** Rural population share (%) and agricultural employment dependence
* **Processing:** Percentage of district residents categorized in rural localities coupled with agrarian employment shares.
* **Limitations:** Does not measure rural remittance diversification or non-farm household micro-enterprises.
