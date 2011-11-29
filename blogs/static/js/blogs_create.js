

var BlogForm =
{
    initCreate: function()
    {
       $(function()
       { //dom ready
           $("input[type=submit]","#createBlogBox").button();
           $("input").labelify({ labelledClass: "helpLabel" });
           $("textarea").labelify({ labelledClass: "helpLabel" });
           //types select
           $("#id_facilities").chosen();
       });
    },
    submit: function(form)
    {
        //gather data
        $(form).submit();
        return false;
    }
};

var BlogGUI =
{
    selectedMenuItem : null,
    showModulesPage: function(url, mDivId, position)
    {
        var modulesSector= $(mDivId +" #modules");
        $(modulesSector).html("Loading...");
        $.ajax(
        {
            "url": url,
            success: function(resp)
            {
                $(modulesSector).html("");
                var modules = eval("("+resp+")");
                for(var i=0; i<modules.length;i++)
                {
                    var module = modules[i]["fields"];
                    var mPreview = $(mDivId+ " #modulePreviewTemplate").clone();
                    $("#name",mPreview).html(module["name"]);
                    $("#logo",mPreview).attr("src", $("#imgBase",mPreview).val()+module["logo"]);
                    $("#descr",mPreview).html(module["descr"]);
                    $(mPreview).show();
                    $(mPreview).attr("id",modules[i]["pk"]);
                    $(modulesSector).append(mPreview);
                }
            }
        });
        var title = $(mDivId).attr("title");
        $(mDivId).dialog({
                "title": title,
                width: 300,
                height: 400,
                modal: true,
                buttons:
                {
                    'Close': function () { $(this).dialog("destroy"); }
                },
                close: function(){ $(this).dialog("destroy"); }
        });
        return false;
    },
    initMenu: function(menuIdent, defaultSelected)
    {
        $(function()
        {
            var hrefs = $("a",menuIdent);
            BlogGUI.selectedMenuItem = null;
            for (var i=0; i<hrefs.length; i++)
            {
                var href = $(hrefs[i]);
                var hrefURL = $(href).attr("href");
                if (hrefURL == defaultSelected)
                    defaultSelected = href;
                $(href).bind("click",function()
                {
                    var hrefURL = $(this).attr("href");
                    BlogGUI.showContent($(this), hrefURL);
                    return false;
                });
            }
            hrefURL = $(defaultSelected).attr("href");
            BlogGUI.showContent($(defaultSelected), hrefURL);
        });
    },
    showContent: function(button, contentId)
    {
        if (BlogGUI.selectedMenuItem != null) $(BlogGUI.selectedMenuItem).removeClass("selected");
        //move edited content back
        $("#blogContent .blogContent").appendTo($("#blogPageBlocks"));
        //insert new content
        $("#blogContent").append($(contentId));
        //mark as selected
        $(button).parent("div").addClass("selected");
        BlogGUI.selectedMenuItem = $(button).parent("div");
        return false;
    }
};

