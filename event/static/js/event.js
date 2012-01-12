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
    var methods ={
        showPartyWindow: function(button)
        {
            var $this= $(this);
            var coord = $(button).offset();
            $this.width(450);
            //$this.height(230);
            /*$this.dialog({
                "height": 250,
                "width": 500,
                "title": title,
                "resizable": false
            });*/
            $this.offset(coord);
            coord.top -= $this.height()+5;
            coord.left -= $this.width()-$(button).width();
            $this.show();
            $this.offset(coord);
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