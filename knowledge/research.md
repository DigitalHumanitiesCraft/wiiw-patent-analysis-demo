# research.md

## Forschungskontext

Netzwerkanalyse von Patentkooperationen zwischen Firmen auf internationaler Ebene. Ziel ist die Berechnung von Netzwerkmetriken und deren Visualisierung für eine Publikation.

## Forschungsfragen

**Makroebene (Länder)**
- Welche Länder sind zentrale Akteure in internationalen Patentkooperationen?
- Gibt es regionale Cluster oder Communities von Ländern mit intensiver Zusammenarbeit?
- Wie hat sich die Netzwerkstruktur zwischen 2010 und 2018 verändert?

**Mikroebene (Firmen)**
- Welche Firmen fungieren als Brücken zwischen verschiedenen Ländern oder Communities?
- Gibt es Unterschiede in den Kooperationsmustern zwischen Firmen aus verschiedenen Ländern?

## Netzwerkmetriken

**Zentralitätsmaße**

*Degree Centrality* zählt die Anzahl direkter Verbindungen eines Knotens. Hoher Degree bedeutet viele Kooperationspartner. Sagt nichts über die strategische Position im Netzwerk.

*Betweenness Centrality* misst, wie oft ein Knoten auf kürzesten Pfaden zwischen anderen Knoten liegt. Hohe Betweenness identifiziert Broker und Gatekeeper, die Informationsflüsse kontrollieren können.

*Eigenvector Centrality* gewichtet Verbindungen nach der Zentralität der Nachbarn. Ein Knoten ist zentral, wenn seine Partner zentral sind. Identifiziert Akteure in einflussreichen Netzwerkregionen.

*Closeness Centrality* misst die durchschnittliche Distanz zu allen anderen Knoten. Hohe Closeness bedeutet schnellen Zugang zum gesamten Netzwerk.

**Community Detection**

*Louvain-Algorithmus* optimiert Modularität durch iteratives Zusammenfassen von Knoten. Schnell, skaliert gut, aber nicht deterministisch.

*Infomap* basiert auf Random Walks und Informationstheorie. Findet Communities, in denen Information lange zirkuliert. Oft genauer als Louvain bei überlappenden Strukturen.

**Globale Eigenschaften**

*Density* ist der Anteil realisierter Kanten an allen möglichen Kanten. Niedrige Dichte ist typisch für große Netzwerke.

*Average Path Length* ist die durchschnittliche kürzeste Distanz zwischen Knotenpaaren. Kurze Pfade deuten auf Small-World-Eigenschaften hin.

*Clustering Coefficient* misst, wie stark Nachbarn eines Knotens untereinander verbunden sind. Hohe Werte zeigen lokale Verdichtung.

*Assortativity* misst, ob ähnliche Knoten bevorzugt verbunden sind (z.B. Länder mit ähnlichem Entwicklungsstand).

## Methodische Entscheidungen

**Gerichtet vs. ungerichtet:** Ungerichtet. Patentkooperationen sind symmetrisch, owner1 und owner2 sind austauschbar. Datenverifikation bestätigt: keine duplizierten Paare vorhanden.

**Gewichtung:** Kanten sind gewichtet (1-14). Metriken sollten gewichtete Varianten verwenden wo sinnvoll. Median=4, Durchschnitt=3.91, rechtsschief verteilt.

**Temporale Analyse:** Netzwerke pro Jahr separat berechnen oder kumulativ? Beides hat Berechtigung. Jährliche Snapshots zeigen Dynamik, kumulative Netzwerke zeigen Gesamtstruktur.

**Aggregation Firmen zu Ländern:** Summation der weights pro Länderpaar und Jahr. Alternativen wären Durchschnitt oder Anzahl der Firmenpaare.

## Tooling (Python)

**Netzwerkanalyse**

*NetworkX* für Netzwerkberechnung und alle Metriken (Degree, Betweenness, Eigenvector, Closeness). Standard-Bibliothek, gut dokumentiert, alle Algorithmen verfügbar.

*igraph (Python-Binding)* als performantere Alternative für sehr große Netzwerke. Schneller als NetworkX bei >100k Knoten.

*graph-tool* für maximale Performance bei Millionen Knoten. Kompiliert (C++), komplexere Installation.

**Community Detection**

NetworkX: Louvain via `python-louvain` oder `networkx.algorithms.community`.

Infomap: Dediziertes Python-Package `infomap`.

Alternativen: Leiden-Algorithmus via `leidenalg` (noch besser als Louvain).

**Visualisierung**

*Matplotlib + NetworkX* für einfache statische Plots.

*Plotly* für interaktive Netzwerke mit Hover-Informationen und Zoom.

*PyVis* für browserbasierte interaktive Visualisierung (nutzt vis.js).

*Gephi* (extern) für explorative Visualisierung großer Netzwerke, Python-Export via `networkx.write_gexf()`.

**Layoutalgorithmen**

NetworkX bietet: `spring_layout` (Fruchterman-Reingold), `kamada_kawai_layout`, `circular_layout`, `spectral_layout`.

Für sehr große Netzwerke (>10k Knoten): `fa2` (ForceAtlas2) via `fa2` Package oder Graph-tool.

Hinweis: Firmennetzwerk mit ~134,000 Knoten → Subgraph-Analyse, Aggregation auf Länderebene, oder spezialisierte Layouts (FA2, DrL via graph-tool) notwendig.

## Limitationen

Korrelation zwischen Zentralität und Innovationserfolg ist nicht kausal ableitbar.

Patentkooperationen sind nur ein Indikator für Wissensflüsse. Andere Formen (Lizenzierung, informeller Austausch, Personalwechsel) sind nicht erfasst.

Die Aggregation auf Länderebene verdeckt Heterogenität innerhalb von Ländern.

Synthetische Daten können strukturelle Eigenschaften des Originalnetzwerks verzerren.

99.15% internationale Kooperationen: Möglicherweise Artefakt der Datenerhebung (nationale Kooperationen systematisch unterrepräsentiert?).

## Offene Fragen

**Forschungspriorisierung**
- Welche Forschungsfragen haben Priorität für die Publikation?
- Gibt es theoretische Vorannahmen über erwartete Netzwerkstrukturen?
- Sollen bestimmte Länder oder Zeiträume fokussiert werden?

**Dateninterpretation**
- Was bedeutet `weight` exakt? Anzahl gemeinsamer Patente, Kollaborationen, oder ein Score/Index?
- Ist `weight` bereits pro Firmenpaar und Jahr aggregiert oder können theoretisch Duplikate existieren? (Verifikation zeigt: keine Duplikate)
- Wie wurden die synthetischen Daten erzeugt? Bleiben strukturelle Eigenschaften (Degree Distribution, Clustering) erhalten?

**Methodische Details**
- Bei gewichteten Metriken: Gewichte direkt verwenden oder transformieren (log, Normalisierung)?
- Community Detection: Welcher Algorithmus hat Priorität? (Louvain schneller, Infomap oft präziser)
- Temporale Analyse: Jährliche Snapshots oder kumulative Fenster (z.B. 3-Jahres-Perioden)?
