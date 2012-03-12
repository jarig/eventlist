
var Common =
{
    
    csrf: "",
    _static: "",
    _media: "",
    _cache: {},
	DEBUG: function(msg)
	{
        var msg = JSON.stringify(msg);
		$(function() // wait till DOM is ready
		{
			$("#debug").append(msg+"<br/>");
		});
        console.log(msg);
	},
    submitForm: function(formId)
    {
        $(formId).submit();
        return false;
    },
    eval: function(data)
    {
        return eval("("+data+")");
    },
    cache: function (key, data)
    {
        Common._cache[key] = data;
    }
};


var CommonGUI =
{
    loadingWindow: '',
    showLoading: function()
    {
        CommonGUI.loadingWindow = $('<div></div>');
        $(CommonGUI.loadingWindow).dialog({
            title: "Loading...",
            height: "80",
            width: "150",
            resizable: false,
            modal: true
        });
    },
    hideLoading: function()
    {
        $(CommonGUI.loadingWindow).dialog("close");
        $(CommonGUI.loadingWindow).remove();
    }
};

//TODO move to google maps.js
var GoogleMaps = {
    map: null,
    markers: [],
    bounds: null,
    init: function(id)
    {
        $(function()
        {
            var latlng = new google.maps.LatLng(0, 0);
            GoogleMaps.bounds = new google.maps.LatLngBounds();
            var myOptions = {
              zoom: 10,
              center: latlng,
              mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            GoogleMaps.map = new google.maps.Map($(id).get(0), myOptions);
            return GoogleMaps.map;
        });
    },
    moveToAddress: function(address, putMarker)
    {
        geocoder = new google.maps.Geocoder();
        geocoder.geocode( { 'address': address}, function(results, status) {
              if (status == google.maps.GeocoderStatus.OK)
              {
                var zoom = results[0].address_components.length*3;
                GoogleMaps.map.setCenter(results[0].geometry.location);
                GoogleMaps.map.setZoom(zoom);
                if (typeof(putMarker) == "boolean" &&  putMarker)
                {
                    GoogleMaps.putMarker(results[0].geometry.location);
                    //GoogleMaps.zoomfit();
                }
                return results[0].geometry.location;
              } else {
                Common.DEBUG(status);
              }
       });
    },
    moveAndMark: function(address)
    {
        GoogleMaps.removeAllMarkers();
        var location = GoogleMaps.moveToAddress(address, true);
    },
    putMarker: function(location)
    {
        var marker = new google.maps.Marker({
            map: GoogleMaps.map,
            position: location
        });
        GoogleMaps.markers.push(marker);
        GoogleMaps.bounds.extend(location);
        return marker;
    },
    removeAllMarkers: function()
    {
      for(var i=0; i< GoogleMaps.markers.length; i++)
          GoogleMaps.removeMarker(GoogleMaps.markers[i]);
      GoogleMaps.markers.length = 0;
    },
    removeMarker: function(marker)
    {
        marker.setMap(null);
    },
    zoomfit: function()
    {
        GoogleMaps.map.fitBounds(GoogleMaps.bounds);
        //newcenter = GoogleMaps.bounds.getCenter();
        //GoogleMaps.map.setCenter(newcenter, 13);
    }
};




jQuery.cachedResource = function(url, options)
{
    if (url.match(/.+\.css$/gi))
    {
        var css = $("<link>");
        css.attr({
            rel:  "stylesheet",
            type: "text/css",
            href: url
        });
        $("head").append(css);
        return true;
    }else if(url.match(/.+\.less$/gi))
    {
        var less = $("<link>");
        less.attr({
            rel:  "stylesheet",
            type: "text/less",
            href: url
        });
        $("head").append(less);
        return true;
    }else
    {
        options = $.extend(options || {}, {
            dataType: "script",
            cache: true,
            url: url
        });
        return jQuery.ajax(options);
    }
};

jQuery.cachedHtml = function(url, options) {
    options = $.extend(options || {}, {
        dataType: "html",
        cache: true,
        url: url
    });
    return jQuery.ajax(options);
};

(function( jQuery ) {

    var componentCounter = 0;
    jQuery.loadComponent = function(url, resources, options, callback )
    {
        var // reference declaration & localization
            length = resources.length,
            deferreds = [],
            idx = 0;
        componentCounter++;
        var html = jQuery.cachedHtml(url, options);
        for ( ; idx < length; idx++ ) {
            deferreds.push(
                jQuery.cachedResource( Common._static + resources[ idx ], options )
            );
        }

        jQuery.when.apply( null, deferreds ).then(function()
        {
            html.done(function(data)
            {
                var $div = $("<div id='component-"+componentCounter+"'></div>");
                var $comp= $($div).append($(data));
                callback && callback($comp);
            });
        });
    };
})( jQuery );