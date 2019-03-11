//Create function createMap, select #map and append attributes
function createMap(width, height) {
    d3.select("#map")
        .attr("width", width)
        .attr("height", height)
      .append("text")
        .attr("x", width / 2)
        .attr("y", "1em")
        .attr("font-size", "1.5em")
        .style("text-anchor", "middle")
        .classed("map-title", true);
  }
  
  function drawMap(geoData, climateData, year, dataType) {
    var map = d3.select("#map");
   //projection function transforms spherical polygonal geometry to planar polygonal geometry
  // geoMercator spherical Mercator projection scale and translate it based on svg
    var projection = d3.geoMercator()
                       .scale(110)
                       .translate([
                         +map.attr("width") / 2,
                         +map.attr("height") / 1.4
                       ]);
  // create new geographic path generator
    var path = d3.geoPath()
                 .projection(projection);
    
  //grabs 'year-val' id to update text to currentYear
    d3.select("#year-val").text(year);
  
  //join climateData to geography. Filter country codes to match data ids.
  //create variable to refer to country
  //d.property keys equal to climatedata if it exists, or simple object if it doesn't
    geoData.forEach(d => {
      var countries = climateData.filter(row => row.countryCode === d.id);
      var name = '';
      if (countries.length > 0) name = countries[0].country;
      d.properties = countries.find(c => c.year === year) || { country: name };
    });
  
    var colors = ["#f1c40f", "#e67e22", "#e74c3c", "#c0392b"];
  
    var domains = {
      emissions: [0, 1000000000, 3000000000, 5000000000, 7000000000, 10000000000],
      emissionsPerCapita: [0, 10, 20, 30, 40, 50, 60]
    };
  
    var mapColorScale = d3.scaleLinear()
                          .domain(domains[dataType])
                          .range(colors);
  
    var update = map.selectAll(".country")
                    .data(geoData);
  //update pattern, merge binds exisiting data elements to new data
    update
      .enter()
      .append("path")
        .classed("country", true)
        .attr("d", path)
        .on("click", function() {
          var currentDataType = d3.select("input:checked")
                                  .property("value");
          var country = d3.select(this);
          var isActive = country.classed("active");
          var countryName = isActive ? "" : country.data()[0].properties.country;
          drawBar(climateData, currentDataType, countryName);
          highlightBars(+d3.select("#year").property("value"));
          d3.selectAll(".country").classed("active", false);
          country.classed("active", !isActive);
        })
      .merge(update)
        .transition()
        .duration(750)
        .attr("fill", d => {
          var val = d.properties[dataType];
          return val ? mapColorScale(val) : "#ccc";
        });
    //select map-title and change the title
    d3.select(".map-title")
        .text("Beef " + graphTitle(dataType) + ", " + year);
  }
  
  // helper function that converts keys from camelcase string, adds space and changes to lowercase
  function graphTitle(str) {
    return str.replace(/[A-Z]/g, c => " " + c.toLowerCase());
  }
  