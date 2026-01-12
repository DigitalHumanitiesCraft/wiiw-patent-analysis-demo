// ============================================================================
// GLOBAL STATE
// ============================================================================

let data = null;           // Full JSON data
let currentYear = 'cumulative';
let currentCentrality = 'degree_centrality';
let currentTopN = 20;
let currentWeightThreshold = 1;

let simulation = null;     // Force simulation
let svg = null;            // SVG selections

// Color scale for communities (will be set after data load)
let colorScale = null;

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
        initTemporal();
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
        .attr('fill', d => colorScale(d.community));

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
        .attr('fill', d => colorScale(d.community));

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

function initTemporal() {
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

    const container = d3.select('#temporal-svg');
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
            .call(d3.axisBottom(xScale).ticks(4).tickFormat(d3.format('d')));

        cell.append('g')
            .call(d3.axisLeft(yScale).ticks(4));

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

function initControls() {
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

    // Play button
    let playInterval = null;
    d3.select('#play-button').on('click', function() {
        if (playInterval) {
            clearInterval(playInterval);
            playInterval = null;
            this.textContent = 'Play';
        } else {
            this.textContent = 'Pause';
            let yearIndex = 0;
            playInterval = setInterval(() => {
                if (yearIndex > 9) {
                    clearInterval(playInterval);
                    playInterval = null;
                    d3.select('#play-button').text('Play');
                    return;
                }
                d3.select('#time-slider').property('value', yearIndex);
                d3.select('#time-slider').dispatch('input');
                yearIndex++;
            }, 500);
        }
    });

    // Reset button
    d3.select('#reset-button').on('click', () => {
        d3.select('#time-slider').property('value', 9).dispatch('input');
        d3.select('#weight-slider').property('value', 1).dispatch('input');
        d3.selectAll('.node').classed('highlighted dimmed', false);
        d3.selectAll('.link').classed('highlighted dimmed', false);
    });
}

// ============================================================================
// INIT
// ============================================================================

loadData();
