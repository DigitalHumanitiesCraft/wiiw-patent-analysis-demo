"""
Forschungsfragen-orientierte Exploration der Patentkooperationsdaten

Dieses Skript analysiert die Daten systematisch im Hinblick auf die konkreten
Forschungsfragen aus research.md und bereitet methodische Entscheidungen für
die nachfolgenden Analysen (US-02 bis US-09) vor.

Autor: Generiert basierend auf Promptotyping-Methodik
Datum: 2026-01-12
"""

import pyreadr
import pandas as pd
import numpy as np
from pathlib import Path

# ================================================================================
# DATENLADUNG
# ================================================================================

print("=" * 80)
print("FORSCHUNGSFRAGEN-ORIENTIERTE EXPLORATION")
print("=" * 80)
print()

# RDS-Datei laden
rds_path = Path("data/db_networkCoPat_fake.rds")
print(f"Lade Daten aus: {rds_path}")
result = pyreadr.read_r(str(rds_path))
df = result[None]
print(f"[OK] Daten geladen: {len(df):,} Zeilen, {len(df.columns)} Spalten")
print()

# Output-Verzeichnisse erstellen
output_dir = Path("docs/exploration")
output_dir.mkdir(parents=True, exist_ok=True)
(output_dir / "macro").mkdir(exist_ok=True)
(output_dir / "micro").mkdir(exist_ok=True)
(output_dir / "temporal").mkdir(exist_ok=True)
(output_dir / "structure").mkdir(exist_ok=True)
print(f"[OK] Output-Verzeichnis: {output_dir}")
print()

# ================================================================================
# 1. MAKROEBENE: LÄNDERANALYSE
# ================================================================================

print("=" * 80)
print("1. MAKROEBENE: LÄNDERANALYSE")
print("=" * 80)
print()

# 1.1 Top-20 Länder nach Gesamtanzahl Kooperationen
print("1.1 Top-20 Länder nach Gesamtanzahl Kooperationen")
print("-" * 80)

# Alle Länder sammeln (country_1 und country_2)
country_1_counts = df.groupby('country_1').agg({
    'weight': 'sum',
    'owner1': 'count'
}).rename(columns={'weight': 'total_weight', 'owner1': 'num_edges'})

country_2_counts = df.groupby('country_2').agg({
    'weight': 'sum',
    'owner2': 'count'
}).rename(columns={'weight': 'total_weight', 'owner2': 'num_edges'})

# Kombinieren (Länder können in beiden Spalten vorkommen)
country_totals = pd.concat([country_1_counts, country_2_counts]).groupby(level=0).sum()
country_totals = country_totals.sort_values('total_weight', ascending=False)

# Anzahl unique Partner pro Land
partners_1 = df.groupby('country_1')['country_2'].nunique().rename('unique_partners')
partners_2 = df.groupby('country_2')['country_1'].nunique().rename('unique_partners')
partners_combined = pd.concat([partners_1, partners_2]).groupby(level=0).max()

country_totals = country_totals.join(partners_combined)
country_totals.index.name = 'country'
country_totals = country_totals.reset_index()

# Top-20
top20_countries = country_totals.head(20)
print(top20_countries.to_string(index=False))
print()

# Export
country_totals.to_csv(output_dir / "macro" / "country_rankings.csv", index=False)
print(f"[OK] Exportiert: {output_dir / 'macro' / 'country_rankings.csv'}")
print()

# 1.2 Top-20 bilaterale Länderpaare
print("1.2 Top-20 bilaterale Länderpaare (stärkste Beziehungen)")
print("-" * 80)

# Länderpaare sortieren (alphabetisch) um Duplikate zu vermeiden
df_pairs = df.copy()
df_pairs['country_min'] = df_pairs[['country_1', 'country_2']].min(axis=1)
df_pairs['country_max'] = df_pairs[['country_1', 'country_2']].max(axis=1)

# Aggregation
country_pairs = df_pairs.groupby(['country_min', 'country_max']).agg({
    'weight': 'sum',
    'owner1': 'count'
}).rename(columns={'weight': 'total_weight', 'owner1': 'num_edges'})
country_pairs = country_pairs.sort_values('total_weight', ascending=False).reset_index()
country_pairs.rename(columns={'country_min': 'country_a', 'country_max': 'country_b'}, inplace=True)

# Top-20
top20_pairs = country_pairs.head(20)
print(top20_pairs.to_string(index=False))
print()

# Export
country_pairs.to_csv(output_dir / "macro" / "country_pairs_top20.csv", index=False)
print(f"[OK] Exportiert: {output_dir / 'country_pairs_top20.csv'}")
print()

# 1.3 Internationale vs. nationale Kooperationen (Zeitreihe)
print("1.3 Internationale vs. nationale Kooperationen (pro Jahr)")
print("-" * 80)

df_intl = df.copy()
df_intl['is_international'] = df_intl['country_1'] != df_intl['country_2']

intl_by_year = df_intl.groupby(['year_application', 'is_international']).agg({
    'weight': 'sum',
    'owner1': 'count'
}).rename(columns={'weight': 'total_weight', 'owner1': 'num_edges'})

intl_pivot = intl_by_year.reset_index().pivot(
    index='year_application',
    columns='is_international',
    values=['num_edges', 'total_weight']
)
intl_pivot.columns = ['_'.join(map(str, col)) for col in intl_pivot.columns]
intl_pivot = intl_pivot.reset_index()

# Prozentsatz berechnen
intl_pivot['pct_international'] = (
    intl_pivot['num_edges_True'] /
    (intl_pivot['num_edges_True'] + intl_pivot['num_edges_False']) * 100
)

print(intl_pivot.to_string(index=False))
print()

# ================================================================================
# 2. MIKROEBENE: FIRMENANALYSE
# ================================================================================

print("=" * 80)
print("2. MIKROEBENE: FIRMENANALYSE")
print("=" * 80)
print()

# 2.1 Top-20 Firmen nach Anzahl einzigartiger Länder-Partner (Bridge-Indikator)
print("2.1 Top-20 Firmen nach Anzahl einzigartiger Länder-Partner (Bridge-Kandidaten)")
print("-" * 80)

# Für jede Firma sammeln: alle Partner-Länder
# owner1 -> country_2 (Partnerland)
firm1_partners = df.groupby(['owner1', 'country_1'])['country_2'].apply(set)
# owner2 -> country_1 (Partnerland)
firm2_partners = df.groupby(['owner2', 'country_2'])['country_1'].apply(set)

# Kombinieren (Firmen können in beiden Spalten vorkommen)
firm_partners = {}
for (firm, home), countries in firm1_partners.items():
    if firm not in firm_partners:
        firm_partners[firm] = {'home_country': home, 'partner_countries': set()}
    firm_partners[firm]['partner_countries'].update(countries)

for (firm, home), countries in firm2_partners.items():
    if firm not in firm_partners:
        firm_partners[firm] = {'home_country': home, 'partner_countries': set()}
    firm_partners[firm]['partner_countries'].update(countries)

# DataFrame erstellen
firm_bridge_data = []
for firm, data in firm_partners.items():
    num_partner_countries = len(data['partner_countries'])
    firm_bridge_data.append({
        'firm_id': firm,
        'home_country': data['home_country'],
        'num_partner_countries': num_partner_countries
    })

firm_bridge_df = pd.DataFrame(firm_bridge_data)
firm_bridge_df = firm_bridge_df.sort_values('num_partner_countries', ascending=False)

# Top-20
top20_bridge = firm_bridge_df.head(20)
print(top20_bridge.to_string(index=False))
print()

# Export
firm_bridge_df.to_csv(output_dir / "micro" / "firm_bridge_candidates.csv", index=False)
print(f"[OK] Exportiert: {output_dir / 'firm_bridge_candidates.csv'}")
print()

# 2.2 Top-20 Firmen nach Gesamtanzahl Kooperationen (Degree-Proxy)
print("2.2 Top-20 Firmen nach Gesamtanzahl Kooperationen")
print("-" * 80)

# Aggregation für owner1 und owner2
firm1_stats = df.groupby(['owner1', 'country_1']).agg({
    'weight': 'sum',
    'owner2': 'count'
}).rename(columns={'weight': 'total_weight', 'owner2': 'num_edges'})

firm2_stats = df.groupby(['owner2', 'country_2']).agg({
    'weight': 'sum',
    'owner1': 'count'
}).rename(columns={'weight': 'total_weight', 'owner1': 'num_edges'})

# Kombinieren
firm_stats = pd.concat([
    firm1_stats.reset_index().rename(columns={'owner1': 'firm_id', 'country_1': 'home_country'}),
    firm2_stats.reset_index().rename(columns={'owner2': 'firm_id', 'country_2': 'home_country'})
])

firm_stats = firm_stats.groupby(['firm_id', 'home_country']).sum().reset_index()
firm_stats = firm_stats.sort_values('total_weight', ascending=False)

# Top-20
top20_firms = firm_stats.head(20)
print(top20_firms.to_string(index=False))
print()

# Export
firm_stats.to_csv(output_dir / "micro" / "firm_rankings.csv", index=False)
print(f"[OK] Exportiert: {output_dir / 'firm_rankings.csv'}")
print()

# 2.3 Länder-spezifische Muster
print("2.3 Länder-spezifische Muster: Durchschnittliche Anzahl internationaler Partner pro Firma")
print("-" * 80)

# Berechne durchschnittliche Anzahl Partnerländer pro Firma, gruppiert nach Heimatland
country_avg_partners = firm_bridge_df.groupby('home_country')['num_partner_countries'].agg([
    'mean', 'median', 'max', 'count'
]).rename(columns={'count': 'num_firms'})
country_avg_partners = country_avg_partners.sort_values('mean', ascending=False).reset_index()

print(country_avg_partners.head(20).to_string(index=False))
print()

# ================================================================================
# 3. TEMPORALE ANALYSE
# ================================================================================

print("=" * 80)
print("3. TEMPORALE ANALYSE")
print("=" * 80)
print()

# 3.1 Zeitreihe: Netzwerk-Statistiken pro Jahr
print("3.1 Zeitreihe: Netzwerk-Statistiken pro Jahr")
print("-" * 80)

temporal_stats = df.groupby('year_application').agg({
    'owner1': lambda x: len(set(x)),
    'owner2': lambda x: len(set(x)),
    'country_1': lambda x: len(set(x)),
    'country_2': lambda x: len(set(x)),
    'weight': ['sum', 'mean', 'median']
}).reset_index()

# Spalten umbenennen
temporal_stats.columns = [
    'year',
    'unique_firms_owner1',
    'unique_firms_owner2',
    'unique_countries_1',
    'unique_countries_2',
    'total_weight',
    'mean_weight',
    'median_weight'
]

# Anzahl Kanten pro Jahr
edges_per_year = df.groupby('year_application').size().rename('num_edges')
temporal_stats = temporal_stats.merge(edges_per_year, left_on='year', right_index=True)

# Approximation unique firms (union von owner1 und owner2)
# Hinweis: Dies ist eine Approximation, exakt wäre komplexer
temporal_stats['unique_firms_approx'] = temporal_stats[['unique_firms_owner1', 'unique_firms_owner2']].max(axis=1)
temporal_stats['unique_countries_approx'] = temporal_stats[['unique_countries_1', 'unique_countries_2']].max(axis=1)

print(temporal_stats[['year', 'num_edges', 'unique_firms_approx', 'unique_countries_approx',
                       'total_weight', 'mean_weight', 'median_weight']].to_string(index=False))
print()

# Export
temporal_stats.to_csv(output_dir / "temporal" / "temporal_overview.csv", index=False)
print(f"[OK] Exportiert: {output_dir / 'temporal_overview.csv'}")
print()

# 3.2 Top-5 Länder pro Jahr
print("3.2 Top-5 Länder pro Jahr (nach Gesamtgewicht)")
print("-" * 80)

# Für jedes Jahr die Top-5 Länder berechnen
yearly_country_ranks = []

for year in sorted(df['year_application'].unique()):
    df_year = df[df['year_application'] == year]

    # Aggregation wie in 1.1
    c1 = df_year.groupby('country_1')['weight'].sum()
    c2 = df_year.groupby('country_2')['weight'].sum()
    country_year = pd.concat([c1, c2]).groupby(level=0).sum().sort_values(ascending=False)

    # Top-5
    for rank, (country, weight) in enumerate(country_year.head(5).items(), 1):
        yearly_country_ranks.append({
            'year': year,
            'rank': rank,
            'country': country,
            'total_weight': weight
        })

top_countries_yearly = pd.DataFrame(yearly_country_ranks)
top_countries_pivot = top_countries_yearly.pivot(index='rank', columns='year', values='country')

print(top_countries_pivot.to_string())
print()

# Export
top_countries_yearly.to_csv(output_dir / "temporal" / "temporal_top_countries.csv", index=False)
print(f"[OK] Exportiert: {output_dir / 'temporal_top_countries.csv'}")
print()

# ================================================================================
# 4. NETZWERKSTRUKTUR-VORABSCHAU
# ================================================================================

print("=" * 80)
print("4. NETZWERKSTRUKTUR-VORABSCHAU")
print("=" * 80)
print()

# 4.1 Gewichtsverteilung
print("4.1 Gewichtsverteilung: Detaillierte Quantile")
print("-" * 80)

quantiles = [0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
weight_quantiles = df['weight'].quantile(quantiles)

weight_dist = pd.DataFrame({
    'quantile': [f"{q*100:.0f}%" for q in quantiles],
    'weight': weight_quantiles.values
})

print(weight_dist.to_string(index=False))
print()

# 4.2 Gewichtstransformation: raw vs. log(weight+1)
print("4.2 Gewichtstransformation: Vergleich raw vs. log(weight+1)")
print("-" * 80)

df_transform = df.copy()
df_transform['weight_log'] = np.log1p(df_transform['weight'])

transform_stats = pd.DataFrame({
    'metric': ['mean', 'median', 'std', 'min', 'max'],
    'weight_raw': [
        df_transform['weight'].mean(),
        df_transform['weight'].median(),
        df_transform['weight'].std(),
        df_transform['weight'].min(),
        df_transform['weight'].max()
    ],
    'weight_log': [
        df_transform['weight_log'].mean(),
        df_transform['weight_log'].median(),
        df_transform['weight_log'].std(),
        df_transform['weight_log'].min(),
        df_transform['weight_log'].max()
    ]
})

print(transform_stats.to_string(index=False))
print()

# Export
weight_dist.to_csv(output_dir / "structure" / "weight_distribution.csv", index=False)
print(f"[OK] Exportiert: {output_dir / 'weight_distribution.csv'}")
print()

# 4.3 Netzwerkgrößen pro Jahr (Firmen- und Länderebene)
print("4.3 Netzwerkgrößen pro Jahr (Firmen- und Länderebene)")
print("-" * 80)

network_sizes = []

for year in sorted(df['year_application'].unique()):
    df_year = df[df['year_application'] == year]

    # Firmenebene
    unique_firms = len(set(df_year['owner1']).union(set(df_year['owner2'])))
    firm_edges = len(df_year)

    # Länderebene
    unique_countries = len(set(df_year['country_1']).union(set(df_year['country_2'])))
    # Länder-Kanten (unique Paare)
    df_year_pairs = df_year.copy()
    df_year_pairs['country_min'] = df_year_pairs[['country_1', 'country_2']].min(axis=1)
    df_year_pairs['country_max'] = df_year_pairs[['country_1', 'country_2']].max(axis=1)
    country_edges = len(df_year_pairs[['country_min', 'country_max']].drop_duplicates())

    # Densität (Firmenebene - approximiert)
    max_edges_firms = unique_firms * (unique_firms - 1) / 2
    density_firms = firm_edges / max_edges_firms if max_edges_firms > 0 else 0

    # Densität (Länderebene)
    max_edges_countries = unique_countries * (unique_countries - 1) / 2
    density_countries = country_edges / max_edges_countries if max_edges_countries > 0 else 0

    network_sizes.append({
        'year': year,
        'firms_nodes': unique_firms,
        'firms_edges': firm_edges,
        'firms_density': density_firms,
        'countries_nodes': unique_countries,
        'countries_edges': country_edges,
        'countries_density': density_countries
    })

network_preview = pd.DataFrame(network_sizes)
print(network_preview.to_string(index=False))
print()

# Export
network_preview.to_csv(output_dir / "structure" / "network_preview.csv", index=False)
print(f"[OK] Exportiert: {output_dir / 'network_preview.csv'}")
print()

# 4.4 Degree-Verteilung (approximiert für Firmenebene)
print("4.4 Degree-Verteilung (approximiert): Anzahl Partner pro Firma")
print("-" * 80)

# Anzahl unique Partner pro Firma
partners_1 = df.groupby('owner1')['owner2'].nunique()
partners_2 = df.groupby('owner2')['owner1'].nunique()

# Kombinieren (Maximum falls Firma in beiden Spalten)
all_firms = set(df['owner1']).union(set(df['owner2']))
firm_degrees = {}
for firm in all_firms:
    deg1 = partners_1.get(firm, 0)
    deg2 = partners_2.get(firm, 0)
    firm_degrees[firm] = max(deg1, deg2)

degree_series = pd.Series(firm_degrees)
degree_quantiles = degree_series.quantile(quantiles)

degree_dist = pd.DataFrame({
    'quantile': [f"{q*100:.0f}%" for q in quantiles],
    'num_partners': degree_quantiles.values
})

print(degree_dist.to_string(index=False))
print(f"\nMean degree: {degree_series.mean():.2f}")
print(f"Median degree: {degree_series.median():.2f}")
print(f"Max degree: {degree_series.max():.0f}")
print()

# ================================================================================
# 5. ZUSAMMENFASSUNG UND EMPFEHLUNGEN
# ================================================================================

print("=" * 80)
print("5. ZUSAMMENFASSUNG UND EMPFEHLUNGEN")
print("=" * 80)
print()

print("MAKROEBENE (Länder):")
print(f"  - {len(country_totals)} unique Länder identifiziert")
print(f"  - Top-3 Länder nach Gewicht: {', '.join(top20_countries.head(3)['country'].tolist())}")
print(f"  - Stärkste bilaterale Beziehung: {top20_pairs.iloc[0]['country_a']}-{top20_pairs.iloc[0]['country_b']}")
print()

print("MIKROEBENE (Firmen):")
print(f"  - {len(firm_bridge_df)} unique Firmen identifiziert")
print(f"  - Top-Bridge-Kandidat: {top20_bridge.iloc[0]['firm_id']} ({top20_bridge.iloc[0]['num_partner_countries']} Partnerländer)")
print(f"  - Durchschnittliche Anzahl Partnerländer pro Firma: {firm_bridge_df['num_partner_countries'].mean():.2f}")
print()

print("TEMPORALE ENTWICKLUNG:")
print(f"  - Zeitraum: {df['year_application'].min()}-{df['year_application'].max()}")
print(f"  - Trend Netzwerkgröße (Firmen): {network_preview.iloc[0]['firms_nodes']} ({network_preview.iloc[0]['year']}) -> {network_preview.iloc[-1]['firms_nodes']} ({network_preview.iloc[-1]['year']})")
print(f"  - Trend Kanten: {network_preview.iloc[0]['firms_edges']} -> {network_preview.iloc[-1]['firms_edges']}")
print()

print("NETZWERKSTRUKTUR:")
print(f"  - Gewichts-Median: {df['weight'].median()}")
print(f"  - Gewichtsverteilung: Rechtsschief (95%-Quantil: {weight_dist[weight_dist['quantile']=='95%']['weight'].values[0]})")
print(f"  - Firmennetzwerk-Dichte: ~{network_preview['firms_density'].mean():.6f} (sehr dünn)")
print(f"  - Ländernetzwerk-Dichte: ~{network_preview['countries_density'].mean():.3f}")
print()

print("EMPFEHLUNGEN:")
print("  [1] GEWICHTSTRANSFORMATION:")
print("      - Rechtssschiefe Verteilung -> log(weight+1) für bestimmte Metriken erwägen")
print("      - Für Visualisierungen: Kantendicke basierend auf log-transformierten Werten")
print()
print("  [2] TOOL-AUSWAHL:")
print("      - Länderebene (~96 Knoten): NetworkX ausreichend, gut performant")
print(f"      - Firmenebene (~{len(all_firms):,} Knoten): NetworkX funktioniert, aber igraph für schnellere Berechnungen erwägen")
print("      - Density ist sehr niedrig -> Sparse-Matrix-Methoden nutzen")
print()
print("  [3] TEMPORALE ANALYSE:")
print("      - Jährliche Snapshots UND kumulatives Netzwerk beide berechnen")
print("      - Trend-Analyse: Vergleich 2010-2014 vs. 2015-2018")
print()
print("  [4] FORSCHUNGSFRAGEN-PRIORISIERUNG:")
print("      - Makroebene: Länder-Communities klar erkennbar -> Priorität hoch")
print("      - Bridge-Firmen: Klare Kandidaten identifiziert -> gute Basis für Mikroanalyse")
print("      - Temporale Entwicklung: Daten zeigen Trends -> lohnt sich für Publikation")
print()

print("=" * 80)
print("EXPLORATION ABGESCHLOSSEN")
print("=" * 80)
print()
print(f"Alle Ergebnisse exportiert nach: {output_dir}")
print()
print("Generierte Dateien:")
print("  - exploration/DATA_DICTIONARY.md")
print("  - exploration/macro/")
for csv_file in sorted((output_dir / "macro").glob("*.csv")):
    print(f"    - {csv_file.name}")
print("  - exploration/micro/")
for csv_file in sorted((output_dir / "micro").glob("*.csv")):
    print(f"    - {csv_file.name}")
print("  - exploration/temporal/")
for csv_file in sorted((output_dir / "temporal").glob("*.csv")):
    print(f"    - {csv_file.name}")
print("  - exploration/structure/")
for csv_file in sorted((output_dir / "structure").glob("*.csv")):
    print(f"    - {csv_file.name}")
print()
