

var CreateEvent =
{
    init: function()
    {
        $(function()
        {
            $("input").labelify({ labelledClass: "helpLabel" });
            $("textarea").labelify({ labelledClass: "helpLabel" });
            CreateEvent.initMultiSelect("#id_activities","Select Event Activities");
            //CreateEvent.initSelect("#id_blogs","Select Event Locations");
            $("#id_blogs").chosen();
            $("#id_organizers").chosen();
            
            CreateEvent.initSchedules();
        });
    },
    initSchedules: function()
    {
        var schedules = $('.eventSchedule');
        for(var i=0; i< schedules.length; i++)
        {
            var sch = schedules[i];
            CreateEvent.initSchedule(sch);
        }
    },
    initSchedule: function(schedule)
    {
        //clear date plugin
        var dClear = $( ".hasDatepicker", schedule);
        for (var i=0; i<dClear.length; i++)
            $(dClear[i]).removeClass("hasDatepicker");
        
        var dates = $( ".dateFrom, .dateTo",schedule ).datepicker({
                changeMonth: true,
                numberOfMonths: 1,
                altFormat: 'dd/mm/yy',
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
        var prefix = $("#schedulePrefix",schedule).val();
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
                //var adrTempl = $("#blogAddress", schedule).show();
                var adrTempl = $("#blogAddressTemplate", schedule).clone().attr("id","address-for-"+blogId);
                adrTempl = $("#blogAddress", schedule).html($(adrTempl).html());
                
                $(".loading", schedule).html("Loading...");
                $.ajax({
                    url: $("#getBlogAddressURL").val(),
                    data: {
                        "blogId": blogId
                    },
                    success: function(resp)
                    {
                      $(".loading", schedule).html("");
                      //add address div
                      var resp = eval("("+resp+")");
                      if (resp.length > 0)
                      {//id_form-1-address
                        $("#id_"+prefix+"-address",schedule).val(resp[0]["pk"]);
                        Address.fillAddress(adrTempl, resp[0]);
                        Common.DEBUG(resp[0]);
                      } else
                        $("#blogAddress", schedule).html("No addresses available");
                    }
                });
            }
        });
        var selectedOpts = $(blogFieldId + " :selected", schedule);
        for(i=0; i< selectedOpts.length; i++)
        {
            var blogId = $(selectedOpts[i]).val();
            if (blogId == "" || blogId <= 0)
                $("#eventAddress",schedule).rest_Address("init", $('#getCityURL').val());
                //$(blogFieldId, schedule).change();
        }
        return schedule;
    },
    addSchedule: function(toClone, insertTo)
    {
        var clone = $(toClone).clone();
        //reset data
        var formPrefix = $("#schedulePrefix",clone).val();
        $("#id_"+formPrefix+"-id",clone).remove();
        var inputs = $('input,select',clone);
        var prefixPattern=new RegExp('(.*)(\\d+)$','i');
        var prefixId = prefixPattern.exec(formPrefix)[1];
        var totalForms = $('#id_form-TOTAL_FORMS').val();
        $('#id_form-TOTAL_FORMS').val(parseInt(totalForms)+1);
        var currentFormId = parseInt(totalForms);// 1 based id
        var currentPrefix = prefixId+currentFormId+"";
        $("#schedulePrefix",clone).val(currentPrefix);
        $(clone).attr("id","schedule-"+currentPrefix);
        //id_form-2-id

        
        //clear plugins
        $(".chzn-container", clone).remove();
        var chosenDone = $(".chzn-done", clone);
        for(var i=0; i<chosenDone.length; i++)
        {
            $(chosenDone[i]).removeClass('chzn-done');
            $(chosenDone[i]).show();
        }
        $("input", clone).labelify({ labelledClass: "helpLabel" });//reinit labelify

        for(var i=0; i<inputs.length; i++)
        {
            var inputId = $(inputs[i]).attr("id");
            var name = $(inputs[i]).attr("name");
            if ( typeof inputId != "undefined" && inputId.indexOf(formPrefix) >= 0)
            {// if this input has formPrefix in id
                var newId = inputId.replace(formPrefix, currentPrefix);
                var newName = name.replace(formPrefix, currentPrefix);
                $(inputs[i]).attr("id",newId);
                $(inputs[i]).attr("name",newName);
            }
        }// forloop

        $(clone).hide();
        $(insertTo).prepend(clone);
        $(clone).slideDown('slow');
        var schedule = CreateEvent.initSchedule(clone);
        var blogFieldId = "#id_"+formPrefix+"-blog";
        $(blogFieldId, schedule).change();
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
    },
    submitForm: function(formId)
    {
        return Common.submitForm(formId);
    }
};