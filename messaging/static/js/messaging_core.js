/**
 * User: jarik
 * Date: 17.03.12
 * Time: 13:12
 */

var Messaging =
{
    initActions: function()
    {
        $(function()
        {
            $('a[action-bind="sendMessage"]').click(function()
            {
                var $this = $(this);

                return false;
            });
        });
    }
};

//run when included
Messaging.initActions();