# design.md

## Übersicht

Forschungsgetriebene Entwicklung der Visualisierungen für das Patent-Kooperationsnetzwerk. Visualisierungen dienen der Beantwortung spezifischer Forschungsfragen, nicht ästhetischen Präferenzen.

**Status:** Draft – Design Sprint Phase 1 (Task Analysis)

## Design-Prinzipien

| Prinzip | Grundlage | Implikation |
|---------|-----------|-------------|
| Research-Driven | Forschungsfragen aus research.md | Jede Visualisierung adressiert explizit eine Forschungsfrage |
| Task-Oriented | Brehmer & Munzner 2013 | Why → What → How Dekomposition |
| Perception-Based | Cleveland & McGill 1984 | Position > Length > Area > Color |
| Scalable | Munzner Framework | Pre-calculated metrics, Progressive Disclosure, Filtering |
| Consistent | Cross-View Coherence | Knotengröße = Weighted Degree, Farbe = Community, durchgängig |

## Task-Analyse

### Forschungsfrage 1: Makro-Zentralität & Communities

> Welche Länder sind zentrale Akteure? Lassen sich regionale Kooperationscluster identifizieren?

| Why | What | How |
|-----|------|-----|
| Discover central actors | Countries, Degree Centrality | Node size = Weighted Degree, Force-directed layout |
| Find regional clusters | Communities | Node color = Community ID |
| Rank countries | Degree Centrality | Sorted bar chart (Position on common scale) |

→ **VIS-1A** (Network Overview) + **VIS-1B** (Centrality Ranking)

### Forschungsfrage 2: Bridge-Firmen (Mikroebene)

> Welche Firmen fungieren als Brücken zwischen Ländern? Multinationale vs. Nischenfirmen?

| Why | What | How |
|-----|------|-----|
| Find bridge firms | Firms, Num Partner Countries | Sorted bar chart, Top-N filtering |
| Compare firm types | Degree distribution | Histogram by firm type |
| Explore connections | Firm → Countries | Bipartite graph (Top-50 bridges) |

→ **VIS-2A** (Bridge Firm Ranking) + **VIS-2B** (Firm-Country Bipartite)

**Status:** ⚠️ Wartet auf US-04 (Firm-Level Data Preparation)

### Forschungsfrage 3: Temporale Entwicklung

> Wie hat sich die Netzwerkstruktur 2010–2018 verändert? Welche Länder haben Zentralität gewonnen/verloren?

| Why | What | How |
|-----|------|-----|
| Track global metrics | Density, Modularity, Clustering over time | Multi-line chart (Small Multiples) |
| Identify winners/losers | Rank changes 2010 → 2018 | Slopegraph |
| Show evolution | Network topology over time | Animated force-directed + Time Slider |

→ **VIS-3A** (Global Metrics Timeline) + **VIS-3B** (Country Centrality Trends) + **VIS-3C** (Animated Network)

## Design-Entscheidung

| Alternative | Beschreibung | Bewertung |
|-------------|--------------|-----------|
| All-in-One Dashboard | Eine große kombinierte Visualisierung | ❌ Cognitive Overload, nicht skalierbar |
| Tab-Based Navigation | Drei separate Tabs für drei Forschungsfragen | ⚠️ Keine Cross-View-Vergleiche |
| **Multiple Coordinated Views** | Hauptviews koordiniert, Brushing/Linking | ✅ Empfohlen |

## Layout-Struktur

```
┌─────────────────────────────────────────────────────────────────┐
│ Header: Titel, Jahr-Selector, Legende                           │
├──────────────────────────────────────┬──────────────────────────┤
│                                      │ VIS-1B: Centrality       │
│     VIS-1A: Network Overview         │ Ranking (Top-20)         │
│     Force-Directed Graph             ├──────────────────────────┤
│     (70% width)                      │ VIS-3A: Temporal         │
│                                      │ Metrics (30% width)      │
├──────────────────────────────────────┴──────────────────────────┤
│ Time Slider: [2010 ────●─────── 2018]  [Play] [Reset]          │
└─────────────────────────────────────────────────────────────────┘
Modal (on-demand): VIS-2A + VIS-2B (Bridge-Firmen)
```

**Responsive Breakpoints:**
- Desktop (>1200px): Layout wie oben
- Tablet (768–1200px): Side Panels stacken vertikal
- Mobile (<768px): Tab-based Fallback, nur statische Charts

## Visual Encodings

### VIS-1A: Network Overview

| Channel | Variable | Scale | Begründung |
|---------|----------|-------|------------|
| Node Position | Force-Directed | – | Reveals community structure |
| Node Size | Weighted Degree | log(degree) → radius [5–30px] | Vermeidet Outlier-Dominanz |
| Node Color | Community ID | d3.schemeCategory10 | Kategorisch, 5–7 Communities |
| Node Label | Country ISO-2 | Text (on hover/zoom) | Reduziert Clutter |
| Edge Width | Weight | sqrt(weight) → [0.5–5px] | Balanciert Extremwerte |
| Edge Opacity | Weight | weight/max → [0.2–0.8] | Verstärkt Importance |

**Force-Directed Parameter:** link distance 50, charge strength -200, collision radius = nodeScale + 2

### VIS-1B: Centrality Ranking

| Channel | Variable | Scale |
|---------|----------|-------|
| Bar Position X | Degree Centrality | Linear [0, max] |
| Bar Position Y | Country (sorted) | Ordinal by centrality |
| Bar Color | Community ID | Wie VIS-1A |

Default: Top-20, Dropdown für Top-N [10/20/50/All]

### VIS-3A: Temporal Metrics

| Channel | Variable | Scale |
|---------|----------|-------|
| Line Position X | Year | Linear [2010–2018] |
| Line Position Y | Metric Value | Linear (per metric) |
| Line Color | Metric Type | Qualitative (4 Farben) |

**Metriken:** Density, Modularity, Num Communities, Avg Clustering
**Layout:** Small Multiples (4 Mini-Charts) bevorzugt gegenüber Dual-Axis

### VIS-3B: Country Centrality Trends (Slopegraph)

| Channel | Variable |
|---------|----------|
| Left Y-Position | Rank 2010 |
| Right Y-Position | Rank 2018 |
| Line Color | Country |
| Line Thickness | abs(Rank Change) |

## Interaktionsdesign

Folgt Shneiderman's Mantra: Overview First → Zoom and Filter → Details on Demand

### Overview First (Initial State)

- VIS-1A: Full network, cumulative view (2010–2018)
- VIS-1B: Top-20 countries by cumulative centrality
- VIS-3A: Alle Metriken, alle Jahre
- Title: "Patent Cooperation Network (2010–2018) – 110 Countries, 5,829 Cooperations"

### Zoom and Filter

| Control | Affects | Default |
|---------|---------|---------|
| Time Slider (2010–2018 + Cumulative) | VIS-1A, VIS-1B, VIS-3A | Cumulative |
| Edge Weight Slider [1–14] | VIS-1A | 1 (alle Edges) |
| Top-N Dropdown [10/20/50/All] | VIS-1B | 20 |
| Play Button | Animiert durch Jahre (500ms/Jahr) | – |

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

## Technologie-Stack

| Komponente | Technologie |
|------------|-------------|
| Visualisierung | d3.js v7 |
| Layout | CSS Grid + Flexbox |
| Tooltips | d3-tip |
| Datenformat | JSON (pre-calculated, 7.1 MB) |

**Performance-Ziele:** Initial Load <2s, Force Simulation <3s, Animation 60fps, Tooltip <16ms

## Offene Fragen

| Frage | Status | Empfehlung |
|-------|--------|------------|
| Bridge-Firmen Data (VIS-2) | ✅ Gelöst | VIS-4 mit Länderebene-Proxy implementiert (Betweenness Centrality) |
| Color Palette bei >10 Communities | ✅ Gelöst | Region-basierte Farbpalette (7 Regionen) ersetzt Community-Colors |
| Animation vs. Small Multiples (VIS-3C) | ✅ Gelöst | Small Multiples (VIS-3A) + Slopegraph (VIS-3B) implementiert |
| Responsive Breakpoints | Desktop-first | Mobile zeigt nur VIS-1B + VIS-3A |
| Accessibility | Phase 1 ohne | Später ColorBrewer-Palettes |
| Export-Funktionen | Nice-to-have | SVG-Export für VIS-1A |
| Publikations-Qualität (300 DPI) | Später | Web-first, Print später |

## Nächste Schritte

1. **Phase 1:** HTML-Skeleton mit Grid-Layout, JSON laden
2. **Phase 2:** VIS-1A (Force-Directed, Tooltips, Click-Highlighting)
3. **Phase 3:** VIS-1B + VIS-3A, Koordination zwischen Views
4. **Phase 4:** Time Slider, Play/Pause, Filtering
5. **Phase 5:** VIS-2 (nach US-04)
6. **Phase 6:** Responsive Design, Export, Performance, A11y

## Design Validation

| Kriterium | Check |
|-----------|-------|
| Research-Driven | ✅ Alle 3 Forschungsfragen adressiert |
| Task-Oriented | ✅ Brehmer & Munzner Tabellen dokumentiert |
| Perception-Based | ✅ Position > Length > Color |
| Scalable | ✅ 110 Nodes + Filtering |
| Consistent | ✅ Color = Community, Size = Degree durchgängig |
| Shneiderman's Mantra | ✅ Overview → Filter → Details implementiert |