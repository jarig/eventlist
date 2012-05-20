
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
        return msg;
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
        CommonGUI.loadingWindow = $('<div class="modal"><div class="modal-body progress progress-striped active"><div class="bar" style="width: 100%;"></div></div></div>');
        $(CommonGUI.loadingWindow).css("top","80%");
        $(".modal-body",CommonGUI.loadingWindow).css("margin-bottom","0");
        $(CommonGUI.loadingWindow).modal({keyboard: false});
    },
    hideLoading: function()
    {
        $(CommonGUI.loadingWindow).modal('hide');
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
        //var location = GoogleMaps.moveToAddress(address, true);
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
            cache: false,//TODO enable
            url: url
        });
        return jQuery.ajax(options);
    }
};

jQuery.cachedHtml = function(url, options) {
    options = $.extend(options || {}, {
        dataType: "html",
        cache: false,//TODO enable
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

(function( $ ){

    var formTemplate;
    var managementForm = {
        totalForms: 0,
        initialForms: 0,
        maxNum: 0
    };
    var baseIdent;
    var formIdent='';
    var formPrefix;
    var methods = {
        init : function( fI )
        {
            baseIdent = $(this);
            formIdent = fI;
            formPrefix = $("#formPrefix" ,this).val();
            managementForm["totalForms"] = $("input[name='"+formPrefix+"-TOTAL_FORMS']" ,this);
            managementForm["initialForms"] = $("input[name='"+formPrefix+"-INITIAL_FORMS']",this);
            managementForm["maxNum"]= $("input[name='"+formPrefix+"-MAX_NUM_FORMS']",this);
            formTemplate = $($($(formIdent).get(0)).clone());
            //reset data
            $("[name^="+formPrefix+"]", formTemplate).each(function()
            {//TODO retrieve initial data
                $(this).val("");
            });
            methods.initForm(formIdent);
        },
        initForm: function(forms)
        {//init any forms ( bound and new ones )
            $(forms).each(function()
            {
                var form = $(this);
                if ($("[name$=-DELETE]", this).is("[value=on]"))
                {
                    form.hide();
                }else
                {
                    $("[action-bind='closeButton']",this).click(function()
                    {
                        return methods.remove(form);
                    });
                    options.onInitForm(form);
                }
            });
        },
        remove: function(form)
        {
            var $form = $(form);
            $form.fadeOut('fast',function()
            {
                $form.hide();
                $('[name$=-DELETE]', $form).val("on");
                //managementForm["totalForms"].val(parseInt(managementForm["totalForms"].val())-1);
                //methods.updateIndices();
            });
            return false;
        },
        add: function( compareData )
        {
            if ( typeof managementForm["maxNum"].val() != "undefined" &&
                 parseInt(managementForm["totalForms"].val()) >=
                 parseInt(managementForm["maxNum"].val()) ) return false;
            var form = $(formTemplate).clone();
            form.hide();
            var last = null;
            $(formIdent, baseIdent).each(function()
            {
                var isGreater = options.compareForms(compareData, $(this));
                Common.DEBUG(isGreater);
                if (isGreater >= 0)
                {
                    $(this).before(form);
                    return false;
                }
                else
                {//less
                    last = $(this);
                }
            });
            if ( last != null ) last.after(form);

            form.fadeIn();
            methods.updateIndex(form, parseInt(managementForm["totalForms"].val()));
            methods.updateOrderIndices();
            methods.initForm(form);
            managementForm["totalForms"].val(parseInt(managementForm["totalForms"].val())+1);
            options.onAdd(form);
            return form;
        },
        updateIndex: function(form, nIndex)
        {
            var formPrefixRegex = new RegExp('(.*)('+formPrefix+'-)(\\d+)(.*)','i');
            $("[name^="+formPrefix+"]", form).each(function()
            {
                var newId =  formPrefixRegex.exec($(this).attr("id"));
                var newName = formPrefixRegex.exec($(this).attr("name"));
                var newActionData = formPrefixRegex.exec($(this).attr("action-data"));
                if ( newId != null )
                    $(this).attr("id", newId[1]+newId[2]+nIndex + newId[4]);
                if ( newName != null )
                    $(this).attr("name", newName[1]+newName[2]+nIndex + newName[4]);
                if ( newActionData != null )
                    $(this).attr("action-data", newActionData[1]+newActionData[2]+nIndex + newActionData[4]);
            });
        },
        updateOrderIndices: function()
        {
            var counter=0;
            //
            $(formIdent, baseIdent).each(function()
            {
                counter++;
                $("[name$=-ORDER]", this).val(counter);
            });
        }
    };

    var options = {
        onAdd: function(form){},
        onInitForm: function(form) {},
        compareForms: function(form1, form2) { return form1;}
    };

    $.fn.ajaxForm = function( method ) {
        // Method calling logic
        if ( methods[method] )
        {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object')
        {
            $.extend(options, method);
        } else if ( ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery' );
        }

    };
})( jQuery );