
var Search =
{
    options: {
      id: "fastSearch"
    },
    init: function( options )
    {
        if ( typeof options != "undefined")
            Search.options = $.extend(Search.options, options);
        $(".criteria a","#"+Search.options["id"]+" .chosenSearchCriteria").click(function()
        {
            var criteriaName = $(this).attr("action-data");
            console.log("Remove criteria:" + criteriaName);
        });
    },
    addCriteria: function(name, value)
    {
        var tag = $("[name='"+name+"']", "#"+Search.options["id"]);
        if ( tag[0].tagName.toLowerCase() == "select")
        {
            console.log($("option[value='"+value+"'",$(tag)));
            $("option[value='"+value+"']",$(tag)).attr("selected", "selected");
        }
    },
    run: function()
    {
        $("#"+Search.options["id"]).submit();//submit form
    }
};