var Party =
{
    findAddressUrl: '',
    invitationURL: '',
    init: function()
    {
        $(function()
        {
            $("#participantList").change(function()
            {
                $("[rel=tooltip]").tooltip();
            });
            $("#participantList").change();
            Party.findAddressUrl = $("#findAddressUrl").val();
            //TODO move to credit init
            $("input").labelify({ labelledClass: "helpLabel" });
            $("textarea").labelify({ labelledClass: "helpLabel" });
            $("#scheduleForms").ajaxForm( {
                   "onInitForm": function(nForm)
                   {
                       Party.initSchedule(nForm);
                   },
                   "compareForms": Party.compareForms
            });

            $("#inviteParticipantButton").click(function()
            {
                CommonGUI.showLoading();
                var invitationURL = $(this).attr('href').replace('#','');
                var toExclude = [];
                $('#participantList [name=invited]').each(function()
                {
                    toExclude.push($(this).val());
                });
                $.loadComponent(invitationURL,[
                                                'js/account_search.js',
                                                'css/party_invite_box.css'
                ],{},function(data)
                {
                    CommonGUI.hideLoading();
                    $("body").append(data);
                    var popup = $(".modal",data).modal();
                    popup.on('hidden', function ()
                    {
                        $(data).remove();
                    });
                    AccountSearch.initFriendSelect(popup,{
                        onSubmit: function(popup, button, friendList, addInfo)
                        {
                            Common.DEBUG(addInfo);
                            for(var i=0; i< friendList.length; i++)
                            {
                                var friendId = friendList[i];
                                var invited = $("#participantList #participantTemplate").clone();
                                $("[name=invited]", invited).val(friendId);
                                $(invited).attr("id", "friend-"+friendId);
                                $(invited).attr("title", addInfo[friendId]['name']);
                                //$(invited).css("background-image", "url('"+addInfo[friendId]['avatar']+"')");
                                $("#participantList").prepend(invited);
                                $(invited).fadeIn();
                            }
                            $("#participantList").change();
                            button.text(button.attr("data-complete-text"));
                            button.addClass("btn-success");
                            $(popup).modal('hide');
                        },
                        toExclude: toExclude
                    });

                });
                return false;
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
                        var nForm = $("#scheduleForms").ajaxForm("add", {'dateFrom': new Date(dateFrom), 'timeFrom': timeFrom} );
                        $("[type=text][name$=-location_text]", nForm).val(adrText);
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
                $("#scheduleForms").ajaxForm("add");
                //$("#customSchedulePopup").modal('show');
                return false;
            });
        });
    },
    initSchedule: function(form)
    {
        var sch = $('[name$="-eventSchedule"]',form).val();
        if ( typeof sch == "string" && sch != "" )
        {
            $('input',form).attr("readonly","readonly");
            $("input", form).datepicker( "destroy");
            return;
        }
        $( "input[name$='-dateFrom']",form).datepicker( "destroy" ).datepicker( {"dateFormat": 'dd/mm/yy' });
        $( "input[name$='-dateTo']", form).datepicker( "destroy" ).datepicker( {"dateFormat": 'dd/mm/yy' });

        var cache = {}, lastXhr;
        $("[name$='-location_text']", form).autocomplete({
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
            $("[name$='-location']", form).val(ui.item.pk);
            return false;
        }
        }).data( "autocomplete" )._renderItem = function( ul, item ) {
            //Common.DEBUG(item);
            return $( "<li></li>" )
                .data( "item.autocomplete", item )
                .append( "<a>" + item.fields.name + "/" +
                                item.fields.street + "/" + item.fields.cityArea + "</a>" )
                .appendTo( ul );
        };
    },
    compareForms: function(formData, form2)
    {
        var date1, time1, date2, time2;
        if (typeof formData == "undefined" || formData == null) return 1;
        try
        { date1 = formData['dateFrom'];
        } catch (e){date1= null;}
        time1 = formData['timeFrom'];
        try
        { date2 = $.datepicker.parseDate( 'dd/mm/yy' , $("input[name$='-dateFrom']", form2).val());
        } catch(e){date2=null;}
        time2 = $("input[name$='-timeFrom']", form2).val();
        if ( date2 == null && date1 == null ) return 0;
        if ( date2 == null || ( date1 != null && date1.getTime() > date2.getTime() ) )
            return 1; //form1 greater
        if ( date1 == null || ( date1.getTime() < date2.getTime() ) )
            return -1;//form2 greater
        return 0; //equal
    }
};