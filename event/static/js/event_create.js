

var CreateEvent =
{
    init: function()
    {
        $(function()
        {
            $("input").labelify({ labelledClass: "helpLabel" });
            $("textarea").labelify({ labelledClass: "helpLabel" });
            CreateEvent.initMultiSelect("#id_activities","Select Event Activities");
            CreateEvent.initSelect("#id_blogs","Select Event Locations");
            $("#id_organizers").chosen();
            //$(".ui-multiselect").css("width","100%");

            var dates = $( "#id_dateFrom, #id_dateTo" ).datepicker({
                changeMonth: true,
                numberOfMonths: 1,
                altFormat: 'dd/mm/yy',
                beforeShowDay: function(date)
                {
                    var fromDate = $('#id_dateFrom').datepicker( "getDate" );
                    if (fromDate.getTime() == date.getTime())
                        return [true, "ui-state-highlight","Event Starts"];
                    return [true, ""];
                },
                onSelect: function( selectedDate ) {
                    var option = this.id == "id_dateFrom" ? "minDate" : "maxDate",
                        instance = $( this ).data( "datepicker" ),
                        date = $.datepicker.parseDate(
                            instance.settings.dateFormat ||
                            $.datepicker._defaults.dateFormat,
                            selectedDate, instance.settings );
                    dates.not( this ).datepicker( "option", option, date );
                }
            });
            var curDate = new Date();
            if ($("#id_dateFrom").val() == "")
                $("#id_dateFrom").datepicker( "setDate" , curDate );
            
            /*$("#id_timeFrom, #id_timeTo").timepicker({
                timeFormat: 'hh:mm'
            });*/
            //$("#timeFrom").val( curDate.getHours() + ":" + curDate.getMinutes() );

            $("#eventAddresses").change(function(){
                //init address close buttons
                $( ".deleteAddressButton", "#eventAddresses").button({
                    icons: {
                        primary: "ui-icon-close"
                    },
                    text: false
                });

                $(".deleteAddressButton", "#eventAddresses").click(function()
                {
                    $(this).parents(".address").remove();
                    //check if last
                    var adr = $(".address","#eventAddresses");
                    if (adr.length == 0)
                        $("#id_blogs").multiselect("uncheckAll");
                });
            });
            $("#eventAddresses").trigger("change");

            $("#id_blogs").change(function(eventObj)
            {
                $("#eventAddresses").html("Loading...");
                var selectedOpts = $("#id_blogs :selected");
                for(var i=0; i< selectedOpts.length; i++)
                {
                    var opt = selectedOpts[i];
                    var belongsTo = $(opt).val();
                    $.ajax({
                        url: $("#getAddressURL").val(),
                        data: {
                            "blogId": $(opt).val()
                        },
                        success: function(resp)
                        {
                          CreateEvent.addAddresses(eval("("+resp+")"), belongsTo);
                          Common.DEBUG(resp);
                        }
                    });
                }
            });
        });
    },
    addAddresses:function(adrObjects, belongsTo)
    {
        $("#eventAddresses").html("");
        for (var i=0; i<adrObjects.length; i++)
        {
            var adrObject = adrObjects[i];
            var address = $("#addressTemplate").clone();
            $(address).attr("id", adrObject["pk"]);
            $("input[name=adr_id]",address).val(adrObject["pk"]);
            $("input[name=belongsTo]",address).val(belongsTo);

            //fill data
            var fields = adrObject["fields"];
            for(var field in fields)
            {
                $(".adr_"+field,address).html(fields[field]);
            }
            //populate
            $("#eventAddresses").append(address);
            $(address).show();
            $("#eventAddresses").trigger("change");
        }
    },
    initSelect: function(id, text)
    {
        //$(id).chosen();
        $(id).multiselect(
               {
                   header: "",
                   noneSelectedText: text,
                   selectedList: 1,
                   "multiple": false,
                   multiselectclick: function(event, ui)
                   {

                   },
                   beforeopen: function()
                   {
                       $(".ui-multiselect-menu").css("width",$(".ui-multiselect").width());
                   }
           }).multiselectfilter();
    },
    initMultiSelect: function(id, text)
    {
        $(id).chosen();
        /*$(id).multiselect(
               {
                   header: "",
                   noneSelectedText: text,
                   selectedList: 4,
                   multiselectclick: function(event, ui)
                   {

                   },
                   beforeopen: function()
                   {
                       $(".ui-multiselect-menu").css("width",$(".ui-multiselect").width());
                   }
           }).multiselectfilter();*/
    },
    submitForm: function(formId)
    {
        return Common.submitForm(formId);
    }
};