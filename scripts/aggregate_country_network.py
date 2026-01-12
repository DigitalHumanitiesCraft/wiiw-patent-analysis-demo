"""
US-02: Aggregation auf Länderebene & Netzwerkanalyse

Dieses Skript:
1. Lädt die Patentkooperationsdaten auf Firmenebene
2. Aggregiert sie auf Länderebene (jährlich + kumulativ)
3. Erstellt NetworkX-Netzwerkobjekte
4. Berechnet Netzwerkmetriken (Degree Centrality, Communities, Globale Metriken)
5. Exportiert alles als JSON für Frontend-Visualisierung
6. Validiert die Ergebnisse

Output: docs/data/country_network.json
"""

import pyreadr
import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import networkx as nx
import community.community_louvain as louvain

# ================================================================================
# HELPER FUNCTIONS
# ================================================================================

def calculate_degree_centrality(G):
    """Berechnet gewichtete und ungewichtete Degree Centrality."""
    return {
        'degree': dict(G.degree()),                           # Ungewichtet
        'weighted_degree': dict(G.degree(weight='weight')),   # Gewichtet
        'degree_centrality': nx.degree_centrality(G)          # Normalisiert
    }


def detect_communities(G):
    """Louvain Community Detection."""
    if G.number_of_nodes() == 0:
        return {
            'partition': {},
            'modularity': 0.0,
            'num_communities': 0
        }

    # Louvain auf gewichtetem Netzwerk
    partition = louvain.best_partition(G, weight='weight')
    modularity = louvain.modularity(partition, G, weight='weight')

    return {
        'partition': partition,           # {country: community_id}
        'modularity': modularity,         # Qualitätsmaß
        'num_communities': len(set(partition.values()))
    }


def calculate_global_metrics(G):
    """Globale Netzwerk-Metriken."""
    if G.number_of_nodes() == 0:
        return {
            'num_nodes': 0,
            'num_edges': 0,
            'density': 0.0,
            'avg_clustering': 0.0,
            'transitivity': 0.0,
            'is_connected': False,
            'num_components': 0
        }

    return {
        'num_nodes': G.number_of_nodes(),
        'num_edges': G.number_of_edges(),
        'density': nx.density(G),
        'avg_clustering': nx.average_clustering(G, weight='weight'),
        'transitivity': nx.transitivity(G),
        'is_connected': nx.is_connected(G),
        'num_components': len(list(nx.connected_components(G)))
    }


def build_json_export(yearly_graphs, yearly_metrics, G_cumulative, cumulative_metrics):
    """Erstellt vollständige JSON-Struktur für Frontend."""

    def graph_to_dict(G, centrality_data, communities_data):
        """Helper: Graph zu Nodes/Edges-Liste."""
        nodes = []
        for node in G.nodes():
            nodes.append({
                'id': node,
                'degree': centrality_data['degree'].get(node, 0),
                'weighted_degree': centrality_data['weighted_degree'].get(node, 0.0),
                'degree_centrality': centrality_data['degree_centrality'].get(node, 0.0),
                'community': communities_data['partition'].get(node, -1)
            })

        edges = []
        for u, v, data in G.edges(data=True):
            edges.append({
                'source': u,
                'target': v,
                'weight': data['weight'],
                'num_firm_pairs': data.get('num_firm_pairs', 0)
            })

        return {'nodes': nodes, 'edges': edges}

    # Build structure
    output = {
        'metadata': {
            'generated': datetime.now().isoformat(),
            'source': 'db_networkCoPat_fake.rds',
            'num_countries': G_cumulative.number_of_nodes(),
            'years': list(range(2010, 2019)),
            'description': 'Country-level patent cooperation network with metrics'
        },

        'cumulative': {
            **graph_to_dict(
                G_cumulative,
                cumulative_metrics['centrality'],
                cumulative_metrics['communities']
            ),
            'metrics': cumulative_metrics['global']
        },

        'temporal': {}
    }

    # Add yearly data
    for year, G in yearly_graphs.items():
        output['temporal'][str(year)] = {
            **graph_to_dict(
                G,
                yearly_metrics[year]['centrality'],
                yearly_metrics[year]['communities']
            ),
            'metrics': yearly_metrics[year]['global']
        }

    return output


# ================================================================================
# MAIN SCRIPT
# ================================================================================

print("=" * 80)
print("LÄNDER-AGGREGATION & NETZWERKANALYSE")
print("=" * 80)
print()

# ================================================================================
# 1. DATENLADUNG
# ================================================================================

print("1. DATENLADUNG")
print("-" * 80)

rds_path = Path("data/db_networkCoPat_fake.rds")
print(f"Lade Daten aus: {rds_path}")

result = pyreadr.read_r(str(rds_path))
df = result[None]

print(f"[OK] Daten geladen: {len(df):,} Zeilen, {len(df.columns)} Spalten")
print()

# ================================================================================
# 2. LÄNDER-AGGREGATION
# ================================================================================

print("2. LÄNDER-AGGREGATION")
print("-" * 80)

# Original weight-Summe für Validierung
original_weight_sum = df['weight'].sum()
print(f"Original weight-Summe: {original_weight_sum:,}")

# Normalisiere Länderpaare (undirected network)
df_agg = df.copy()
df_agg['country_a'] = df_agg[['country_1', 'country_2']].min(axis=1)
df_agg['country_b'] = df_agg[['country_1', 'country_2']].max(axis=1)

# Aggregiere pro Jahr
print("Aggregiere pro Jahr...")
country_edges_yearly = df_agg.groupby(['year_application', 'country_a', 'country_b']).agg({
    'weight': 'sum',           # Summe der Kooperationen
    'owner1': 'count'          # Anzahl firm-pairs
}).rename(columns={'weight': 'total_weight', 'owner1': 'num_firm_pairs'}).reset_index()

print(f"[OK] Jährliche Aggregation: {len(country_edges_yearly):,} Länderpaare über alle Jahre")

# Kumulatives Netzwerk (alle Jahre)
print("Aggregiere kumulativ...")
country_edges_cumulative = df_agg.groupby(['country_a', 'country_b']).agg({
    'weight': 'sum',
    'owner1': 'count'
}).rename(columns={'weight': 'total_weight', 'owner1': 'num_firm_pairs'}).reset_index()

print(f"[OK] Kumulative Aggregation: {len(country_edges_cumulative):,} Länderpaare gesamt")

# Validierung: Weight-Summe
aggregated_weight_sum = country_edges_yearly['total_weight'].sum()
assert original_weight_sum == aggregated_weight_sum, f"Weight mismatch: {original_weight_sum} != {aggregated_weight_sum}"
print(f"[OK] Weight-Validierung: {original_weight_sum:,} = {aggregated_weight_sum:,}")
print()

# ================================================================================
# 3. NETZWERKOBJEKTE ERSTELLEN
# ================================================================================

print("3. NETZWERKOBJEKTE ERSTELLEN")
print("-" * 80)

# 3.1 Jährliche Netzwerke
yearly_graphs = {}
for year in range(2010, 2019):
    year_data = country_edges_yearly[country_edges_yearly['year_application'] == year]

    G = nx.Graph()
    for _, row in year_data.iterrows():
        G.add_edge(
            row['country_a'],
            row['country_b'],
            weight=row['total_weight'],
            num_firm_pairs=row['num_firm_pairs']
        )

    yearly_graphs[year] = G
    print(f"  {year}: {G.number_of_nodes()} Knoten, {G.number_of_edges()} Kanten")

print(f"[OK] {len(yearly_graphs)} jährliche Netzwerke erstellt")

# 3.2 Kumulatives Netzwerk
G_cumulative = nx.Graph()
for _, row in country_edges_cumulative.iterrows():
    G_cumulative.add_edge(
        row['country_a'],
        row['country_b'],
        weight=row['total_weight'],
        num_firm_pairs=row['num_firm_pairs']
    )

print(f"[OK] Kumulatives Netzwerk: {G_cumulative.number_of_nodes()} Knoten, {G_cumulative.number_of_edges()} Kanten")
print()

# ================================================================================
# 4. METRIKEN BERECHNEN
# ================================================================================

print("4. METRIKEN BERECHNEN")
print("-" * 80)

# Pro Jahr
print("Berechne Metriken für jedes Jahr...")
yearly_metrics = {}
for year, G in yearly_graphs.items():
    yearly_metrics[year] = {
        'centrality': calculate_degree_centrality(G),
        'communities': detect_communities(G),
        'global': calculate_global_metrics(G)
    }

    communities_info = yearly_metrics[year]['communities']
    global_info = yearly_metrics[year]['global']
    print(f"  {year}: {communities_info['num_communities']} Communities, "
          f"Modularity={communities_info['modularity']:.3f}, "
          f"Density={global_info['density']:.3f}")

print(f"[OK] Metriken für {len(yearly_metrics)} Jahre berechnet")

# Kumulativ
print("Berechne kumulative Metriken...")
cumulative_metrics = {
    'centrality': calculate_degree_centrality(G_cumulative),
    'communities': detect_communities(G_cumulative),
    'global': calculate_global_metrics(G_cumulative)
}

print(f"[OK] Kumulative Metriken: "
      f"{cumulative_metrics['communities']['num_communities']} Communities, "
      f"Modularity={cumulative_metrics['communities']['modularity']:.3f}, "
      f"Density={cumulative_metrics['global']['density']:.3f}")
print()

# ================================================================================
# 5. JSON-EXPORT
# ================================================================================

print("5. JSON-EXPORT")
print("-" * 80)

output_dir = Path("docs/data")
output_dir.mkdir(parents=True, exist_ok=True)

print("Erstelle JSON-Struktur...")
json_data = build_json_export(yearly_graphs, yearly_metrics, G_cumulative, cumulative_metrics)

json_path = output_dir / "country_network.json"
print(f"Exportiere nach: {json_path}")

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)

# Dateigröße
file_size_kb = json_path.stat().st_size / 1024
print(f"[OK] JSON exportiert: {file_size_kb:.1f} KB")
print()

# ================================================================================
# 6. VALIDIERUNG
# ================================================================================

print("6. VALIDIERUNG")
print("-" * 80)

# 6.1 Weight-Summe (bereits oben)
print(f"[OK] Weight-Summe: {original_weight_sum:,} = {aggregated_weight_sum:,}")

# 6.2 Länder-Anzahl
countries_in_data = set(df['country_1']).union(set(df['country_2']))
countries_in_graph = set(G_cumulative.nodes())
assert countries_in_data == countries_in_graph, "Country mismatch"
print(f"[OK] Länder-Validierung: {len(countries_in_graph)} Länder")

# 6.3 JSON-Struktur
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

assert 'metadata' in data, "Missing metadata"
assert 'cumulative' in data, "Missing cumulative"
assert 'temporal' in data, "Missing temporal"
assert '2010' in data['temporal'], "Missing 2010"
assert '2018' in data['temporal'], "Missing 2018"
print(f"[OK] JSON-Struktur: Alle erforderlichen Felder vorhanden")

# 6.4 Metadata-Check
assert data['metadata']['num_countries'] == len(countries_in_graph), "Metadata country count mismatch"
assert len(data['cumulative']['nodes']) == len(countries_in_graph), "Node count mismatch"
print(f"[OK] Metadata-Validierung: {data['metadata']['num_countries']} Länder in Metadata")

print()

# ================================================================================
# ZUSAMMENFASSUNG
# ================================================================================

print("=" * 80)
print("ZUSAMMENFASSUNG")
print("=" * 80)
print()

print(f"INPUT:")
print(f"  - Datenquelle: {rds_path}")
print(f"  - Firmen-Level Kooperationen: {len(df):,}")
print(f"  - Zeitraum: {df['year_application'].min()}-{df['year_application'].max()}")
print()

print(f"AGGREGATION:")
print(f"  - Länder identifiziert: {len(countries_in_graph)}")
print(f"  - Länderpaare (kumulativ): {len(country_edges_cumulative):,}")
print(f"  - Länderpaare (über alle Jahre): {len(country_edges_yearly):,}")
print()

print(f"NETZWERKMETRIKEN (kumulativ):")
print(f"  - Knoten: {cumulative_metrics['global']['num_nodes']}")
print(f"  - Kanten: {cumulative_metrics['global']['num_edges']}")
print(f"  - Dichte: {cumulative_metrics['global']['density']:.3f}")
print(f"  - Communities: {cumulative_metrics['communities']['num_communities']}")
print(f"  - Modularity: {cumulative_metrics['communities']['modularity']:.3f}")
print(f"  - Verbunden: {cumulative_metrics['global']['is_connected']}")
print(f"  - Komponenten: {cumulative_metrics['global']['num_components']}")
print()

print(f"TOP-5 LÄNDER (nach gewichtetem Degree):")
top_countries = sorted(
    cumulative_metrics['centrality']['weighted_degree'].items(),
    key=lambda x: x[1],
    reverse=True
)[:5]
for i, (country, degree) in enumerate(top_countries, 1):
    community = cumulative_metrics['communities']['partition'].get(country, -1)
    print(f"  {i}. {country}: {degree:.0f} (Community {community})")
print()

print(f"OUTPUT:")
print(f"  - {json_path}")
print(f"  - Dateigröße: {file_size_kb:.1f} KB")
print()

print("=" * 80)
print("FERTIG!")
print("=" * 80)
