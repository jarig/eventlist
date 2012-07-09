var BlogModule =
{
    showModuleList: function(url, renderUrl, position, formPrefix)
    {
        CommonGUI.showLoading();
        $.loadComponent(url,[
            //resources here
        ],{},function(data)
        {
            CommonGUI.hideLoading();
            var wrapper = $("<div></div>");
            $("body").append($(wrapper).append(data));
            var popup = $(".modal",data).modal();
            popup.on('hidden', function ()
            {
                $(wrapper).remove();
            });
            $("._blogModule", popup).click(function()
            {
                //send request to render module, append it to position
                var moduleHash = $("#moduleHash",this).val();
                $.ajax(
                {
                    url: renderUrl,
                    data: { moduleHash: moduleHash, "position": position },
                    success: function(data)
                    {
                        //remove previous module
                        try{
                            BlogModule.removeModule(formPrefix, position);
                        }catch(e){Common.DEBUG(e);}
                        //add formset form
                        var form = $(formPrefix).ajaxSimpleForm("add","#moduleForms", true);
                        $(form).attr("id","modules-"+position);
                        //fill form
                        $("[name$=module]",$(form)).val(moduleHash);
                        $("[name$=position]",form).val(position);
                        $("[name$=parameters]",form).val("");
                        $("#module-"+position).html(data);
                        $(popup).modal('hide');
                    }
                });
            });
        });
        return false;
    },
    removeModule: function(formPrefix, position)
    {
        $(formPrefix).ajaxSimpleForm("remove",$("#modules-"+position));
        $("#module-"+position).html("");
        return false;
    },
    showModuleSettings: function(url)
    {
        //send request to render module settings, save them to form on submit
    }
};
