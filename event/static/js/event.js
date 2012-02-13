/**
 * Created by PyCharm.
 * User: jarik
 * Date: 10.01.12
 * Time: 0:40
 * To change this template use File | Settings | File Templates.
 */

var Event =
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
                    $('.partyWindow', $this).rest_Event("showPartyWindow", $this);
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
                                $('#goButton',$this).show();
                                $('#unGoButton',$this).hide();
                            }
                        }
                        );
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
            if ( data && data.initialized)
                return $this.rest_Event('hide');

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
                function() { $this.rest_Event('hide'); return false; }
            );
            $this.css({top: coord.top-($this.height()+5),
                          left: coord.left - ($this.width()-$(button).width())});
            $this.show();
            $(".createPartyButton", $this).click(function()
            {
                $.post($("#createSimpleParty").attr("action"),
                       $("#createSimpleParty").serialize(),
                        function(data, textStatus)
                        {
                            Common.DEBUG(JSON.stringify(data));
                            $(".createPartyButton", $this).parent(".partySubTitle").addClass("partyCreated");
                            $("#partyCreatedMessage", $this).show();
                            $("#createPartyButton", $this).hide();
                            $(".editPartyButton", $this).removeClass("hidden");
                            $(".createPartyButton", $this).unbind("click");
                            $('#goButton',container).hide();
                            $('#unGoButton',container).show();
                        }
                );
                return false;
            });
        }
    };
    $.fn.rest_Event = function(method)
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