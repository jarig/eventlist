


var Base =
{
    init: function()
    {
        $(function()
        {
            try
            {
                prBoxId = $.cookie('profileBoxId');
                prBoxVisible = $.cookie('profileBoxStatus');
                if(typeof(prBoxId) != "undefined" && prBoxVisible == "false")
                    $(prBoxId).hide();
            }catch(e)
            {
            }
        });
    },
    switchMode: function(url, cMode, fromMode)
    {
        /*toPage = $.cookie(cMode+'lastPage');
        $.cookie(cMode+'lastPage', document.URL, {path: '/'}); //save current mode page as last one
        if( typeof(toPage) != "undefined" && toPage != null)
        {
            window.location = toPage;
            return false;
        }*/
        window.location = url;
        return false;
    },
    toggle_profileBox: function(profileContainer)
    {
        var isVisible = !$(profileContainer).is(":visible");
        $(profileContainer).slideToggle();
        $.cookie('profileBoxStatus', isVisible, {path: '/'});
        $.cookie('profileBoxId', profileContainer, {path: '/'});
    }
}

var BaseGUI =
{
    toggleRightColumn: function()
    {
        var isVisible = $("#column_right").is(":visible");
        var targetWidth = 20;
        var origWidth = $('#column_right').css("width");
        if (!isVisible)//if hidden
        {
            targetWidth = origWidth;
            $('#column_right').css("width", 0);
            $("#column_right").show();
        }
        $('#column_right').animate({
                    width: targetWidth
                  }, 200, function() {
                    if (isVisible)
                        $("#column_right").hide();
                    $('#column_right').css("width", origWidth);
                  });
        return false;
    },
    hideRightColumn: function()
    {
        $(function()
        {
           var isVisible = $("#column_right").is(":visible");
           if (!isVisible) return false;
           $("#column_right").hide();
           //BaseGUI.toggleRightColumn();//hide
        });
    },
    showLeftColumn: function()
    {
        $(function()
        {
            $("#column_left").css('display','block');
        });
        return false;
    }
}