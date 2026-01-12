"""
Umfassende Validierung der country_network.json Datei

Prüft:
- Struktur-Vollständigkeit
- Wertebereich-Korrektheit
- Konsistenz zwischen Feldern
- Temporal-Konsistenz
- Edge-Validität
"""

import json
import sys
from pathlib import Path

# Windows encoding fix
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print('='*80)
print('UMFASSENDE JSON-VALIDIERUNG')
print('='*80)
print()

# JSON laden
json_path = Path('docs/data/country_network.json')
print(f'Lade: {json_path}')
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
print(f'[OK] JSON geladen')
print()

errors = []

# ============================================================================
# 1. STRUKTUR-CHECKS
# ============================================================================

print('1. STRUKTUR-CHECKS')
print('-'*80)

# Top-Level Keys
required_keys = ['metadata', 'cumulative', 'temporal']
for key in required_keys:
    status = '✓' if key in data else '✗'
    print(f'{status} {key}')
    if key not in data:
        errors.append(f'Fehlendes Top-Level-Feld: {key}')

# Metadata
metadata_keys = ['generated', 'source', 'num_countries', 'years', 'description']
print(f'\nMetadata Felder:')
for key in metadata_keys:
    status = '✓' if key in data['metadata'] else '✗'
    print(f'  {status} {key}')
    if key not in data['metadata']:
        errors.append(f'Fehlendes Metadata-Feld: {key}')

# Temporal Jahre
years_expected = [str(y) for y in range(2010, 2019)]
years_found = sorted(data['temporal'].keys())
print(f'\nTemporale Jahre: {years_found}')
print(f'Erwartete Jahre: {years_expected}')
years_match = years_found == years_expected
print(f'Match: {"✓" if years_match else "✗"}')
if not years_match:
    errors.append(f'Temporal Jahre inkorrekt: {years_found} != {years_expected}')

# ============================================================================
# 2. NODE-STRUKTUR (Cumulative)
# ============================================================================

print()
print('2. NODE-STRUKTUR (Cumulative)')
print('-'*80)

node_keys_expected = [
    'id', 'degree', 'weighted_degree', 'degree_centrality',
    'betweenness_centrality', 'closeness_centrality', 'eigenvector_centrality',
    'community'
]
sample_node = data['cumulative']['nodes'][0]
node_keys_found = sorted(sample_node.keys())

print(f'Erwartete Felder ({len(node_keys_expected)}): {sorted(node_keys_expected)}')
print(f'Gefundene Felder ({len(node_keys_found)}): {node_keys_found}')

keys_match = set(node_keys_found) == set(node_keys_expected)
print(f'Match: {"✓" if keys_match else "✗"}')

missing = set(node_keys_expected) - set(node_keys_found)
extra = set(node_keys_found) - set(node_keys_expected)
if missing:
    print(f'✗ Fehlende Felder: {missing}')
    errors.append(f'Fehlende Node-Felder: {missing}')
if extra:
    print(f'⚠ Zusätzliche Felder: {extra}')

# ============================================================================
# 3. EDGE-STRUKTUR (Cumulative)
# ============================================================================

print()
print('3. EDGE-STRUKTUR (Cumulative)')
print('-'*80)

edge_keys_expected = ['source', 'target', 'weight', 'num_firm_pairs']
sample_edge = data['cumulative']['edges'][0]
edge_keys_found = sorted(sample_edge.keys())

print(f'Erwartete Felder: {edge_keys_expected}')
print(f'Gefundene Felder: {edge_keys_found}')

edge_keys_match = set(edge_keys_found) == set(edge_keys_expected)
print(f'Match: {"✓" if edge_keys_match else "✗"}')
if not edge_keys_match:
    errors.append(f'Edge-Felder inkorrekt')

# ============================================================================
# 4. GLOBAL METRICS-STRUKTUR (Cumulative)
# ============================================================================

print()
print('4. GLOBAL METRICS-STRUKTUR (Cumulative)')
print('-'*80)

metrics_expected = [
    'num_nodes', 'num_edges', 'density', 'avg_clustering', 'transitivity',
    'is_connected', 'num_components', 'avg_path_length', 'assortativity'
]
metrics_found = sorted(data['cumulative']['metrics'].keys())

print(f'Erwartete Metriken ({len(metrics_expected)}): {sorted(metrics_expected)}')
print(f'Gefundene Metriken ({len(metrics_found)}): {metrics_found}')

metrics_match = set(metrics_found) == set(metrics_expected)
print(f'Match: {"✓" if metrics_match else "✗"}')

missing = set(metrics_expected) - set(metrics_found)
extra = set(metrics_found) - set(metrics_expected)
if missing:
    print(f'✗ Fehlende Metriken: {missing}')
    errors.append(f'Fehlende Global Metriken: {missing}')
if extra:
    print(f'⚠ Zusätzliche Metriken: {extra}')

# ============================================================================
# 5. WERTEBEREICHE (Cumulative Nodes)
# ============================================================================

print()
print('5. WERTEBEREICHE (Cumulative Nodes)')
print('-'*80)

nodes = data['cumulative']['nodes']

# Centrality-Werte müssen in [0, 1] sein
centrality_fields = ['degree_centrality', 'betweenness_centrality', 'closeness_centrality', 'eigenvector_centrality']

for field in centrality_fields:
    values = [n[field] for n in nodes]
    min_val = min(values)
    max_val = max(values)
    in_range = all(0 <= v <= 1 for v in values)
    status = '✓' if in_range else '✗'
    print(f'{status} {field}: [{min_val:.6f}, {max_val:.6f}]')
    if not in_range:
        errors.append(f'{field} außerhalb [0,1]: [{min_val}, {max_val}]')

# Degree und weighted_degree müssen >= 0 sein
for field in ['degree', 'weighted_degree']:
    values = [n[field] for n in nodes]
    min_val = min(values)
    max_val = max(values)
    valid = all(v >= 0 for v in values)
    status = '✓' if valid else '✗'
    print(f'{status} {field}: [{min_val:.1f}, {max_val:.1f}]')
    if not valid:
        errors.append(f'{field} negativ: min={min_val}')

# ============================================================================
# 6. WERTEBEREICHE (Global Metrics)
# ============================================================================

print()
print('6. WERTEBEREICHE (Global Metrics)')
print('-'*80)

metrics = data['cumulative']['metrics']

# Density in [0, 1]
density_ok = 0 <= metrics['density'] <= 1
print(f'{"✓" if density_ok else "✗"} density: {metrics["density"]:.6f} (muss in [0,1])')
if not density_ok:
    errors.append(f'density außerhalb [0,1]: {metrics["density"]}')

# Assortativity in [-1, 1]
assort = metrics['assortativity']
assort_ok = assort is None or (-1 <= assort <= 1)
print(f'{"✓" if assort_ok else "✗"} assortativity: {assort} (muss in [-1,1] oder None)')
if not assort_ok:
    errors.append(f'assortativity außerhalb [-1,1]: {assort}')

# avg_path_length >= 0 oder None
avg_path = metrics['avg_path_length']
path_ok = avg_path is None or avg_path >= 0
print(f'{"✓" if path_ok else "✗"} avg_path_length: {avg_path} (muss >= 0 oder None)')
if not path_ok:
    errors.append(f'avg_path_length negativ: {avg_path}')

# is_connected boolean
is_conn = metrics['is_connected']
conn_ok = isinstance(is_conn, bool)
print(f'{"✓" if conn_ok else "✗"} is_connected: {is_conn} (muss boolean sein)')
if not conn_ok:
    errors.append(f'is_connected kein boolean: {type(is_conn)}')

# ============================================================================
# 7. KONSISTENZ-CHECKS
# ============================================================================

print()
print('7. KONSISTENZ-CHECKS')
print('-'*80)

# Anzahl Nodes
num_nodes_metadata = data['metadata']['num_countries']
num_nodes_cumulative = len(data['cumulative']['nodes'])
num_nodes_metrics = metrics['num_nodes']

print(f'Anzahl Länder:')
print(f'  metadata.num_countries: {num_nodes_metadata}')
print(f'  cumulative.nodes length: {num_nodes_cumulative}')
print(f'  cumulative.metrics.num_nodes: {num_nodes_metrics}')

nodes_consistent = (num_nodes_metadata == num_nodes_cumulative == num_nodes_metrics)
print(f'{"✓" if nodes_consistent else "✗"} Alle gleich: {nodes_consistent}')
if not nodes_consistent:
    errors.append(f'Inkonsistente Node-Anzahl: {num_nodes_metadata}, {num_nodes_cumulative}, {num_nodes_metrics}')

# Anzahl Edges
num_edges_cumulative = len(data['cumulative']['edges'])
num_edges_metrics = metrics['num_edges']

print(f'\nAnzahl Kanten:')
print(f'  cumulative.edges length: {num_edges_cumulative}')
print(f'  cumulative.metrics.num_edges: {num_edges_metrics}')

edges_consistent = (num_edges_cumulative == num_edges_metrics)
print(f'{"✓" if edges_consistent else "✗"} Gleich: {edges_consistent}')
if not edges_consistent:
    errors.append(f'Inkonsistente Edge-Anzahl: {num_edges_cumulative} != {num_edges_metrics}')

# ============================================================================
# 8. TEMPORAL-KONSISTENZ (alle Jahre)
# ============================================================================

print()
print('8. TEMPORAL-KONSISTENZ (alle Jahre)')
print('-'*80)

temporal_ok = True
for year in years_expected:
    year_data = data['temporal'][year]

    # Struktur-Check
    has_nodes = 'nodes' in year_data
    has_edges = 'edges' in year_data
    has_metrics = 'metrics' in year_data

    if not (has_nodes and has_edges and has_metrics):
        print(f'✗ {year}: Fehlende Struktur (nodes={has_nodes}, edges={has_edges}, metrics={has_metrics})')
        temporal_ok = False
        errors.append(f'{year}: Fehlende Struktur')
    else:
        # Konsistenz-Check
        num_nodes_year = len(year_data['nodes'])
        num_edges_year = len(year_data['edges'])
        num_nodes_metrics_year = year_data['metrics']['num_nodes']
        num_edges_metrics_year = year_data['metrics']['num_edges']

        year_consistent = (num_nodes_year == num_nodes_metrics_year and
                          num_edges_year == num_edges_metrics_year)

        if year_consistent:
            print(f'✓ {year}: {num_nodes_year} Nodes, {num_edges_year} Edges')
        else:
            print(f'✗ {year}: Inkonsistent (Nodes: {num_nodes_year} vs {num_nodes_metrics_year}, Edges: {num_edges_year} vs {num_edges_metrics_year})')
            temporal_ok = False
            errors.append(f'{year}: Inkonsistenz')

if temporal_ok:
    print(f'\n✓ Alle Jahre konsistent')

# ============================================================================
# 9. UNIQUE NODE IDs
# ============================================================================

print()
print('9. UNIQUE NODE IDs')
print('-'*80)

node_ids = [n['id'] for n in data['cumulative']['nodes']]
unique_ids = set(node_ids)
duplicates = len(node_ids) - len(unique_ids)

print(f'Gesamt Node IDs: {len(node_ids)}')
print(f'Unique Node IDs: {len(unique_ids)}')
print(f'Duplikate: {duplicates}')
print(f'{"✓" if duplicates == 0 else "✗"} Keine Duplikate: {duplicates == 0}')

if duplicates > 0:
    errors.append(f'{duplicates} duplizierte Node IDs')

# ============================================================================
# 10. EDGE-VALIDIERUNG
# ============================================================================

print()
print('10. EDGE-VALIDIERUNG')
print('-'*80)

edges = data['cumulative']['edges']
invalid_edges = []

for i, edge in enumerate(edges):
    source = edge['source']
    target = edge['target']
    weight = edge['weight']

    # Source und Target müssen in Node IDs vorkommen
    if source not in unique_ids:
        invalid_edges.append(f'Edge {i}: source "{source}" nicht in Nodes')
    if target not in unique_ids:
        invalid_edges.append(f'Edge {i}: target "{target}" nicht in Nodes')

    # Weight muss > 0 sein
    if weight <= 0:
        invalid_edges.append(f'Edge {i}: weight {weight} <= 0')

if len(invalid_edges) == 0:
    print(f'✓ Alle {len(edges)} Kanten valide')
else:
    print(f'✗ {len(invalid_edges)} invalide Kanten gefunden:')
    for err in invalid_edges[:5]:  # Zeige nur erste 5
        print(f'  - {err}')
    if len(invalid_edges) > 5:
        print(f'  ... und {len(invalid_edges) - 5} weitere')
    errors.extend(invalid_edges[:10])  # Nur erste 10 zu errors hinzufügen

# ============================================================================
# ZUSAMMENFASSUNG
# ============================================================================

print()
print('='*80)
print('ZUSAMMENFASSUNG')
print('='*80)

if len(errors) == 0:
    print('✓✓✓ ALLE VALIDIERUNGEN BESTANDEN ✓✓✓')
    print()
    print('Die JSON-Daten sind vollständig konsistent und valide.')
    print()
    print(f'Statistiken:')
    print(f'  - {num_nodes_cumulative} Länder (Nodes)')
    print(f'  - {num_edges_cumulative} Kooperationen (Edges)')
    print(f'  - 9 Jahre (2010-2018)')
    print(f'  - 8 Node-Felder (inkl. 4 Centrality-Metriken)')
    print(f'  - 9 Global Metrics (inkl. Avg Path Length, Assortativity)')
    print()
    sys.exit(0)
else:
    print(f'✗✗✗ {len(errors)} FEHLER GEFUNDEN ✗✗✗')
    print()
    print('Fehler:')
    for i, err in enumerate(errors, 1):
        print(f'{i}. {err}')
    print()
    sys.exit(1)
