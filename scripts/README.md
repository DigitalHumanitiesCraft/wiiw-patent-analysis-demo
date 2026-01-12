# Scripts Documentation

Dieses Verzeichnis enthält Python-Skripte zur Analyse der Patent-Netzwerkdaten.

## Übersicht

| Skript | Beschreibung | Verwendung |
|--------|--------------|------------|
| [explore_rds.py](explore_rds.py) | Explorative Datenanalyse der RDS-Datei | `python scripts/explore_rds.py` |
| [verify_data.py](verify_data.py) | Detaillierte Datenverifizierung und Qualitätsprüfung | `python scripts/verify_data.py` |

## Installation

Installiere die erforderlichen Python-Bibliotheken:

```bash
pip install pyreadr pandas
```

## Skript-Details

### explore_rds.py

**Zweck:** Erste Exploration und Übersicht über die RDS-Daten

**Ausgabe:**
- Anzahl und Struktur der DataFrames
- Spalten und Datentypen mit Null-Wert-Statistik
- Erste 5 Zeilen
- Statistische Zusammenfassung numerischer Spalten
- Zufällige Beispielzeilen

**Verwendung:**
```bash
python scripts/explore_rds.py
```

### verify_data.py

**Zweck:** Tiefgehende Verifizierung der Datenqualität und -eigenschaften

**Prüfungen:**
1. Owner-Beziehungen (owner1 vs owner2)
2. Länderverteilung und grenzüberschreitende Beziehungen
3. Weight-Verteilung
4. Zeitliche Verteilung (Jahre)
5. Netzwerktyp (gerichtet vs. ungerichtet)
6. Duplikate und Selbstverbindungen

**Verwendung:**
```bash
python scripts/verify_data.py
```

## Datenquelle

Beide Skripte arbeiten mit der Datei [../data/db_networkCoPat_fake.rds](../data/db_networkCoPat_fake.rds).

Die vollständige Dokumentation der Datenstruktur befindet sich in [../knowledge/data.md](../knowledge/data.md).

## Anforderungen

- Python 3.7+
- pyreadr 0.5.0+
- pandas 1.3.0+

## Hinweise

- Die Skripte müssen vom Root-Verzeichnis des Repositories ausgeführt werden
- Relative Pfade zu `data/` werden verwendet
- Alle Ausgaben erfolgen auf der Konsole
