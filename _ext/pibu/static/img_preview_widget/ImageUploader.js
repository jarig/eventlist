

var ImageUploader =
{
    "openUploadWindow": function(logoSrcId, inputId, frameUrl)
    {
        var dailogWindow = $("<div><iframe src='#' frameborder='0' width='100%' height='100%'></iframe></div>");
        $("iframe", dailogWindow).attr("src",frameUrl);

        $(dailogWindow).dialog(
            {
                title: "Upload Logo",
                height: "180",
                width: "350",
                modal: true,
                buttons: {
                    submit: function()
                    {
                        $("iframe",dailogWindow).load(function()
                        {
                            $(this).unbind('load');
                            var imgPath = $("iframe",dailogWindow).contents().find("#imagePath").val();
                            var imgUrl = $("iframe",dailogWindow).contents().find("#imageUrl").val();
                            if (imgPath != "False")
                            {
                                CommonGUI.showLoading();
                                Common.DEBUG(imgPath);
                                Common.DEBUG(imgUrl);
                                $(logoSrcId).load(function()
                                {
                                    //hide loading
                                    CommonGUI.hideLoading();
                                    $(this).unbind('load');
                                });
                                $(logoSrcId).attr("src",imgUrl);
                                if (typeof(inputId) != "undefined")
                                    $("input[id="+inputId+"]").val(imgUrl);
                                $(dailogWindow).dialog("destroy");
                            }
                        });
                        $('iframe',dailogWindow).contents().find("form").submit();
                    },
                    close: function()
                    {
                        $(this).dialog("close");
                    }
                }
            }
        );
        return false;
    }
};
