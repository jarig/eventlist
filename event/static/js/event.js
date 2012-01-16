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
            $(".partyButton").click(function()
            {
                $("#partyWindow").rest_Event("showPartyWindow", this);
                return false;
            });
            
        });
    }
};

(function($)
{
    var $this;
    function hide()
    {
        //$(this).unbind('click');
        $this.hide();
        return false;
    }
    var methods ={
        showPartyWindow: function(button)
        {
            $this= $(this);
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
            $('a[role="button"]',$this).click(hide);
            $this.css({top: coord.top-($this.height()+5),
                          left: coord.left - ($this.width()-$(button).width())});
            $this.show();
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