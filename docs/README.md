# Exploration Results: Patent Cooperation Network

This folder contains the results of the research question-oriented exploration of the patent cooperation data (2010-2018).

**Generated on:** 2026-01-12
**Script:** `scripts/explore_research_questions.py`
**Data basis:** Synthetic dataset with 137,990 collaborations

---

## Directory Structure

```
docs/
├── README.md                          (this file - overview)
├── data/                              (Aggregated network data for frontend)
│   └── country_network.json           (7.2 MB, complete country network data + metrics, 5,751 edges)
└── exploration/                       (Exploration results)
    ├── DATA_DICTIONARY.md             (Complete documentation of all files)
    ├── macro/                         (Macro level: Country analyses)
    │   ├── country_rankings.csv       (110 countries by weight)
    │   └── country_pairs_top20.csv    (Strongest bilateral relationships)
    ├── micro/                         (Micro level: Firm analyses)
    │   ├── firm_bridge_candidates.csv (267k firms by bridge potential)
    │   └── firm_rankings.csv          (Firms by collaborations)
    ├── temporal/                      (Time series 2010-2018)
    │   ├── temporal_overview.csv      (Annual network statistics)
    │   └── temporal_top_countries.csv (Top-5 countries per year)
    └── structure/                     (Network structure properties)
        ├── network_preview.csv        (Size, density per year)
        └── weight_distribution.csv    (Quantiles of weights)
```

**For detailed information:** See [exploration/DATA_DICTIONARY.md](exploration/DATA_DICTIONARY.md)

---

## File Overview

### Macro Level (Countries)

**`country_rankings.csv`**
Ranking of all 110 countries by total weight of collaborations.

- **Top-3 Countries:** Taiwan (TW), Poland (PL), Ukraine (UA)
- **Variables:** country, total_weight, num_edges, unique_partners

**`country_pairs_top20.csv`**
The 20 strongest bilateral country relationships.

- **Strongest relationship:** Costa Rica - Curacao (CR-CW, weight: 228)
- **Variables:** country_a, country_b, total_weight, num_edges

### Micro Level (Firms)

**`firm_bridge_candidates.csv`**
All 267,068 firms sorted by number of unique partner countries (bridge potential).

- **Top bridge:** CH257552054L (4 partner countries)
- **Average:** 1.03 partner countries per firm
- **Variables:** firm_id, home_country, num_partner_countries

**`firm_rankings.csv`**
Firm rankings by total number of collaborations.

- **Variables:** firm_id, home_country, total_weight, num_edges

### Temporal Analyses

**`temporal_overview.csv`**
Annual network statistics (2010-2018).

- **Firm trend:** 30,246 (2010) → 30,492 (2018)
- **Edge trend:** 15,173 → 15,304
- **Variables:** year, num_edges, unique_firms_approx, unique_countries_approx, total_weight, mean_weight, median_weight

**`temporal_top_countries.csv`**
Top-5 countries per year by total weight.

- Shows rise/fall of individual countries over time
- **Variables:** year, rank, country, total_weight

### Network Structure

**`network_preview.csv`**
Structural properties per year at firm and country level.

- **Firm network density:** ~0.000033 (very sparse)
- **Country network density:** ~0.873 (very dense)
- **Variables:** year, firms_nodes, firms_edges, firms_density, countries_nodes, countries_edges, countries_density

**`weight_distribution.csv`**
Quantiles of weight distribution.

- **Median:** 4
- **95% quantile:** 7
- **Distribution:** Right-skewed
- **Variables:** quantile, weight

---

## Key Findings

### Macro Level: Countries

- **110 unique countries** identified in the network
- **Top-3 countries** by total weight: Taiwan (TW), Poland (PL), Ukraine (UA)
- **Strongest bilateral relationship:** Costa Rica - Curacao (CR-CW)
- **International dominance:** >99% of all collaborations are cross-border (consistent across all years)
- **High density:** Country network has density ~0.87 → almost fully connected

### Micro Level: Firms

- **267,068 unique firms** identified
- **Bridge candidates:** Top firm collaborates with 4 different countries
- **Average:** 1.03 partner countries per firm → most firms collaborate with only one country
- **Degree distribution:** Median=1, 99% quantile=2 → very few highly connected firms
- **Firm network very sparse:** Density ~0.000033 (typical for large networks)

### Temporal Evolution

- **Time period:** 2010-2018
- **Slight growth:** Firms +0.8%, edges +0.9%
- **Stable structure:** Number of countries constant at 110, weight distribution stable
- **Top countries vary** between years (no dominant actor over entire period)

### Network Structure

- **Weights right-skewed:** Median=4, but 95% quantile=7, Max=14
- **Log transformation useful** for visualizations (reduces skewness from σ=1.71 to σ=0.36)
- **Two very different network levels:**
  - Country level: Small (110 nodes), dense (87%), easily manageable
  - Firm level: Large (267k nodes), sparse (0.003%), computationally intensive

---

## Methodological Recommendations

### 1. Weight Transformation

**Problem:** Right-skewed distribution (standard deviation 1.71)

**Recommendation:**
- For visualizations: Use `log(weight+1)` (reduces σ to 0.36)
- For metrics: Weighted variants where appropriate, but raw weights for interpretability

### 2. Tool Selection

**Country level (~110 nodes):**
- **NetworkX** sufficient and well-performing
- All metrics (Centrality, Communities) computable without performance issues

**Firm level (~267k nodes):**
- **NetworkX** works but slow for complex metrics
- **igraph** worth considering for faster computations
- **Alternative:** Top-N subgraph analysis instead of full network

### 3. Temporal Analysis

**Recommendation:** Use both approaches in parallel

- **Annual snapshots:** Show dynamics and trends (2010 vs. 2018)
- **Cumulative network:** Shows overall structure and persistent patterns
- **Comparison periods:** 2010-2014 vs. 2015-2018

### 4. Research Question Prioritization

All three main questions have good data basis:

1. **Macro centrality (Countries):** ✅ High priority
   - Clear top countries identified
   - Dense network structure → good community structure expected

2. **Bridge firms (Micro):** ✅ Good basis
   - Clear candidates identified
   - Few highly connected firms → interesting analysis possible

3. **Temporal evolution:** ✅ Worthwhile
   - Trends visible (though moderate)
   - Top countries vary → dynamics present

---

## Answered Open Questions

From `knowledge/data.md`:

✅ **Weight distribution:** Confirmed as Median=4, Mean=3.91, Range 1-14, right-skewed

✅ **International dominance:** Confirmed across all years (>99% consistent)

✅ **Network sizes:** Documented per year for informed tool decisions

✅ **Duplicates:** None found (as expected from prior verification)

---

## Next Steps

Based on this exploration:

1. **US-02:** Implement country-level aggregation
   - Foundation available: `country_pairs_top20.csv` shows required structure
   - Summation of weights per country pair and year

2. **US-03:** Create network objects (country level)
   - NetworkX sufficient for ~110 nodes
   - Undirected, weighted network

3. **US-04:** Create network objects (firm level)
   - **Decision needed:** Full or top-N subgraph?
   - Consider igraph for performance in full analysis

4. **US-05-07:** Calculate metrics
   - Foundation available, methodological decisions made

---

## Data Quality & Limitations

**Synthetic Dataset:**
- These analyses are based on synthetic data
- Structural properties may differ from the original
- Country codes and weights possibly not representative

**Known Artifacts:**
- Unusually uniform distribution of top countries (all ~11,600-12,000 weight)
- Unusual top countries (TW, PL, UA instead of expected US, CN, DE)
- 99%+ international collaborations could be data collection artifact

**For real analyses:**
- Repeat all steps with real data
- Validate results substantively (are top countries plausible?)
- Perform additional quality checks

---

---

## Interactive Visualization

**Frontend:** [index.html](index.html) (GitHub Pages)

Fully interactive d3.js-based visualization of the patent cooperation network with 3-tab navigation:

**Tab 1: Network Analysis**
- **Force-Directed Network** (VIS-1A): 110 countries, ~5,751 international collaborations
  - Node Size = Weighted Degree, Color = Region (7 geographic regions)
  - Zoom/Pan, Drag, Tooltips with 4 Centrality metrics
  - Ego-Network Highlighting (Click on Node)
  - Edge Weight Filter (threshold 1-14)
- **Country Ranking** (VIS-1B): Top-N Bar Chart (10/20/50/All)
  - 4 Centrality metrics selectable: Degree, Betweenness, Closeness, Eigenvector
  - Region-based color coding
- **Temporal Metrics** (VIS-3A): Small Multiples (2x2 Grid)
  - Density, Modularity, Num Communities, Avg Clustering (2010-2018)
- **Controls**: Time Slider (2010-2018 + cumulative), Centrality Selector, Top-N Selector, Edge Weight Filter

**Tab 2: Temporal Evolution**
- **Slopegraph** (VIS-3B): Rank Changes 2010 → 2018
  - Line Color: Green = Improved, Red = Worsened, Gray = Unchanged
  - Line Thickness proportional to abs(ΔRank)
  - Tooltips with Rank 2010/2018, ΔRank, Centrality 2010/2018, Δ Centrality
  - Centrality Selector (4 metrics), Top-N Selector (10/20/50)
- **Temporal Metrics** (VIS-3A): Small Multiples (reused)

**Tab 3: Bridge Countries**
- **Bridge Evolution** (VIS-4): Slopegraph 2010 → 2018
  - Sorted by Betweenness Centrality (bridge indicator)
  - Line Color: Green = Improved, Red = Worsened, Gray = Unchanged
  - Line Thickness proportional to abs(ΔRank)
  - Tooltips with Rank 2010/2018, ΔRank, Betweenness 2010/2018, Δ Betweenness
  - Top-N Selector (10/20/50)
- **Temporal Metrics** (VIS-3A): Small Multiples (reused)
- **Note:** Firm-level data (US-04) not available, country level as proxy

**Tab 4: Data & Methodology**
- **Data Aggregation Pipeline**: Visual workflow (RDS → Python → JSON)
  - 3-Step Flowchart: Raw Data, Processing, Output
  - Details on input/output formats
- **Network Metrics Definitions**: Formulas + interpretations
  - Degree Centrality: Number of direct connections
  - Betweenness Centrality: Bridge positions
  - Closeness Centrality: Average distance
  - Eigenvector Centrality: Connections to important nodes
- **Data Quality Warnings**: Transparent limitations
  - ⚠️ Synthetic Data Notice (placeholder data)
  - 🔴 Network Density 95.9% (unrealistically high)
  - 🔴 Modularity 0.010 (community detection failed)
  - ℹ️ Temporal Snapshots (2010-2018, 9 years annual)
- **Documentation Embed**: Collapsible Markdown viewer
  - 📄 data.md (Data Structure & Variables)
  - 📄 research.md (Research Questions & Context)
  - 📄 requirements.md (User Stories & Requirements)
  - Lazy loading via fetch(), basic Markdown→HTML conversion

**Technology:**
- d3.js v7 (Force Simulation, Data Join, Scales, Zoom, Slopegraph)
- CSS Grid + Flexbox (70/30 Layout), Tab Navigation (CSS-only)
- Vanilla JavaScript (ES6+), Lazy Initialization

**Data Source:**
- `data/country_network.json` (7.2 MB, 9 years + cumulative)
- Complete network metrics (Centrality, Communities, Global Metrics)

**Region-based Color Coding:**
- Europe (Blue), Asia (Green), North America (Red), South/Central America (Purple)
- Africa (Orange), Oceania (Turquoise), Middle East (Brown)
- Replaces community-based colors (Modularity 0.010 statistically meaningless)

**Code Statistics (after Session 10 Refactoring):**
- docs/index.html: 294 lines
- docs/styles.css: 453 lines
- docs/app.js: 1081 lines (-204 / -15.9% through code deduplication)

**⚠️ Note:** The visualization is based on synthetic data with known artifacts (see below). Structural properties (high density, low modularity) are not representative of real patent networks.

---

## Contact & Documentation

**Project documentation:** `knowledge/` folder
- `data.md` - Data structure and properties
- `research.md` - Research questions and methodology
- `requirements.md` - User stories and technology stack
- `journal.md` - Process documentation and learnings
- `design.md` - InfoVis design specification

**Scripts:**
- `scripts/explore_research_questions.py` - Initial exploration
- `scripts/aggregate_country_network.py` - Country aggregation + network metrics

**Methodology:** Promptotyping (see `CLAUDE.md`)
