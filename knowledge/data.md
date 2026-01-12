# Datendokumentation: db_networkCoPat_fake.rds

## Übersicht

**Dateipfad:** `data/db_networkCoPat_fake.rds`
**Dateigröße:** ~2.8 MB
**Format:** RDS (R Data Serialization)
**Anzahl Datensätze:** 137,990 Zeilen
**Anzahl Spalten:** 6

## Beschreibung

Diese Datei enthält ein Patent-Netzwerk mit Verbindungen zwischen verschiedenen Patent-Inhabern (Ownern). Jede Zeile repräsentiert eine gewichtete Beziehung zwischen zwei unterschiedlichen Patent-Inhabern. Die genaue Bedeutung der Beziehung (Co-Ownership, Zitation, Technologietransfer, etc.) muss aus dem Kontext oder der Datenquelle ermittelt werden.

## Datenstruktur

### Spalten

| Spalte | Datentyp | Beschreibung | Unique Values | Null-Werte |
|--------|----------|--------------|---------------|------------|
| `year_application` | float64 | Jahr der Patentanmeldung | 9 (2010-2018) | 0 |
| `owner1` | object | ID des ersten Patent-Inhabers | 134,455 | 0 |
| `country_1` | object | Land des ersten Inhabers | 96 | 0 |
| `owner2` | object | ID des zweiten Patent-Inhabers | 134,468 | 0 |
| `country_2` | object | Land des zweiten Inhabers | 92 | 0 |
| `weight` | float64 | Gewichtung/Stärke der Verbindung | 14 (1-14) | 0 |

### Zeitraum

- **Minimum Jahr:** 2010
- **Maximum Jahr:** 2018
- **Median Jahr:** 2014
- **Durchschnitt:** 2014.0

### Gewichtung (Weight)

- **Minimum:** 1.0
- **Maximum:** 14.0
- **Median:** 4.0
- **Durchschnitt:** 3.91
- **Verteilung:** Stark rechtsschief, die meisten Werte liegen zwischen 2-5
- **Interpretation:** Die Gewichtung repräsentiert vermutlich die Stärke oder Intensität der Beziehung zwischen den beiden Inhabern (z.B. Anzahl gemeinsamer Patente, Häufigkeit der Zusammenarbeit, etc.)

### Länder

- **Anzahl unterschiedlicher Länder (Owner1):** 96
- **Anzahl unterschiedlicher Länder (Owner2):** 92
- **Grenzüberschreitende Beziehungen:** 99.15% (136,823 von 137,990)
- **Innerhalb desselben Landes:** 0.85% (1,167 von 137,990)
- **Top Länder (Owner1):** ID, TW, MO, FI, TR, SK, UA, SE, IN, FR
- **Top Länder (Owner2):** AE, UY, HK, PY, CR, NO, ZW, TZ, SE, IE
- **Verteilung:** Relativ gleichmäßig über viele Länder verteilt

## Netzwerkstruktur

- **Knoten:** Patent-Inhaber (Owner IDs) - ca. 134,455-134,468 eindeutige Inhaber
- **Kanten:** Beziehungen zwischen Inhabern (137,990 Verbindungen)
- **Kantengewicht:** Stärke der Beziehung (1-14)
- **Netzwerktyp:** Ungerichtetes Netzwerk (keine duplizierten Paare gefunden)
- **Eigenschaft:** Alle Kanten verbinden unterschiedliche Owner (keine Selbstverbindungen)
- **Internationalität:** Stark grenzüberschreitend (99.15% internationale Verbindungen)

## Beispieldaten

```
year_application | owner1          | country_1 | owner2          | country_2 | weight
2013.0          | QA3470001011260 | IN        | different_owner | different | 5.0
2011.0          | AT1341110434146 | MC        | different_owner | different | 4.0
2017.0          | SG000849327     | JP        | different_owner | different | 4.0
```

**Hinweis:** Alle 137,990 Zeilen enthalten unterschiedliche Owner-Paare (owner1 ≠ owner2).

## Verwendungszweck

Diese Daten eignen sich für:
- Netzwerkanalyse von Patent-Inhabern und deren Beziehungen
- Identifikation von Kooperations-Clustern und Communities
- Internationale Innovations-Netzwerke und grenzüberschreitende Zusammenarbeit
- Zeitliche Entwicklung von Patent-Beziehungen (2010-2018)
- Graph-Visualisierung und Social Network Analysis (SNA)
- Zentrale Akteure und Influencer im Patent-Netzwerk identifizieren

## Technische Hinweise

- Datei kann mit `pyreadr` in Python gelesen werden
- Alternative: Laden in R mit `readRDS()`
- Keine fehlenden Werte (vollständiger Datensatz)
- Owner-IDs sind alphanumerisch und variieren in der Länge

## Verfügbare Analyse-Skripte

Siehe [../scripts/README.md](../scripts/README.md) für Details zu den Python-Skripten:

- [scripts/explore_rds.py](../scripts/explore_rds.py) - Explorative Datenanalyse
- [scripts/verify_data.py](../scripts/verify_data.py) - Datenverifizierung und Qualitätsprüfung
