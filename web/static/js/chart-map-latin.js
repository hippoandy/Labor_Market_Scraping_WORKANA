// reference: https://bl.ocks.org/john-guerra/43c7656821069d00dcbc

var req_url = "{{ url_for( 'frontend.countryHRSkills' ) }}";

function latin()
{ // default settings
  var $el = d3.select("body");
  var data = {};
  var data_avg = {};
  var total_avg = 0;
  var width = 800,
      height = 600,
      scale = 300,
      center = [-74, -15];

  // define color scale
  //var color = d3.scale.category20c();
  var color = d3.scale.linear()
        .domain([1, width])
        .range(['#fff', '#0A428A'])
        .interpolate( d3.interpolateHcl ); //interpolateHsl interpolateHcl interpolateRgb
  
  // projection settings
  var projection = d3.geo.mercator()
    .scale( scale )
    .center( center )
    .translate([width / 2, height / 2]);
  var path = d3.geo.path().projection( projection );

  var svg, g, centered, effectLayer, mapLayer, bigText;
  var object = {};

  var info_card = document.getElementById( 'map-detail' );
  var no_data = '<red>NO DATA!</red>';

  // method for render/refresh graph
  object.render = function()
  {
      // set svg width & height
      svg = $el.append('svg')
        .attr('width', width)
        .attr('height', height);

      // add background
      svg.append('rect')
        .attr('class', 'background')
        .attr('width', width)
        .attr('height', height)
        .on('click', clicked);

      g = svg.append('g');
      effectLayer = g.append('g').classed('effect-layer', true);
      mapLayer = g.append('g').classed('map-layer', true);
      bigText = g.append('text')
        .classed('big-text', true)
        .attr('x', 0)
        .attr('y', 25);

      // load map data
      d3.json( data, function(error, mapData)
      {   var features = mapData.features;
          // update color scale domain based on data
          color.domain([0, d3.max(features, country_avg)]);
          // draw each country as a path
          mapLayer.selectAll('path')
            .data(features)
            .enter().append('path')
            .attr('d', path)
            .attr('vector-effect', 'non-scaling-stroke')
            .style('fill', fill_country)
            .on('mouseover', mouseover)
            .on('mouseout', mouseout)
            .on('click', clicked);
      });

      return object;
  };

  // getter and setter methods
  object.data = function(value) {
    if (!arguments.length) return data;
    data = value;
    return object;
  };

  object.data_avg = function(value) {
    if (!arguments.length) return data;
    data_avg = value;
    return object;
  };

  object.total_avg = function(value) {
    if (!arguments.length) return data;
    total_avg = value;
    return object;
  };

  object.center = function(value) {
    if (!arguments.length) return width;
    center = value;
    return object;
  };

  object.scale = function(value) {
    if (!arguments.length) return width;
    scale = value;
    return object;
  };

  object.width = function(value) {
    if (!arguments.length) return width;
    width = value;
    return object;
  };

  object.height = function(value) {
    if (!arguments.length) return height;
    height = value;
    return object;
  };

  object.$el = function(value) {
    if (!arguments.length) return $el;
    $el = value;
    return object;
  };

  // get country name
  function country_name(d)
  {
    return d && d.properties ? d.properties.name : null;
  }

  // get country avg. value
  function country_avg(d)
  { var n = country_name(d);
    return n ? data_avg[ n ] : 0;
  }

  // get country color
  function fill_country(d)
  { var v = country_avg(d);
    if( v == 0 || v == undefined ) return '#fff';
    else return color(v);
  }

  // when clicked, zoom in
  function clicked(d)
  { var x, y, k;

    // compute centroid of the selected path
    if (d && centered !== d)
    {
      // clear bar chart
      document.getElementById( 'map-detail-hbar' ).innerHTML = "";

      var centroid = path.centroid(d);
      x = centroid[0];
      y = centroid[1];
      k = 2.5;
      centered = d;

      // hide bigText
      bigText.style( 'visibility', 'hidden' );
      // show info-card
      info_card.setAttribute( 'style', 'visibility: visible; opacity: 1; transition-delay: 0s;' );
      // update info-card content
      var v = data_avg[ d.properties.name ];
      var val_container = document.getElementById( 'map-detail-value' );
      var vstat_container = document.getElementById( 'map-detail-vstat' );
      if( v == undefined )
      {
        val_container.innerHTML = no_data;
        document.getElementById( 'map-detail-hbar' ).innerHTML = no_data;
      }
      else
      {
        // get hourly rate distribution for each selected country
        $(function()
        {
          // $.getJSON( '/_country_hr_dist',
          $.getJSON( req_url,
          // $.getJSON( "{{ url_for( 'frontend.countryHRSkills' ) }}",
            { country: d.properties.name },
            function( data )
            {
              h_bar()
                .$el( d3.select("#map-detail-hbar") )
                .data( data )
                .render();
            }
        );});
        val_container.innerHTML = "$" + v + " USD";
      }
      document.getElementById( 'map-detail-title' ).innerHTML = d.properties.name;
      if( v > total_avg )
        vstat_container.innerHTML = "<green>Above average</green>";
      else if( v == total_avg )
        vstat_container.innerHTML = "<yellow>Same as average</yellow>";
      else if( v == undefined )
        vstat_container.innerHTML = no_data;
      else
        vstat_container.innerHTML = "<red>Below average</red>";
    }
    else
    {
      x = width / 2;
      y = height / 2;
      k = 1;
      centered = null;

      bigText.style( 'visibility', 'visible' )
      info_card.setAttribute( 'style', 'visibility: hidden; opacity: 0;' );
    }

    // highlight the clicked country
    highlight_country();

    // zoom
    g.transition()
      .duration(750)
      .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')scale(' + k + ')translate(' + -x + ',' + -y + ')');
  }

  function mouseover(d)
  {
    // highlight hovered country
    d3.select(this).style('fill', '#F6F06C');
    var msg;
    if( data_avg[ d.properties.name ] == undefined )
      msg = d.properties.name + ": NO DATA!";
    else
      msg = d.properties.name + ": $" + data_avg[ d.properties.name ] + " USD";

    bigText.html( msg );
  }

  function mouseout(d)
  {
    highlight_country();
    // remove effect text
    effectLayer.selectAll('text').transition()
      .style('opacity', 0)
      .remove();

    // clear bigText name
    bigText.html('');
  }

  function highlight_country()
  {
    // reset country highlight
    mapLayer.selectAll('path').style('fill', fill_country);
    mapLayer.selectAll( 'path' )
      .style( 'stroke', function(d)
      {
        return centered && d===centered ? 'black' : '#aaa';
      });
  }

  return object;
};