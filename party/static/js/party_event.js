/**
 * Created by PyCharm.
 * User: jarik
 * Date: 10.01.12
 * Time: 0:40
 * To change this template use File | Settings | File Templates.
 */

var PartyEvent =
{
    init: function()
    {
        $(function()
        {
            $(".event-container").each(function()
            {
                var $this = $(this);
                $('#goButton',$this).click(function()
                {
                    $('.partyWindow', $this).rest_Party("showPartyWindow", $this);
                    return false;
                });
                $("#unGoButton",$this).click(function()
                {
                    $.post($("#unGoForm", $this).attr("action"),
                        $("#unGoForm",$this).serialize(),
                        function(data, textStatus)
                        {
                            if (data == "True")
                            {
                                $('.partyWindow', $this).hide();
                                $('.ifGoes',$this).hide();
                                $('.ifNotGo',$this).show();
                                $("#partyStatus", $this).removeClass("partyCreated");
                            }
                        }
                        );
                    return false;
                });
                var invitationURL = $("#invitationURL", $this).val();
                $(".partyInviteButton", $this).click(function()
                {
                    CommonGUI.showLoading();
                    $.loadComponent(invitationURL,['js/party_invite.js','css/party_invite_box.css'],{},function(data)
                    {
                        CommonGUI.hideLoading();
                        $("body").append(data);
                        var popup = $(".modal",data).modal();
                        popup.on('hidden', function ()
                        {
                            $(data).remove();
                        });
                        PartyInvite.initPartyInvitePopup(popup,invitationURL);

                    });
                    return false;
                });
            });
        });
    }
};

(function($)
{
    var methods ={
        hide: function()
        {
            var $this= $(this);
            $this.hide();
            //$this.remove();
            $this.data('showPartyWindow',
                    {
                        "initialized": false
                    });
            return false;
        },
        showPartyWindow: function(container, onCloseMethod)
        {
            var $this= $(this);
            var button = $("#goButton",container);
            var data = $this.data('showPartyWindow');
            if ( $this.is(":visible") )
            {
                $this.hide(); return false;
            }

            if ( !data || !data.initialized)
            {
                $this.data('showPartyWindow',
                    {
                        "onClose": onCloseMethod,
                        "initialized": true
                    });
            }
            //alert(data.showPartyWindow['initialized']);
            $this.show();
            var coord = $(button).offset();
            $this.width(450);
            $('a[role="button"]',$this).hover(
                function(eO)
                {
                    $(this).addClass("ui-state-hover");
                },
                function(eO)
                {
                    $(this).removeClass("ui-state-hover");
                }
            );
            $('a[role="button"]',$this).click(
                function() { $this.rest_Party('hide'); return false; }
            );
            $this.css({top: coord.top-($this.height()+5),
                          left: coord.left - ($this.width()-$(button).width())});
            $this.show();
            $(".createPartyButton", $this).click(function()
            {
                $.post($("#createSimpleParty",$this).attr("action"),
                       $("#createSimpleParty",$this).serialize(),
                        function(data, textStatus)
                        {
                            Common.DEBUG(JSON.stringify(data));
                            try
                            {
                                var data = Common.eval(data);
                                if (data.id > 0)
                                {
                                    $("#partyStatus", $this).addClass("partyCreated");
                                    $("#partyCreatedMessage", $this).show();
                                    $("#createPartyButton", $this).hide();
                                    $(".editPartyButton", $this).removeClass("hidden");
                                    $(".createPartyButton", $this).unbind("click");
                                    $('.ifGoes',container).show();
                                    $('.ifNotGo',container).hide();
                                    $('.ifGoes',$this).show();
                                    $('.ifNotGo',$this).hide();
                                }
                            }catch(e)
                            {
                                Common.DEBUG(e);
                            }
                        }
                );
                return false;
            });
        }
    };
    $.fn.rest_Party = function(method)
    {
        if ( method && typeof method === "string" )
        {
            methods[method].apply(this, Array.prototype.slice.call( arguments, 1 ));
        } else
        {
            $.error("No such method");
        }
        return this;
    }
})(jQuery);