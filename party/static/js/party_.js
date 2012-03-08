/**
 * User: jarik
 * Date: 19.02.12
 * Time: 23:52
 */

var Party =
{
    init: function()
    {
        $(function()
        {
            $("input").labelify({ labelledClass: "helpLabel" });
            $("textarea").labelify({ labelledClass: "helpLabel" });
        });
    }
}