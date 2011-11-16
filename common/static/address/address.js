

var Address =
{
    addressDiv : '',
    cityURL: '',
    init: function(addressDiv, cityURL, onChange)
    {
        Address.cityURL = cityURL;
        Address.addressDiv = addressDiv;
        $(function()
        {
            $(addressDiv + " input").labelify();
            Address.initMultiSelect($(addressDiv + ' .adr_country select'),
                                    'Select Country',
                                    function(event, ui)
                                    {
                                        var targetVal = $(event.target).val();
                                        Address.initCities(targetVal);
                                        if (typeof(onChange) == "function")
                                            onChange();
                                    });
            Address.initMultiSelect($(addressDiv + ' .adr_city select'),
                                    'Select City',
                                    function(event, ui)
                                    {
                                        if (typeof(onChange) == "function")
                                            onChange();
                                    });
            $(addressDiv + ' .adr_cityArea input').blur(function()
            {
                if (typeof(onChange) == "function")
                    onChange();
            });
            $(addressDiv + ' .adr_street input').blur(function()
            {
                if (typeof(onChange) == "function")
                    onChange();
            });
            //$(".ui-multiselect").css("width","100%");
        });
    },
    initCities: function(country)
    {
        $('.adr_city option',Address.addressDiv).remove();
        $('.adr_city select',Address.addressDiv).append('<option id="loadingOption" value="0">Loading...</option>');
        $(".adr_city select").trigger("liszt:updated");
        $.ajax({
                url: Address.cityURL,
                data:{
                  'country': country
                },
                success: function(cities)
                {
                    $('.adr_city #loadingOption').remove();
                    var cities = eval('('+cities+')');
                    for(var i=0; i< cities.length; i++)
                    {
                        var city = cities[i];
                        $('.adr_city select',Address.addressDiv).append('<option value='+city['pk']+'>'+city['fields']['name']+'</option>');
                        $('.adr_city select').change();
                    }
                    $(".adr_city select", Address.addressDiv).trigger("liszt:updated");
                }
            });
    },
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
    }
};
