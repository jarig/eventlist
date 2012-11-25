
//extend jquery
(function($)
{
    var methods ={
        init: function(cityURL, onChange)
        {
            var $this = $(this);
            $('.adr_country select',$this).chosen();
            $('.adr_country select',$this).change(function(event, ui){
                var targetVal = $(event.target).val();
                methods.initCities($this, cityURL, targetVal);
                if (typeof(onChange) === "function")
                    onChange();
            });
            $('.adr_city select',$this).chosen();
            $('.adr_city select',$this).change(function(event,ui){
               if (typeof(onChange) === "function")
                    onChange();
            });
            $('.adr_cityArea input',$this).blur(function()
            {
                if (typeof(onChange) === "function")
                    onChange();
            });
            $('.adr_street input',$this).blur(function()
            {
                if (typeof(onChange) === "function")
                    onChange();
            });
            $('.adr_country select',$this).change();
            //$("input",$this).labelify();
        },
        initCities: function ($this, url,countryId)
        {
            var prevSelected = $('.adr_city option:selected',$this);
            $('.adr_city option',$this).remove();
            $('.adr_city select',$this).append('<option id="loadingOption" value="0">Loading...</option>');
            $(".adr_city select",$this).trigger("liszt:updated");
            $.ajax({
                    url: url,
                    data:{
                      'country': countryId
                    },
                    success: function(cities)
                    {
                        $('.adr_city #loadingOption').remove();
                        var cities = eval('('+cities+')');
                        for(var i=0; i< cities.length; i++)
                        {
                            var city = cities[i];
                            var option = $('<option value='+city['pk']+'>'+city['fields']['name']+'</option>');
                            for (var s=0; s< prevSelected.length; s++)
                                if ( $(prevSelected[s]).val() == city['pk'])
                                {
                                    $(option).attr("selected","selected");
                                    break;
                                }
                            $('.adr_city select',$this).append(option);
                            $('.adr_city select',$this).change();
                        }
                        $(".adr_city select", $this).trigger("liszt:updated");
                    }
            });
        }
    };
    $.fn.rest_Address = function(method)
    {
        if ( method && typeof method === "string" )
        {
            methods[method].apply(this, Array.prototype.slice.call( arguments, 1 ));
        } else
        {
            $.error("No such method");
        }
        return this;
    }
})(jQuery);

var Address =
{
    initMultiSelect: function(id, text, clickCallBack)
    {
        $(id).chosen().change( clickCallBack );
    },
    refreshGoogleMap: function(formId, callback)
    {
        $(function()
        {
            var country = $(formId+' .adr_country select option:selected');
            var city = $(formId+' .adr_city select option:selected');
            var area = $(formId+' .adr_cityArea input');
            var street = $(formId+' .adr_street input');
            var searchText = "";
            if ($(country).val() != 0) searchText += $(country).html();
            if ($(city).val() != 0) searchText += ","+$(city).html();
            if ($(area).val() != $(area).attr("title")) searchText += ","+$(area).val();
            if ($(street).val() != $(street).attr("title")) searchText += ","+$(street).val();
            callback(searchText);
        });
    },
    fillAddress: function(addressDiv, request)
    {
        $("#adr_id",addressDiv).val(request["pk"]);
        var fields = request["fields"];
        $(".adr_country",addressDiv).html(fields["country"]);
        $(".adr_city",addressDiv).html(fields["city"]);
        $(".adr_cityArea",addressDiv).html(fields["cityArea"]);
        $(".adr_street",addressDiv).html(fields["street"]);
        $(".adr_postalCode",addressDiv).html(fields["postalCode"]);
    }
};
