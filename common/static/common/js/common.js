
var Common =
{
    
    csrf: "",
	DEBUG: function(msg)
	{
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
    }
};


var CommonGUI =
{
    loadingWindow: '',
    showLoading: function()
    {
        CommonGUI.loadingWindow = $('<div>Loading...</div>');
        $(CommonGUI.loadingWindow).dialog({
            title: "Loading...",
            height: "80",
            width: "150",
            modal: true
        });
    },
    hideLoading: function()
    {
        $(CommonGUI.loadingWindow).dialog("close");
        $(CommonGUI.loadingWindow).remove();
    },
    openUploadWindow: function(dialogId, logoSrcId, inputId)
    {
      $(dialogId + " iframe").attr("src",$(dialogId + " iframe").attr("src"));
      var dailogWindow = $(dialogId);
      $(dialogId).dialog(
          {
              title: "Upload Logo",
              height: "180",
              width: "350",
              modal: true,
              buttons: {
                  submit: function()
                  {
                     $("iframe",dialogId).load(function()
                     {
                        $(this).unbind('load');
                        var imgPath = $(dialogId + " iframe").contents().find("#imagePath").val();
                        var imgUrl = $(dialogId + " iframe").contents().find("#imageUrl").val();
                        if (imgPath != "False")
                        {
                            CommonGUI.showLoading();
                            $(logoSrcId).load(function()
                            {
                               //hide loading
                               CommonGUI.hideLoading();
                               $(this).unbind('load');
                            });
                            $(logoSrcId).attr("src",imgUrl);
                            if (typeof(inputId) != "undefined")
                                $("input[id="+inputId+"]").val(imgPath);
                            $(dailogWindow).dialog("destroy");
                        }
                     });
                     $(dialogId + ' iframe').contents().find("form").submit();
                  },
                  close: function()
                  {
                    $(this).dialog("close");
                  }
              }
          }
        );
        return false;
    },
    uploadButton: function(ident, labelText, inputForm)
    {
        $(function()
        {
            $(ident).css("position", "relative");
            $(ident).css("height", "20px");
            $(ident).css("width", "100%");
            $(ident).css("margin-top", "2px");
            $(ident).css("margin-bottom", "2px");
            
            var label = $("<div>"+labelText+"</div>");
            $(label).css("position", "absolute");
            $(label).css("padding-top", "4px");
            $(label).css("width", "100%");
            $(label).css("height", "100%");


            var input = $(inputForm);
            $(input).css("position","relative");
            $(input).css("opacity","0");
            $(input).css("-moz-opacity","0");
            $(input).css("filter","alpha(opacity: 0)");
            $(input).css("width","100%");
            $(input).css("height","100%");
            $(ident).append(label);
            $(ident).append(input);
            
            $(ident).hover(
            function()
            {
                $(this).css("background-color","#e6e6fa");
                $(this).css("text-decoration","underline");
            },
            function()
            {
                $(this).css("background-color","white");
                $(this).css("text-decoration","none");
            });
        });//dom loaded
    }
};

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