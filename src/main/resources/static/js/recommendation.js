var svgContainer;

d3.csv("rating.csv", function(error, data) {
    if (error) throw error;

    popularity_type = data[0]['rating'];
    star_magnet = data[1]['rating'];

    var popularity_icon;
    if (popularity_type == 'the classic') {
    	popularity_icon = "=";
    } else if (popularity_type == 'once-famous') {
    	popularity_icon = "-";
    } else {
    	popularity_icon = "+"
    }

    svgContainer = d3.select("#recommendation").append("svg")
					.attr("width", 600)
 					.attr("height", 250)
 					.append('g')
    				.attr('transform', 'translate(' + 90 + ',' + 70 + ')');

	var popularity = svgContainer.append("circle")
					.attr("r",55)
					.attr("stroke",'#00a1ff')
					.attr("stroke-width",15)
					.attr("fill","none");

	var popularity_text = svgContainer
					.append("text")
	        		.attr("fill", "white")
	        		.attr("font-size", "20px")
	        		.attr("font-family", "Ubuntu")
	        		.attr("x", "10%")
	        		.attr("y", "36%")
	        		.attr("letter-spacing","3")
	        		.style("text-anchor", "middle")
		      		.text(popularity_type)
	var popularity_val = svgContainer
					.append("text")
	        		.attr("fill", "#00a1ff")
	        		.attr("font-size", "75px")
	        		.attr("font-family", "Ubuntu")
	        		.attr("x", "3.5%")
	        		.attr("y", "9%")
	        		.attr("letter-spacing","3")
	        		.style("text-anchor", "end")
		      		.text(popularity_icon)

	var language = svgContainer.append("circle")
					.attr("r",55)
					.attr("cx", 200)
					.attr("stroke",'#2655ff')
					.attr("stroke-width",15)
					.attr("fill","none");

	var star = svgContainer.append("circle")
					.attr("r",55)
					.attr("cx", 400)
					.attr("stroke",'#0e468c')
					.attr("stroke-width",15)
					.attr("fill","none");

	var star = svgContainer
					.append("text")
	        		.attr("fill", "white")
	        		.attr("font-size", "20px")
	        		.attr("font-family", "Ubuntu")
	        		.attr("x", "78%")
	        		.attr("y", "36%")
	        		.attr("letter-spacing","3")
	        		.style("text-anchor", "end")
		      		.text("star magnet")

	var star_val = svgContainer
					.append("text")
	        		.attr("fill", "#0e468c")
	        		.attr("font-size", "60px")
	        		.attr("font-family", "Ubuntu")
	        		.attr("x", "72.5%")
	        		.attr("y", "7.5%")
	        		.attr("letter-spacing","3")
	        		.style("text-anchor", "end")
		      		.text(star_magnet)

	d3.csv("language.csv", function(error, data) {
    if (error) throw error;

    language_name = String(data[0]['language']);
    score = data[0]['score'];

	var language = svgContainer.append("circle")
					.attr("r",55)
					.attr("cx", 200)
					.attr("stroke",'#2655ff')
					.attr("stroke-width",15)
					.attr("fill","none");

	var language_text = svgContainer
					.append("text")
	        		.attr("fill", "white")
	        		.attr("font-size", "20px")
	        		.attr("font-family", "Ubuntu")
	        		.attr("x", "33%")
	        		.attr("y", "36%")
	        		.attr("letter-spacing","3")
	        		.style("text-anchor", "middle")
		      		.text(language_name);

	var language_val = svgContainer
					.append("text")
	        		.attr("fill", "#2655ff")
	        		.attr("font-size", "60px")
	        		.attr("font-family", "Ubuntu")
	        		.attr("x", "39%")
	        		.attr("y", "7.5%")
	        		.attr("letter-spacing","3")
	        		.style("text-anchor", "end")
		      		.text(score)
	});
});




