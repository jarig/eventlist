/**
 * Created by PyCharm.
 * User: jarik
 * Date: 19.02.12
 * Time: 23:52
 * To change this template use File | Settings | File Templates.
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