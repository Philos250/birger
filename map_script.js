// map_script.js

// D3.js setup
const color = d3.scaleQuantize([1, 10], d3.schemeBlues[9]);
const path = d3.geoPath();
const format = d => `${d}%`;
const valuemap = new Map(unemployment.map(d => [namemap.get(d.name), d.rate]));

// Create SVG container
const svg = d3.create("svg")
    .attr("width", 975)
    .attr("height", 610)
    .attr("viewBox", [0, 0, 975, 610])
    .attr("style", "max-width: 100%; height: auto;");

// Legend
svg.append("g")
    .attr("transform", "translate(610,20)")
    .append(() => Legend(color, {title: "Unemployment rate (%)", width: 260}));

// Draw states
svg.append("g")
    .selectAll("path")
    .data(topojson.feature(us, us.objects.states).features)
    .join("path")
    .attr("fill", d => color(valuemap.get(d.id)))
    .attr("d", path)
    .append("title")
    .text(d => `${d.properties.name} ${valuemap.get(d.id)}%`);

// Draw state borders
svg.append("path")
    .datum(topojson.mesh(us, us.objects.states, (a, b) => a !== b))
    .attr("fill", "none")
    .attr("stroke", "white")
    .attr("stroke-linejoin", "round")
    .attr("d", path);

// Return the SVG container
svg.node();
