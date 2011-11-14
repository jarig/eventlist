
var Common =
{
    
    csrf: "",
	DEBUG: function(msg)
	{
		$(function() // wait till DOM is ready
		{
			$("#debug").append(msg+"<br/>");
		});
	},
    submitForm: function(formId)
    {
        $(formId).submit();
        return false;
    }
};


var CommonGUI =
{
    loadingWindow: '',
    showLoading: function()
    {
        CommonGUI.loadingWindow = $('<div>Loading...</div>');
        $(CommonGUI.loadingWindow).dialog({
            title: "Loading...",
            height: "80",
            width: "150",
            modal: true
        });
    },
    hideLoading: function()
    {
        $(CommonGUI.loadingWindow).dialog("close");
        $(CommonGUI.loadingWindow).remove();
    },
    openUploadWindow: function(dialogId, logoSrcId, inputId)
    {
      $(dialogId + " iframe").attr("src",$(dialogId + " iframe").attr("src"));
      var dailogWindow = $(dialogId);
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
                        $(this).unbind('load');
                        var imgPath = $(dialogId + " iframe").contents().find("#imagePath").val();
                        var imgUrl = $(dialogId + " iframe").contents().find("#imageUrl").val();
                        if (imgPath != "False")
                        {
                            CommonGUI.showLoading();
                            $(logoSrcId).load(function()
                            {
                               //hide loading
                               CommonGUI.hideLoading();
                               $(this).unbind('load');
                            });
                            $(logoSrcId).attr("src",imgUrl);
                            if (typeof(inputId) != "undefined")
                                $(inputId).val(imgPath);
                            $(dailogWindow).dialog("destroy");
                        }
                     });
                     $(dialogId + ' iframe').contents().find("form").submit();
                  },
                  close: function()
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