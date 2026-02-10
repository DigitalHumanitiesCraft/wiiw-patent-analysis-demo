# design.md

## Overview

Research-driven development of visualizations for the patent cooperation network. Visualizations serve to answer specific research questions, not aesthetic preferences.

**Status:** Draft – Design Sprint Phase 1 (Task Analysis)

## Design Principles

| Principle | Foundation | Implication |
|-----------|------------|-------------|
| Research-Driven | Research questions from research.md | Every visualization explicitly addresses a research question |
| Task-Oriented | Brehmer & Munzner 2013 | Why → What → How decomposition |
| Perception-Based | Cleveland & McGill 1984 | Position > Length > Area > Color |
| Scalable | Munzner Framework | Pre-calculated metrics, Progressive Disclosure, Filtering |
| Consistent | Cross-View Coherence | Node size = Weighted Degree, Color = Community, throughout |

## Task Analysis

### Research Question 1: Macro Centrality & Communities

> Which countries are central actors? Can regional cooperation clusters be identified?

| Why | What | How |
|-----|------|-----|
| Discover central actors | Countries, Degree Centrality | Node size = Weighted Degree, Force-directed layout |
| Find regional clusters | Communities | Node color = Community ID |
| Rank countries | Degree Centrality | Sorted bar chart (Position on common scale) |

→ **VIS-1A** (Network Overview) + **VIS-1B** (Centrality Ranking)

### Research Question 2: Bridge Firms (Micro Level)

> Which firms act as bridges between countries? Multinational vs. niche firms?

| Why | What | How |
|-----|------|-----|
| Find bridge firms | Firms, Num Partner Countries | Sorted bar chart, Top-N filtering |
| Compare firm types | Degree distribution | Histogram by firm type |
| Explore connections | Firm → Countries | Bipartite graph (Top-50 bridges) |

→ **VIS-2A** (Bridge Firm Ranking) + **VIS-2B** (Firm-Country Bipartite)

**Status:** ⚠️ Waiting for US-04 (Firm-Level Data Preparation)

### Research Question 3: Temporal Evolution

> How has the network structure changed 2010–2018? Which countries have gained/lost centrality?

| Why | What | How |
|-----|------|-----|
| Track global metrics | Density, Modularity, Clustering over time | Multi-line chart (Small Multiples) |
| Identify winners/losers | Rank changes 2010 → 2018 | Slopegraph |
| Show evolution | Network topology over time | Animated force-directed + Time Slider |

→ **VIS-3A** (Global Metrics Timeline) + **VIS-3B** (Country Centrality Trends) + **VIS-3C** (Animated Network)

## Design Decision

| Alternative | Description | Evaluation |
|-------------|-------------|------------|
| All-in-One Dashboard | One large combined visualization | ❌ Cognitive Overload, not scalable |
| Tab-Based Navigation | Three separate tabs for three research questions | ⚠️ No cross-view comparisons |
| **Multiple Coordinated Views** | Main views coordinated, Brushing/Linking | ✅ Recommended |

## Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│ Header: Title, Year Selector, Legend                            │
├──────────────────────────────────────┬──────────────────────────┤
│                                      │ VIS-1B: Centrality       │
│     VIS-1A: Network Overview         │ Ranking (Top-20)         │
│     Force-Directed Graph             ├──────────────────────────┤
│     (70% width)                      │ VIS-3A: Temporal         │
│                                      │ Metrics (30% width)      │
├──────────────────────────────────────┴──────────────────────────┤
│ Time Slider: [2010 ────●─────── 2018]  [Play] [Reset]          │
└─────────────────────────────────────────────────────────────────┘
Modal (on-demand): VIS-2A + VIS-2B (Bridge Firms)
```

**Responsive Breakpoints:**
- Desktop (>1200px): Layout as above
- Tablet (768–1200px): Side panels stack vertically
- Mobile (<768px): Tab-based fallback, only static charts

## Visual Encodings

### VIS-1A: Network Overview

| Channel | Variable | Scale | Justification |
|---------|----------|-------|---------------|
| Node Position | Force-Directed | – | Reveals community structure |
| Node Size | Weighted Degree | log(degree) → radius [5–30px] | Avoids outlier dominance |
| Node Color | Community ID | d3.schemeCategory10 | Categorical, 5–7 Communities |
| Node Label | Country ISO-2 | Text (on hover/zoom) | Reduces clutter |
| Edge Width | Weight | sqrt(weight) → [0.5–5px] | Balances extreme values |
| Edge Opacity | Weight | weight/max → [0.2–0.8] | Reinforces importance |

**Force-Directed Parameters:** link distance 50, charge strength -200, collision radius = nodeScale + 2

### VIS-1B: Centrality Ranking

| Channel | Variable | Scale |
|---------|----------|-------|
| Bar Position X | Degree Centrality | Linear [0, max] |
| Bar Position Y | Country (sorted) | Ordinal by centrality |
| Bar Color | Community ID | As VIS-1A |

Default: Top-20, Dropdown for Top-N [10/20/50/All]

### VIS-3A: Temporal Metrics

| Channel | Variable | Scale |
|---------|----------|-------|
| Line Position X | Year | Linear [2010–2018] |
| Line Position Y | Metric Value | Linear (per metric) |
| Line Color | Metric Type | Qualitative (4 colors) |

**Metrics:** Density, Modularity, Num Communities, Avg Clustering
**Layout:** Small Multiples (4 mini-charts) preferred over dual-axis

### VIS-3B: Country Centrality Trends (Slopegraph)

| Channel | Variable |
|---------|----------|
| Left Y-Position | Rank 2010 |
| Right Y-Position | Rank 2018 |
| Line Color | Country |
| Line Thickness | abs(Rank Change) |

## Interaction Design

Follows Shneiderman's Mantra: Overview First → Zoom and Filter → Details on Demand

### Overview First (Initial State)

- VIS-1A: Full network, cumulative view (2010–2018)
- VIS-1B: Top-20 countries by cumulative centrality
- VIS-3A: All metrics, all years
- Title: "Patent Cooperation Network (2010–2018) – 110 Countries, 5,829 Cooperations"

### Zoom and Filter

| Control | Affects | Default |
|---------|---------|---------|
| Time Slider (2010–2018 + Cumulative) | VIS-1A, VIS-1B, VIS-3A | Cumulative |
| Edge Weight Slider [1–14] | VIS-1A | 1 (all edges) |
| Top-N Dropdown [10/20/50/All] | VIS-1B | 20 |
| Play Button | Animates through years (500ms/year) | – |

### Details on Demand

**Hover Tooltip (Schema):**
```
[Entity]: [Name] ([Code])
[Primary Metric]: [Value]
[Secondary Metric]: [Value]
[Context]: [Top Partners / Year / etc.]
```

**Click:** Highlight Ego-Network (1-hop neighbors), Dim rest (opacity 0.2), Scroll linked views
**Double-Click:** Reset all filters and highlights

## Technology Stack

| Component | Technology |
|-----------|------------|
| Visualization | d3.js v7 |
| Layout | CSS Grid + Flexbox |
| Tooltips | d3-tip |
| Data Format | JSON (pre-calculated, 7.1 MB) |

**Performance Goals:** Initial Load <2s, Force Simulation <3s, Animation 60fps, Tooltip <16ms

## Open Questions

| Question | Status | Recommendation |
|----------|--------|----------------|
| Bridge Firms Data (VIS-2) | ✅ Resolved | VIS-4 implemented with country-level proxy (Betweenness Centrality) |
| Color Palette for >10 Communities | ✅ Resolved | Region-based color palette (7 regions) replaces Community Colors |
| Animation vs. Small Multiples (VIS-3C) | ✅ Resolved | Small Multiples (VIS-3A) + Slopegraph (VIS-3B) implemented |
| Responsive Breakpoints | Desktop-first | Mobile shows only VIS-1B + VIS-3A |
| Accessibility | Phase 1 without | Later ColorBrewer palettes |
| Export Functions | Nice-to-have | SVG export for VIS-1A |
| Publication Quality (300 DPI) | Later | Web-first, print later |

## Next Steps

1. **Phase 1:** HTML skeleton with grid layout, load JSON
2. **Phase 2:** VIS-1A (Force-Directed, Tooltips, Click-Highlighting)
3. **Phase 3:** VIS-1B + VIS-3A, coordination between views
4. **Phase 4:** Time Slider, Play/Pause, Filtering
5. **Phase 5:** VIS-2 (after US-04)
6. **Phase 6:** Responsive Design, Export, Performance, A11y

## Design Validation

| Criterion | Check |
|-----------|-------|
| Research-Driven | ✅ All 3 research questions addressed |
| Task-Oriented | ✅ Brehmer & Munzner tables documented |
| Perception-Based | ✅ Position > Length > Color |
| Scalable | ✅ 110 Nodes + Filtering |
| Consistent | ✅ Color = Community, Size = Degree throughout |
| Shneiderman's Mantra | ✅ Overview → Filter → Details implemented |
