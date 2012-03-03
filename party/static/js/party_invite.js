/**
 * User: jarik
 * Date: 2.03.12
 * Time: 0:36
 */


var PartyInvite =
{
  init: function()
  {
        $(function()
        {
            $('#partyInvitePopup #inviteButton').click(function()
            {
                //create party
                var $this = $(this);
                $this.bsbutton('loading');
                //$this.bsbutton('complete');
            });
        });
  }
};