

var BlogForm =
{
    init: function()
    {
       $(function()
       { //dom ready
           $("input[type=submit]","#createBlogBox").button();
       });
    },
    submit: function()
    {
        
    }
};

var BlogGUI =
{
    selectedMenuItem : null,
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

