# data.md

## Datei

**Pfad:** `data/db_networkCoPat_fake.rds`
**Format:** RDS (R Data Serialization)
**Größe:** ~2.8 MB
**Zeilen:** 137,990
**Zeitraum:** 2010–2018

Dies ist ein synthetischer Datensatz für Cloud-basierte Entwicklung. Echte Daten verbleiben lokal und werden nie in Cloud-Umgebungen hochgeladen.

## Struktur

Edge-List von Patentkooperationen zwischen Firmen.

| Variable | Typ | Beschreibung |
|----------|-----|--------------|
| `year_application` | integer | Jahr der Patentanmeldung |
| `owner1` | character | Firmen-ID (Kooperationspartner 1) |
| `country_1` | character | ISO2-Ländercode von owner1 |
| `owner2` | character | Firmen-ID (Kooperationspartner 2) |
| `country_2` | character | ISO2-Ländercode von owner2 |
| `weight` | integer | Anzahl der Kollaborationen zwischen den Firmen in diesem Jahr |

Hinweis: Python (pyreadr) liest integer-Spalten teilweise als float64. Die Quelldefinition in R ist integer.

## Netzwerkeigenschaften

**Knoten:** ~134,000 eindeutige Firmen (owner IDs)
**Kanten:** 137,990 Verbindungen
**Typ:** Ungerichtet, gewichtet
**Selbstverbindungen:** Keine (owner1 != owner2 in allen Zeilen)
**Duplikate:** Keine

## Länderverteilung

**Länder (owner1):** 96
**Länder (owner2):** 92
**Grenzüberschreitend:** 99.15% (136,823 Kanten)
**Innerhalb eines Landes:** 0.85% (1,167 Kanten)

## Gewichtung

**Bereich:** 1–14
**Median:** 4
**Durchschnitt:** 3.91
**Verteilung:** Rechtsschief, Schwerpunkt bei 2–5

## Aggregationsebenen

Die Daten können auf zwei Ebenen analysiert werden.

**Firmenebene (disaggregiert):** Netzwerk zwischen einzelnen Firmen. ~134,000 Knoten.

**Länderebene (aggregiert):** Summation der weights pro Länderpaar und Jahr. ~96 Knoten.

## Lesen der Daten

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

## Output-Daten (JSON)

**Pfad:** `docs/data/country_network.json`
**Format:** JSON (für d3.js Visualisierung)
**Größe:** 7.1 MB
**Generierung:** Python-Skript `scripts/aggregation.py` (RDS → JSON)

### Struktur

Das JSON enthält drei Hauptabschnitte:

**1. metadata** - Projektinformationen
```json
{
  "years": [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018],
  "num_years": 9,
  "num_countries": 110,
  "centrality_metrics": ["degree_centrality", "betweenness_centrality",
                         "closeness_centrality", "eigenvector_centrality"]
}
```

**2. cumulative** - Aggregiertes Netzwerk über alle Jahre
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

**3. temporal** - Jährliche Snapshots (9 Jahre)
```json
{
  "2010": { /* gleiche Struktur wie cumulative */ },
  "2011": { /* ... */ },
  ...
  "2018": { /* ... */ }
}
```

### Netzwerk-Metriken (Node-Ebene)

| Metrik | Beschreibung | Bereich | Interpretation |
|--------|--------------|---------|----------------|
| `degree_centrality` | Normalisierte Anzahl direkter Verbindungen | [0, 1] | Wie viele Länder kooperieren direkt? |
| `betweenness_centrality` | Anteil kürzester Pfade durch den Knoten | [0, 1] | Brückenposition zwischen Clustern |
| `closeness_centrality` | Durchschnittliche Distanz zu allen Knoten | [0, 1] | Wie schnell erreicht man andere Länder? |
| `eigenvector_centrality` | Zentralität der Nachbarn | [0, 1] | Verbindungen zu wichtigen Ländern |
| `weighted_degree` | Summe der Edge-Gewichte | Integer | Gesamte Kollaborationsintensität |
| `community` | Community-ID (Louvain) | Integer | Cluster-Zugehörigkeit (bei low modularity bedeutungslos) |

### Globale Metriken (Graph-Ebene)

| Metrik | Beschreibung | Wert (Cumulative) | Interpretation |
|--------|--------------|-------------------|----------------|
| `density` | Anteil realisierter Kanten | 0.959 | Fast vollständig vernetzt (unrealistisch) |
| `modularity` | Community-Qualität | 0.010 | Keine signifikanten Communities |
| `num_communities` | Anzahl Communities (Louvain) | 3 | Statistisch bedeutungslos bei modularity 0.010 |
| `avg_clustering` | Durchschnittlicher Clustering-Koeffizient | 0.961 | Hohe lokale Dichte |

### Data Quality Warnings

**Synthetische Daten:** Die JSON-Daten basieren auf `db_networkCoPat_fake.rds` und sind nicht repräsentativ für echte Patentnetzwerke.

**Artefakte:**
- Density 95.9%: Unrealistisch hoch (echte Netzwerke haben Density <10%)
- Modularity 0.010: Keine erkennbaren Communities (statistically insignificant)
- Community-basierte Farbkodierung: In Frontend durch Region-basierte Farben ersetzt

## Offene Fragen

**Datenmodell und Semantik**
- Was definiert eine Kooperation? Co-Anmeldung, Co-Ownership, Zitation, Technologietransfer?
- Ist year_application das Anmelde- oder Erteilungsjahr?

**Owner-IDs**
- Woher stammt die ID-Systematik? Die Präfixe (QA, AT, SG) scheinen auf Länder hinzudeuten, aber country_1/country_2 existieren separat.
- Sind die IDs persistent über Jahre oder können Firmen mehrere IDs haben?

**Datenherkunft**
- Welche Originaldatenquelle liegt zugrunde (EPO, USPTO, PATSTAT)?
- Welche Vorverarbeitung wurde bereits durchgeführt?

**Synthetischer Datensatz**
- Wie wurde db_networkCoPat_fake.rds aus den Originaldaten erzeugt? Anonymisierung, Shuffling, vollständig generiert?
- Sind die statistischen Eigenschaften (Verteilungen, Netzwerkstruktur) repräsentativ für die echten Daten?

**Aggregation**
- Ist weight bereits pro Firmenpaar und Jahr aggregiert, oder können Duplikate existieren?
- Wie wurde bei der Aggregation auf Länderebene mit Firmen umgegangen, die in mehreren Ländern aktiv sind?