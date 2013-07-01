/**
 * Created by PyCharm.
 * User: jarik
 * Date: 10.01.12
 * Time: 0:40
 * To change this template use File | Settings | File Templates.
 */

var PartyEvent =
{
    init: function(rootElement, revertPopup, goes)
    {
        $(function()
        {
            $(rootElement).each(function()
            {
                var $this = $(this);
                $('#goButton',$this).click(function()
                {
                    $('.partyWindow', $this).rest_Party("showPartyWindow", $this, null, revertPopup);
                    return false;
                });
                if (typeof goes != "undefined")
                {
                    if (goes == "True")
                    {
                        $('.ifGoes',$this).show();
                        $('.ifNotGo',$this).hide();
                    }else
                    {
                        $('.ifGoes',$this).hide();
                        $('.ifNotGo',$this).show();
                        Common.DEBUG("do not go");
                    }
                }
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
                    $.loadComponent(invitationURL,[
                        'js/account_search.js',
                        'js/party_invite.js',
                        'css/party_invite_box.css'],{},function(data)
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
        createSimpleParty: function(url, data, callback)
        {
            var $this= $(this);
            $.post(
                url,
                data,
                function(data, textStatus)
                {
                    Common.DEBUG(JSON.stringify(data));
                    try
                    {
                        var eData = Common.eval(data);
                        if (eData.id > 0)
                        {
                            if ( typeof callback == 'function' )
                                callback(eData);
                        }
                    }catch(e)
                    {
                        Common.DEBUG(e);
                    }
                }
            );
            return this;
        },
        showPartyWindow: function(container, onCloseMethod, upsideDown)
        {
            if (typeof upsideDown == "undefined")
                upsideDown = false;
            Common.DEBUG(upsideDown);
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
            var buttonCoord = $(button).offset();
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
            var nubOffset = 45;
            var top = buttonCoord.top-($this.height()+5);
            if (upsideDown)
            {
                $("#topNub").show();
                $("#bottomNub").hide();
                top += $this.height()+5+$(button).outerHeight();
            }
            $this.css({top: top,
                       left: (buttonCoord.left +$(button).outerWidth()/2) - ($this.width() - nubOffset) });
            $this.show();
            //$('body').click(function(){$this.hide(); delete this;});
            $(".createPartyButton", $this).click(function()
            {
                var url = $("#createSimpleParty",$this).attr("action");
                var data = $("#createSimpleParty",$this).serialize();
                //create simple party
                methods.createSimpleParty(url, data, function(eData){
                    $("#partyStatus", $this).addClass("partyCreated");
                    $("#partyCreatedMessage", $this).show();
                    $("#createPartyButton", $this).hide();
                    $(".editPartyButton", $this).removeClass("hidden");
                    $(".createPartyButton", $this).unbind("click");
                    $('.ifGoes',container).show();
                    $('.ifNotGo',container).hide();
                    $('.ifGoes',$this).show();
                    $('.ifNotGo',$this).hide();
                });
                return false;
            });
            return this;
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