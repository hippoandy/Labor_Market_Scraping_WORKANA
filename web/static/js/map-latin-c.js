function latin()
{
    // default settings
    var $el = d3.select("body");
    var data = {};
    var data_avg = {};

    var width = 800,
        height = 600,
        centered;

    // define color scale
    var color = d3.scale.category20c();

    var projection = d3.geo.mercator()
        .scale(300)
        .center([-74, -15])
        .translate([width / 2, height / 2]);

    var path = d3.geo.path().projection( projection );

    var svg, g;
    var object = {};

    var effectLayer, mapLayer, bigText;

    // method for render/refresh graph
    object.render = function()
    {
        // Set svg width & height
        svg = $el.append('svg')
            .attr('width', width)
            .attr('height', height);

        // Add background
        svg.append('rect')
            .attr('class', 'background')
            .attr('width', width)
            .attr('height', height)
            .on('click', clicked);

        g = svg.append('g');

        effectLayer = g.append('g')
            .classed('effect-layer', true);

        mapLayer = g.append('g')
            .classed('map-layer', true);

        bigText = g.append('text')
            .classed('big-text', true)
            .attr('x', 10)
            .attr('y', 25);

        // Load map data
        d3.json( data, function(error, mapData)
        {   var features = mapData.features;

            // Update color scale domain based on data
            color.domain([0, d3.max(features, country_avg)]);

            // Draw each country as a path
            mapLayer.selectAll('path')
                .data(features)
                .enter().append('path')
                .attr('d', path)
                .attr('vector-effect', 'non-scaling-stroke')
                .style('fill', fill_country)
                .on('mouseover', mouseover)
                .on('mouseout', mouseout);
                // .on('click', clicked);
        });

        return object;
    };

    // Getter and setter methods
    object.data = function(value)
    {
        if (!arguments.length) return data;
        data = value;
        return object;
    };

    object.data_avg = function(value)
    {
        if (!arguments.length) return data;
        data_avg = value;
        return object;
    };

    object.$el = function(value)
    {
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
    {   var n = country_name(d);
        return n ? data_avg[ n ] : 0;
    }

    // Get country color
    function fill_country(d)
    {   var v = country_avg(d);
        if( v == 0 || v == undefined ) return '#fff';
        else return color(v);
    }

    // When clicked, zoom in
    function clicked(d)
    {   var x, y, k;

        // Compute centroid of the selected path
        if (d && centered !== d) {
            var centroid = path.centroid(d);
            x = centroid[0];
            y = centroid[1];
            k = 4;
            centered = d;
        } else {
            x = width / 2;
            y = height / 2;
            k = 1;
            centered = null;
        }

        // highlight the clicked country
        mapLayer.selectAll('path')
            .style('fill', function(d){return centered && d===centered ? '#D5708B' : fill_country(d);});

        // zoom
        g.transition()
            .duration(750)
            .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')scale(' + k + ')translate(' + -x + ',' + -y + ')');
    }

    function mouseover(d)
    {
        // highlight hovered country
        d3.select(this).style('fill', 'orange');
        var msg;
        if( data_avg[ d.properties.name ] == undefined )
            msg = d.properties.name + ": NO DATA";
        else
            msg = d.properties.name + ": $" + data_avg[ d.properties.name ] + " USD"

        bigText.html( msg );
    }

    function mouseout(d)
    {
        // reset country color
        mapLayer.selectAll('path')
            .style('fill', function(d){return centered && d===centered ? '#D5708B' : fill_country(d);});

        // remove effect text
        effectLayer.selectAll('text').transition()
            .style('opacity', 0)
            .remove();

        // clear country name
        bigText.html('');
    }

    return object;
};