

var Address =
{
    addressDiv : '',
    cityURL: '',
    init: function(addressDiv, cityURL)
    {
        Address.cityURL = cityURL;
        Address.addressDiv = addressDiv;
        $(function()
        {
            Address.initMultiSelect($('#id_country',addressDiv),
                                    'Select Country',
                                    function(event, ui)
                                    {
                                        Address.initCities(ui.value);
                                    });
            Address.initMultiSelect($('#id_city',addressDiv),
                                    'Select City',
                                    function(event, ui)
                                    {
                                    });
            $(".ui-multiselect").css("width","100%");
        });
    },
    initCities: function(country)
    {
        $('#id_city option',Address.addressDiv).remove();
        $('#id_city',Address.addressDiv).append('<option id="loadingOption">Loading...</option>');
        $('#id_city',Address.addressDiv).multiselect('refresh');
        $(".ui-multiselect").css("width","100%");
        $.ajax({
                url: Address.cityURL,
                data:{
                  'country': country
                },
                success: function(cities)
                {
                    $('#id_city #loadingOption').remove();
                    var cities = eval('('+cities+')');
                    for(var i=0; i< cities.length; i++)
                    {
                        var city = cities[i];
                        $('#id_city',Address.addressDiv).append('<option value='+city['pk']+'>'+city['fields']['name']+'</option>');
                    }
                    $('#id_city',Address.addressDiv).multiselect('refresh');
                    $(".ui-multiselect").css("width","100%");
                }
            });
    },
    initMultiSelect: function(id, text, clickCallBack)
    {
        $(id).multiselect(
                   {
                       header: "",
                       noneSelectedText: text,
                       selectedList: 1,
                       "multiple": false,
                       click: clickCallBack,
                       beforeopen: function()
                       {
                           $(".ui-multiselect-menu").css("width",$(".ui-multiselect").width());
                       }
               }).multiselectfilter();
    }
};
