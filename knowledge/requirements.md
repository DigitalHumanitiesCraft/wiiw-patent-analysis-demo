# requirements.md

## Übersicht

Dieses Dokument definiert die Anforderungen für die Netzwerkanalyse der Patentkooperationsdaten. User Stories sind nach Priorität geordnet. Jede Story enthält Akzeptanzkriterien und Status.

## Technologie-Stack

**Programmiersprache:** Python 3.11+

**Kernbibliotheken:**
- pandas, pyreadr (Datenverarbeitung)
- networkx (Netzwerkanalyse, Standard)
- python-louvain / leidenalg (Community Detection)
- matplotlib, plotly, pyvis (Visualisierung)

**Optional für Performance:**
- igraph (Python-Binding) bei >100k Knoten
- graph-tool (maximale Performance, komplexere Installation)

## User Stories

### Phase 1: Datenvorbereitung

**US-01: Daten laden und validieren**
Als Forschender möchte ich die RDS-Datei laden und die Datenqualität prüfen, um sicherzustellen, dass die Daten für die Analyse geeignet sind.

Akzeptanzkriterien:
- Daten sind in Python als pandas DataFrame verfügbar (via pyreadr)
- Spaltentypen entsprechen der Spezifikation in data.md
- Keine unerwarteten Nullwerte oder Duplikate
- Explorative Zusammenfassung dokumentiert

Status: Abgeschlossen (siehe scripts/explore_rds.py, scripts/verify_data.py)

---

**US-02: Aggregation auf Länderebene**
Als Forschender möchte ich die Firmendaten auf Länderebene aggregieren, um makroökonomische Kooperationsmuster analysieren zu können.

Akzeptanzkriterien:
- Neuer Datensatz mit country_1, country_2, year_application, weight (summiert)
- Dokumentation der Aggregationslogik
- Validierung: Summe der Gewichte bleibt erhalten

Status: Abgeschlossen (siehe scripts/aggregate_country_network.py, docs/data/country_network.json)

---

### Phase 2: Netzwerkkonstruktion

**US-03: Netzwerkobjekte erstellen (Länderebene)**
Als Forschender möchte ich aus den aggregierten Daten Netzwerkobjekte erstellen, um Netzwerkmetriken berechnen zu können.

Akzeptanzkriterien:
- NetworkX Graph-Objekt pro Jahr und kumulativ
- Ungerichtetes, gewichtetes Netzwerk
- Knotenanzahl entspricht Anzahl der Länder (~96)
- Kantengewichte entsprechen aggregierten weights

Technologie: NetworkX (Standard), igraph optional für Vergleich

Status: Abgeschlossen (siehe scripts/aggregate_country_network.py, 9 jährliche Graphs + 1 kumulativ)

---

**US-04: Netzwerkobjekte erstellen (Firmenebene)**
Als Forschender möchte ich aus den Originaldaten Netzwerkobjekte auf Firmenebene erstellen, um disaggregierte Analysen durchführen zu können.

Akzeptanzkriterien:
- NetworkX Graph-Objekt pro Jahr und kumulativ
- Ungerichtetes, gewichtetes Netzwerk
- Performant für ~134,000 Knoten (ggf. igraph verwenden)
- Alternative: Subgraph-Analyse (Top-N Firmen nach Degree)

Technologie: NetworkX (wenn performant genug), sonst igraph

Performance-Warnung: Bei ~134k Knoten kann NetworkX langsam werden. Benchmarking erforderlich.

Status: Offen

---

### Phase 3: Metriken

**US-05: Zentralitätsmaße berechnen**
Als Forschender möchte ich Zentralitätsmaße (Degree, Betweenness, Eigenvector, Closeness) berechnen, um zentrale Akteure im Netzwerk zu identifizieren.

Akzeptanzkriterien:
- Metriken für beide Ebenen (Länder und Firmen)
- Gewichtete Varianten wo sinnvoll
- Export als Tabelle (CSV)
- Top-10-Ranking pro Metrik

Status: Teilweise abgeschlossen (Degree Centrality für Länderebene in JSON, Betweenness/Eigenvector/Closeness offen)

---

**US-06: Community Detection**
Als Forschender möchte ich Communities im Netzwerk identifizieren, um Kooperationscluster zu erkennen.

Akzeptanzkriterien:
- Louvain (via python-louvain oder networkx.algorithms.community) angewendet
- Optional: Leiden (via leidenalg) als Verbesserung
- Modularitätswerte dokumentiert
- Community-Zuordnung als Knotenattribut im DataFrame
- Vergleich der Ergebnisse wenn mehrere Algorithmen verwendet

Technologie: python-louvain (primär), leidenalg (optional)

Status: Abgeschlossen (Louvain für Länderebene in JSON, Modularity dokumentiert, Leiden optional offen)

---

**US-07: Globale Netzwerkeigenschaften**
Als Forschender möchte ich globale Eigenschaften (Density, Average Path Length, Clustering Coefficient, Assortativity) berechnen, um die Gesamtstruktur des Netzwerks zu charakterisieren.

Akzeptanzkriterien:
- Metriken pro Jahr berechnet
- Zeitliche Entwicklung als Tabelle
- Interpretation im Kontext von Patentkooperationen

Status: Abgeschlossen (Density, Clustering, Transitivity, Konnektivität in JSON, Path Length/Assortativity offen)

---

### Phase 4: Visualisierung

**US-08: Statische Netzwerkvisualisierung**
Als Forschender möchte ich das Netzwerk visualisieren, um Strukturen und Muster visuell erkennbar zu machen.

Akzeptanzkriterien:
- Ländernetzwerk als lesbare Grafik
- Knotengröße kodiert Degree oder Patentzahl
- Knotenfarbe kodiert Community oder Region
- Kantendicke kodiert Gewicht
- Export als PNG (300 DPI) und PDF (Vektor)

Technologie: Matplotlib + NetworkX (statisch) oder Plotly (interaktiv mit statischem Export)

Layout: spring_layout (Fruchterman-Reingold) für Ländernetzwerk (~96 Knoten)

Status: Offen

---

**US-09: Temporale Visualisierung**
Als Forschender möchte ich die zeitliche Entwicklung des Netzwerks visualisieren, um Veränderungen zwischen 2010 und 2018 sichtbar zu machen.

Akzeptanzkriterien:
- Small Multiples (ein Panel pro Jahr) oder Animation
- Konsistentes Layout über Jahre hinweg
- Erkennbare Trends

Status: Offen

---

## Priorisierung

| Priorität | Stories | Begründung |
|-----------|---------|------------|
| Hoch | US-01, US-02, US-03 | Grundlage für alle weiteren Analysen |
| Hoch | US-05, US-08 | Kernmetriken und Basisvisualisierung |
| Mittel | US-06, US-07 | Vertiefende Analysen |
| Mittel | US-09 | Temporale Dimension |
| Niedriger | US-04 | Firmenebene ist rechenintensiv, Länderebene hat Priorität |

## Publikations-Workflow

**Lokale Verarbeitung:**
- Python-Skripte verarbeiten `data/db_networkCoPat_fake.rds` (lokal, nicht im Git)
- Berechnete Metriken, Visualisierungen und Ergebnisse werden in `docs/` gespeichert
- `docs/` enthält nur aggregierte Ergebnisse, keine Rohdaten

**GitHub Pages:**
- `docs/` Ordner wird via GitHub Pages veröffentlicht
- HTML-Visualisierungen (Plotly, PyVis) direkt im Browser nutzbar
- Statische Plots (PNG, PDF) für Download
- CSV-Exporte mit aggregierten Metriken

**Datenschutz:**
- Nur synthetische Daten im Repository
- Echte Daten bleiben lokal, werden nie gepusht
- `.gitignore` verhindert versehentliches Hochladen sensibler Daten

## Offene Fragen

- Welche Metriken sind für die Publikation am relevantesten?
- Gibt es Präferenzen für Visualisierungsstile?
- Soll die Firmenebene vollständig oder nur für ausgewählte Länder/Jahre analysiert werden?
- GitHub Pages Design: Minimalistisch oder mit Framework (z.B. Jupyter Book, Sphinx)?