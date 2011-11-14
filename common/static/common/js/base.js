


var Base =
{
    init: function()
    {
        $(function()
        {
            try
            {
                var prBoxId = $.cookie('profileBoxId');
                var prBoxVisible = $.cookie('profileBoxStatus');
                if(typeof(prBoxId) != "undefined" && prBoxVisible == "false")
                    $(prBoxId).hide();
            }catch(e)
            {
            }

        });
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
            $("#column_left").show();
        });
        return false;
    }
}