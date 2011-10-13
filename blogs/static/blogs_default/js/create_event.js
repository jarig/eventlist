

var BlogEvent =
{
    submitForm: function(container, formId)
    {
        var formData = $("input",formId);
        var data = new Object();
        for ( var i=0; i< formData.length; i++)
        {
            var field = formData[i];
            var value = $(field).val();
            if ( value == $(field).attr("title"))
                $(field).val("");//reset value
        }
        $.post($(formId).attr("action"),
            $(formId).serialize(),
            function(data)
            {
                $(container).html(data);
            }
        );
        return false;
    },
    toggleCreateBox: function(link, contentBox, createBox, createURL, urlText)
    {
        var isVisible = $(contentBox).is(":visible");

        if (isVisible)
        {
            this.prevText = $(link).text();
            $(link).text(urlText);
            $('#loadContent').load(createURL);
            $(contentBox).hide("slide", { direction: "left" }, 200,
            function()
            {
                $(createBox).show("slide", { direction: "right" }, 200);
            });
        }else
        {
            $(link).text(this.prevText);
            $(createBox).hide("slide", { direction: "right" }, 200, function()
            {
                $(contentBox).show("slide", { direction: "left" }, 200);
            });
        }
        return false;
    }
}