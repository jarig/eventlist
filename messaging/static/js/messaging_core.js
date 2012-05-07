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
            var $this = $(this);
            $('#createMessageButton').click(function()
            {
                var msgURL = $(this).attr("action-data");
                CommonGUI.showLoading();
                $.loadComponent(msgURL,[ 'css/messaging_send.css' ],
                {},function(data)
                {
                    CommonGUI.hideLoading();
                    $("body").append(data);
                    var popup = $(".modal",data).modal();
                    popup.on('hidden', function ()
                    {
                        $(data).remove();
                    });
                    var $form = $("#sendMessageForm",popup);
                    $("#sendMessageButton", popup).click(function()
                    {
                        var $this = $(this);
                        $this.bsbutton('loading');
                        $.post($form.attr("action"), $form.serialize())
                        .success(function() { $this.bsbutton('complete'); })
                        .error(function(data) {
                                var errorData = Common.eval(data["responseText"]);
                                for (var errorKey in errorData)
                                {
                                    var error = errorData[errorKey];
                                    var parent = $("#id_"+errorKey,$form).parents(".control-group");
                                    parent.addClass("error");
                                }
                            })
                        .complete(function() {  });
                        $this.bsbutton('reset');
                    });
                });
                return false;
            });
        });
    }
};

//run when included
Messaging.initActions();