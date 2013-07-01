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
            $(".read-narrow-button").tooltip();
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
                    $("#id_to", popup).chosen();
                    $("#sendMessageButton", popup).click(function()
                    {
                        var $this = $(this);
                        $this.bsbutton('loading');
                        $(".control-group", popup).removeClass("error");
                        $.post($form.attr("action"), $form.serialize())
                        .success(function()
                            {
                                $this.bsbutton('complete');
                                $this.addClass("btn-success");
                                $this.attr("disabled","disabled");
                            }
                        )
                        .error(function(data) {
                                var errorData = Common.eval(data["responseText"]);
                                var errorKey;
                                for (errorKey in errorData)
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

            });//create message button click

            //read actions
            $.each("._messageContainer",function(){
                var $this = $(this);
                $(".read-narrow-button", $this).click(function()
                {
                });
            });

        });// DOM init
    }
};

//run when included
Messaging.initActions();