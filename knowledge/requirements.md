# requirements.md

## Overview

This document defines the requirements for the network analysis of patent cooperation data. User stories are ordered by priority. Each story contains acceptance criteria and status.

## Technology Stack

**Programming Language:** Python 3.11+

**Core Libraries:**
- pandas, pyreadr (data processing)
- networkx (network analysis, standard)
- python-louvain / leidenalg (community detection)
- matplotlib, plotly, pyvis (visualization)

**Optional for Performance:**
- igraph (Python binding) for >100k nodes
- graph-tool (maximum performance, more complex installation)

## User Stories

### Phase 1: Data Preparation

**US-01: Load and validate data**
As a researcher, I want to load the RDS file and check data quality to ensure the data is suitable for analysis.

Acceptance Criteria:
- Data is available in Python as pandas DataFrame (via pyreadr)
- Column types match the specification in data.md
- No unexpected null values or duplicates
- Exploratory summary documented

Status: Completed (see scripts/explore_rds.py, scripts/verify_data.py)

---

**US-02: Country-level aggregation**
As a researcher, I want to aggregate firm data to country level to analyze macroeconomic cooperation patterns.

Acceptance Criteria:
- New dataset with country_1, country_2, year_application, weight (summed)
- Documentation of aggregation logic
- Validation: Sum of weights is preserved

Status: Completed (see scripts/aggregate_country_network.py, docs/data/country_network.json)

---

### Phase 2: Network Construction

**US-03: Create network objects (country level)**
As a researcher, I want to create network objects from aggregated data to calculate network metrics.

Acceptance Criteria:
- NetworkX Graph object per year and cumulative
- Undirected, weighted network
- Node count matches number of countries (~96)
- Edge weights match aggregated weights

Technology: NetworkX (standard), igraph optional for comparison

Status: Completed (see scripts/aggregate_country_network.py, 9 annual graphs + 1 cumulative)

---

**US-04: Create network objects (firm level)**
As a researcher, I want to create network objects at firm level from original data to conduct disaggregated analyses.

Acceptance Criteria:
- NetworkX Graph object per year and cumulative
- Undirected, weighted network
- Performant for ~134,000 nodes (consider using igraph)
- Alternative: Subgraph analysis (top-N firms by degree)

Technology: NetworkX (if performant enough), otherwise igraph

Performance Warning: NetworkX can be slow with ~134k nodes. Benchmarking required.

Status: Open

---

### Phase 3: Metrics

**US-05: Calculate centrality measures**
As a researcher, I want to calculate centrality measures (degree, betweenness, eigenvector, closeness) to identify central actors in the network.

Acceptance Criteria:
- Metrics for both levels (countries and firms)
- Weighted variants where appropriate
- Export as table (CSV)
- Top-10 ranking per metric

Status: Completed (Country level: All centrality metrics in JSON - Degree, Betweenness, Closeness, Eigenvector, weighted + normalized. Firm level open, see US-04)

---

**US-06: Community detection**
As a researcher, I want to identify communities in the network to recognize cooperation clusters.

Acceptance Criteria:
- Louvain (via python-louvain or networkx.algorithms.community) applied
- Optional: Leiden (via leidenalg) as improvement
- Modularity values documented
- Community assignment as node attribute in DataFrame
- Comparison of results when multiple algorithms used

Technology: python-louvain (primary), leidenalg (optional)

Status: Completed (Louvain for country level in JSON, modularity documented, Leiden optional open)

---

**US-07: Global network properties**
As a researcher, I want to calculate global properties (density, average path length, clustering coefficient, assortativity) to characterize the overall network structure.

Acceptance Criteria:
- Metrics calculated per year
- Temporal evolution as table
- Interpretation in context of patent cooperations

Status: Completed (All metrics in JSON: Density, Clustering, Transitivity, Connectivity, Average Path Length, Assortativity - yearly + cumulative)

---

### Phase 4: Visualization

**US-08: Static network visualization**
As a researcher, I want to visualize the network to make structures and patterns visually recognizable.

Acceptance Criteria:
- Country network as readable graphic
- Node size encodes degree or patent count
- Node color encodes community or region
- Edge thickness encodes weight
- Export as PNG (300 DPI) and PDF (vector)

Technology: d3.js v7 (Force-Directed Layout), CSS Grid, Vanilla JavaScript

Layout: d3.forceSimulation (Force-Directed) for 110 countries

Status: Completed (docs/index.html, docs/app.js, docs/styles.css - Force-Directed Network + Country Ranking Bar Chart, Zoom/Pan, Tooltips, Ego-Network Highlighting)

---

**US-09: Temporal visualization**
As a researcher, I want to visualize the temporal evolution of the network to make changes between 2010 and 2018 visible.

Acceptance Criteria:
- Small multiples (one panel per year) or animation
- Consistent layout across years
- Recognizable trends
- Rank comparisons between years (slopegraph)

Status: Completed (3-tab navigation: Network | Temporal | Bridge Countries. Time Slider coordinates Network + Ranking Views. Temporal Metrics as Small Multiples [2x2 Grid] with 4 metrics. VIS-3B Slopegraph for Rank Changes 2010→2018 with 4 Centrality metrics, Top-N Selector [10/20/50], Tooltips with ΔRank and Δ Centrality, improved Y-Spacing. VIS-4 Bridge Analysis (Betweenness Centrality Bar Chart) implemented. Region-based color coding replaces Community Colors.)

---

**US-10: Method transparency & documentation**
As a researcher, I want to view the data processing pipeline and calculation methods to understand the reproducibility and validity of the analyses.

Acceptance Criteria:
- Visual workflow of data processing (RDS → Python → JSON)
- Definitions of all network metrics with formulas
- Transparent presentation of data quality issues (Synthetic Data Warnings)
- Access to complete project documentation (data.md, research.md, requirements.md)
- Collapsible accordion for Markdown documents (Lazy Loading)

Technology: Vanilla JavaScript (fetch API), Basic Markdown→HTML Parser (Regex-based, no dependencies)

Status: Completed (Tab 4 "Data & Methodology" with 4 sections: Data Pipeline Flowchart, Network Metrics Definitions [4 Centrality formulas], Data Quality Warnings [Density 95.9%, Modularity 0.010, Synthetic Data Notice], Documentation Embed [Accordion UI with knowledge/*.md files]. Basic Markdown Parser supports Headers, Bold, Italic, Code Blocks, Links, Lists.)

---

## Prioritization

| Priority | Stories | Justification |
|----------|---------|---------------|
| High | US-01, US-02, US-03 | Foundation for all further analyses |
| High | US-05, US-08 | Core metrics and basic visualization |
| Medium | US-06, US-07 | In-depth analyses |
| Medium | US-09 | Temporal dimension |
| Lower | US-04 | Firm level is computationally intensive, country level has priority |

## Publication Workflow

**Local Processing:**
- Python scripts process `data/db_networkCoPat_fake.rds` (local, not in Git)
- Calculated metrics, visualizations and results are saved in `docs/`
- `docs/` contains only aggregated results, no raw data

**GitHub Pages:**
- `docs/` folder is published via GitHub Pages
- HTML visualizations (Plotly, PyVis) directly usable in browser
- Static plots (PNG, PDF) for download
- CSV exports with aggregated metrics

**Data Privacy:**
- Only synthetic data in repository
- Real data remains local, never pushed
- `.gitignore` prevents accidental upload of sensitive data

## Open Questions

- Which metrics are most relevant for publication?
- Are there preferences for visualization styles?
- Should the firm level be analyzed completely or only for selected countries/years?
- GitHub Pages design: Minimalist or with framework (e.g., Jupyter Book, Sphinx)?
