function donut_label()
{
  var $el = d3.select("body")

  var max = 10000;

  // var color = d3.scale.ordinal()
  //   .domain(["Lorem ipsum", "dolor sit", "amet", "consectetur", "adipisicing", "elit", "sed", "do", "eiusmod", "tempor", "incididunt"])
  //   .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c", "#ff8c00"]);
  var color = d3.scale.category20c();
  // var color = d3.scale.linear()
  //       .domain([1, max])
  //       .range(['#6EACFF', '#1F549B']);
  // var color = d3.scale.linear()
  //   .domain([1, max])
  //   .interpolate(d3.interpolateHcl)
  //   .range([d3.rgb("#6EACFF"), d3.rgb('#184F97')]);
  var data = [];

  var width = 960,
      height = 600,
      radius = Math.min(width, height) / 2;

  var pie = d3.layout.pie()
    .sort(null)
    .value(function(d) {
      return d.value;
    });

  var svg, g, arc;
  var object = {};

  object.render = function()
  {
    arc = d3.svg.arc()
      .outerRadius(radius * 0.8)
      .innerRadius(radius * 0.4);

    var outerArc = d3.svg.arc()
      .innerRadius(radius * 0.9)
      .outerRadius(radius * 0.9);

    svg = $el.append("svg")
      .attr( 'width', width )
      .attr( 'height', height );
      // .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
    var g = svg.append("g")
      .attr( 'width', width )
      .attr( 'height', height )
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    g.append("g")
      .attr("class", "labels");
    g.append("g")
      .attr("class", "slices");
    g.append("g")
      .attr("class", "lines");

    var key = function(d){ return d.data.label; };

    /* ------- PIE SLICES -------*/
    var slice = svg.select(".slices").selectAll("path.slice")
      .data(pie(data), key);
    slice.enter()
      .insert("path")
      .style("fill", function(d) { return color(d.value); })
      .attr("class", "slice");
    slice		
      .transition().duration(1000)
      .attrTween("d", function(d) {
        this._current = this._current || d;
        var interpolate = d3.interpolate(this._current, d);
        this._current = interpolate(0);
        return function(t) {
          return arc(interpolate(t));
        };
      })
    slice.exit().remove();

    /* ------- TEXT LABELS -------*/
    var text = svg.select(".labels").selectAll("text")
      .data(pie(data), key);

    text.enter()
      .append("text")
      .attr("dy", ".25em")
      .attr( 'style', 'font-size: 10px;' )
      .text(function(d) {
        return d.data.label+": "+d.data.value;
      });

    function midAngle(d){
      return d.startAngle + (d.endAngle - d.startAngle)/2;
    }

    text.transition().duration(1000)
      .attrTween("transform", function(d) {
        this._current = this._current || d;
        var interpolate = d3.interpolate(this._current, d);
        this._current = interpolate(0);
        return function(t) {
          var d2 = interpolate(t);
          var pos = outerArc.centroid(d2);
          pos[0] = radius * (midAngle(d2) < Math.PI ? 1 : -1);
          return "translate("+ pos +")";
        };
      })
      .styleTween("text-anchor", function(d){
        this._current = this._current || d;
        var interpolate = d3.interpolate(this._current, d);
        this._current = interpolate(0);
        return function(t) {
          var d2 = interpolate(t);
          return midAngle(d2) < Math.PI ? "start":"end";
        };
      });
    text.exit().remove();

    /* ------- SLICE TO TEXT POLYLINES -------*/
    var polyline = svg.select(".lines").selectAll("polyline")
      .data(pie(data), key);
    polyline.enter().append("polyline");
    polyline.transition().duration(1000)
      .attrTween("points", function(d){
        this._current = this._current || d;
        var interpolate = d3.interpolate(this._current, d);
        this._current = interpolate(0);
        return function(t) {
          var d2 = interpolate(t);
          var pos = outerArc.centroid(d2);
          pos[0] = radius * 0.95 * (midAngle(d2) < Math.PI ? 1 : -1);
          return [arc.centroid(d2), outerArc.centroid(d2), pos];
        };			
      });
    polyline.exit().remove();

    return object;
  }

  // Getter and setter methods
  object.max = function(value){
    if (!arguments.length) return data;
    max = value;
    return object;
  };

  object.data = function(value){
    if (!arguments.length) return data;
    data = value;
    return object;
  };

  object.$el = function(value){
    if (!arguments.length) return $el;
    $el = value;
    return object;
  };

  object.width = function(value){
    if (!arguments.length) return width;
    width = value;
    radius = Math.min(width, height) / 2;
    return object;
  };

  object.height = function(value){
    if (!arguments.length) return height;
    height = value;
    radius = Math.min(width, height) / 2;
    return object;
  };

  return object;
};