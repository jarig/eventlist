

var CreateEvent =
{
    init: function()
    {
        $(function()
        {

            $("textarea").labelify({ labelledClass: "helpLabel" });
            CreateEvent.initMultiSelect("#id_organizers");
            CreateEvent.initMultiSelect("#id_activities","Select Event Activities");
        });
    },
    initSchedule: function(schedule)
    {
        $("input", schedule).labelify({ labelledClass: "helpLabel" });//reinit labelify
        var dates = $( ".dateFrom, .dateTo",schedule ).datepicker({
                changeMonth: true,
                numberOfMonths: 1,
                dateFormat: 'dd/mm/yy',
                beforeShowDay: function(date)
                {
                    var fromDate = $('.dateFrom',schedule).datepicker( "getDate" );
                    if (fromDate.getTime() == date.getTime())
                        return [true, "ui-state-highlight","Event Starts"];
                    return [true, ""];
                },
                onSelect: function( selectedDate ) {
                    var option = $(this).hasClass("dateFrom") ? "minDate" : "maxDate",
                        instance = $( this ).data( "datepicker" ),
                        date = $.datepicker.parseDate(
                            instance.settings.dateFormat ||
                            $.datepicker._defaults.dateFormat,
                            selectedDate, instance.settings );
                    dates.not( this ).datepicker( "option", option, date );
                }
        });

        var curDate = new Date();
        if ($(".dateFrom",schedule).val() == "")
            $(".dateFrom",schedule).datepicker( "setDate" , curDate );


        //id_form-0-blog
        var prefix = $("#schedulePrefix",schedule).attr("name");
        var blogFieldId = "#id_"+prefix+"-blog";
        $(blogFieldId, schedule).chosen();
        $(blogFieldId, schedule).change(function(eventObj)
        {
            var selectedOpts = $(blogFieldId + " :selected", schedule);
            for(var i=0; i< selectedOpts.length; i++)
            {
                var opt = selectedOpts[i];
                var blogId = $(opt).val();
                if (blogId == "undefined" || blogId == 0)
                {
                    var customAddress = $("#customAddress",schedule);
                    //init city choice
                    $("#id_"+prefix+"-address",schedule).val(0);
                    $("#blogAddress", schedule).hide();
                    $(customAddress).show(); //custom address;
                    $("#eventAddress",schedule).rest_Address("init", $('#getCityURL').val());
                    $("input", schedule).labelify({ labelledClass: "helpLabel" });
                    $("textarea", schedule).labelify({ labelledClass: "helpLabel" });
                    return schedule;
                }
                $("#customAddress",schedule).hide();
                $("#blogAddress", schedule).html("Loading...");
                
                $(".loading", schedule).html("Loading...");
                $.ajax({
                    url: $("#getBlogAddressURL").val(),
                    data: {
                        "blogId": blogId
                    },
                    success: function(resp)
                    {
                      $(".loading", schedule).html("");
                      $("#blogAddress",schedule).show();
                      var adrTempl = $("#blogAddressTemplate").clone();
                      //add address div
                      resp = eval("("+resp+")");
                      if (resp.length > 0)
                      {//id_form-1-address
                        $("#id_"+prefix+"-address",schedule).val(resp[0]["pk"]);
                        Address.fillAddress(adrTempl, resp[0]);
                        $("#blogAddress",schedule).html(adrTempl.html());
                        Common.DEBUG(resp[0]);
                      } else
                        $("#blogAddress", schedule).html("No addresses available");
                    }
                });
            }
        });
        var selectedOpts = $(blogFieldId + " :selected", schedule);
        for(var i=0; i< selectedOpts.length; i++)
        {
            var blogId = $(selectedOpts[i]).val();
            if (blogId == "" || blogId <= 0)
                $("#eventAddress",schedule).rest_Address("init", $('#getCityURL').val());
                //$(blogFieldId, schedule).change();
        }

        return schedule;
    },
    addSchedule: function(formPrefix, insertTo)
    {
        $(formPrefix).ajaxSimpleForm("add",insertTo, {"append":false});
        return false;
    },
    addAddresses:function(adrObjects, belongsTo)
    {
        $(".eventAddresses").html("");
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
    initMultiSelect: function(id, text)
    {
        $(id).chosen();
    },
    submitForm: function(formId)
    {
        return Common.submitForm(formId);
    }
};