# Patent Co-Ownership Network Analysis

Netzwerkanalyse internationaler Patentkooperationen zwischen Firmen (2010-2018).

## Quick Start

```bash
# Installation
pip install pyreadr pandas networkx

# Daten explorieren
python scripts/explore_rds.py

# Datenqualität verifizieren
python scripts/verify_data.py
```

## Projektstruktur

```
data/         RDS-Daten (lokal, .gitignore, synthetischer Datensatz für Entwicklung)
scripts/      Python-Analyseskripte
knowledge/    Promptotyping-Dokumentation
docs/         GitHub Pages Output (Visualisierungen, Metriken, HTML)
```

**Workflow:** Lokale Python-Verarbeitung (`data/` → `scripts/` → `docs/`) → GitHub Pages Publikation

## Daten

**Datensatz:** `data/db_networkCoPat_fake.rds`
- 137,990 Patentkooperationen
- ~134,000 eindeutige Firmen
- 96 Länder
- Zeitraum: 2010-2018
- Ungerichtetes, gewichtetes Netzwerk

Details: [knowledge/data.md](knowledge/data.md)

## Forschungsfragen

**Makroebene:** Welche Länder sind zentrale Akteure? Gibt es regionale Cluster?

**Mikroebene:** Welche Firmen fungieren als Brücken zwischen Ländern?

**Temporal:** Wie verändert sich die Netzwerkstruktur über Zeit?

Details: [knowledge/research.md](knowledge/research.md)

## Methodik

Dieses Projekt folgt der **Promptotyping-Methode** für LLM-gestützte Forschung.

Kernprinzip: Dokumentation ist die Quelle der Wahrheit, Code ist ein wiederverwendbares Artefakt.

Details: [knowledge/CLAUDE.md](knowledge/CLAUDE.md)

## Dokumentation

| Dokument | Inhalt |
|----------|--------|
| [knowledge/data.md](knowledge/data.md) | Datenstruktur, Variablen, Qualität |
| [knowledge/research.md](knowledge/research.md) | Forschungsfragen, Metriken, Python-Tooling |
| [knowledge/requirements.md](knowledge/requirements.md) | User Stories, Akzeptanzkriterien, Tech Stack |
| [knowledge/journal.md](knowledge/journal.md) | Entwicklungsprozess, Entscheidungen, Learnings |
| [scripts/README.md](scripts/README.md) | Skript-Dokumentation |

## Workflow

1. **Vorbereitung:** Lies `knowledge/` Dokumente
2. **Implementierung:** Entwickle Skripte basierend auf Dokumentation
3. **Validierung:** Verifiziere Ergebnisse
4. **Dokumentation:** Aktualisiere `journal.md` mit neuen Erkenntnissen

## Technologie-Stack

**Python 3.11+**

**Datenverarbeitung:** pandas, pyreadr

**Netzwerkanalyse:** NetworkX (Standard), igraph (optional für >100k Knoten)

**Community Detection:** python-louvain, leidenalg (optional)

**Visualisierung:** Matplotlib, Plotly, PyVis

**Publikation:** GitHub Pages (statische HTML, interaktive Plots)

## Hinweise

Dies ist ein **synthetischer Datensatz**.
