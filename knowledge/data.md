# data.md

## File

**Path:** `data/db_networkCoPat_fake.rds`
**Format:** RDS (R Data Serialization)
**Size:** ~2.8 MB
**Rows:** 137,990
**Time Period:** 2010–2018

This is a synthetic dataset for cloud-based development. Real data remains local and is never uploaded to cloud environments.

## Structure

Edge list of patent cooperations between firms.

| Variable | Type | Description |
|----------|------|-------------|
| `year_application` | integer | Year of patent application |
| `owner1` | character | Firm ID (cooperation partner 1) |
| `country_1` | character | ISO2 country code of owner1 |
| `owner2` | character | Firm ID (cooperation partner 2) |
| `country_2` | character | ISO2 country code of owner2 |
| `weight` | integer | Number of collaborations between firms in this year |

Note: Python (pyreadr) reads integer columns partially as float64. The source definition in R is integer.

## Network Properties

**Nodes:** ~134,000 unique firms (owner IDs)
**Edges:** 137,990 connections
**Type:** Undirected, weighted
**Self-connections:** None (owner1 != owner2 in all rows)
**Duplicates:** None

## Country Distribution

**Countries (owner1):** 96
**Countries (owner2):** 92
**Cross-border:** 99.15% (136,823 edges)
**Within one country:** 0.85% (1,167 edges)

## Weighting

**Range:** 1–14
**Median:** 4
**Mean:** 3.91
**Distribution:** Right-skewed, concentration at 2–5

## Aggregation Levels

The data can be analyzed at two levels.

**Firm level (disaggregated):** Network between individual firms. ~134,000 nodes.

**Country level (aggregated):** Summation of weights per country pair and year. ~96 nodes.

## Reading the Data

R:
```r
data <- readRDS("data/db_networkCoPat_fake.rds")
```

Python:
```python
import pyreadr
result = pyreadr.read_r("data/db_networkCoPat_fake.rds")
df = result[None]
```

## Output Data (JSON)

**Path:** `docs/data/country_network.json`
**Format:** JSON (for d3.js visualization)
**Size:** 7.1 MB
**Generation:** Python script `scripts/aggregation.py` (RDS → JSON)

### Structure

The JSON contains three main sections:

**1. metadata** - Project information
```json
{
  "years": [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
  "num_years": 9,
  "num_countries": 110,
  "centrality_metrics": ["degree_centrality", "betweenness_centrality",
                         "closeness_centrality", "eigenvector_centrality"]
}
```

**2. cumulative** - Aggregated network across all years
```json
{
  "nodes": [
    {
      "id": "US",
      "degree_centrality": 0.963,
      "betweenness_centrality": 0.012,
      "closeness_centrality": 0.015,
      "eigenvector_centrality": 0.089,
      "weighted_degree": 5234,
      "community": 0
    },
    ...
  ],
  "edges": [
    {
      "source": "US",
      "target": "CN",
      "weight": 523
    },
    ...
  ],
  "metrics": {
    "density": 0.959,
    "modularity": 0.010,
    "num_communities": 3,
    "avg_clustering": 0.961
  }
}
```

**3. temporal** - Annual snapshots (9 years)
```json
{
  "2010": { /* same structure as cumulative */ },
  "2011": { /* ... */ },
  ...
  "2018": { /* ... */ }
}
```

### Network Metrics (Node Level)

| Metric | Description | Range | Interpretation |
|--------|-------------|-------|----------------|
| `degree_centrality` | Normalized number of direct connections | [0, 1] | How many countries cooperate directly? |
| `betweenness_centrality` | Proportion of shortest paths through node | [0, 1] | Bridge position between clusters |
| `closeness_centrality` | Average distance to all nodes | [0, 1] | How fast to reach other countries? |
| `eigenvector_centrality` | Centrality of neighbors | [0, 1] | Connections to important countries |
| `weighted_degree` | Sum of edge weights | Integer | Total collaboration intensity |
| `community` | Community ID (Louvain) | Integer | Cluster membership (meaningless at low modularity) |

### Global Metrics (Graph Level)

| Metric | Description | Value (Cumulative) | Interpretation |
|--------|-------------|---------------------|----------------|
| `density` | Proportion of realized edges | 0.959 | Almost fully connected (unrealistic) |
| `modularity` | Community quality | 0.010 | No significant communities |
| `num_communities` | Number of communities (Louvain) | 3 | Statistically meaningless at modularity 0.010 |
| `avg_clustering` | Average clustering coefficient | 0.961 | High local density |

### Data Quality Warnings

**Synthetic Data:** The JSON data is based on `db_networkCoPat_fake.rds` and is not representative of real patent networks.

**Artifacts:**
- Density 95.9%: Unrealistically high (real networks have density <10%)
- Modularity 0.010: No recognizable communities (statistically insignificant)
- Community-based color coding: Replaced by region-based colors in frontend

## Open Questions

**Data Model and Semantics**
- What defines a cooperation? Co-application, co-ownership, citation, technology transfer?
- Is year_application the application or grant year?

**Owner IDs**
- Where does the ID system come from? The prefixes (QA, AT, SG) seem to indicate countries, but country_1/country_2 exist separately.
- Are the IDs persistent across years or can firms have multiple IDs?

**Data Origin**
- What original data source is the basis (EPO, USPTO, PATSTAT)?
- What preprocessing has already been performed?

**Synthetic Dataset**
- How was db_networkCoPat_fake.rds generated from the original data? Anonymization, shuffling, fully generated?
- Are the statistical properties (distributions, network structure) representative of real data?

**Aggregation**
- Is weight already aggregated per firm pair and year, or can duplicates exist?
- How were firms active in multiple countries handled in country-level aggregation?
