# Explorationsergebnisse: Patent-Kooperationsnetzwerk

Dieser Ordner enthält die Ergebnisse der forschungsfragen-orientierten Exploration der Patentkooperationsdaten (2010-2018).

**Generiert am:** 2026-01-12
**Skript:** `scripts/explore_research_questions.py`
**Datenbasis:** Synthetischer Datensatz mit 137,990 Kooperationen

---

## Verzeichnisstruktur

```
docs/
├── README.md                          (diese Datei - Übersicht)
├── data/                              (Aggregierte Netzwerkdaten für Frontend)
│   └── country_network.json           (7.2 MB, vollständige Länder-Netzwerkdaten + Metriken, 5,751 Kanten)
└── exploration/                       (Explorationsergebnisse)
    ├── DATA_DICTIONARY.md             (Vollständige Dokumentation aller Dateien)
    ├── macro/                         (Makroebene: Länderanalysen)
    │   ├── country_rankings.csv       (110 Länder nach Gewicht)
    │   └── country_pairs_top20.csv    (Stärkste bilaterale Beziehungen)
    ├── micro/                         (Mikroebene: Firmenanalysen)
    │   ├── firm_bridge_candidates.csv (267k Firmen nach Bridge-Potenzial)
    │   └── firm_rankings.csv          (Firmen nach Kooperationen)
    ├── temporal/                      (Zeitreihen 2010-2018)
    │   ├── temporal_overview.csv      (Jährliche Netzwerk-Statistiken)
    │   └── temporal_top_countries.csv (Top-5 Länder pro Jahr)
    └── structure/                     (Netzwerkstruktur-Eigenschaften)
        ├── network_preview.csv        (Größe, Dichte pro Jahr)
        └── weight_distribution.csv    (Quantile der Gewichte)
```

**Für detaillierte Informationen:** Siehe [exploration/DATA_DICTIONARY.md](exploration/DATA_DICTIONARY.md)

---

## Übersicht der Dateien

### Makroebene (Länder)

**`country_rankings.csv`**
Ranking aller 110 Länder nach Gesamtgewicht der Kooperationen.

- **Top-3 Länder:** Taiwan (TW), Polen (PL), Ukraine (UA)
- **Variablen:** country, total_weight, num_edges, unique_partners

**`country_pairs_top20.csv`**
Die 20 stärksten bilateralen Länderbeziehungen.

- **Stärkste Beziehung:** Costa Rica - Curacao (CR-CW, Gewicht: 228)
- **Variablen:** country_a, country_b, total_weight, num_edges

### Mikroebene (Firmen)

**`firm_bridge_candidates.csv`**
Alle 267,068 Firmen sortiert nach Anzahl einzigartiger Partnerländer (Bridge-Potenzial).

- **Top-Bridge:** CH257552054L (4 Partnerländer)
- **Durchschnitt:** 1.03 Partnerländer pro Firma
- **Variablen:** firm_id, home_country, num_partner_countries

**`firm_rankings.csv`**
Firmen-Rankings nach Gesamtanzahl Kooperationen.

- **Variablen:** firm_id, home_country, total_weight, num_edges

### Temporale Analysen

**`temporal_overview.csv`**
Jährliche Netzwerk-Statistiken (2010-2018).

- **Trend Firmen:** 30,246 (2010) → 30,492 (2018)
- **Trend Kanten:** 15,173 → 15,304
- **Variablen:** year, num_edges, unique_firms_approx, unique_countries_approx, total_weight, mean_weight, median_weight

**`temporal_top_countries.csv`**
Top-5 Länder pro Jahr nach Gesamtgewicht.

- Zeigt Auf-/Abstiege einzelner Länder über Zeit
- **Variablen:** year, rank, country, total_weight

### Netzwerkstruktur

**`network_preview.csv`**
Strukturelle Eigenschaften pro Jahr auf Firmen- und Länderebene.

- **Firmennetzwerk-Dichte:** ~0.000033 (sehr dünn)
- **Ländernetzwerk-Dichte:** ~0.873 (sehr dicht)
- **Variablen:** year, firms_nodes, firms_edges, firms_density, countries_nodes, countries_edges, countries_density

**`weight_distribution.csv`**
Quantile der Gewichtsverteilung.

- **Median:** 4
- **95%-Quantil:** 7
- **Verteilung:** Rechtsschief
- **Variablen:** quantile, weight

---

## Kernerkenntnisse

### Makroebene: Länder

- **110 unique Länder** im Netzwerk identifiziert
- **Top-3 Länder** nach Gesamtgewicht: Taiwan (TW), Polen (PL), Ukraine (UA)
- **Stärkste bilaterale Beziehung:** Costa Rica - Curacao (CR-CW)
- **Internationale Dominanz:** >99% aller Kooperationen sind grenzüberschreitend (durchgängig über alle Jahre)
- **Hohe Dichte:** Ländernetzwerk hat Dichte ~0.87 → fast vollständig verbunden

### Mikroebene: Firmen

- **267,068 unique Firmen** identifiziert
- **Bridge-Kandidaten:** Top-Firma kooperiert mit 4 verschiedenen Ländern
- **Durchschnitt:** 1.03 Partnerländer pro Firma → die meisten Firmen kooperieren nur mit einem Land
- **Degree-Verteilung:** Median=1, 99%-Quantil=2 → sehr wenige hochvernetzte Firmen
- **Firmennetzwerk sehr dünn:** Dichte ~0.000033 (typisch für große Netzwerke)

### Temporale Entwicklung

- **Zeitraum:** 2010-2018
- **Leichtes Wachstum:** Firmen +0.8%, Kanten +0.9%
- **Stabile Struktur:** Anzahl Länder konstant bei 110, Gewichtsverteilung stabil
- **Top-Länder variieren** zwischen Jahren (kein dominanter Akteur über gesamten Zeitraum)

### Netzwerkstruktur

- **Gewichte rechtsschief verteilt:** Median=4, aber 95%-Quantil=7, Max=14
- **Log-Transformation sinnvoll** für Visualisierungen (reduziert Schiefe von σ=1.71 auf σ=0.36)
- **Zwei sehr unterschiedliche Netzwerk-Ebenen:**
  - Länderebene: Klein (110 Knoten), dicht (87%), gut handhabbar
  - Firmenebene: Groß (267k Knoten), dünn (0.003%), rechenintensiv

---

## Methodische Empfehlungen

### 1. Gewichtstransformation

**Problem:** Rechtsschiefe Verteilung (Standardabweichung 1.71)

**Empfehlung:**
- Für Visualisierungen: `log(weight+1)` verwenden (reduziert σ auf 0.36)
- Für Metriken: Gewichtete Varianten wo sinnvoll, aber raw weights für Interpretierbarkeit

### 2. Tool-Auswahl

**Länderebene (~110 Knoten):**
- **NetworkX** ausreichend und gut performant
- Alle Metriken (Centrality, Communities) ohne Performance-Probleme berechenbar

**Firmenebene (~267k Knoten):**
- **NetworkX** funktioniert, aber langsam bei komplexen Metriken
- **igraph** für schnellere Berechnungen erwägen
- **Alternative:** Top-N-Subgraph-Analyse statt vollständigem Netzwerk

### 3. Temporale Analyse

**Empfehlung:** Beide Ansätze parallel nutzen

- **Jährliche Snapshots:** Zeigen Dynamik und Trends (2010 vs. 2018)
- **Kumulatives Netzwerk:** Zeigt Gesamtstruktur und persistente Muster
- **Vergleichsperioden:** 2010-2014 vs. 2015-2018

### 4. Forschungsfragen-Priorisierung

Alle drei Hauptfragen haben gute Datenbasis:

1. **Makro-Zentralität (Länder):** ✅ Hohe Priorität
   - Klare Top-Länder identifiziert
   - Dichte Netzwerkstruktur → gute Community-Struktur erwartbar

2. **Bridge-Firmen (Mikro):** ✅ Gute Basis
   - Klare Kandidaten identifiziert
   - Wenige hochvernetzte Firmen → interessante Analyse möglich

3. **Temporale Entwicklung:** ✅ Lohnt sich
   - Trends erkennbar (wenn auch moderat)
   - Top-Länder variieren → Dynamik vorhanden

---

## Beantwortete offene Fragen

Aus `knowledge/data.md`:

✅ **Weight-Verteilung:** Bestätigt als Median=4, Durchschnitt=3.91, Range 1-14, rechtsschief

✅ **Internationale Dominanz:** Bestätigt über alle Jahre (>99% durchgängig)

✅ **Netzwerkgrößen:** Dokumentiert pro Jahr für informierte Tool-Entscheidungen

✅ **Duplikate:** Keine gefunden (wie erwartet aus vorheriger Verifikation)

---

## Nächste Schritte

Basierend auf dieser Exploration:

1. **US-02:** Aggregation auf Länderebene implementieren
   - Grundlage vorhanden: `country_pairs_top20.csv` zeigt benötigte Struktur
   - Summation der weights pro Länderpaar und Jahr

2. **US-03:** Netzwerkobjekte erstellen (Länderebene)
   - NetworkX ausreichend für ~110 Knoten
   - Ungerichtetes, gewichtetes Netzwerk

3. **US-04:** Netzwerkobjekte erstellen (Firmenebene)
   - **Entscheidung nötig:** Vollständig oder Top-N-Subgraph?
   - igraph für Performance erwägen bei vollständiger Analyse

4. **US-05-07:** Metriken berechnen
   - Basis vorhanden, methodische Entscheidungen getroffen

---

## Datenqualität & Limitationen

**Synthetischer Datensatz:**
- Diese Analysen basieren auf synthetischen Daten
- Strukturelle Eigenschaften können vom Original abweichen
- Länder-Codes und Gewichte möglicherweise nicht repräsentativ

**Bekannte Artefakte:**
- Ungewöhnlich gleichmäßige Verteilung der Top-Länder (alle ~11,600-12,000 Gewicht)
- Ungewöhnliche Top-Länder (TW, PL, UA statt erwartete US, CN, DE)
- 99%+ internationale Kooperationen könnte Datenerhebungsartefakt sein

**Für echte Analysen:**
- Alle Schritte mit echten Daten wiederholen
- Ergebnisse inhaltlich validieren (sind Top-Länder plausibel?)
- Zusätzliche Qualitätsprüfungen durchführen

---

---

## Interaktive Visualisierung

**Frontend:** [index.html](index.html) (GitHub Pages)

Vollständig interaktive d3.js-basierte Visualisierung des Patent-Kooperationsnetzwerks mit 3-Tab-Navigation:

**Tab 1: Netzwerk-Analyse**
- **Force-Directed Network** (VIS-1A): 110 Länder, ~5,751 internationale Kooperationen
  - Node Size = Weighted Degree, Color = Region (7 geografische Regionen)
  - Zoom/Pan, Drag, Tooltips mit 4 Centrality-Metriken
  - Ego-Network Highlighting (Click auf Node)
  - Edge Weight Filter (Schwellenwert 1-14)
- **Country Ranking** (VIS-1B): Top-N Bar Chart (10/20/50/All)
  - 4 Centrality-Metriken wählbar: Degree, Betweenness, Closeness, Eigenvector
  - Region-basierte Farbkodierung
- **Temporal Metrics** (VIS-3A): Small Multiples (2x2 Grid)
  - Density, Modularity, Num Communities, Avg Clustering (2010-2018)
- **Controls**: Time Slider (2010-2018 + kumulativ), Centrality Selector, Top-N Selector, Edge Weight Filter

**Tab 2: Temporale Entwicklung**
- **Slopegraph** (VIS-3B): Rank Changes 2010 → 2018
  - Line Color: Grün = Improved, Rot = Worsened, Grau = Unchanged
  - Line Thickness proportional zu abs(ΔRank)
  - Tooltips mit Rank 2010/2018, ΔRank, Centrality 2010/2018, Δ Centrality
  - Centrality Selector (4 Metriken), Top-N Selector (10/20/50)
- **Temporal Metrics** (VIS-3A): Small Multiples (wiederverwendet)

**Tab 3: Bridge-Länder**
- **Bridge Evolution** (VIS-4): Slopegraph 2010 → 2018
  - Sortiert nach Betweenness Centrality (Bridge-Indikator)
  - Line Color: Grün = Improved, Rot = Worsened, Grau = Unchanged
  - Line Thickness proportional zu abs(ΔRank)
  - Tooltips mit Rank 2010/2018, ΔRank, Betweenness 2010/2018, Δ Betweenness
  - Top-N Selector (10/20/50)
- **Temporal Metrics** (VIS-3A): Small Multiples (wiederverwendet)
- **Hinweis:** Firmenebene-Daten (US-04) nicht verfügbar, Länderebene als Proxy

**Technologie:**
- d3.js v7 (Force Simulation, Data Join, Scales, Zoom, Slopegraph)
- CSS Grid + Flexbox (70/30 Layout), Tab-Navigation (CSS-only)
- Vanilla JavaScript (ES6+), Lazy Initialization

**Datengrundlage:**
- `data/country_network.json` (7.2 MB, 9 Jahre + kumulativ)
- Vollständige Netzwerkmetriken (Centrality, Communities, Global Metrics)

**Region-basierte Farbkodierung:**
- Europa (Blau), Asien (Grün), Nordamerika (Rot), Süd-/Mittelamerika (Violett)
- Afrika (Orange), Ozeanien (Türkis), Naher Osten (Braun)
- Ersetzt Community-basierte Farben (Modularity 0.010 statistisch bedeutungslos)

**Code-Statistiken:**
- docs/index.html: 158 Zeilen
- docs/styles.css: 323 Zeilen
- docs/app.js: 1033 Zeilen

**⚠️ Hinweis:** Die Visualisierung basiert auf synthetischen Daten mit bekannten Artefakten (siehe unten). Strukturelle Eigenschaften (hohe Dichte, niedrige Modularity) sind nicht repräsentativ für reale Patent-Netzwerke.

---

## Kontakt & Dokumentation

**Projektdokumentation:** `knowledge/` Ordner
- `data.md` - Datenstruktur und -eigenschaften
- `research.md` - Forschungsfragen und Methodik
- `requirements.md` - User Stories und Technologie-Stack
- `journal.md` - Prozessdokumentation und Learnings
- `design.md` - InfoVis Design-Spezifikation

**Skripte:**
- `scripts/explore_research_questions.py` - Initiale Exploration
- `scripts/aggregate_country_network.py` - Länder-Aggregation + Netzwerkmetriken

**Methodik:** Promptotyping (siehe `CLAUDE.md`)
