
var Common =
{
    
    csrf: "",
	DEBUG: function(msg)
	{
		$(function() // wait till DOM is ready
		{
			$("#debug").append(msg+"<br/>");
		});
	}
};


var CommonGUI =
{
    openUploadWindow: function(dialogId, logoSrcId)
    {
      $(dialogId).dialog(
          {
              title: "Upload Logo",
              height: "150",
              width: "150",
              modal: true,
              buttons: {
                  submit: function()
                  {
                         $("iframe",dialogId).load(function()
                             {
                                var imgUrl = $("iframe",dialogId).contents().find("#imageUrl").val();
                                if (imgUrl != "False")
                                {
                                    $(logoSrcId).attr("src",imgUrl);
                                    $(dialogId).dialog("close");
                                }
                             });
                         $('iframe',dialogId).contents().find("form").submit();
                  },
                  cancel: function()
                  {
                    $(this).dialog("close");
                  }
              }
          }
        );
        return false;
    },
    uploadButton: function(ident, labelText, inputForm)
    {
        $(function()
        {
            $(ident).css("position", "relative");
            $(ident).css("height", "20px");
            $(ident).css("width", "100%");
            $(ident).css("margin-top", "2px");
            $(ident).css("margin-bottom", "2px");
            
            var label = $("<div>"+labelText+"</div>");
            $(label).css("position", "absolute");
            $(label).css("padding-top", "4px");
            $(label).css("width", "100%");
            $(label).css("height", "100%");


            var input = $(inputForm);
            $(input).css("position","relative");
            $(input).css("opacity","0");
            $(input).css("-moz-opacity","0");
            $(input).css("filter","alpha(opacity: 0)");
            $(input).css("width","100%");
            $(input).css("height","100%");
            $(ident).append(label);
            $(ident).append(input);
            
            $(ident).hover(
            function()
            {
                $(this).css("background-color","#e6e6fa");
                $(this).css("text-decoration","underline");
            },
            function()
            {
                $(this).css("background-color","white");
                $(this).css("text-decoration","none");
            });
        });//dom loaded
    }
};