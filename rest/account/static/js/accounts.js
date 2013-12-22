var Accounts =
{
    firstName: '',
    lastName: '',
    avatarURL: '',
    userType: '',
    logoutProc: null,
    fid: 0,
    id: 0,
    signinLogoImg: '',
    fullName: '',
    openSignoutBox: function()
    {

    },
    openLoginBox: function()
    {
        $("#signinPopup").dialog({
            "title": "Login",
            height: '600',
            width: "640",
            resizable: false,
            modal: true });
        return false;
    },
    login: function ()
    {
        $.ajax(
            {
                url: '/ajax.php',
                data:
                {
                    module: "user",
                    action: "login"
                },
                success: function(data)
                {
                    if(data != "failed")
                    {
                        var user = eval('('+data+')');
                        $(document).ready(function()
                        {
                            initUser(user);
                            window.loggedIn(user);
                        });
                    }
                }

            });
        $(document).ready(
            function()
            {
                window.userDataLoaded(user);
            });

    },
    logout: function ()
    {
        $("#signin").html("<a href='#'>Signing out...</a>");
        $.ajax(
            {
                url: ''
            });
    },
    init: function()
    {
       $(function()
       { //dom ready
           //$("#submitButton","#editAccountBox").button();
       });
    },
    initLoginPopup: function()
    {
        $(function()
        {
            $("#signInTabs").tab();
            $("#registerButton").click(function()
            {
                try
                {
                    $("#registerErrors").html("");
                    $("#registerAlert").hide();
                    $(".control-group").removeClass("error");
                    $(".errorText").hide();
                    if ( $("input[name=password1]","#registerForm").val() != $("input[name=password2]","#registerForm").val())
                    {
                        $("#password1").addClass("error");
                        $("#err_pass_mismtach").show();
                        throw new Error("Pass mismtach");
                    }
                    var $this = $(this);
                    $this.bsbutton("loading");
                    var request = $.ajax({
                        url: $("#registerForm").attr("action"),
                        type: "POST",
                        data: $("#registerForm").serialize(),
                        statusCode:{
                            200: function(data) //success
                            {
                                $this.addClass("btn-success");
                                $this.text($this.attr("data-complete-text"));
                                $this.attr("disabled","true");
                            },
                            405: function(data)
                            {
                                $("#registerAlert").show();
                                var errors = Common.eval(data.responseText);
                                for(var i=0; i<errors.length; i++)
                                    for(var e=0; e < errors[i].length; e++)
                                    {
                                        $("#registerErrors").append(errors[i][e]+"<br/>");
                                    }
                                $this.bsbutton("reset");
                            },
                            500: function(data)
                            {
                                $this.bsbutton("reset");
                                $("#registerErrors").append("Unknown error<br/>");
                            }
                        }
                    }).always(function(jqXHR, textStatus)
                        {
                            $(".alert").hide();
                        });
                }catch(e)
                {

                }
            });


            $("#nativeLoginButton").click(function(){
                var $this = $(this);
                $this.bsbutton("loading");
                var request = $.ajax({
                    url: $("#nativeLoginForm").attr("action"),
                    type: "POST",
                    data: $("#nativeLoginForm").serialize(),
                    statusCode:{
                        200: function(data) //success
                        {
                            $("#nativeLoginForm").submit();
                        },
                        202: function(data) //not activated
                        {
                            $("#notActivatedAlert").show();
                        },
                        405: function(data)
                        {
                            $("#wrongPasswordAlert").show();
                        }
                    }
                }).always(function(jqXHR, textStatus)
                    {
                        $(".alert").hide();
                        $this.bsbutton("reset");
                    });
            });
        });

    },
    submit: function()
    {
        
    },
    initActions: function()
    {
        $(function()
        {
            $("[action-bind='addToFriends']").each(function()
            {
                var $this = $(this);
                var $thisHref = $("a",this);
                $thisHref.click(function()
                {
                    var url = $thisHref.attr("href");
                    $.ajax({
                        url: url,
                        data:{
                          "next": window.location.pathname
                        },
                        type: "GET",
                        success: function(data) //success
                            {
                                $('#action-success',$this).show();
                                $thisHref.hide();
                            }
                    });
                    return false;
                });
            });
        });
    }
};

Accounts.initActions();