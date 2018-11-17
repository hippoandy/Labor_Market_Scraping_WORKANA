// reference: http://bl.ocks.org/ericcoopey/6382449

function wordcloud()
{ // default settings
  var $el = d3.select("body");
  var width = 250,
      height = 250;
  var data = [];

  var max = 0;

  var object = {};

  object.render = function()
  {
    // define color scale
    // var color = d3.scale.linear()
    //   .domain([0,1,2,3,4,5,6,10,15,20,100])
    //   .range(["#ddd", "#ccc", "#bbb", "#aaa", "#999", "#888", "#777", "#666", "#555", "#444", "#333", "#222"]);
    var color = d3.scale.category20c();

    // functions locate in file "draw-wordcloud.js"
    d3.layout.cloud().size([width, height])
      .padding( 2 )
      .words( data )
      .rotate(0)
      .fontSize(function(d) { return (d.val * 2); })
      .on("end", draw)
      .start();

    function draw( words )
    {
      $el.append("svg")
        .attr("width", (width + width/2))
        .attr("height", height)
        .attr("class", "wordcloud")
        .append("g")
        /* without the transform, words would get cutoff to the left and top,
            they would appear outside of the SVG area */
        .attr("transform", "translate(" + width/2 + "," + height/2 + ")")
        .selectAll("text")
        .data(words)
        .enter().append("text")
        .style("font-size", function(d) {
          if( max <= 15 )
            return (d.val*3) + "px";
          else if( max > 15 && max <= 50 )
            return (d.val*2) + "px";
          else if( max > 50 && max <= 100 )
            return (d.val*1) + "px";
          else
            return (d.val*0.9) + "px";
        })
        .style("fill", function(d, i) { return color(i); })
        .attr("transform", function(d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.name; });
    }
    return object;
  }

  // getter and setter methods
  object.data = function(value)
  {
    if (!arguments.length) return data;
    data = value;

    // find the max
    max = Math.max.apply(Math, data.map(function(o) { return o.val; }))
    return object;
  };

  object.width = function(value){
    if (!arguments.length) return width;
    width = value;
    return object;
  };

  object.height = function(value){
    if (!arguments.length) return height;
    height = value
    return object;
  };

  object.$el = function(value)
  {
    if (!arguments.length) return $el;
    $el = value;
    return object;
  };

  return object;
}