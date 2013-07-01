var PartyInvite =
{
  initPartyInvitePopup: function(popup, invitationURL)
  {
        $(function()
        {
            AccountSearch.initFriendSelect(popup,
                {
                onSubmit: function(popup, button, inviteList) {
                    $.ajax({
                        url: invitationURL,
                        type: "POST",
                        data: { "friends[]": inviteList },
                        dataType: "",
                        success: function(data, status)
                        {
                            button.text(button.attr("data-complete-text"));
                            button.addClass("btn-success");
                        }
                    });
                }
            });//init friend select

        }); // dom ready
  }
};