
//Create function createBar and append x and y axis,text
function createBar(width, height) {
    var bar = d3.select("#bar")
                    .attr("width", width)
                    .attr("height", height);
  
    bar.append("g")
        .classed("x-axis", true);
  
    bar.append("g")
        .classed("y-axis", true);
  
    bar.append("text")
        .attr("transform", "rotate(-90)")
        .attr("x", - height / 2)
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .style("font-size", "1em")
        .classed("y-axis-label", true);
  
    bar.append("text")
        .attr("x", width / 2)
        .attr("y", "1em")
        .attr("font-size", "1.5em")
        .style("text-anchor", "middle")
        .classed("bar-title", true);
  }
  // create function highlightBars grabs all rectangles and updates "fill" based on current year
  function highlightBars(year) {
    d3.select("#bar")
      .selectAll("rect")
        .attr("fill", d => d.year === year ? "#16a085" : "#1abc9c");
  }
  // Create function drawBar
  function drawBar(data, dataType, country) {
    var bar = d3.select("#bar");
    var padding = {
      top: 40,
      right: 20,
      bottom: 30,
      left: 130
    };
    var barPadding = 1;
    var width = +bar.attr("width");
    var height = +bar.attr("height");
    var countryData = data.filter(d => d.country === country)
                          .sort((a, b) => a.year - b.year);
  
    var xScale = d3.scaleLinear()
                   .domain(d3.extent(data, d => d.year))
                   .range([padding.left, width - padding.right]);
  
    var yScale = d3.scaleLinear()
                   .domain([0, d3.max(countryData, d => d[dataType])])
                   .range([height - padding.bottom, padding.top]);
  
    var barWidth = xScale(xScale.domain()[0] + 1) - xScale.range()[0];
  
    var xAxis = d3.axisBottom(xScale)
                  .tickFormat(d3.format(".0f"));
  
    d3.select(".x-axis")
        .attr("transform", "translate(0, " + (height - padding.bottom) + ")")
        .call(xAxis);
  
    var yAxis = d3.axisLeft(yScale);
  
    d3.select(".y-axis")
        .attr("transform", "translate(" + (padding.left - barWidth / 2) + ",0)")
        .transition()
        .duration(1000)
        .call(yAxis);
  
    var axisLabel = dataType === "emissions" ?
      "Consumption, thousand metric tons" :
      "Consumption, metric tons per capita";
  
    var barTitle = country ?
      "Beef Consumption, " + country :
      "Click on a country to see annual trends.";
  
    d3.select(".y-axis-label")
        .text(axisLabel);
  
    d3.select(".bar-title")
        .text(barTitle);
    
  // create variable for transition with easeBounceOut
    var t = d3.transition()
              .duration(1000)
              .ease(d3.easeBounceOut);
  
    var update = bar 
                   .selectAll(".bar")
                   .data(countryData);
  
    update
      .exit()
      .transition(t)
        .delay((d, i, nodes) => (nodes.length - i - 1) * 100)
        .attr("y", height - padding.bottom)
        .attr("height", 0)
        .remove();
    
  //Add rectangles merge/bind new data
    update
      .enter()
      .append("rect")
        .classed("bar", true)
        .attr("y", height - padding.bottom)
        .attr("height", 0)
      .merge(update)
        .attr("x", d => (xScale(d.year) + xScale(d.year - 1)) / 2)
        .attr("width", barWidth - barPadding)
        .transition(t)
        .delay((d, i) => i * 100)
          .attr("y", d => yScale(d[dataType]))
          .attr("height", d => height - padding.bottom - yScale(d[dataType]));
  }