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
data/         RDS-Daten (synthetischer Datensatz)
scripts/      Python-Analyseskripte
knowledge/    Promptotyping-Dokumentation
plots/        Visualisierungen (generiert)
reports/      Ergebnisse und Berichte (generiert)
```

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
| [knowledge/research.md](knowledge/research.md) | Forschungsfragen, Metriken, Tooling |
| [knowledge/journal.md](knowledge/journal.md) | Entwicklungsprozess, Entscheidungen, Learnings |
| [scripts/README.md](scripts/README.md) | Skript-Dokumentation |

## Workflow

1. **Vorbereitung:** Lies `knowledge/` Dokumente
2. **Implementierung:** Entwickle Skripte basierend auf Dokumentation
3. **Validierung:** Verifiziere Ergebnisse
4. **Dokumentation:** Aktualisiere `journal.md` mit neuen Erkenntnissen

## Technologie-Stack

**Datenverarbeitung:** Python, pandas, pyreadr

**Netzwerkanalyse:** NetworkX, igraph (optional für Performance)

**Visualisierung:** Matplotlib, Plotly, PyVis

## Hinweise

Dies ist ein **synthetischer Datensatz** für Cloud-basierte Entwicklung. Echte Daten verbleiben lokal.

Alle Analysen sind reproduzierbar. Skripte dokumentieren ihre Abhängigkeiten und Verwendung.
