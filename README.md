This visualization was built by modifying [choropleth example code by Scott Murray](https://github.com/alignedleft/d3-book/blob/master/chapter_12/05_choropleth.html), [tooltip example code by Malcolm Maclean](http://www.d3noob.org/2013/01/adding-tooltips-to-d3js-graph.html), and [legend code example by Mike Bostock](http://bl.ocks.org/mbostock/3888852). 


<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<script src="http://d3js.org/d3.v3.min.js"></script>
<style type="text/css">
path:hover {
	fill-opacity: .7;
}
div.tooltip {
 	position: absolute;
	text-align: center;
	width: 300px;
	height: 800px;
	padding: 2px;
	font: 12px sans-serif;
	background: white;
	border: 0px;
	border-radius: 8px;
	/* pointer-events: none; */
}


body {
	font: 11px sans-serif;
}

.legend {
	position:absolute;
	left:800px;
	top:350px;
}

</style>
</head>
<body>
<script type="text/javascript">

//Width and height of map
var width = 960;
var height = 500;

// D3 Projection
var projection = d3.geo.albersUsa()
				   .translate([width/2, height/2])    // translate to center of screen
				   .scale([1000]);          // scale things down so see entire US

// Define path generator
var path = d3.geo.path()               // path generator that will convert GeoJSON to SVG paths
		  	 .projection(projection);  // tell path generator to use albersUsa projection


// Define linear scale for output
var color = d3.scale.linear()
			  .range(["rgb(213,222,217)","rgb(69,173,168)","rgb(84,36,55)","rgb(217,91,67)"]);

var legendText = ["Cities Lived", "States Lived", "States Visited", "Nada"];

//Create SVG element and append map to the SVG
var svg = d3.select("body")
			.append("svg")
			.attr("width", width)
			.attr("height", height);


// Append Div for tooltip to SVG
var div = d3.select("body")
		    .append("div")
    		.attr("class", "tooltip")
    		.style("opacity", 0);

var newEngland = ["Massachusetts", "Rhode Island", "Connecticut", "New Hampshire", "Vermont", "Maine", "New York", "Pennsylvania"];
var oeffa = ["Ohio", "Indiana", "Illinois", "Iowa", "Missouri", "Wisconsin", "Michigan", "Kentucky", "West Virginia", "Virginia", "New York", "Pennsylvania"]

var hoverText = function(d) {
	var text = ""
	for (i = 0; i < d.length; i++) {
		text = text + "<strong>Certification: " + d[i][0] + "</strong><br />" + "Link: <a href=\"" + d[i][2] + "\" target=\"_blank\">" + d[i][1] + "</a>" + "<br /> <br />"
	}
	console.log(text)
	return text
}

// Load in my states data!
d3.csv("redtomato.csv", function(data) {
color.domain([0,1,2,3]); // setting the range of the input data

// Load GeoJSON data and merge with states data
d3.json("us-states.json", function(json) {

// Loop through each state data value in the .csv file
for (var j = 0; j < json.features.length;j++) {
	var jsonState = json.features[j].properties.name;
	var certifications = []
	for (var i = 0; i < data.length; i++) {
		// Grab State Name
		var dataState = data[i]["Area of Coverage"].trim();

		// Grab data value
		var dataName = data[i]["Program"];

		var dataValue = data[i]["Link to Website"]
		var dataLink = data[i]["Real link"]
		if (dataState === jsonState) {
			certifications.push([dataName, dataValue, dataLink])
		}
		var temp = dataState.toLowerCase()
		if (temp == "national" || temp == "international" || temp == "north america" || temp == "u.s.a and canada") {
			certifications.push([dataName, dataValue, dataLink])
		}
		if (dataState == "New England") {
			if (newEngland.indexOf(jsonState) != -1) {
				certifications.push([dataName, dataValue, dataLink])
			}
		}
		if (dataName === "OEFFA Certification") {
			if (oeffa.indexOf(jsonState) != -1) {
				certifications.push([dataName, dataValue, dataLink])
			}
		}
	}
	json.features[j].properties.certs = certifications
}

// Bind the data to the SVG and create one path per GeoJSON feature
svg.selectAll("path")
	.data(json.features)
	.enter()
	.append("path")
	.attr("d", path)
	.style("stroke", "#fff")
	.style("stroke-width", "1")
	.style("fill", d3.color("steelblue") )
	.style("opacity", 0.85)
	.on("click", function(d) {
			div.transition()
            .duration(500)
            .style("opacity", 0);
			div.transition()
			.duration(500)
			.style("opacity", 1);
			div.style('pointer-events', 'visible');
			div.html( "<h2><br/>"+ d.properties.name +"</h2><br/>"+"<br/>"
            + hoverText(d.properties.certs))
						.style("left", (d3.event.pageX - 100) + "px")
						.style("top", (d3.event.pageY - 28) + "px");
		  d3.event.stopPropagation();
	});
});
d3.select('body').on('click', resetTooltip)

  function resetTooltip() {
    // reset tooltip state
    div.style('opacity', 0)
		div.text("")
		div.style('pointer-events', 'none')
    $(".tooltip1").hide()
  }

	});
</script>
</body>
</html>
