

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
            $(".ui-multiselect").css("width","100%");

            CreateEvent.initSchedules();
            
            $(".address").change(function(){
                //init address close buttons
                $( ".deleteAddressButton .address").button({
                    icons: {
                        primary: "ui-icon-close"
                    },
                    text: false
                });

                $(".deleteAddressButton .address").click(function()
                {
                    $(this).parents(".address").remove();
                });
            });
            $(".address").trigger("change");

            $("#id_blogs").change(function(eventObj)
            {
                $(".eventAddresses").html("Loading...");
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
    },
    addSchedule: function(toClone, insertTo)
    {
        var clone = $(toClone).clone();
        //reset data
        var formPrefix = $("#schedulePrefix",clone).val();
        var inputs = $('input,select',clone);
        var prefixPattern=new RegExp('(.*)(\\d+)$','i');
        var prefix = prefixPattern.exec(formPrefix)[1];
        var totalForms = $('#id_form-TOTAL_FORMS').val();
        $('#id_form-TOTAL_FORMS').val(parseInt(totalForms)+1);
        var currentFormId = parseInt(totalForms);// 1 based id
        var currentPrefix = prefix+currentFormId+"";
        $(clone).attr("id","schedule-"+currentPrefix);

        for(var i=0; i<inputs.length; i++)
        {
            var inputId = $(inputs[i]).attr("id");
            var name = $(inputs[i]).attr("name");
            if ( inputId.indexOf(formPrefix) >= 0)
            {// if this input has formPrefix in id
                var newId = inputId.replace(formPrefix, currentPrefix);
                var newName = name.replace(formPrefix, currentPrefix);
                $(inputs[i]).attr("id",newId);
                $(inputs[i]).attr("name",newName);
            }
        }// forloop
        
        $(insertTo).prepend(clone);
        $(clone).show();
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