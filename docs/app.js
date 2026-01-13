// ============================================================================
// CONSTANTS
// ============================================================================

const YEARS = {
    START: 2010,
    END: 2018,
    CUMULATIVE: 'cumulative'
};

const DIRECTION_COLORS = {
    improved: '#27ae60',
    worsened: '#e74c3c',
    unchanged: '#95a5a6'
};

const REGION_NAMES = {
    europe: 'Europa',
    asia: 'Asien',
    north_america: 'Nordamerika',
    south_america: 'Süd-/Mittelamerika',
    africa: 'Afrika',
    oceania: 'Ozeanien',
    middle_east: 'Naher Osten'
};

// ============================================================================
// GLOBAL STATE
// ============================================================================

let data = null;           // Full JSON data
let currentYear = YEARS.CUMULATIVE;
let currentCentrality = 'degree_centrality';
let currentTopN = 20;
let currentWeightThreshold = 1;

let currentTab = 'network'; // Current active tab
let temporalCentrality = 'degree_centrality'; // Centrality for temporal tab
let temporalTopN = 10;      // Top-N for temporal tab (reduced from 20 for better readability)
let bridgeTopN = 10;        // Top-N for bridge tab

let simulation = null;     // Force simulation
let svg = null;            // SVG selections
let slopegraphInitialized = false; // Track if slopegraph has been initialized
let bridgeInitialized = false;     // Track if bridge view has been initialized
let methodologyInitialized = false; // Track if methodology view has been initialized

// Color scale for communities (will be set after data load)
let colorScale = null;

// Region mapping (ISO-2 codes → regions)
const regionMapping = {
    // Europe (40 countries)
    'AL': 'europe', 'AD': 'europe', 'AT': 'europe', 'BY': 'europe', 'BE': 'europe',
    'BA': 'europe', 'BG': 'europe', 'HR': 'europe', 'CY': 'europe', 'CZ': 'europe',
    'DK': 'europe', 'EE': 'europe', 'FI': 'europe', 'FR': 'europe', 'DE': 'europe',
    'GR': 'europe', 'HU': 'europe', 'IS': 'europe', 'IE': 'europe', 'IT': 'europe',
    'XK': 'europe', 'LV': 'europe', 'LI': 'europe', 'LT': 'europe', 'LU': 'europe',
    'MT': 'europe', 'MD': 'europe', 'MC': 'europe', 'ME': 'europe', 'NL': 'europe',
    'MK': 'europe', 'NO': 'europe', 'PL': 'europe', 'PT': 'europe', 'RO': 'europe',
    'RU': 'europe', 'SM': 'europe', 'RS': 'europe', 'SK': 'europe', 'SI': 'europe',
    'ES': 'europe', 'SE': 'europe', 'CH': 'europe', 'UA': 'europe', 'GB': 'europe',
    'VA': 'europe',

    // Asia (25 countries)
    'AF': 'asia', 'AM': 'asia', 'AZ': 'asia', 'BH': 'asia', 'BD': 'asia',
    'BT': 'asia', 'BN': 'asia', 'KH': 'asia', 'CN': 'asia', 'GE': 'asia',
    'HK': 'asia', 'IN': 'asia', 'ID': 'asia', 'JP': 'asia', 'KZ': 'asia',
    'KP': 'asia', 'KR': 'asia', 'KG': 'asia', 'LA': 'asia', 'MO': 'asia',
    'MY': 'asia', 'MV': 'asia', 'MN': 'asia', 'MM': 'asia', 'NP': 'asia',
    'PK': 'asia', 'PH': 'asia', 'SG': 'asia', 'LK': 'asia', 'TW': 'asia',
    'TJ': 'asia', 'TH': 'asia', 'TL': 'asia', 'TM': 'asia', 'UZ': 'asia',
    'VN': 'asia',

    // North America (3 countries)
    'CA': 'north_america', 'MX': 'north_america', 'US': 'north_america',

    // Central America & Caribbean
    'AG': 'south_america', 'BS': 'south_america', 'BB': 'south_america', 'BZ': 'south_america',
    'CR': 'south_america', 'CU': 'south_america', 'CW': 'south_america', 'DM': 'south_america',
    'DO': 'south_america', 'SV': 'south_america', 'GD': 'south_america', 'GT': 'south_america',
    'HT': 'south_america', 'HN': 'south_america', 'JM': 'south_america', 'NI': 'south_america',
    'PA': 'south_america', 'KN': 'south_america', 'LC': 'south_america', 'VC': 'south_america',
    'TT': 'south_america',

    // South America (12 countries)
    'AR': 'south_america', 'BO': 'south_america', 'BR': 'south_america', 'CL': 'south_america',
    'CO': 'south_america', 'EC': 'south_america', 'GF': 'south_america', 'GY': 'south_america',
    'PY': 'south_america', 'PE': 'south_america', 'SR': 'south_america', 'UY': 'south_america',
    'VE': 'south_america',

    // Africa (20 countries - representative selection)
    'DZ': 'africa', 'AO': 'africa', 'BJ': 'africa', 'BW': 'africa', 'BF': 'africa',
    'BI': 'africa', 'CM': 'africa', 'CV': 'africa', 'CF': 'africa', 'TD': 'africa',
    'KM': 'africa', 'CG': 'africa', 'CD': 'africa', 'CI': 'africa', 'DJ': 'africa',
    'EG': 'africa', 'GQ': 'africa', 'ER': 'africa', 'ET': 'africa', 'GA': 'africa',
    'GM': 'africa', 'GH': 'africa', 'GN': 'africa', 'GW': 'africa', 'KE': 'africa',
    'LS': 'africa', 'LR': 'africa', 'LY': 'africa', 'MG': 'africa', 'MW': 'africa',
    'ML': 'africa', 'MR': 'africa', 'MU': 'africa', 'MA': 'africa', 'MZ': 'africa',
    'NA': 'africa', 'NE': 'africa', 'NG': 'africa', 'RW': 'africa', 'ST': 'africa',
    'SN': 'africa', 'SC': 'africa', 'SL': 'africa', 'SO': 'africa', 'ZA': 'africa',
    'SS': 'africa', 'SD': 'africa', 'SZ': 'africa', 'TZ': 'africa', 'TG': 'africa',
    'TN': 'africa', 'UG': 'africa', 'ZM': 'africa', 'ZW': 'africa',

    // Oceania (5 countries)
    'AU': 'oceania', 'FJ': 'oceania', 'KI': 'oceania', 'MH': 'oceania', 'FM': 'oceania',
    'NR': 'oceania', 'NZ': 'oceania', 'PW': 'oceania', 'PG': 'oceania', 'WS': 'oceania',
    'SB': 'oceania', 'TO': 'oceania', 'TV': 'oceania', 'VU': 'oceania',

    // Middle East (5 countries - separate from Asia for geopolitical clarity)
    'IQ': 'middle_east', 'IL': 'middle_east', 'JO': 'middle_east', 'KW': 'middle_east',
    'LB': 'middle_east', 'OM': 'middle_east', 'PS': 'middle_east', 'QA': 'middle_east',
    'SA': 'middle_east', 'SY': 'middle_east', 'TR': 'middle_east', 'AE': 'middle_east',
    'YE': 'middle_east', 'IR': 'middle_east'
};

// Region color scales (each region has multiple shades)
const regionColorScales = {
    'europe': d3.scaleOrdinal(['#3498db', '#5dade2', '#85c1e9', '#aed6f1', '#2874a6', '#1f618d']),
    'asia': d3.scaleOrdinal(['#27ae60', '#52be80', '#82e0aa', '#abebc6', '#1e8449', '#186a3b']),
    'north_america': d3.scaleOrdinal(['#e74c3c', '#ec7063', '#f1948a', '#f5b7b1']),
    'south_america': d3.scaleOrdinal(['#8e44ad', '#a569bd', '#bb8fce', '#d2b4de', '#7d3c98', '#6c3483']),
    'africa': d3.scaleOrdinal(['#e67e22', '#f39c12', '#f8b739', '#fad7a0', '#d68910', '#b9770e']),
    'oceania': d3.scaleOrdinal(['#16a085', '#48c9b0', '#76d7c4', '#a3e4d7']),
    'middle_east': d3.scaleOrdinal(['#a04000', '#ba6832', '#d49464', '#edc2a0'])
};

function getCountryColor(countryId) {
    const region = regionMapping[countryId] || 'europe'; // Default to Europe if not found
    const regionScale = regionColorScales[region];
    return regionScale(countryId);
}

// ============================================================================
// DATA LOADING
// ============================================================================

async function loadData() {
    try {
        data = await d3.json('data/country_network.json');
        console.log('Data loaded:', data.metadata);

        // Set color scale based on number of communities
        const numCommunities = data.cumulative.metrics.num_communities;
        colorScale = d3.scaleOrdinal(d3.schemeCategory10);

        // Initialize visualizations
        initNetwork();
        initRanking();
        initTemporalMetrics();
        initControls();

    } catch (error) {
        console.error('Error loading data:', error);
        document.body.innerHTML = '<h1>Error loading data. Please check console.</h1>';
    }
}

// ============================================================================
// VIS-1A: NETWORK OVERVIEW
// ============================================================================

function initNetwork() {
    const container = d3.select('#network-svg');
    const width = container.node().clientWidth;
    const height = container.node().clientHeight;

    svg = container
        .attr('width', width)
        .attr('height', height);

    // Create groups for layers
    const g = svg.append('g');
    const linkLayer = g.append('g').attr('class', 'links');
    const nodeLayer = g.append('g').attr('class', 'nodes');

    // Zoom behavior
    const zoom = d3.zoom()
        .scaleExtent([0.5, 5])
        .on('zoom', (event) => g.attr('transform', event.transform));

    svg.call(zoom);

    updateNetwork();
}

function updateNetwork() {
    const yearData = currentYear === 'cumulative'
        ? data.cumulative
        : data.temporal[currentYear];

    // Filter edges by weight threshold
    const edges = yearData.edges.filter(e => e.weight >= currentWeightThreshold);
    const nodes = yearData.nodes;

    // Scales
    const nodeSizeScale = d3.scaleSqrt()
        .domain(d3.extent(nodes, d => d.weighted_degree))
        .range([5, 30]);

    const edgeWidthScale = d3.scaleSqrt()
        .domain(d3.extent(edges, d => d.weight))
        .range([0.5, 5]);

    const edgeOpacityScale = d3.scaleLinear()
        .domain(d3.extent(edges, d => d.weight))
        .range([0.2, 0.8]);

    // Force simulation
    if (simulation) simulation.stop();

    simulation = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(edges)
            .id(d => d.id)
            .distance(50))
        .force('charge', d3.forceManyBody().strength(-200))
        .force('center', d3.forceCenter(
            d3.select('#network-svg').node().clientWidth / 2,
            d3.select('#network-svg').node().clientHeight / 2
        ))
        .force('collision', d3.forceCollide().radius(d => nodeSizeScale(d.weighted_degree) + 2));

    // Update links
    const link = d3.select('.links')
        .selectAll('line')
        .data(edges, d => `${d.source.id || d.source}-${d.target.id || d.target}`)
        .join('line')
        .attr('class', 'link')
        .attr('stroke-width', d => edgeWidthScale(d.weight))
        .attr('stroke-opacity', d => edgeOpacityScale(d.weight));

    // Update nodes
    const node = d3.select('.nodes')
        .selectAll('g')
        .data(nodes, d => d.id)
        .join('g')
        .attr('class', 'node')
        .call(d3.drag()
            .on('start', dragStarted)
            .on('drag', dragged)
            .on('end', dragEnded));

    node.selectAll('circle').remove();
    node.selectAll('text').remove();

    node.append('circle')
        .attr('r', d => nodeSizeScale(d.weighted_degree))
        .attr('fill', d => getCountryColor(d.id));

    node.append('text')
        .attr('dy', 4)
        .attr('text-anchor', 'middle')
        .text(d => d.id)
        .style('display', 'none');

    // Tooltips
    node.on('mouseover', showTooltip)
        .on('mouseout', hideTooltip)
        .on('click', highlightEgoNetwork);

    // Update simulation
    simulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        node.attr('transform', d => `translate(${d.x},${d.y})`);
    });
}

// Drag functions
function dragStarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
}

function dragEnded(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

// Tooltip functions
function showTooltip(event, d) {
    const tooltip = d3.select('body').append('div')
        .attr('class', 'tooltip')
        .style('left', (event.pageX + 10) + 'px')
        .style('top', (event.pageY - 10) + 'px')
        .html(`
            <strong>${d.id}</strong><br>
            Degree Centrality: ${d.degree_centrality.toFixed(3)}<br>
            Weighted Degree: ${d.weighted_degree.toFixed(0)}<br>
            Community: ${d.community}
        `);

    d3.select(event.currentTarget).select('text').style('display', 'block');
}

function hideTooltip(event) {
    d3.selectAll('.tooltip').remove();
    d3.select(event.currentTarget).select('text').style('display', 'none');
}

function highlightEgoNetwork(event, d) {
    // Get neighbors
    const yearData = currentYear === 'cumulative'
        ? data.cumulative
        : data.temporal[currentYear];

    const neighbors = new Set();
    yearData.edges.forEach(e => {
        if (e.source.id === d.id || e.source === d.id) neighbors.add(e.target.id || e.target);
        if (e.target.id === d.id || e.target === d.id) neighbors.add(e.source.id || e.source);
    });
    neighbors.add(d.id);

    // Highlight
    d3.selectAll('.node')
        .classed('highlighted', n => neighbors.has(n.id))
        .classed('dimmed', n => !neighbors.has(n.id));

    d3.selectAll('.link')
        .classed('highlighted', e =>
            (e.source.id === d.id || e.source === d.id) ||
            (e.target.id === d.id || e.target === d.id))
        .classed('dimmed', e =>
            (e.source.id !== d.id && e.source !== d.id) &&
            (e.target.id !== d.id && e.target !== d.id));
}

// ============================================================================
// VIS-1B: CENTRALITY RANKING
// ============================================================================

function initRanking() {
    updateRanking();
}

function updateRanking() {
    const yearData = currentYear === 'cumulative'
        ? data.cumulative
        : data.temporal[currentYear];

    // Sort and filter top-N
    const sortedNodes = [...yearData.nodes]
        .sort((a, b) => b[currentCentrality] - a[currentCentrality])
        .slice(0, currentTopN);

    const container = d3.select('#ranking-svg');
    const margin = {top: 20, right: 20, bottom: 20, left: 50};
    const width = container.node().clientWidth - margin.left - margin.right;
    const height = Math.max(400, sortedNodes.length * 25);

    container.attr('height', height + margin.top + margin.bottom);
    container.selectAll('*').remove();

    const g = container.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales
    const xScale = d3.scaleLinear()
        .domain([0, d3.max(sortedNodes, d => d[currentCentrality])])
        .range([0, width]);

    const yScale = d3.scaleBand()
        .domain(sortedNodes.map(d => d.id))
        .range([0, height])
        .padding(0.1);

    // Bars
    g.selectAll('rect')
        .data(sortedNodes)
        .join('rect')
        .attr('x', 0)
        .attr('y', d => yScale(d.id))
        .attr('width', d => xScale(d[currentCentrality]))
        .attr('height', yScale.bandwidth())
        .attr('fill', d => getCountryColor(d.id));

    // Labels
    g.selectAll('text')
        .data(sortedNodes)
        .join('text')
        .attr('x', -5)
        .attr('y', d => yScale(d.id) + yScale.bandwidth() / 2)
        .attr('dy', '0.35em')
        .attr('text-anchor', 'end')
        .attr('font-size', '10px')
        .text(d => d.id);

    // Axis
    g.append('g')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(xScale).ticks(5));
}

// ============================================================================
// VIS-3A: TEMPORAL METRICS
// ============================================================================

function initTemporalMetrics() {
    const metrics = ['density', 'modularity', 'num_communities', 'avg_clustering'];
    const years = data.metadata.years;

    // Extract temporal data
    const temporalData = metrics.map(metric => ({
        metric,
        values: years.map(year => ({
            year,
            value: data.temporal[year].metrics[metric]
        }))
    }));

    const container = d3.select('#temporal-metrics-svg');
    const margin = {top: 20, right: 20, bottom: 30, left: 50};
    const width = container.node().clientWidth - margin.left - margin.right;
    const height = container.node().clientHeight - margin.top - margin.bottom;

    container.selectAll('*').remove();

    const g = container.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Small multiples layout (2x2 grid)
    const cellWidth = width / 2 - 10;
    const cellHeight = height / 2 - 10;

    temporalData.forEach((d, i) => {
        const col = i % 2;
        const row = Math.floor(i / 2);
        const offsetX = col * (cellWidth + 10);
        const offsetY = row * (cellHeight + 10);

        const cell = g.append('g')
            .attr('transform', `translate(${offsetX},${offsetY})`);

        // Scales
        const xScale = d3.scaleLinear()
            .domain(d3.extent(years))
            .range([0, cellWidth]);

        const yScale = d3.scaleLinear()
            .domain(d3.extent(d.values, v => v.value))
            .range([cellHeight, 0])
            .nice();

        // Line
        const line = d3.line()
            .x(v => xScale(v.year))
            .y(v => yScale(v.value));

        cell.append('path')
            .datum(d.values)
            .attr('fill', 'none')
            .attr('stroke', 'steelblue')
            .attr('stroke-width', 2)
            .attr('d', line);

        // Axes
        cell.append('g')
            .attr('transform', `translate(0,${cellHeight})`)
            .call(d3.axisBottom(xScale).ticks(4).tickFormat(d3.format('d')))
            .style('font-size', '11px');

        cell.append('g')
            .call(d3.axisLeft(yScale).ticks(4))
            .style('font-size', '11px');

        // Title
        cell.append('text')
            .attr('x', cellWidth / 2)
            .attr('y', -5)
            .attr('text-anchor', 'middle')
            .attr('font-size', '12px')
            .attr('font-weight', 'bold')
            .text(d.metric.replace(/_/g, ' '));
    });
}

// ============================================================================
// VIS-3B: SLOPEGRAPH
// ============================================================================

function prepareRankData(startYear, endYear, metric, topN) {
    // Get data for both years
    const startYearStr = String(startYear);
    const endYearStr = String(endYear);

    const startData = data.temporal[startYearStr];
    const endData = data.temporal[endYearStr];

    // Sort and rank for start year
    const startSorted = [...startData.nodes]
        .sort((a, b) => b[metric] - a[metric])
        .map((node, index) => ({
            country: node.id,
            rank: index + 1,
            value: node[metric]
        }));

    // Sort and rank for end year
    const endSorted = [...endData.nodes]
        .sort((a, b) => b[metric] - a[metric])
        .map((node, index) => ({
            country: node.id,
            rank: index + 1,
            value: node[metric]
        }));

    // Create lookup maps
    const startMap = new Map(startSorted.map(d => [d.country, d]));
    const endMap = new Map(endSorted.map(d => [d.country, d]));

    // Get top-N countries from both years (union)
    const topStartCountries = startSorted.slice(0, topN).map(d => d.country);
    const topEndCountries = endSorted.slice(0, topN).map(d => d.country);
    const allTopCountries = new Set([...topStartCountries, ...topEndCountries]);

    // Prepare rank comparison data
    const rankData = Array.from(allTopCountries).map(country => {
        const startRank = startMap.get(country)?.rank || 999;
        const endRank = endMap.get(country)?.rank || 999;
        const startValue = startMap.get(country)?.value || 0;
        const endValue = endMap.get(country)?.value || 0;

        return {
            country,
            startRank,
            endRank,
            rankChange: startRank - endRank, // Positive = improved (moved up)
            startValue,
            endValue,
            direction: startRank < endRank ? 'worsened' : (startRank > endRank ? 'improved' : 'unchanged')
        };
    });

    // DIAGNOSE: Log rank changes
    console.log(`[${metric}] Rank Changes:`, rankData.map(d => ({
        country: d.country,
        '2010': d.startRank,
        '2018': d.endRank,
        delta: d.rankChange,
        direction: d.direction
    })));

    // Sort by start rank for display
    rankData.sort((a, b) => a.startRank - b.startRank);

    return rankData;
}

function initSlopegraph() {
    const container = d3.select('#slopegraph-svg');
    const width = container.node().clientWidth;
    const height = container.node().clientHeight;

    container
        .attr('width', width)
        .attr('height', height);

    updateSlopegraph();
}

function updateSlopegraph() {
    const container = d3.select('#slopegraph-svg');
    const width = container.node().clientWidth;

    // Prepare data FIRST to calculate required height
    const rankData = prepareRankData(YEARS.START, YEARS.END, temporalCentrality, temporalTopN);

    const margin = {top: 60, right: 150, bottom: 40, left: 150};
    const plotWidth = width - margin.left - margin.right;

    // Calculate required height: 25px per label minimum
    const minLabelSpacing = 25;
    const requiredPlotHeight = Math.max(400, rankData.length * minLabelSpacing);
    const plotHeight = requiredPlotHeight;
    const height = plotHeight + margin.top + margin.bottom;

    // Set SVG height dynamically
    container.attr('height', height);

    // Update summary statistics
    const stats = rankData.reduce((acc, d) => {
        acc[d.direction]++;
        return acc;
    }, {improved: 0, worsened: 0, unchanged: 0});

    d3.select('#slopegraph-stats').html(`
        <span style="color: ${DIRECTION_COLORS.improved};">↑ ${stats.improved} improved</span>
        <span style="color: ${DIRECTION_COLORS.worsened};">↓ ${stats.worsened} worsened</span>
        <span style="color: ${DIRECTION_COLORS.unchanged};">− ${stats.unchanged} unchanged</span>
    `);

    // Clear previous content
    container.selectAll('*').remove();

    const g = container.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Y-Scale (rank position, 1 = top) - with aggressive padding for label spacing
    const maxRank = Math.max(...rankData.map(d => Math.max(d.startRank, d.endRank)));
    const yScale = d3.scaleLinear()
        .domain([-2, maxRank + 3])  // Increased padding: -2 to maxRank+3
        .range([0, plotHeight]);

    // Line thickness scale (based on absolute rank change)
    const thicknessScale = d3.scaleLinear()
        .domain([0, d3.max(rankData, d => Math.abs(d.rankChange))])
        .range([1, 4]);

    // Color scale for direction
    const directionColor = DIRECTION_COLORS;

    // Column headers
    g.append('text')
        .attr('x', 0)
        .attr('y', -30)
        .attr('text-anchor', 'middle')
        .attr('font-size', '16px')
        .attr('font-weight', 'bold')
        .text(YEARS.START);

    g.append('text')
        .attr('x', plotWidth)
        .attr('y', -30)
        .attr('text-anchor', 'middle')
        .attr('font-size', '16px')
        .attr('font-weight', 'bold')
        .text(YEARS.END);

    // Draw lines
    const lines = g.selectAll('.slope-line')
        .data(rankData)
        .join('line')
        .attr('class', 'slope-line')
        .attr('x1', 0)
        .attr('y1', d => yScale(d.startRank))
        .attr('x2', plotWidth)
        .attr('y2', d => yScale(d.endRank))
        .attr('stroke', d => directionColor[d.direction])
        .attr('stroke-width', d => thicknessScale(Math.abs(d.rankChange)))
        .attr('stroke-opacity', 0.6)
        .on('mouseover', showSlopeTooltip)
        .on('mouseout', hideSlopeTooltip)
        .style('cursor', 'pointer');

    // Left labels (2010)
    g.selectAll('.label-left')
        .data(rankData)
        .join('text')
        .attr('class', 'label-left')
        .attr('x', -10)
        .attr('y', d => yScale(d.startRank))
        .attr('dy', '0.35em')
        .attr('text-anchor', 'end')
        .attr('font-size', '12px')
        .text(d => `${d.startRank}. ${d.country}`);

    // Right labels (2018)
    g.selectAll('.label-right')
        .data(rankData)
        .join('text')
        .attr('class', 'label-right')
        .attr('x', plotWidth + 10)
        .attr('y', d => yScale(d.endRank))
        .attr('dy', '0.35em')
        .attr('text-anchor', 'start')
        .attr('font-size', '12px')
        .text(d => `${d.endRank}. ${d.country}`);
}

// Slopegraph tooltip functions
function showSlopeTooltip(event, d) {
    // Amplify line width on hover
    d3.select(event.currentTarget)
        .attr('stroke-width', function() {
            return parseFloat(d3.select(this).attr('stroke-width')) * 2;
        })
        .attr('stroke-opacity', 1);

    // Show tooltip
    const changeSymbol = d.rankChange > 0 ? '↑' : (d.rankChange < 0 ? '↓' : '−');
    const changeClass = d.direction === 'improved' ? 'positive' : (d.direction === 'worsened' ? 'negative' : 'neutral');

    const tooltip = d3.select('body').append('div')
        .attr('class', 'tooltip')
        .style('left', (event.pageX + 10) + 'px')
        .style('top', (event.pageY - 10) + 'px')
        .html(`
            <strong>${d.country}</strong><br>
            <div style="margin-top: 5px;">
                <span style="color: #aaa;">Rank 2010:</span> ${d.startRank}<br>
                <span style="color: #aaa;">Rank 2018:</span> ${d.endRank}<br>
                <span style="color: #aaa;">Change:</span> <span class="${changeClass}">${Math.abs(d.rankChange)} ${changeSymbol}</span><br>
            </div>
            <div style="margin-top: 5px; border-top: 1px solid #555; padding-top: 5px;">
                <span style="color: #aaa;">Centrality 2010:</span> ${d.startValue.toFixed(3)}<br>
                <span style="color: #aaa;">Centrality 2018:</span> ${d.endValue.toFixed(3)}<br>
                <span style="color: #aaa;">Δ Centrality:</span> ${(d.endValue - d.startValue).toFixed(3)}
            </div>
        `);
}

function hideSlopeTooltip(event) {
    // Reset line width
    d3.select(event.currentTarget)
        .attr('stroke-width', function() {
            return parseFloat(d3.select(this).attr('stroke-width')) / 2;
        })
        .attr('stroke-opacity', 0.6);

    // Remove tooltip
    d3.selectAll('.tooltip').remove();
}

function initTemporalMetrics2() {
    // Initialize second instance of temporal metrics for temporal tab
    const metrics = ['density', 'modularity', 'num_communities', 'avg_clustering'];
    const years = data.metadata.years;

    const temporalData = metrics.map(metric => ({
        metric,
        values: years.map(year => ({
            year,
            value: data.temporal[year].metrics[metric]
        }))
    }));

    const container = d3.select('#temporal-metrics-svg-2');
    const margin = {top: 20, right: 20, bottom: 30, left: 50};
    const width = container.node().clientWidth - margin.left - margin.right;
    const height = container.node().clientHeight - margin.top - margin.bottom;

    container.selectAll('*').remove();

    const g = container.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Small multiples layout (2x2 grid)
    const cellWidth = width / 2 - 10;
    const cellHeight = height / 2 - 10;

    temporalData.forEach((d, i) => {
        const col = i % 2;
        const row = Math.floor(i / 2);
        const offsetX = col * (cellWidth + 10);
        const offsetY = row * (cellHeight + 10);

        const cell = g.append('g')
            .attr('transform', `translate(${offsetX},${offsetY})`);

        // Scales
        const xScale = d3.scaleLinear()
            .domain(d3.extent(years))
            .range([0, cellWidth]);

        const yScale = d3.scaleLinear()
            .domain(d3.extent(d.values, v => v.value))
            .range([cellHeight, 0])
            .nice();

        // Line
        const line = d3.line()
            .x(v => xScale(v.year))
            .y(v => yScale(v.value));

        cell.append('path')
            .datum(d.values)
            .attr('fill', 'none')
            .attr('stroke', 'steelblue')
            .attr('stroke-width', 2)
            .attr('d', line);

        // Axes
        cell.append('g')
            .attr('transform', `translate(0,${cellHeight})`)
            .call(d3.axisBottom(xScale).ticks(4).tickFormat(d3.format('d')))
            .style('font-size', '11px');

        cell.append('g')
            .call(d3.axisLeft(yScale).ticks(4))
            .style('font-size', '11px');

        // Title
        cell.append('text')
            .attr('x', cellWidth / 2)
            .attr('y', -5)
            .attr('text-anchor', 'middle')
            .attr('font-size', '12px')
            .attr('font-weight', 'bold')
            .text(d.metric.replace(/_/g, ' '));
    });
}

// ============================================================================
// VIS-4: BRIDGE SLOPEGRAPH (Betweenness Centrality 2010→2018)
// ============================================================================

function initBridge() {
    const container = d3.select('#bridge-svg');
    const width = container.node().clientWidth;
    const height = container.node().clientHeight;

    container
        .attr('width', width)
        .attr('height', height);

    updateBridge();
    initTemporalMetrics3(); // Initialize third temporal metrics view
}

function updateBridge() {
    const container = d3.select('#bridge-svg');
    const width = container.node().clientWidth;

    // Prepare data FIRST to calculate required height
    const rankData = prepareRankData(YEARS.START, YEARS.END, 'betweenness_centrality', bridgeTopN);

    const margin = {top: 60, right: 150, bottom: 40, left: 150};
    const plotWidth = width - margin.left - margin.right;

    // Calculate required height: 25px per label minimum
    const minLabelSpacing = 25;
    const requiredPlotHeight = Math.max(400, rankData.length * minLabelSpacing);
    const plotHeight = requiredPlotHeight;
    const height = plotHeight + margin.top + margin.bottom;

    // Set SVG height dynamically
    container.attr('height', height);

    // Update summary statistics
    const stats = rankData.reduce((acc, d) => {
        acc[d.direction]++;
        return acc;
    }, {improved: 0, worsened: 0, unchanged: 0});

    d3.select('#bridge-stats').html(`
        <span style="color: ${DIRECTION_COLORS.improved};">↑ ${stats.improved} improved</span>
        <span style="color: ${DIRECTION_COLORS.worsened};">↓ ${stats.worsened} worsened</span>
        <span style="color: ${DIRECTION_COLORS.unchanged};">− ${stats.unchanged} unchanged</span>
    `);

    // Clear previous content
    container.selectAll('*').remove();

    const g = container.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Y-Scale (rank position, 1 = top) - with aggressive padding for label spacing
    const maxRank = Math.max(...rankData.map(d => Math.max(d.startRank, d.endRank)));
    const yScale = d3.scaleLinear()
        .domain([-2, maxRank + 3])  // Increased padding: -2 to maxRank+3
        .range([0, plotHeight]);

    // Line thickness scale
    const thicknessScale = d3.scaleLinear()
        .domain([0, d3.max(rankData, d => Math.abs(d.rankChange))])
        .range([1, 4]);

    // Color scale for direction
    const directionColor = DIRECTION_COLORS;

    // Column headers
    g.append('text')
        .attr('x', 0)
        .attr('y', -30)
        .attr('text-anchor', 'middle')
        .attr('font-size', '16px')
        .attr('font-weight', 'bold')
        .text(YEARS.START);

    g.append('text')
        .attr('x', plotWidth)
        .attr('y', -30)
        .attr('text-anchor', 'middle')
        .attr('font-size', '16px')
        .attr('font-weight', 'bold')
        .text(YEARS.END);

    // Draw lines
    g.selectAll('.slope-line')
        .data(rankData)
        .join('line')
        .attr('class', 'slope-line')
        .attr('x1', 0)
        .attr('y1', d => yScale(d.startRank))
        .attr('x2', plotWidth)
        .attr('y2', d => yScale(d.endRank))
        .attr('stroke', d => directionColor[d.direction])
        .attr('stroke-width', d => thicknessScale(Math.abs(d.rankChange)))
        .attr('stroke-opacity', 0.6)
        .on('mouseover', showBridgeTooltip)
        .on('mouseout', hideBridgeTooltip)
        .style('cursor', 'pointer');

    // Left labels (2010)
    g.selectAll('.label-left')
        .data(rankData)
        .join('text')
        .attr('class', 'label-left')
        .attr('x', -10)
        .attr('y', d => yScale(d.startRank))
        .attr('dy', '0.35em')
        .attr('text-anchor', 'end')
        .attr('font-size', '12px')
        .text(d => `${d.startRank}. ${d.country}`);

    // Right labels (2018)
    g.selectAll('.label-right')
        .data(rankData)
        .join('text')
        .attr('class', 'label-right')
        .attr('x', plotWidth + 10)
        .attr('y', d => yScale(d.endRank))
        .attr('dy', '0.35em')
        .attr('text-anchor', 'start')
        .attr('font-size', '12px')
        .text(d => `${d.endRank}. ${d.country}`);
}

function showBridgeTooltip(event, d) {
    // Amplify line width on hover
    d3.select(event.currentTarget)
        .attr('stroke-width', function() {
            return parseFloat(d3.select(this).attr('stroke-width')) * 2;
        })
        .attr('stroke-opacity', 1);

    // Show tooltip
    const changeSymbol = d.rankChange > 0 ? '↑' : (d.rankChange < 0 ? '↓' : '−');
    const changeClass = d.direction === 'improved' ? 'positive' : (d.direction === 'worsened' ? 'negative' : 'neutral');

    const tooltip = d3.select('body').append('div')
        .attr('class', 'tooltip')
        .style('left', (event.pageX + 10) + 'px')
        .style('top', (event.pageY - 10) + 'px')
        .html(`
            <strong>${d.country}</strong><br>
            <div style="margin-top: 5px;">
                <span style="color: #aaa;">Rank 2010:</span> ${d.startRank}<br>
                <span style="color: #aaa;">Rank 2018:</span> ${d.endRank}<br>
                <span style="color: #aaa;">Change:</span> <span class="${changeClass}">${Math.abs(d.rankChange)} ${changeSymbol}</span><br>
            </div>
            <div style="margin-top: 5px; border-top: 1px solid #555; padding-top: 5px;">
                <span style="color: #aaa;">Betweenness 2010:</span> ${d.startValue.toFixed(4)}<br>
                <span style="color: #aaa;">Betweenness 2018:</span> ${d.endValue.toFixed(4)}<br>
                <span style="color: #aaa;">Δ Betweenness:</span> ${(d.endValue - d.startValue).toFixed(4)}
            </div>
        `);
}

function hideBridgeTooltip(event) {
    // Reset line width
    d3.select(event.currentTarget)
        .attr('stroke-width', function() {
            return parseFloat(d3.select(this).attr('stroke-width')) / 2;
        })
        .attr('stroke-opacity', 0.6);

    // Remove tooltip
    d3.selectAll('.tooltip').remove();
}

function initTemporalMetrics3() {
    // Initialize third instance of temporal metrics for bridge tab
    const metrics = ['density', 'modularity', 'num_communities', 'avg_clustering'];
    const years = data.metadata.years;

    const temporalData = metrics.map(metric => ({
        metric,
        values: years.map(year => ({
            year,
            value: data.temporal[year].metrics[metric]
        }))
    }));

    const container = d3.select('#temporal-metrics-svg-3');
    const margin = {top: 20, right: 20, bottom: 30, left: 50};
    const width = container.node().clientWidth - margin.left - margin.right;
    const height = container.node().clientHeight - margin.top - margin.bottom;

    container.selectAll('*').remove();

    const g = container.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Small multiples layout (2x2 grid)
    const cellWidth = width / 2 - 10;
    const cellHeight = height / 2 - 10;

    temporalData.forEach((d, i) => {
        const col = i % 2;
        const row = Math.floor(i / 2);
        const offsetX = col * (cellWidth + 10);
        const offsetY = row * (cellHeight + 10);

        const cell = g.append('g')
            .attr('transform', `translate(${offsetX},${offsetY})`);

        // Scales
        const xScale = d3.scaleLinear()
            .domain(d3.extent(years))
            .range([0, cellWidth]);

        const yScale = d3.scaleLinear()
            .domain(d3.extent(d.values, v => v.value))
            .range([cellHeight, 0])
            .nice();

        // Line
        const line = d3.line()
            .x(v => xScale(v.year))
            .y(v => yScale(v.value));

        cell.append('path')
            .datum(d.values)
            .attr('fill', 'none')
            .attr('stroke', 'steelblue')
            .attr('stroke-width', 2)
            .attr('d', line);

        // Axes
        cell.append('g')
            .attr('transform', `translate(0,${cellHeight})`)
            .call(d3.axisBottom(xScale).ticks(4).tickFormat(d3.format('d')))
            .style('font-size', '11px');

        cell.append('g')
            .call(d3.axisLeft(yScale).ticks(4))
            .style('font-size', '11px');

        // Title
        cell.append('text')
            .attr('x', cellWidth / 2)
            .attr('y', -5)
            .attr('text-anchor', 'middle')
            .attr('font-size', '12px')
            .attr('font-weight', 'bold')
            .text(d.metric.replace(/_/g, ' '));
    });
}

// ============================================================================
// CONTROLS
// ============================================================================

function switchTab(tabName) {
    // Update global state
    currentTab = tabName;

    // Update tab buttons
    d3.selectAll('.tab-button')
        .classed('active', false)
        .attr('aria-selected', false);

    d3.select(`.tab-button[data-tab="${tabName}"]`)
        .classed('active', true)
        .attr('aria-selected', true);

    // Update tab content
    d3.selectAll('.tab-content')
        .classed('active', false);

    d3.select(`#tab-${tabName}`)
        .classed('active', true);

    // Show/hide time controls based on tab
    const timeControls = d3.select('#time-controls');
    if (tabName === 'network') {
        timeControls.style('display', 'flex');
    } else {
        timeControls.style('display', 'none');
    }

    // Lazy initialization for slopegraph
    if (tabName === 'temporal' && !slopegraphInitialized) {
        initSlopegraph();
        initTemporalMetrics2(); // Initialize second temporal metrics view
        slopegraphInitialized = true;
    }

    // Lazy initialization for bridge view
    if (tabName === 'bridge' && !bridgeInitialized) {
        initBridge();
        bridgeInitialized = true;
    }

    // Lazy initialization for methodology view
    if (tabName === 'methodology' && !methodologyInitialized) {
        initMethodology();
        methodologyInitialized = true;
    }
}

function initControls() {
    // Tab switching
    d3.selectAll('.tab-button').on('click', function() {
        const tabName = d3.select(this).attr('data-tab');
        if (!this.disabled) {
            switchTab(tabName);
        }
    });

    // Time slider
    d3.select('#time-slider').on('input', function() {
        const value = +this.value;
        if (value === 9) {
            currentYear = 'cumulative';
            d3.select('#year-label').text('Cumulative');
        } else {
            currentYear = String(2010 + value);
            d3.select('#year-label').text(currentYear);
        }
        updateNetwork();
        updateRanking();
    });

    // Centrality selector
    d3.select('#centrality-selector').on('change', function() {
        currentCentrality = this.value;
        updateRanking();
    });

    // Top-N selector
    d3.select('#topn-selector').on('change', function() {
        currentTopN = +this.value;
        updateRanking();
    });

    // Weight slider
    d3.select('#weight-slider').on('input', function() {
        currentWeightThreshold = +this.value;
        d3.select('#weight-value').text(this.value);
        updateNetwork();
    });

    // Reset button
    d3.select('#reset-button').on('click', () => {
        d3.select('#time-slider').property('value', 9).dispatch('input');
        d3.select('#weight-slider').property('value', 1).dispatch('input');
        d3.selectAll('.node').classed('highlighted dimmed', false);
        d3.selectAll('.link').classed('highlighted dimmed', false);
    });

    // Temporal tab controls
    d3.select('#temporal-centrality-selector').on('change', function() {
        temporalCentrality = this.value;
        if (slopegraphInitialized) {
            updateSlopegraph();
        }
    });

    d3.select('#temporal-topn-selector').on('change', function() {
        temporalTopN = +this.value;
        if (slopegraphInitialized) {
            updateSlopegraph();
        }
    });

    // Bridge tab controls
    d3.select('#bridge-topn-selector').on('change', function() {
        bridgeTopN = +this.value;
        if (bridgeInitialized) {
            updateBridge();
        }
    });
}

// ============================================================================
// INIT
// ============================================================================
// METHODOLOGY TAB (Tab 4)
// ============================================================================

function initMethodology() {
    console.log('Initializing methodology tab...');

    // Setup accordion toggles
    const toggles = document.querySelectorAll('.doc-toggle');
    toggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const docName = this.getAttribute('data-doc');
            const content = document.getElementById(`doc-${docName}`);
            const isVisible = content.style.display === 'block';

            // Toggle visibility
            content.style.display = isVisible ? 'none' : 'block';

            // Toggle active class for icon rotation
            this.classList.toggle('active');

            // Load markdown if not already loaded
            if (!isVisible && content.innerHTML.includes('Loading documentation')) {
                loadMarkdown(docName);
            }
        });
    });
}

async function loadMarkdown(docName) {
    const content = document.getElementById(`doc-${docName}`);

    // Map doc names to file paths
    const fileMap = {
        'data': '../knowledge/data.md',
        'research': '../knowledge/research.md',
        'requirements': '../knowledge/requirements.md'
    };

    const filePath = fileMap[docName];

    try {
        const response = await fetch(filePath);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const markdown = await response.text();

        // Simple markdown to HTML conversion (basic)
        const html = markdownToHTML(markdown);
        content.innerHTML = html;
    } catch (error) {
        console.error(`Failed to load ${docName}.md:`, error);
        content.innerHTML = `<p style="color: #dc3545;"><strong>Error loading documentation:</strong> ${error.message}</p>
            <p>File path: <code>${filePath}</code></p>
            <p>This is expected in local development. Markdown files are served from the knowledge/ folder.</p>`;
    }
}

function markdownToHTML(markdown) {
    // Basic markdown conversion (simple implementation)
    let html = markdown;

    // Headers
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

    // Bold
    html = html.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');

    // Italic
    html = html.replace(/\*(.*?)\*/gim, '<em>$1</em>');

    // Code blocks
    html = html.replace(/```([^`]+)```/gim, '<pre><code>$1</code></pre>');

    // Inline code
    html = html.replace(/`([^`]+)`/gim, '<code>$1</code>');

    // Links
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2" target="_blank">$1</a>');

    // Unordered lists
    html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

    // Line breaks
    html = html.replace(/\n\n/g, '</p><p>');
    html = '<p>' + html + '</p>';

    // Clean up
    html = html.replace(/<p><\/p>/g, '');
    html = html.replace(/<p>(<h[1-6]>)/g, '$1');
    html = html.replace(/(<\/h[1-6]>)<\/p>/g, '$1');
    html = html.replace(/<p>(<ul>)/g, '$1');
    html = html.replace(/(<\/ul>)<\/p>/g, '$1');
    html = html.replace(/<p>(<pre>)/g, '$1');
    html = html.replace(/(<\/pre>)<\/p>/g, '$1');

    return html;
}

// ============================================================================

loadData();
