(function( $ ){

    var formTemplate;
    var managementForm = {
        totalForms: 0,
        initialForms: 0,
        maxNum: 0
    };
    var formPrefix;
    var formIdent;
    var emptyFormId;
    var methods = {
        init : function()
        {
            formIdent = this.selector;//class of div wrapper around form
            formPrefix = options["prefix"];//prefix of form
            emptyFormId = options["emptyFormId"];//empty form instance
            managementForm["totalForms"] = $("input[name='"+formPrefix+"-TOTAL_FORMS']");
            managementForm["initialForms"] = $("input[name='"+formPrefix+"-INITIAL_FORMS']");
            managementForm["maxNum"]= $("input[name='"+formPrefix+"-MAX_NUM_FORMS']");
            formTemplate = $("#"+emptyFormId).clone();
            methods.initForms();
        },
        initForm: function(form)
        {
            $("[action-bind='closeButton']",form).click(function()
            {
                return methods.remove(form);
            });
            options.onInitForm(form);
        },
        initForms: function()
        {//init any forms ( bound and new ones )
            $(formIdent).each(function()
            {
                var form = $(this);
                if (form.attr("id") == emptyFormId) return;
                if ($("[name$=-DELETE]", this).is("[value=on]"))
                {
                    form.hide();
                }else
                {
                    methods.initForm(form);
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
                //id_eventForm-1-id
                var id = $("[id^='id_"+formPrefix+"'][id$='-id']",$form).val();
                if (typeof id == "undefined" || id == "" || parseInt(id) <= 0 )
                {
                    //remove form and recalc indexes
                    $form.remove();
                    var tForms = parseInt(managementForm["totalForms"].val());
                    $(managementForm["totalForms"]).val(tForms-1);
                    $(formIdent).each(function()
                    {
                        //if(tForms <0 )return;
                        tForms -= 1;
                        methods.updateIndex($(this), tForms);
                    });
                }
                options.onRemove($form);
            });
            return false;
        },
        add: function( addTo, opts )
        {
            var addOptions ={ hidden: false, append: true};
            if ( typeof opts != "undefined ")
                $.extend(addOptions, opts);
            if ( typeof managementForm["maxNum"].val() != "undefined" &&
                parseInt(managementForm["totalForms"].val()) >=
                    parseInt(managementForm["maxNum"].val()) ) return false;
            var num  = parseInt(managementForm["totalForms"].val());
            var form = $(formTemplate).clone();
            form.hide();
            $(form).attr("id",formPrefix+"-form-"+num);
            methods.updateIndex(form, num);
            if (addOptions["append"])
                $(addTo).append(form);
            else
                $(addTo).prepend(form);
            if(!addOptions["hidden"]) form.fadeIn();
            options.onAdd(form);
            methods.initForm(form);
            managementForm["totalForms"].val(parseInt(managementForm["totalForms"].val())+1);
            return $(form);
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
        onAdd: function(form){return form;},
        onRemove: function(form) {return form;},
        onInitForm: function(form) {return form;},
        compareForms: function(form1, form2) { return 0;},
        emptyFormId: "form-empty_form",
        prefix: "form"
    };

    $.fn.ajaxSimpleForm = function( method, opts ) {
        // Method calling logic
        if ( methods[method] )
        {
            if (typeof opts === "object")
                $.extend(options, opts);
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object')
        {
            $.extend(options, method);
        } else if ( ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on Ajax form plugin' );
        }

    };
})( jQuery );
