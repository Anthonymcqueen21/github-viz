$(document).ready(function() {
	var margin = {top: 20, right: 20, bottom: 50, left: 60},
	    width = 500 - margin.left - margin.right,
	    height = 400 - margin.top - margin.bottom;

	var x = d3.time.scale()
	    .range([0, width]);

	var y = d3.scale.linear()
	    .range([height, 0]);

	var color = d3.scale.category10();

	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left");

	var svg_stars = d3.select("#star").append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	  	.append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	d3.csv("avg_stars.csv", function(error, data) {
	  if (error) throw error;

	  y.domain(d3.extent(data, function(d) { return d.avg_stars; })).nice();

    var parseDate = d3.time.format("%Y/%m").parse;
    var mindate = parseDate(data[0]['time']),
        maxdate = parseDate(data[data.length-1]['time']);

    var x = d3.time.scale()
      .domain([mindate, maxdate])
      .range([0, width]);

    var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("bottom");

    svg_stars.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .attr("fill", "white")
        .attr("font-size", "12px")
        .call(xAxis);

	  svg_stars.append("g")
	      .attr("class", "y axis")
	      .attr("fill", "white")
          .attr("font-size", "12px")
	      .call(yAxis)
	    .append("text")
	      .attr("class", "label")
	      .attr("transform", "rotate(-90)")
	      .attr("y", 6)
	      .attr("dy", ".71em")
        .style("fill", "white")
        .attr("font-size", "15px")
	      .style("text-anchor", "end")
	      .text("Average Stars")

	  svg_stars.selectAll(".dot")
	      .data(data)
	    .enter().append("circle")
	      .attr("class", "dot")
	      .attr("r", 2.5)
	      .attr("cx", function(d) { return x(parseDate(d.time)); })
	      .attr("cy", function(d) { return y(d.avg_stars); })
	      .style("fill", "#00a1ff");
	})
});