"""
Data Verification Script

Führt detaillierte Überprüfungen der RDS-Datei durch, um die Korrektheit
der Dokumentation zu verifizieren.

Prüfungen:
- Überprüfung ob owner1 und owner2 unterschiedlich sind
- Analyse der Länderverteilung
- Weight-Verteilung
- Jahr-Verteilung
- Netzwerktyp-Analyse (gerichtet vs. ungerichtet)

Verwendung:
    python scripts/verify_data.py

Voraussetzungen:
    pip install pyreadr pandas
"""

import pyreadr
import pandas as pd
from pathlib import Path

# RDS-Datei laden
rds_path = Path("data/db_networkCoPat_fake.rds")
result = pyreadr.read_r(str(rds_path))
df = result[None]

print("DETAILLIERTE ÜBERPRÜFUNG DER DOKUMENTATION")
print("=" * 80)

# 1. Überprüfung: Sind owner1 und owner2 wirklich unterschiedliche Personen?
print("\n1. KRITISCHE FRAGE: Sind owner1 und owner2 unterschiedlich?")
print("-" * 80)
same_owners = (df['owner1'] == df['owner2']).sum()
total_rows = len(df)
print(f"Anzahl Zeilen wo owner1 == owner2: {same_owners}")
print(f"Anzahl Zeilen wo owner1 != owner2: {total_rows - same_owners}")
print(f"Prozentsatz gleicher Owners: {same_owners/total_rows*100:.2f}%")

# 2. Beispiele anschauen
print("\n2. BEISPIELE mit gleichen Ownern:")
print("-" * 80)
same_owner_df = df[df['owner1'] == df['owner2']].head(10)
print(same_owner_df)

print("\n3. BEISPIELE mit unterschiedlichen Ownern:")
print("-" * 80)
diff_owner_df = df[df['owner1'] != df['owner2']].head(10)
print(diff_owner_df)

# 3. Überprüfung der Länder
print("\n4. LÄNDER-ANALYSE:")
print("-" * 80)
print(f"Gleiche Länder (country_1 == country_2): {(df['country_1'] == df['country_2']).sum()}")
print(f"Unterschiedliche Länder: {(df['country_1'] != df['country_2']).sum()}")

# 4. Was bedeutet die Interpretation wirklich?
print("\n5. INTERPRETATION DER DATEN:")
print("-" * 80)
print("Wenn owner1 == owner2, dann ist es KEIN Co-Ownership!")
print("Es wäre eher eine Zählung von Patenten PRO Owner")
print("")
print("Wenn owner1 != owner2, dann ist es echtes Co-Ownership")

# 5. Weight-Verteilung analysieren
print("\n6. WEIGHT-VERTEILUNG:")
print("-" * 80)
print(df['weight'].value_counts().sort_index())

# 6. Jahr-Verteilung
print("\n7. JAHR-VERTEILUNG:")
print("-" * 80)
print(df['year_application'].value_counts().sort_index())

# 7. Länder-Verteilung
print("\n8. TOP 20 LÄNDER (country_1):")
print("-" * 80)
print(df['country_1'].value_counts().head(20))

print("\n9. TOP 20 LÄNDER (country_2):")
print("-" * 80)
print(df['country_2'].value_counts().head(20))

# 8. Netzwerktyp prüfen
print("\n10. NETZWERKTYP-ANALYSE:")
print("-" * 80)
print("Ist das Netzwerk gerichtet oder ungerichtet?")
print("Prüfe: Gibt es sowohl (A->B) als auch (B->A)?")

# Erstelle eine sortierte Kombination für Vergleich
df['pair_sorted'] = df.apply(lambda x: tuple(sorted([x['owner1'], x['owner2']])), axis=1)
duplicated_pairs = df[df.duplicated(subset=['pair_sorted', 'year_application'], keep=False)]
print(f"Anzahl duplizierter Paare (beide Richtungen): {len(duplicated_pairs)}")

if len(duplicated_pairs) > 0:
    print("\nBeispiel für duplizierte Paare:")
    print(duplicated_pairs.head(10))
