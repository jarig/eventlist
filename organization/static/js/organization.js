/**
 * Created by PyCharm.
 * User: jarik
 * Date: 10/30/11
 * Time: 2:28 PM
 * To change this template use File | Settings | File Templates.
 */

var OrganizationCreate = {
    init: function()
    {
        $(function()
        {
            $("input").labelify({ labelledClass: "helpLabel" });
            $("textarea").labelify({ labelledClass: "helpLabel" });
            //restore logo
            var logoURL = $("#id_logo").val();
            if (logoURL != "")
            {
                $("#orgLogoSrc").attr("alt","logo")
                $("#orgLogoSrc").attr("src",logoURL);
            }
        });
    }
};