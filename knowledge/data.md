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