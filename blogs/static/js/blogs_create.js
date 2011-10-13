

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
           $("#id_facilities").multiselect(
               {
                   header: "",
                   noneSelectedText: 'Select facility types',
                   selectedList: 4,
                   multiselectclick: function(event, ui)
                   {
                       /*
                       ui.value: value of the checkbox
                        ui.text: text of the checkbox
                        ui.checked: whether or not the input was checked
                        or unchecked (boolean)
                       */
                       
                   },
                   beforeopen: function()
                   {
                       $(".ui-multiselect-menu").css("width",$(".ui-multiselect").width());
                   }
           }).multiselectfilter();
           //$(".ui-helper-reset").hide();
           $(".ui-multiselect").css("width","100%");
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
    openUploadWindow: function()
    {
      $("#uploadDialog").dialog(
          {
              title: "Upload Logo",
              height: "150",
              modal: true,
              buttons: {
                  submit: function()
                  {
                         $("#uploadLogoFrame").load(function()
                             {
                                var imgUrl = $("#uploadLogoFrame").contents().find("#imageUrl").val();
                                if (imgUrl != "False")
                                {
                                    $("#blogLogoSrc").attr("src",imgUrl);
                                    $("#uploadDialog").dialog("close");
                                }
                             });
                         $("#uploadLogoFrame").contents().find("form").submit();
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

