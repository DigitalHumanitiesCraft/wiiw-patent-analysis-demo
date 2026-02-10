# Patent Co-Ownership Network Analysis

Network analysis of international patent collaborations between firms (2010-2018).

## Quick Start

```bash
# Installation
pip install pyreadr pandas networkx

# Explore data
python scripts/explore_rds.py

# Verify data quality
python scripts/verify_data.py
```

## Project Structure

```
data/         RDS data (local, .gitignore, synthetic dataset for development)
scripts/      Python analysis scripts
knowledge/    Promptotyping documentation
docs/         GitHub Pages output (visualizations, metrics, HTML)
```

**Workflow:** Local Python processing (`data/` → `scripts/` → `docs/`) → GitHub Pages publication

## Data

**Dataset:** `data/db_networkCoPat_fake.rds`
- 137,990 patent collaborations
- ~134,000 unique firms
- 96 countries
- Time period: 2010-2018
- Undirected, weighted network

Details: [knowledge/data.md](knowledge/data.md)

## Research Questions

**Macro level:** Which countries are central actors? Are there regional clusters?

**Micro level:** Which firms act as bridges between countries?

**Temporal:** How does the network structure change over time?

Details: [knowledge/research.md](knowledge/research.md)

## Methodology

This project follows the **Promptotyping method** for LLM-assisted research.

Core principle: Documentation is the source of truth, code is a reusable artifact.

Details: [knowledge/CLAUDE.md](knowledge/CLAUDE.md)

## Documentation

| Document | Content |
|----------|---------|
| [knowledge/data.md](knowledge/data.md) | Data structure, variables, quality |
| [knowledge/research.md](knowledge/research.md) | Research questions, metrics, Python tooling |
| [knowledge/requirements.md](knowledge/requirements.md) | User stories, acceptance criteria, tech stack |
| [knowledge/journal.md](knowledge/journal.md) | Development process, decisions, learnings |
| [scripts/README.md](scripts/README.md) | Script documentation |

## Workflow

1. **Preparation:** Read `knowledge/` documents
2. **Implementation:** Develop scripts based on documentation
3. **Validation:** Verify results
4. **Documentation:** Update `journal.md` with new insights

## Technology Stack

**Python 3.11+**

**Data processing:** pandas, pyreadr

**Network analysis:** NetworkX (standard), igraph (optional for >100k nodes)

**Community detection:** python-louvain, leidenalg (optional)

**Visualization:** Matplotlib, Plotly, PyVis

**Publication:** GitHub Pages (static HTML, interactive plots)

## Notes

This is a **synthetic dataset**.
