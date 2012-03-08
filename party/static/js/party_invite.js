/**
 * User: jarik
 * Date: 2.03.12
 * Time: 0:36
 */


var PartyInvite =
{
  initPartyInvitePopup: function(popup, invitationURL)
  {
        $(function()
        {
            $("a[rel=tooltip]",popup).tooltip();
            $('#inviteButton',popup).click(function()
            {
                //create party
                var $this = $(this);
                if($this.attr("disabled") == "true" || $this.hasClass('disabled')) return;
                $this.attr("disabled","true");
                $this.bsbutton('loading');
                //collect friends
                var toInvite = [];
                $('#invited-list input[name=friend]',popup).each(function()
                {
                   toInvite.push($(this).val());
                });
                Common.DEBUG(toInvite);

                $.ajax({
                    url: invitationURL,
                    type: "POST",
                    data: { "friends[]": toInvite },
                    dataType: "",
                    success: function(data, status)
                    {
                        $this.text($this.attr("data-complete-text"));
                        $this.addClass("btn-success");
                    }
                });
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
        });
  }
};