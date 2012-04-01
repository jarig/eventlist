var Party =
{
    findAddressUrl: '',
    init: function()
    {
        $(function()
        {
            Party.findAddressUrl = $("#findAddressUrl").val();
            //TODO move to credit init
            $("input").labelify({ labelledClass: "helpLabel" });
            $("textarea").labelify({ labelledClass: "helpLabel" });
            $("#scheduleForms").ajaxForm( {
                   "onInitForm": function(nForm)
                   {
                       Party.initSchedule(nForm);
                   }
            });
            $("#scheduleForms").ajaxForm("init", ".partySchedule");

            $("#searchEventButton").click(function()
            {
                var searchEventURL = $("#searchEventURL").val();
                CommonGUI.showLoading();
                $.loadComponent(searchEventURL,
                                ['js/event_search.js',
                                 'css/event_search_box.css'],{},
                function(data)
                {
                    CommonGUI.hideLoading();
                    $("body").click();
                    $("body").append(data);
                    var popup = $(".modal",data).modal();
                    popup.on('hidden', function ()
                    {
                        $(data).remove();
                    });
                    //init popup
                    EventSearch.initPopup(popup, searchEventURL);
                    $(".addEventButton",popup).click(function()
                    {
                        var event = $(this).parents(".eventEntryRow");
                        var eventId = $("#eventId",event).val();
                        var dateFrom = $("#dateFrom", event).val();
                        var timeFrom = $("#timeFrom", event).val();
                        var dateTo = $("#dateTo", event).val();
                        var timeTo = $("#timeTo", event).val();
                        var descr = $("#eventDescr", event).val();
                        var adrId = $("#eventLocation", event).val();
                        var adrText = $("#eventLocationText", event).val();
                        var nForm = $("#scheduleForms").ajaxForm("add", "#scheduleForms");
                        $("[type=text][name$=-location]", nForm).val(adrText);
                        $("[type=hidden][name$=-location]", nForm).val(adrId);
                        $("[name$=-dateFrom]", nForm).datepicker( "setDate" , new Date(dateFrom) ).datepicker( "destroy" );
                        $("[name$=-timeFrom]", nForm).val(timeFrom);
                        $("[name$=-dateTo]", nForm).datepicker( "setDate" , new Date(dateTo) ).datepicker( "destroy" );
                        $("[name$=-timeTo]", nForm).val(timeTo);
                        $("[name$=-descr]", nForm).val(descr);
                        $("[name$=-eventSchedule]", nForm).val(eventId);
                        $("input", nForm).attr("readonly","readonly");
                        $(popup).modal("hide");
                        return false;
                    });
                });
                return false;
            });
            $("#addCustomScheduleButton").click(function()
            {
                $("body").click();
                $("#scheduleForms").ajaxForm("add", "#scheduleForms");
                return false;
            });
        });
    },
    initSchedule: function(form)
    {
        //$('select[name$="-location"]',form).chosen();
        //$('select[name$="-eventSchedule"]', form).chosen();
        $( "input[name$='-dateFrom']" ).datepicker( "destroy").datepicker( {"dateFormat": 'dd/mm/yy' });
        $( "input[name$='-dateTo']").datepicker( "destroy").datepicker( {"dateFormat": 'dd/mm/yy' });

        var cache = {}, lastXhr;
        $('#locationSearchField', form).autocomplete({
        source: function( request, response ) {
                var term = request.term;
                if ( term in cache ) {
                    response( cache[ term ] );
                    return;
                }
                lastXhr = $.getJSON( Party.findAddressUrl, request, function( data, status, xhr ) {
                    cache[ term ] = data;
                    if ( xhr === lastXhr ) {
                        response( data );
                    }
                })
        },
        minLength: 2,
        focus: function( event, ui ) {
            $(this, form).val(ui.item.fields.street);
            return false;
        },
        select: function( event, ui )
        {
            $(this, form).val(ui.item.fields.street);
            $('[type=hidden][name='+$(this).attr("name")+']', form).val(ui.item.pk);
            return false;
        }
        }).data( "autocomplete" )._renderItem = function( ul, item ) {
            //Common.DEBUG(item);
            return $( "<li></li>" )
                .data( "item.autocomplete", item )
                .append( "<a>" + item.fields.name + "/" +
                                item.fields.street + "/" + item.fields.cityArea + "</a>" )
                .appendTo( ul );
        };;
    }
};