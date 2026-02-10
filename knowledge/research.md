# research.md

## Research Context

Network analysis of patent cooperations between firms at international level. Goal is the calculation of network metrics and their visualization for publication.

## Research Questions

**Macro Level (Countries)**
- Which countries are central actors in international patent cooperations?
- Are there regional clusters or communities of countries with intensive collaboration?
- How has the network structure changed between 2010 and 2018?

**Micro Level (Firms)**
- Which firms act as bridges between different countries or communities?
- Are there differences in cooperation patterns between firms from different countries?

## Network Metrics

**Centrality Measures**

*Degree Centrality* counts the number of direct connections of a node. High degree means many cooperation partners. Says nothing about strategic position in the network.

*Betweenness Centrality* measures how often a node lies on shortest paths between other nodes. High betweenness identifies brokers and gatekeepers who can control information flows.

*Eigenvector Centrality* weights connections by the centrality of neighbors. A node is central if its partners are central. Identifies actors in influential network regions.

*Closeness Centrality* measures the average distance to all other nodes. High closeness means fast access to the entire network.

**Community Detection**

*Louvain Algorithm* optimizes modularity through iterative merging of nodes. Fast, scales well, but not deterministic.

*Infomap* is based on Random Walks and information theory. Finds communities where information circulates for a long time. Often more accurate than Louvain with overlapping structures.

**Global Properties**

*Density* is the proportion of realized edges to all possible edges. Low density is typical for large networks.

*Average Path Length* is the average shortest distance between node pairs. Short paths indicate small-world properties.

*Clustering Coefficient* measures how strongly neighbors of a node are connected to each other. High values show local densification.

*Assortativity* measures whether similar nodes are preferentially connected (e.g., countries with similar development level).

## Methodological Decisions

**Directed vs. undirected:** Undirected. Patent cooperations are symmetric, owner1 and owner2 are interchangeable. Data verification confirms: no duplicated pairs present.

**Weighting:** Edges are weighted (1-14). Metrics should use weighted variants where appropriate. Median=4, mean=3.91, right-skewed distribution.

**Temporal analysis:** Calculate networks per year separately or cumulatively? Both have justification. Annual snapshots show dynamics, cumulative networks show overall structure.

**Aggregation firms to countries:** Summation of weights per country pair and year. Alternatives would be average or number of firm pairs.

## Tooling (Python)

**Network Analysis**

*NetworkX* for network computation and all metrics (Degree, Betweenness, Eigenvector, Closeness). Standard library, well documented, all algorithms available.

*igraph (Python binding)* as more performant alternative for very large networks. Faster than NetworkX with >100k nodes.

*graph-tool* for maximum performance with millions of nodes. Compiled (C++), more complex installation.

**Community Detection**

NetworkX: Louvain via `python-louvain` or `networkx.algorithms.community`.

Infomap: Dedicated Python package `infomap`.

Alternatives: Leiden algorithm via `leidenalg` (even better than Louvain).

**Visualization**

*Matplotlib + NetworkX* for simple static plots.

*Plotly* for interactive networks with hover information and zoom.

*PyVis* for browser-based interactive visualization (uses vis.js).

*Gephi* (external) for exploratory visualization of large networks, Python export via `networkx.write_gexf()`.

**Layout Algorithms**

NetworkX offers: `spring_layout` (Fruchterman-Reingold), `kamada_kawai_layout`, `circular_layout`, `spectral_layout`.

For very large networks (>10k nodes): `fa2` (ForceAtlas2) via `fa2` package or graph-tool.

Note: Firm network with ~134,000 nodes → subgraph analysis, aggregation to country level, or specialized layouts (FA2, DrL via graph-tool) necessary.

## Limitations

Correlation between centrality and innovation success is not causally inferable.

Patent cooperations are only one indicator for knowledge flows. Other forms (licensing, informal exchange, personnel changes) are not captured.

Aggregation to country level obscures heterogeneity within countries.

Synthetic data can distort structural properties of the original network.

99.15% international cooperations: Possibly artifact of data collection (national cooperations systematically underrepresented?).

## Open Questions

**Research Prioritization**
- Which research questions have priority for publication?
- Are there theoretical assumptions about expected network structures?
- Should certain countries or time periods be focused on?

**Data Interpretation**
- What does `weight` mean exactly? Number of shared patents, collaborations, or a score/index?
- Is `weight` already aggregated per firm pair and year, or could duplicates theoretically exist? (Verification shows: no duplicates)
- How were the synthetic data generated? Are structural properties (degree distribution, clustering) preserved?

**Methodological Details**
- For weighted metrics: Use weights directly or transform (log, normalization)?
- Community detection: Which algorithm has priority? (Louvain faster, Infomap often more precise)
- Temporal analysis: Annual snapshots or cumulative windows (e.g., 3-year periods)?
