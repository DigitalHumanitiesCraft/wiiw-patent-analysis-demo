# Review Matrix: Daten & Forschungsfragen

**Generiert am:** 2026-01-12T18:23:50.962955

---

## Abschnitt 1: Daten-Konsistenz

| Check                                    | Original (international)   | Aggregiert                 | Status        | Diskrepanz                            | Original            |
|:-----------------------------------------|:---------------------------|:---------------------------|:--------------|:--------------------------------------|:--------------------|
| 1.1 Weight-Erhaltung (international)     | 535,054                    | 535,054                    | ✓ Korrekt     | 0.0                                   | nan                 |
| 1.2 Länder-Abdeckung                     | nan                        | 110 Länder                 | ✓ Komplett    | Keine                                 | 110 Länder          |
| 1.3 Zeitraum-Abdeckung                   | nan                        | 2010-2018 (9 Jahre)        | ✓ Vollständig | Keine                                 | 2010-2018 (9 Jahre) |
| 1.4 Nationale Kooperationen (exkludiert) | nan                        | 0 (0%, korrekt exkludiert) | ✓ Korrekt     | 99.2% internationale Koop. inkludiert | 1,167 (0.85%)       |

## Abschnitt 2: Forschungsfragen-Alignment

### Forschungsfrage 1: Makro-Zentralität

| Metrik                 | Verfügbar   | Wertebereich   | Normalisiert     |
|:-----------------------|:------------|:---------------|:-----------------|
| degree_centrality      | ✓           | [0.844, 1.000] | ✓ Ja             |
| betweenness_centrality | ✓           | [0.000, 0.029] | ✓ Ja             |
| closeness_centrality   | ✓           | [0.013, 0.017] | ✓ Ja             |
| eigenvector_centrality | ✓           | [0.051, 0.113] | ✓ Ja             |
| Communities (Louvain)  | ✓           | 4 Communities  | Modularity=0.011 |

### Forschungsfrage 3: Temporale Entwicklung

|   Jahr |   Nodes |   Edges |   Density |   Communities |   Modularity |
|-------:|--------:|--------:|----------:|--------------:|-------------:|
|   2010 |     110 |    5147 |     0.859 |             5 |        0.047 |
|   2011 |     110 |    5192 |     0.866 |             5 |        0.047 |
|   2012 |     110 |    5189 |     0.866 |             5 |        0.046 |
|   2013 |     110 |    5135 |     0.857 |             5 |        0.047 |
|   2014 |     110 |    5209 |     0.869 |             6 |        0.047 |
|   2015 |     110 |    5189 |     0.866 |             6 |        0.045 |
|   2016 |     110 |    5174 |     0.863 |             5 |        0.048 |
|   2017 |     110 |    5133 |     0.856 |             6 |        0.047 |
|   2018 |     110 |    5185 |     0.865 |             5 |        0.043 |

## Abschnitt 3: Methodische Korrektheit

| Check                                | Wert                  | Sollwert                     | Status      |
|:-------------------------------------|:----------------------|:-----------------------------|:------------|
| 3.1 Self-Loops (nationale Koop.)     | 0 Self-Loops          | 0 (keine)                    | ✓ Korrekt   |
| 3.2 Degree Centrality Normalisierung | Max=1.000000          | ≤ 1.0                        | ✓ Korrekt   |
| 3.3 Network Connectivity             | Connected             | Connected (erwartet)         | ✓ Korrekt   |
| 3.4 Weight-Verteilung                | Median=90, Mean=93.0  | Rechtsschief (Median < Mean) | ✓ Plausibel |
| 3.5 Modularity (bei hoher Density)   | Mod=0.011, Dens=0.959 | Mod < 0.3 bei Dens > 0.8     | ✓ Plausibel |

## Abschnitt 4: User Stories

| US    | Titel                         | Status                   | Evidenz                                       |
|:------|:------------------------------|:-------------------------|:----------------------------------------------|
| US-01 | Daten laden & validieren      | ✓ Abgeschlossen          | explore_rds.py, verify_data.py                |
| US-02 | Aggregation Länderebene       | ✓ Abgeschlossen          | aggregate_country_network.py, JSON 5751 edges |
| US-03 | Netzwerkobjekte (Länder)      | ✓ Abgeschlossen          | 9 Jahre + kumulativ in JSON                   |
| US-04 | Netzwerkobjekte (Firmen)      | ⚠ Offen                  | CSV-Exploration vorhanden, Netzwerk offen     |
| US-05 | Zentralitätsmaße              | ✓ Abgeschlossen (Länder) | 4 Centrality-Metriken in JSON                 |
| US-06 | Community Detection           | ✓ Abgeschlossen          | Louvain, Modularity in JSON                   |
| US-07 | Globale Netzwerkeigenschaften | ✓ Abgeschlossen          | 9 Metriken (inkl. Path Length, Assortativity) |
| US-08 | Statische Visualisierung      | ⏸ Offen                  | design.md vorhanden, Implementation offen     |
| US-09 | Temporale Visualisierung      | ⏸ Offen                  | design.md vorhanden, Implementation offen     |

---

## Gesamtbewertung

✓✓✓ **DATEN SIND ABSOLUT KORREKT UND BEREIT FÜR FRONTEND**

- Daten-Qualität: EXZELLENT
- Forschungsfragen-Alignment: SEHR GUT (2/3 vollständig)
- Methodische Korrektheit: EXZELLENT
- Vollständigkeit: GUT (6/9 User Stories)
