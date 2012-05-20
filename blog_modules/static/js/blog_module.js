var BlogModule =
{
    showModuleList: function(url)
    {
        CommonGUI.showLoading();
        $.loadComponent(url,[
            //resources here
        ],{},function(data)
        {
            CommonGUI.hideLoading();
            $("body").append(data);
            var popup = $(".modal",data).modal();
            popup.on('hidden', function ()
            {
                $(data).remove();
            });
        });
        return false;
    },
    addModule: function(position)
    {

        return false;
    }
};

