// reference: https://bl.ocks.org/hrecht/f84012ee860cb4da66331f18d588eee3

function h_bar()
{ // default settings
  var $el = d3.select("body");
  var data = [];
  var margin = {
    top: 0,
    right: 30,
    bottom: 0,
    left: 50
  };
  var width = 300 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

  // define color scale
  var color = d3.scale.category20c();

  var svg, x, y, yAxis;
  var object = {};

  object.render = function()
  {
    svg = $el.append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    x = d3.scale.linear()
      .range([0, width])
      .domain([0, d3.max(data, function (d) { return d.val; })]);

    y = d3.scale.ordinal()
      .rangeRoundBands([height, 0], .1)
      .domain(data.map(function (d) {
          return d.name;
      }));

    //make y axis to show bar names
    yAxis = d3.svg.axis()
      .scale(y)
      //no tick marks
      .tickSize(0)
      .orient("left");

    var gy = svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
      .attr( 'fill', 'white' )
      .style( "font-size", "10px" );
  
    var bars = svg.selectAll(".bar")
      .data(data)
      .enter()
      .append("g")
  
    //append rects
    bars.append("rect")
      .attr("class", "bar")
      .attr("y", function (d) {
        return y(d.name);
      })
      .attr("height", y.rangeBand())
      .attr("x", 0)
      .attr("width", function (d) {
        return x(d.val);
      })
      .style( 'fill', function(d) { return color( d.val ); } );
  
    //add a value label
    bars.append("text")
      .attr("class", "label")
      //y position of the label is halfway down the bar
      .attr("y", function (d) {
        return y(d.name) + y.rangeBand() / 2 + 4;
      })
      //x position is halfway of the bar
      .attr("x", function (d) {
        return x(d.val/2) - 5;
      })
      .text(function (d) {
        return d.val;
      })
      .attr( 'fill', 'white' );

    return object;
  };

  // getter and setter methods
  object.data = function(value)
  {
    if (!arguments.length) return data;
    data = value;

    //sort bars based on value
    data = data.sort(function (a, b)
    {
      a = String(a.name).split( '-' );
      b = String(b.name).split( '-' );

      if( a == 'N/A' )
        return d3.ascending( -1, b[ 0 ] );
      else if( b == 'N/A' )
        return d3.ascending( a[ 0 ], -1 );
      else
        return d3.ascending( a[ 0 ], b[ 0 ] );
    });

    return object;
  };

  object.width = function(value){
    if (!arguments.length) return width;
    width = value - margin.left - margin.right;
    return object;
  };

  object.height = function(value){
    if (!arguments.length) return height;
    height = value - margin.top - margin.bottom;
    return object;
  };

  object.$el = function(value)
  {
    if (!arguments.length) return $el;
    $el = value;
    return object;
  };

  return object;
};