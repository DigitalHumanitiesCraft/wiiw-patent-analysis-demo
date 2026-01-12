# Journal

## 2026-01-12 (Session 1): Datenexploration und Verifikation

RDS-Datei (`db_networkCoPat_fake.rds`, 137,990 Zeilen, 6 Spalten) mit Python/pyreadr exploriert. Erste Dokumentation erstellt, dann systematisch verifiziert mit `verify_data.py`. Dabei drei Fehler gefunden: (1) Netzwerk fälschlich als "bipartit" klassifiziert, (2) Beispieldaten zeigten identische statt unterschiedliche Owner, (3) Weight-Interpretation spekulativ. Korrekturen durchgeführt. Skripte in `scripts/` organisiert mit vollständiger Dokumentation. `data.md` kompakt umformuliert mit Fokus auf verifizierbare Fakten, Hinweis auf synthetischen Datensatz, Code-Beispiele R/Python, Sektion "Offene Fragen" ergänzt. Initial Commit erstellt. Zweite Verifikation zeigte: Weight-Semantik bleibt spekulative Interpretation ohne Datenbeweis.

**Learnings:**
- Systematische Verifikation verhindert Fehlerfortpflanzung
- Dokumentation muss Spekulationen von Fakten trennen
- "Offene Fragen" dokumentieren ist wissenschaftlich sauberer als unsichere Behauptungen
- Reproduzierbare Skripte ermöglichen iterative Qualitätsprüfung

## 2026-01-12 (Session 2): Python-Migration und Publikations-Workflow

Komplette Migration auf Python-Stack dokumentiert. `research.md` von R-Paketen auf Python-Bibliotheken umgestellt (NetworkX, python-louvain, Plotly, PyVis). `requirements.md` erstellt mit User Stories, Akzeptanzkriterien und Technologie-Stack. US-01 als "Abgeschlossen" markiert (explore_rds.py, verify_data.py vorhanden). Inkonsistenzen zwischen Dokumenten behoben: R → Python, igraph → NetworkX (Standard), user-story.md → requirements.md. Publikations-Workflow definiert: Lokale Verarbeitung (data/ → scripts/ → docs/), GitHub Pages für HTML/Plots/CSVs, Datenschutz durch .gitignore. Repository-Struktur in CLAUDE.md und ReadMe.md aktualisiert. Alle .md-Dateien synchronisiert.

**Learnings:**
- Technologie-Entscheidungen müssen dokumentenübergreifend konsistent sein
- Explizite Workflows (lokal → GitHub Pages) vermeiden Missverständnisse
- User Stories mit Status-Tracking ermöglichen Fortschrittskontrolle
- Dokumentations-Synchronisation nach größeren Änderungen essentiell

## 2026-01-12 (Session 3): Forschungsfragen-Exploration

Systematische Exploration der Patentkooperationsdaten im Hinblick auf die Forschungsfragen aus research.md. Skript `explore_research_questions.py` erstellt mit granularer Output-Struktur (docs/exploration/{macro,micro,temporal,structure}). Umfassendes Data Dictionary erstellt (DATA_DICTIONARY.md) mit vollständiger Dokumentation aller Variablen, Verwendungszwecke und methodischen Empfehlungen.

**Erkenntnisse Makroebene (Länder):**
- 110 unique Länder identifiziert (synthetischer Datensatz zeigt ungewöhnlich gleichmäßige Verteilung)
- Top-3 Länder nach Gesamtgewicht: TW (12,049), PL (11,994), UA (11,965)
- Stärkste bilaterale Beziehung: CR-CW (Gewicht: 228)
- Internationale Kooperationen dominieren durchgängig über alle Jahre (>99%)
- Ländernetzwerk sehr dicht (~87%) → fast vollständig verbunden

**Erkenntnisse Mikroebene (Firmen):**
- 267,068 unique Firmen identifiziert
- Top-Bridge-Kandidat: CH257552054L mit 4 verschiedenen Partnerländern
- Durchschnittliche Anzahl Partnerländer pro Firma: 1.03 (Median=1)
- 6 Firmen mit Maximum 4 Partnerländer (scheint unrealistisch niedrig für multinationale Konzerne)
- Firmennetzwerk sehr dünn (~0.000033 Dichte) → typisch für große Netzwerke

**Temporale Entwicklung:**
- Zeitraum: 2010-2018
- Netzwerkgröße (Firmen): 30,246 (2010) → 30,492 (2018) → +0.8%
- Anzahl Kanten: 15,173 → 15,304 → +0.9%
- Anzahl Länder: Stabil bei 110 über alle Jahre
- Gewichtsverteilung: Sehr stabil (Median=4, Mean~3.9 durchgängig)

**Netzwerkstruktur:**
- Gewichtsverteilung: Rechtsschief (Median=4.0, 95%-Quantil=7.0, Max=14)
- Log-Transformation reduziert Std von 1.71 auf 0.36
- Zwei sehr unterschiedliche Netzwerk-Ebenen:
  * Länder: Klein (110 Knoten), dicht (87%), gut handhabbar mit NetworkX
  * Firmen: Groß (267k Knoten), dünn (0.003%), igraph empfohlen

**Methodische Empfehlungen:**
1. Gewichtstransformation: log(weight+1) für Visualisierungen und bestimmte Metriken
2. Tool-Auswahl: NetworkX für Länderebene ausreichend, igraph für Firmenebene erwägen
3. Temporale Analyse: Sowohl jährliche Snapshots als auch kumulatives Netzwerk berechnen
4. Forschungsfragen-Priorisierung: Alle drei Hauptfragen haben gute Datenbasis

**Beantwortete offene Fragen aus data.md:**
- Weight-Verteilung bestätigt: Median=4, Durchschnitt=3.91, Range 1-14, rechtsschief
- Internationale Dominanz über alle Jahre bestätigt (>99% durchgängig)
- Netzwerkgrößen pro Jahr dokumentiert für informierte Tool-Entscheidungen

**Exports erstellt (granular organisiert):**
- docs/exploration/macro/: country_rankings.csv, country_pairs_top20.csv
- docs/exploration/micro/: firm_bridge_candidates.csv, firm_rankings.csv
- docs/exploration/temporal/: temporal_overview.csv, temporal_top_countries.csv
- docs/exploration/structure/: network_preview.csv, weight_distribution.csv
- docs/exploration/DATA_DICTIONARY.md: Vollständige Dokumentation aller Dateien mit Variablendefinitionen, Verwendungszwecken und methodischen Hinweisen
- docs/README.md: Übersicht und Schnellreferenz

**Learnings:**
- Forschungsfragen-orientierte Exploration liefert präzisere Grundlage für methodische Entscheidungen als generische Exploration
- Granulare Ordnerstruktur (macro/micro/temporal/structure) verbessert Übersichtlichkeit und Wartbarkeit
- Umfassendes Data Dictionary (mit Variablen-Beschreibungen, Wertebereichen, Verwendungszwecken) ist essentiell für Reproduzierbarkeit
- CSV-Exports in docs/exploration/ ermöglichen spätere GitHub Pages Publikation ohne Rohdaten zu teilen
- Systematische Quantil-Analysen zeigen konkrete Transformationsbedarfe (log für rechtsschiefe Daten)
- Bridge-Kandidaten-Identifikation bereits vor Netzwerkberechnung möglich (effizient)
- Synthetischer Datensatz zeigt Artefakte (gleichmäßige Verteilung, unerwartete Top-Länder) → alle Analysen mit echten Daten wiederholen und validieren

**Nächste Schritte:**
- US-02: Aggregation auf Länderebene implementieren (Grundlage vorhanden)
- US-03: Netzwerkobjekte erstellen mit NetworkX
- Entscheidung: Firmenebene vollständig oder Top-N-Subgraph für Performance
