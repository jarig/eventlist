/**
 * User: jarik
 * Date: 7.04.12
 * Time: 18:28
 */


var AccountSearch =
{
    initFriendSelect: function(popup, opts)
    {
        var options =
        {
            toExclude: [],
            onSubmit: function(popup, button, friendList, additionalInfo){}
        };
        options = $.extend(options, opts);
        $(function()
        {
            $("a[rel=tooltip]",popup).tooltip();
            $('#inviteButton',popup).click(function()
            {
                //create party
                var $this = $(this);
                if($this.attr("disabled") == "true" || $this.hasClass('disabled')) return;
                $this.attr("disabled","true");
                $this.button('loading');
                //collect friends
                var toInvite = [];
                var addInfo = {};
                $('#invited-list .friend-item',popup).each(function()
                {
                    var id = $("input[name=friend]", this).val();
                    toInvite.push(id);
                    addInfo[id] = {
                        'avatar': $(".thumbnail img", this).attr("src"),
                        'name': $("#friend-name", this).text()
                    };
                });
                //Common.DEBUG(toInvite);
                options.onSubmit(popup, $this, toInvite, addInfo);
            });
            $("#invited-list", popup).change(function()
            {
                if ( $("#invited-list .friend-item", popup).size() == 0 )
                    $('#inviteButton',popup).attr("disabled","true");
                else
                    $('#inviteButton',popup).removeAttr("disabled");
            });
            $("#invited-list", popup).change();
            $("#searchFriendInput", popup).keyup(function()
            {
                setTimeout(function()
                {
                    var val = $("#searchFriendInput", popup).val();
                    $("#invitation-list .friend-item").each(function(index)
                    {
                        var $this = $(this);
                        var name = $("#friend-name",$this).text();
                        var re = new RegExp('('+val.replace(/[\s\-,]+/g, '|').replace(/[\/\\\(\)\[\]\{\}\*,]/g, '').replace(/^\||\|$/g, '')+')', 'gi');
                        $this.scrollTop(0);
                        if (re.exec(name) && !$this.attr("selected"))
                            $this.show();
                        else
                            $this.hide();
                    });
                },0);//do in thread
            });
            //hide invited from invite list
            $("#invitation-list .friend-item", popup).click(function()
            {
                var $this = $(this);
                var friend = $this.clone();
                friend.click(function()
                {
                    var $this = $(this);
                    var origItem = $("#invitation-list #"+$this.attr("id"), popup);
                    origItem.removeAttr('selected');
                    $this.remove();
                    $("#invited-list", popup).change();
                    $("#searchFriendInput", popup).keyup();
                });
                $("#invited-list", popup).append(friend);
                $("#minusSign",friend).css("display","block");
                $("#plusSign",friend).hide();
                $this.hide();
                $this.attr("selected","true");
                $("#invited-list", popup).change();
            });
            $('#invitation-list .friend-item',popup).each(function()
            {   //remove excluded ones
                var input = $("input[name=friend]", this);
                //Common.DEBUG($(input).val());
                if ( $.inArray($(input).val(), options.toExclude) > -1 )
                    $(this).remove();
            });
        });
    }
};