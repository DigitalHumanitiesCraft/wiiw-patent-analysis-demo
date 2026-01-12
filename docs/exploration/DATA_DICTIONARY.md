# Data Dictionary: Explorationsergebnisse

**Generiert:** 2026-01-12
**Skript:** `scripts/explore_research_questions.py`
**Datenbasis:** Synthetischer Datensatz (137,990 Kooperationen, 2010-2018)
**Zweck:** Systematische Exploration zur Vorbereitung der Netzwerkanalysen (US-02 bis US-09)

---

## Verzeichnisstruktur

```
docs/exploration/
├── DATA_DICTIONARY.md     (diese Datei)
├── macro/                 (Makroebene: Länderanalysen)
├── micro/                 (Mikroebene: Firmenanalysen)
├── temporal/              (Zeitreihen 2010-2018)
└── structure/             (Netzwerkstruktur-Eigenschaften)
```

---

## 1. Makroebene (Länder)

### `macro/country_rankings.csv`

**Beschreibung:** Vollständiges Ranking aller Länder nach Gesamtgewicht der Kooperationen (aggregiert über 2010-2018).

**Variablen:**

| Variable | Typ | Beschreibung | Wertebereich |
|----------|-----|--------------|--------------|
| `country` | string | ISO2-Ländercode | 110 unique Länder (TW, PL, UA, ...) |
| `total_weight` | float | Summe aller weights für dieses Land | 11,635 - 12,049 |
| `num_edges` | integer | Anzahl Kooperations-Kanten | 2,946 - 3,076 |
| `unique_partners` | integer | Anzahl einzigartiger Partnerländer | 96 für alle Länder |

**Sortierung:** Absteigend nach `total_weight`

**Verwendung:**
- Identifikation zentraler Länder für Degree Centrality
- Grundlage für Forschungsfrage: "Welche Länder sind zentrale Akteure?"
- Input für US-02 (Länder-Aggregation)

**Top-3:**
1. Taiwan (TW): 12,049
2. Polen (PL): 11,994
3. Ukraine (UA): 11,965

**Bemerkung:** Synthetischer Datensatz zeigt ungewöhnlich gleichmäßige Verteilung (SD sehr niedrig). In echten Daten erwarten wir stärkere Power-Law-Verteilung (USA, China, Deutschland dominant).

---

### `macro/country_pairs_top20.csv`

**Beschreibung:** Die 20 stärksten bilateralen Länderbeziehungen nach summiertem Gewicht.

**Variablen:**

| Variable | Typ | Beschreibung | Wertebereich |
|----------|-----|--------------|--------------|
| `country_a` | string | ISO2-Code Land A (alphabetisch sortiert) | AA < country_b |
| `country_b` | string | ISO2-Code Land B (alphabetisch sortiert) | country_a < BB |
| `total_weight` | float | Summe aller weights zwischen A und B | 186 - 228 |
| `num_edges` | integer | Anzahl Kooperations-Kanten zwischen A und B | 41 - 56 |

**Sortierung:** Absteigend nach `total_weight`

**Verwendung:**
- Identifikation starker bilateraler Beziehungen
- Vorbereitung für Community Detection (starke Paare → gleicher Cluster?)
- Visualisierung: Diese Kanten besonders hervorheben

**Stärkste Beziehung:** Costa Rica - Curacao (CR-CW): 228

**Vollständiger Datensatz:** Alle Länderpaare verfügbar durch Aggregation von Rohdaten (nicht nur Top-20).

---

## 2. Mikroebene (Firmen)

### `micro/firm_bridge_candidates.csv`

**Beschreibung:** Alle 267,068 Firmen sortiert nach Anzahl einzigartiger Partnerländer (Bridge-Potenzial).

**Variablen:**

| Variable | Typ | Beschreibung | Wertebereich |
|----------|-----|--------------|--------------|
| `firm_id` | string | Eindeutige Firmen-ID | 267,068 unique IDs |
| `home_country` | string | ISO2-Heimatland der Firma | 110 Länder |
| `num_partner_countries` | integer | Anzahl verschiedener Länder, mit denen kooperiert wurde | 1 - 4 |

**Sortierung:** Absteigend nach `num_partner_countries`

**Verwendung:**
- Identifikation von Bridge-Firmen für Mikro-Forschungsfrage
- Betweenness Centrality Kandidaten (Firmen, die Länder verbinden)
- Analyse: Welche Firmen fungieren als internationale Knotenpunkte?

**Verteilung:**
- **Median:** 1 Partnerland (die meisten Firmen kooperieren nur national oder mit einem Land)
- **99%-Quantil:** 2 Partnerländer
- **Maximum:** 4 Partnerländer (6 Firmen)

**Top-Bridge-Kandidaten:**
- CH257552054L (Schweiz): 4 Partnerländer
- RU5130001028411 (Russland): 4 Partnerländer
- IS1345110140068 (Island): 4 Partnerländer
- MU4030001025865 (Mauritius): 4 Partnerländer
- BY1501220009087 (Belarus): 4 Partnerländer
- BE70708746 (Belgien): 4 Partnerländer

**Durchschnitt:** 1.03 Partnerländer pro Firma

---

### `micro/firm_rankings.csv`

**Beschreibung:** Alle Firmen sortiert nach Gesamtanzahl Kooperationen (Degree-Proxy).

**Variablen:**

| Variable | Typ | Beschreibung | Wertebereich |
|----------|-----|--------------|--------------|
| `firm_id` | string | Eindeutige Firmen-ID | 267,068 unique IDs |
| `home_country` | string | ISO2-Heimatland der Firma | 110 Länder |
| `total_weight` | float | Summe aller weights für diese Firma | 1 - 23 |
| `num_edges` | integer | Anzahl Kooperations-Kanten | 1 - 4 |

**Sortierung:** Absteigend nach `total_weight`

**Verwendung:**
- Identifikation hochvernetzter Firmen
- Degree Centrality auf Firmenebene
- Vergleich: Hohe Kooperationszahl vs. hohe Länder-Diversität

**Top-Firma:** ID8130042746 (Indonesien): 23 total_weight, 3 Kanten

**Bemerkung:** `total_weight` und `num_edges` relativ niedrig → Netzwerk ist sehr dünn verteilt, keine dominanten "Super-Hubs".

---

## 3. Temporale Analysen

### `temporal/temporal_overview.csv`

**Beschreibung:** Jährliche Netzwerk-Statistiken (2010-2018) für Firmen- und Länderebene.

**Variablen:**

| Variable | Typ | Beschreibung | Wertebereich |
|----------|-----|--------------|--------------|
| `year` | float | Jahr der Patentanmeldung | 2010.0 - 2018.0 |
| `unique_firms_owner1` | integer | Anzahl unique Firmen in owner1-Spalte | 15,134 - 15,467 |
| `unique_firms_owner2` | integer | Anzahl unique Firmen in owner2-Spalte | 15,134 - 15,467 |
| `unique_countries_1` | integer | Anzahl unique Länder in country_1-Spalte | 96 konstant |
| `unique_countries_2` | integer | Anzahl unique Länder in country_2-Spalte | 96 konstant |
| `total_weight` | float | Summe aller weights im Jahr | 59,322 - 61,034 |
| `mean_weight` | float | Durchschnittliches weight pro Kante | 3.89 - 3.95 |
| `median_weight` | float | Median weight pro Kante | 4.0 konstant |
| `num_edges` | integer | Anzahl Kooperations-Kanten im Jahr | 15,173 - 15,506 |
| `unique_firms_approx` | integer | Approximierte Anzahl unique Firmen (max von owner1/owner2) | 15,134 - 15,467 |
| `unique_countries_approx` | integer | Approximierte Anzahl unique Länder | 96 konstant |

**Sortierung:** Aufsteigend nach `year`

**Verwendung:**
- Zeitreihen-Visualisierung für Publikation
- Trend-Analyse: Wachstum vs. Stabilität
- Input für temporale Netzwerk-Snapshots (US-03, jährlich)

**Trends:**
- **Firmen:** Leichtes Wachstum von 30,246 (2010) auf 30,492 (2018) → +0.8%
- **Kanten:** Leichtes Wachstum von 15,173 auf 15,304 → +0.9%
- **Länder:** Stabil bei 96 über alle Jahre
- **Gewichte:** Sehr stabil (Median=4, Mean~3.9 durchgängig)

**Interpretation:** Netzwerkstruktur ist über Zeit sehr stabil, moderates Wachstum in Anzahl Akteure.

---

### `temporal/temporal_top_countries.csv`

**Beschreibung:** Top-5 Länder pro Jahr nach Gesamtgewicht (für Tracking von Auf-/Abstiegen).

**Variablen:**

| Variable | Typ | Beschreibung | Wertebereich |
|----------|-----|--------------|--------------|
| `year` | float | Jahr der Patentanmeldung | 2010.0 - 2018.0 |
| `rank` | integer | Rang (1=höchstes Gewicht) | 1 - 5 |
| `country` | string | ISO2-Ländercode | Variiert pro Jahr |
| `total_weight` | float | Summe aller weights für dieses Land im Jahr | Variabel |

**Sortierung:** Nach `year` und `rank`

**Verwendung:**
- Visualisierung zeitlicher Dynamik der Top-Akteure
- Identifikation von aufsteigenden/absteigenden Ländern
- Small-Multiples-Plots oder Sankey-Diagramme

**Beispiel Top-5 pro Jahr:**

| Rank | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 |
|------|------|------|------|------|------|------|------|------|------|
| 1 | GR | HK | ID | TW | PY | PL | TW | QA | GR |
| 2 | NO | US | IT | TH | ID | UA | GE | TR | IT |
| 3 | CY | SA | SK | CZ | CR | RO | RS | HK | CU |
| 4 | BG | PT | AE | NO | CH | QA | CN | CN | DK |
| 5 | SE | LI | ZA | CR | CO | UY | UY | NO | PH |

**Interpretation:** Hohe Volatilität in Top-5 → kein einzelner dominanter Akteur über gesamten Zeitraum (Artefakt synthetischer Daten?).

---

## 4. Netzwerkstruktur

### `structure/network_preview.csv`

**Beschreibung:** Strukturelle Eigenschaften pro Jahr auf Firmen- und Länderebene (Knoten, Kanten, Dichte).

**Variablen:**

| Variable | Typ | Beschreibung | Wertebereich |
|----------|-----|--------------|--------------|
| `year` | float | Jahr der Patentanmeldung | 2010.0 - 2018.0 |
| `firms_nodes` | integer | Anzahl Firmen-Knoten (unique firms) | 30,246 - 30,903 |
| `firms_edges` | integer | Anzahl Firmen-Kanten (cooperations) | 15,173 - 15,506 |
| `firms_density` | float | Netzwerkdichte Firmenebene | 0.000032 - 0.000033 |
| `countries_nodes` | integer | Anzahl Länder-Knoten | 110 konstant |
| `countries_edges` | integer | Anzahl unique Länderpaare | 5,196 - 5,271 |
| `countries_density` | float | Netzwerkdichte Länderebene | 0.867 - 0.879 |

**Formeln:**
- `density = (2 * edges) / (nodes * (nodes - 1))` für ungerichtete Netzwerke

**Sortierung:** Aufsteigend nach `year`

**Verwendung:**
- Tool-Entscheidung: NetworkX vs. igraph basierend auf Größe
- Erwartungen für globale Metriken (Average Path Length bei niedriger Dichte?)
- Vergleich Firmen- vs. Länderebene

**Interpretation:**
- **Firmennetzwerk:** Sehr dünn (Dichte ~0.000033) → typisch für große Netzwerke, viele isolierte Komponenten erwartet
- **Ländernetzwerk:** Sehr dicht (Dichte ~0.87) → fast vollständig verbunden, kurze Pfade, hohe Konnektivität

**Maximale Kanten:**
- Firmen (30,000 Knoten): max = 449,985,000 → realisiert: 15,000 → 0.003%
- Länder (110 Knoten): max = 5,995 → realisiert: 5,250 → 87.6%

---

### `structure/weight_distribution.csv`

**Beschreibung:** Detaillierte Quantile der Gewichtsverteilung über alle Kooperationen.

**Variablen:**

| Variable | Typ | Beschreibung | Wertebereich |
|----------|-----|--------------|--------------|
| `quantile` | string | Quantil-Bezeichnung | "1%", "5%", ..., "99%" |
| `weight` | float | Weight-Wert am jeweiligen Quantil | 1.0 - 9.0 |

**Quantile:**

| Quantil | Weight | Interpretation |
|---------|--------|----------------|
| 1% | 1.0 | Unterste 1% haben weight=1 |
| 5% | 1.0 | |
| 10% | 2.0 | |
| 25% | 3.0 | Unteres Quartil |
| **50%** | **4.0** | **Median** |
| 75% | 5.0 | Oberes Quartil |
| 90% | 6.0 | |
| 95% | 7.0 | Top 5% beginnen hier |
| 99% | 9.0 | Top 1% haben weight ≥9 |

**Verwendung:**
- Entscheidung für Gewichtstransformation
- Outlier-Identifikation (Maximum=14, aber 99%-Quantil=9)
- Visualisierung: Kantendicke basierend auf Quantilen

**Statistische Eigenschaften:**
- **Mean:** 3.91
- **Median:** 4.0
- **Std:** 1.71 (hohe Streuung)
- **Min:** 1.0
- **Max:** 14.0
- **IQR:** 5 - 3 = 2

**Verteilungsform:** Rechtsschief (mean < median wäre linksschief, aber hier mean~median → leichte Rechtsschiefe durch Ausreißer)

**Log-Transformation:**
- `log(weight+1)` reduziert Std von 1.71 auf 0.36 → bessere Normalverteilung
- Empfehlung: Für Visualisierungen und Regressionsanalysen log-transformieren

---

## Zusammenfassende Statistiken

### Gesamtdatensatz

- **Zeitraum:** 2010-2018 (9 Jahre)
- **Kooperationen (Kanten):** 137,990
- **Firmen (Knoten):** 267,068 unique
- **Länder (Knoten):** 110 unique
- **Internationale Kooperationen:** 99.15% (136,823 Kanten)
- **Nationale Kooperationen:** 0.85% (1,167 Kanten)

### Netzwerk-Charakteristika

**Firmenebene:**
- Sehr dünn (Dichte < 0.0001)
- Niedrige Degree-Verteilung (Median=1, Mean=1.03)
- Wenige Hubs (Max Degree=4)
- Erwartung: Viele isolierte Komponenten oder kleine Cluster

**Länderebene:**
- Sehr dicht (Dichte ~0.87)
- Fast vollständig verbunden
- Alle Länder haben 96 Partner (alle anderen Länder)
- Erwartung: Ein großer zusammenhängender Komponente, kurze Pfade

### Methodische Implikationen

**1. Aggregationsebene:**
- Länderebene gut handhabbar (~110 Knoten, NetworkX ausreichend)
- Firmenebene rechenintensiv (~267k Knoten, igraph oder Subgraph-Analyse empfohlen)

**2. Metriken:**
- Degree Centrality: Auf beiden Ebenen sinnvoll, aber stark unterschiedliche Verteilungen
- Betweenness Centrality: Länderebene aussagekräftig (hohe Dichte), Firmenebene schwierig (dünn)
- Eigenvector Centrality: Nur auf Länderebene sinnvoll (Firmennetzwerk zu fragmentiert)

**3. Community Detection:**
- Länderebene: Louvain/Leiden sollte klare Cluster finden (trotz hoher Dichte)
- Firmenebene: Communities wahrscheinlich durch Heimatland dominiert

**4. Temporale Analyse:**
- Moderate Trends → Snapshots UND kumulativ berechnen
- Vergleichsperioden: 2010-2014 vs. 2015-2018

---

## Datenqualität & Limitationen

### Synthetischer Datensatz

⚠️ **Kritische Einschränkung:** Alle Analysen basieren auf synthetischen Daten!

**Bekannte Artefakte:**

1. **Ungewöhnlich gleichmäßige Länder-Verteilung:**
   - Top-20 Länder haben fast identisches Gewicht (11,635 - 12,049)
   - In echten Daten: Erwartung einer Power-Law-Verteilung (wenige dominante Länder)

2. **Unerwartete Top-Länder:**
   - Taiwan, Polen, Ukraine statt erwartete USA, China, Deutschland
   - Wahrscheinlich Artefakt der Anonymisierung

3. **Sehr niedrige Firm-Degree:**
   - Max 4 Partnerländer scheint unrealistisch niedrig
   - Multinationale Konzerne sollten >10 Länder haben

4. **99%+ internationale Kooperationen:**
   - Könnte Datenerhebungsartefakt sein (nationale Kooperationen systematisch unterrepräsentiert?)

### Für echte Analysen

**Notwendige Schritte:**

1. **Alle Skripte mit echten Daten wiederholen**
2. **Inhaltliche Validierung:**
   - Sind Top-Länder plausibel? (USA, China, Deutschland erwartet)
   - Sind Top-Firmen bekannte multinationale Konzerne?
   - Stimmen bilaterale Beziehungen mit bekannten Handelsbeziehungen überein?
3. **Zusätzliche Qualitätsprüfungen:**
   - Duplikate in echten Daten?
   - Missing Values in echten Daten?
   - Zeitliche Konsistenz (Firmen-IDs über Jahre persistent?)

---

## Nutzung in nachfolgenden Analysen

### US-02: Länder-Aggregation

**Input:** `macro/country_pairs_top20.csv` (Struktur-Vorlage)

**Aufgabe:** Vollständige Aggregation aller Firmenkooperationen auf Länderebene

**Output:** DataFrame mit `country_1`, `country_2`, `year`, `total_weight`

### US-03: Netzwerkobjekte (Länderebene)

**Input:**
- `macro/country_rankings.csv` (Knotenliste)
- Aggregierte Daten aus US-02 (Kantenliste)

**Tool:** NetworkX (ausreichend für ~110 Knoten)

### US-04: Netzwerkobjekte (Firmenebene)

**Input:**
- `micro/firm_rankings.csv` (Knotenliste)
- Rohdaten (Kantenliste)

**Entscheidung nötig:**
- Vollständiges Netzwerk (~267k Knoten) → igraph empfohlen
- Top-N-Subgraph (z.B. Top-1000 Firmen nach Degree)

### US-05: Zentralitätsmaße

**Input:** Netzwerkobjekte aus US-03/US-04

**Bridge-Kandidaten priorisieren:**
- `micro/firm_bridge_candidates.csv` (Top-20 für detaillierte Analyse)

### US-06: Community Detection

**Input:** Netzwerkobjekte aus US-03 (Länderebene Priorität)

**Erwartung:** Regionale Cluster erkennbar trotz hoher Dichte

### US-08/US-09: Visualisierung

**Input:**
- `temporal/temporal_top_countries.csv` für temporale Plots
- `structure/weight_distribution.csv` für Kantendicken-Skalierung (log-transformiert)

---

## Kontakt & Dokumentation

**Projekt-Methodik:** Siehe `CLAUDE.md` (Promptotyping)

**Knowledge Base:** `knowledge/` Ordner
- `data.md` - Rohdaten-Beschreibung
- `research.md` - Forschungsfragen und Methodik
- `requirements.md` - User Stories
- `journal.md` - Prozess-Dokumentation

**Skript:** `scripts/explore_research_questions.py`

**Journal-Update:** `docs/journal_update.txt` (manuell in `knowledge/journal.md` einpflegen nach Review)
