


var Base =
{
    init: function()
    {
        $(function()
        {
            try
            {
                var prBoxId = $.cookie('profileBoxId');
                var prBoxVisible = $.cookie('profileBoxStatus');
                if(typeof(prBoxId) != "undefined" && prBoxVisible == "false")
                    $(prBoxId).hide();
            }catch(e)
            {
            }
            $("#langSwitch").change(function()
                                    {
                                        $(this).parents("form").submit();
                                    });

        });
    },
    toggle_profileBox: function(profileContainer)
    {
        var isVisible = !$(profileContainer).is(":visible");
        $(profileContainer).slideToggle();
        $.cookie('profileBoxStatus', isVisible, {path: '/'});
        $.cookie('profileBoxId', profileContainer, {path: '/'});
    }
};

var BaseGUI =
{
    initLoginPopup: function()
    {
      $(function()
      {
          $("#signInAccordion").accordion({
              fillSpace: false,
              autoHeight: false
          });

          $("#registerButton").click(function()
          {
              try
              {
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
                              //$("#registerForm").submit();
                          },
                          202: function(data) //not activated
                          {
                          },
                          405: function(data)
                          {
                          }
                      }
                  }).always(function(jqXHR, textStatus)
                      {
                          $(".alert").hide();
                          $this.bsbutton("reset");
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
    toggleRightColumn: function()
    {
        var isVisible = $("#column_right").is(":visible");
        var targetWidth = 20;
        var origWidth = $('#column_right').css("width");
        if (!isVisible)//if hidden
        {
            targetWidth = origWidth;
            $('#column_right').css("width", 0);
            $("#column_right").show();
        }
        $('#column_right').animate({
                    width: targetWidth
                  }, 200, function() {
                    if (isVisible)
                        $("#column_right").hide();
                    $('#column_right').css("width", origWidth);
                  });
        return false;
    },
    hideRightColumn: function()
    {
        $(function()
        {
           var isVisible = $("#column_right").is(":visible");
           if (!isVisible) return false;
           $("#column_right").hide();
           //BaseGUI.toggleRightColumn();//hide
        });
    },
    showLeftColumn: function()
    {
        $(function()
        {
            $("#column_left").show();
        });
        return false;
    }
}