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
                    data: { moduleHash: moduleHash },
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


(function( $ ){

    var formTemplate;
    var managementForm = {
        totalForms: 0,
        initialForms: 0,
        maxNum: 0
    };
    var formPrefix;
    var methods = {
        init : function()
        {
            formPrefix = this.selector;
            managementForm["totalForms"] = $("input[name='"+formPrefix+"-TOTAL_FORMS']");
            managementForm["initialForms"] = $("input[name='"+formPrefix+"-INITIAL_FORMS']");
            managementForm["maxNum"]= $("input[name='"+formPrefix+"-MAX_NUM_FORMS']");
            formTemplate = $("#"+formPrefix+"-empty_form").clone();
            methods.initForms();
        },
        initForms: function()
        {//init any forms ( bound and new ones )
            $("[name^="+formPrefix+"]").each(function()
            {
                var form = $(this);
                if ($("[name$=-DELETE]", this).is("[value=on]"))
                {
                    form.hide();
                }else
                {
                    $("[action-bind='closeButton']",this).click(function()
                    {
                        return methods.remove(form);
                    });
                    options.onInitForm(form);
                }
            });
        },
        remove: function(form)
        {
            var $form = $(form);
            $form.fadeOut('fast',function()
            {
                $form.hide();
                $('[name$=-DELETE]', $form).val("on");
                $('[name$=-DELETE]', $form).attr("checked","checked");
                $form.attr("id","DELETED");
                //$form.remove();
                //var tForms = parseInt(managementForm["totalForms"].val()-1);
                //managementForm["totalForms"].val(tForms);
                //$("._"+formPrefix).each(function()
                //{
                //    methods.updateIndex($(this), tForms-1);
                //});
            });
            return false;
        },
        add: function( addTo, hidden )
        {
            if (typeof hidden == "undefined") hidden = false;
            if ( typeof managementForm["maxNum"].val() != "undefined" &&
                parseInt(managementForm["totalForms"].val()) >=
                    parseInt(managementForm["maxNum"].val()) ) return false;
            var num  = parseInt(managementForm["totalForms"].val());
            var form = $(formTemplate).clone();
            form.hide();
            $(form).attr("id",formPrefix+"-form-"+num);
            methods.updateIndex(form, num);
            $(addTo).append(form);
            if(!hidden) form.fadeIn();
            managementForm["totalForms"].val(parseInt(managementForm["totalForms"].val())+1);
            options.onAdd(form);
            return form;
        },
        updateIndex: function(form, nIndex)
        {
            var formPrefixRegex = new RegExp('(.*)('+formPrefix+'-)(\\d+|__prefix__)(.*)','i');
            $("[name^="+formPrefix+"]", form).each(function()
            {
                var newId =  formPrefixRegex.exec($(this).attr("id"));
                var newName = formPrefixRegex.exec($(this).attr("name"));
                var newActionData = formPrefixRegex.exec($(this).attr("action-data"));
                if ( newId != null )
                    $(this).attr("id", newId[1]+newId[2]+nIndex + newId[4]);
                if ( newName != null )
                    $(this).attr("name", newName[1]+newName[2]+nIndex + newName[4]);
                if ( newActionData != null )
                    $(this).attr("action-data", newActionData[1]+newActionData[2]+nIndex + newActionData[4]);
            });
        }
    };

    var options = {
        onAdd: function(form){},
        onInitForm: function(form) {},
        compareForms: function(form1, form2) { return form1;}
    };

    $.fn.ajaxSimpleForm = function( method ) {
        // Method calling logic
        if ( methods[method] )
        {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object')
        {
            $.extend(options, method);
        } else if ( ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery' );
        }

    };
})( jQuery );
