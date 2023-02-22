function visualize(context){
    // set the dimensions and margins of the graph
    var margin = {top: 10, right: 150, bottom: 20, left: 30},
    divW = d3.select('#my_dataviz').node().getBoundingClientRect().width,
    width = divW - margin.left - margin.right,
    height = divW/2 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    var svg = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

    var x = context;
    console.log(x)
    const graph = JSON.parse(x.replace(/'/g, '"'))
    console.log(graph);

    /* MAKE GRAPH */
    var allGroup = graph.rel_terms

    // Reformat the data: we need an array of arrays of {x, y} tuples
    var dataReady =  graph.dataready

    // I strongly advise to have a look to dataReady with
    console.log(dataReady)

    // A color scale: one color for each group
    var myColor = d3.scaleOrdinal()
    .domain(allGroup)
    .range(d3.schemeSet2);

    // Add X axis --> it is a date format
    var x = d3.scaleLinear()
    .domain([0,7])
    .range([ 0, width ]);

    svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

    // Add Y axis
    var y = d3.scaleLinear()
    .domain( [0,1.2])
    .range([ height, 0 ]);

    svg.append("g")
    .call(d3.axisLeft(y));

    // Add the lines
    var line = d3.line()
    .x(function(d) { return x(+d.time) })
    .y(function(d) { return y(+d.value) })

    svg.selectAll("myLines")
    .data(dataReady)
    .enter()
    .append("path")
    .attr("class", function(d){ return d.name })
    .attr("d", function(d){ return line(d.values) } )
    .attr("stroke", function(d){ return myColor(d.name) })
    .style("stroke-width", 4)
    .style("fill", "none")

    // Add the points
    svg
    // First we need to enter in a group
    .selectAll("myDots")
    .data(dataReady)
    .enter()
    .append('g')
    .style("fill", function(d){ return myColor(d.name) })
    .attr("class", function(d){ return d.name })
    // Second we need to enter in the 'values' part of this group
    .selectAll("myPoints")
    .data(function(d){ return d.values })
    .enter()
    .append("circle")
    .attr("cx", function(d) { return x(d.time) } )
    .attr("cy", function(d) { return y(d.value) } )
    .attr("r", 5)
    .attr("stroke", "white")

    // Add a label at the end of each line
    svg
    .selectAll("myLabels")
    .data(dataReady)
    .enter()
    .append('g')
    .append("text")
    .attr("class", function(d){ return d.name })
    .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; }) // keep only the last value of each time series
    .attr("transform", function(d) { return "translate(" + x(d.value.time) + "," + y(d.value.value) + ")"; }) // Put the text at the position of the last point
    .attr("x", 12) // shift the text a bit more right
    .text(function(d) { return d.name; })
    .style("fill", function(d){ return myColor(d.name) })
    .style("font-size", 15)

    // temp datafor spacing legend
    var first = true;
    var dist = 30;
    var last = 0;

    // Add a legend (interactive)
    svg
    .selectAll("myLegend")
    .data(dataReady)
    .enter()
    .append('g')
    .append("text")
    .attr('x', function(d,i){ 
        if (first) {
            first = false;
            last = d.name.length;
            return 30;
        } else {
            dist += (last+2)*9;
            last = d.name.length;
            return dist;
        }	
    })
    .attr('y', 30)
    .text(function(d) { return d.name; })
    .style("fill", function(d){ return myColor(d.name) })
    .style("font-size", 15)
    .style("cursor", "pointer")
        .on("click", function(d){
        // is the element currently visible ?
        currentOpacity = d3.selectAll("." + d.name).style("opacity")
        // Change the opacity: from 0 to 1 or from 1 to 0
        d3.selectAll("." + d.name).transition().style("opacity", currentOpacity == 1 ? 0:1)
        })		
}	