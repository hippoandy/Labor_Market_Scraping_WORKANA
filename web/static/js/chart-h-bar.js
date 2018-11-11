function hippo()
{
  alert( 'f**K' );
}

function h_bar()
{
  // default settings
  var $el = d3.select("body");
  var data = [];

  // define color scale
  var color = d3.scale.category20c();

  //set up svg using margin conventions - we'll need plenty of room on the left for labels
  var margin = {
    top: 0,
    right: 30,
    bottom: 0,
    left: 50
  };

  var svg, x, y, yAxis;
  var object = {};

  var width = 300 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

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
      .attr( 'fill', 'white' );
  
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
      //x position
      .attr("x", function (d) {
          // return x(d.val) + 3;
          return x(d.val/2);
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

    console.log( data );

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
    })

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