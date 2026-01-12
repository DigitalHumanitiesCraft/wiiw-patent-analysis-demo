"""
RDS Data Explorer

Dieses Skript liest eine RDS-Datei (R Data Serialization) und zeigt eine
umfassende Übersicht über die enthaltenen Daten an.

Funktionen:
- Laden von RDS-Dateien mit pyreadr
- Anzeige von Datenstruktur, Datentypen und statistischen Zusammenfassungen
- Ausgabe von Beispieldaten

Verwendung:
    python scripts/explore_rds.py

Voraussetzungen:
    pip install pyreadr pandas
"""

import pyreadr
import pandas as pd
from pathlib import Path

# RDS-Datei laden
rds_path = Path("data/db_networkCoPat_fake.rds")
print(f"Exploring: {rds_path}")
print("=" * 80)

# RDS-Datei lesen
result = pyreadr.read_r(str(rds_path))

# Alle enthaltenen DataFrames anzeigen
print(f"\nAnzahl der DataFrames in der RDS-Datei: {len(result)}")
print(f"Keys: {list(result.keys())}\n")

# Für jeden DataFrame Informationen ausgeben
for key, df in result.items():
    print(f"\n{'=' * 80}")
    print(f"DataFrame: {key if key else 'Unnamed'}")
    print(f"{'=' * 80}")

    print(f"\nShape: {df.shape} (Zeilen: {df.shape[0]}, Spalten: {df.shape[1]})")

    print("\nSpalten und Datentypen:")
    print("-" * 80)
    for col in df.columns:
        dtype = df[col].dtype
        non_null = df[col].notna().sum()
        null_count = df[col].isna().sum()
        unique_count = df[col].nunique()
        print(f"  {col:30} | {str(dtype):15} | Non-Null: {non_null:6} | Null: {null_count:6} | Unique: {unique_count:6}")

    print("\nErste 5 Zeilen:")
    print("-" * 80)
    print(df.head())

    print("\nStatistische Zusammenfassung (nur numerische Spalten):")
    print("-" * 80)
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        print(df[numeric_cols].describe())
    else:
        print("Keine numerischen Spalten vorhanden")

    print("\nSample von 5 zufälligen Zeilen:")
    print("-" * 80)
    print(df.sample(min(5, len(df))))

print("\n" + "=" * 80)
print("Exploration abgeschlossen!")
print("=" * 80)
