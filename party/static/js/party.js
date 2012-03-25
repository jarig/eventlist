/**
 * User: jarik
 * Date: 19.02.12
 * Time: 23:52
 */

var Party =
{
    init: function()
    {
        $(function()
        {
            //TODO move to credit init
            $("input").labelify({ labelledClass: "helpLabel" });
            $("textarea").labelify({ labelledClass: "helpLabel" });
            Party.addSchedule();
            $("#searchEventButton").click(function()
            {
                var searchEventURL = $("#searchEventURL").val();
                CommonGUI.showLoading();
                $.loadComponent(searchEventURL,['js/event_search.js','css/event_search_box.css'],{},function(data)
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
                });
                return false;
            });
        });
    },
    addSchedule: function()
    {
        $('select[name$="-location"]').chosen();
        $('select[name$="-eventSchedule"]').chosen();
    }
};