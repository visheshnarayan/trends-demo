// TODO : Add line chart with zoom (https://d3-graph-gallery.com/graph/line_brushZoom.html)
// TODO : Line Plot with annotations (https://d3-graph-gallery.com/graph/connectedscatter_tooltip.html)
// TODO : show base term

function visualize() {
    console.log("===graph visualize===");

    // Set dimensions and margins
    var margin = { top: 10, right: 100, bottom: 50, left: 30 },
        divW = d3.select('#my_dataviz').node().getBoundingClientRect().width,
        width = divW - margin.left - margin.right,
        height = divW / 2 - margin.top - margin.bottom;

    // Clear any existing SVG content
    d3.select("#my_dataviz").selectAll('*').remove();

    // Append the SVG object to the body of the page
    var svg = d3.select("#my_dataviz")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Load data and plot
    d3.csv(graph_src, function(data) {
        var allGroup = graph_context.rel_terms;

        // Prepare data, splitting line segments where values are -1.0
        var dataReady = allGroup.map(function(grpName) {
            return {
                name: grpName,
                values: data.map(function(d) {
                    return { time: +d.time, value: +d[grpName] };
                })
            };
        });

        // Filter out groups where all values are negative
        var invalidGroups = [];
        dataReady = dataReady.filter(function(group) {
            var hasValidValue = group.values.some(function(d) { return d.value >= 0; });
            if (!hasValidValue) {
                invalidGroups.push(group.name);
            }
            return hasValidValue;
        });

        // Update the group names to only include valid groups
        var validGroups = dataReady.map(function(d) { return d.name; });

        // Color scale
        var myColor = d3.scaleOrdinal()
            .domain(validGroups)
            .range(d3.schemeSet2);

        // Define scales and axes
        var xScale = d3.scaleBand().range([0, width]).padding(0.4);
        xScale.domain(graph_context.period_labels);

        var x = d3.scaleLinear()
            .domain([0, graph_context.rangeX])
            .range([0, width]);

        var y = d3.scaleLinear()
            .domain([0, graph_context.rangeY])
            .range([height, 1.5 * margin.top + margin.bottom]);

        // Append axes
        var xAxis = svg.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(xScale));

        // Rotate the tick labels
        xAxis.selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "-0.8em")
            .attr("dy", "0.15em")
            .attr("transform", "rotate(-65)");

        // Append y-axis
        svg.append("g")
            .call(d3.axisLeft(y));

        // Line generator with `defined` to skip negative values
        var line = d3.line()
            .defined(function(d) {
                return d.value >= 0; 
            }) // Ignore points with negative values
            .x(function(d) { return x(d.time); })
            .y(function(d) { return y(d.value); });

        // Draw lines, with breaks for -1.0 values
        svg.selectAll("myLines")
            .data(dataReady)
            .enter()
            .append("path")
            .attr("class", function(d) { return d.name; })
            .attr("d", function(d) { return line(d.values); })
            .attr("stroke", function(d) { return myColor(d.name); })
            .style("stroke-width", 4)
            .style("fill", "none");

        // Add the points, only for positive values
        svg.selectAll("myDots")
            .data(dataReady)
            .enter()
            .append('g')
            .style("fill", function(d) { return myColor(d.name); })
            .attr("class", function(d) { return d.name; })
            .selectAll("myPoints")
            .data(function(d) { return d.values; })
            .enter()
            .append("circle")
            .filter(function(d) { return d.value >= 0; }) // Only show points with positive values
            .attr("cx", function(d) { return x(d.time); })
            .attr("cy", function(d) { return y(d.value); })
            .attr("r", 5)
            .attr("stroke", "white");

        // Add a label at the end of each line
        svg.selectAll("myLabels")
            .data(dataReady)
            .enter()
            .append('g')
            .append("text")
            .attr("class", function(d) { return d.name; })
            .datum(function(d) { 
                // Filter values to get the last valid data point
                let lastValid = d.values.filter(v => v.value >= 0).pop(); 
                return { name: d.name, value: lastValid };
            })
            .attr("transform", function(d) { return "translate(" + x(d.value.time) + "," + y(d.value.value) + ")"; })
            .attr("x", 12) // shift the text a bit more right
            .text(function(d) { return d.name; })
            .style("fill", function(d) { return myColor(d.name); })
            .style("font-size", 15);

        // temp data for spacing legend
        var dist = 20;
        var last = 0;

        // Add a legend (interactive)
        svg.selectAll("myLegend")
            .data(dataReady)
            .enter()
            .append('g')
            .append("text")
            .attr('x', function(d, i) {
                dist += (last + 2) * 9;
                last = d.name.length;
                return dist;
            })
            .style("stroke-width", 4)
            .attr('y', 30)
            .text(function(d) { return d.name; })
            .style("fill", function(d) { return myColor(d.name); })
            .style("font-size", 15)
            .style("cursor", "pointer")
            .on("click", function(d) {
                // Check if the element is currently visible
                var currentOpacity = d3.selectAll("." + d.name).style("opacity");
                // Toggle opacity between 0 and 1
                d3.selectAll("." + d.name).transition().style("opacity", currentOpacity == 1 ? 0 : 1);
            });

        // Display a message if there are terms with no data
        if (invalidGroups.length > 0) {
            svg.append("text")
                .attr("x", margin.left)             
                .attr("y", 50)
                .attr("text-anchor", "start")  
                .style("font-size", "12px") 
                .style("fill", "red")
                .text("No data for terms: " + invalidGroups.join(", "));
        }
    });

    console.log("graph visualize end!!!");
}
