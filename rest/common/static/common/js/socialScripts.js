var Vkontakte =
{
    logout: function()
    {
          VK.Auth.revokeGrants(function()
          {
             window.location = '';
          });
    },
    login: function(loginURL)
    {
          var oldVal = $("#vkSignName").html();
          $("#vkSignName").html("Signing in...");
          VK.Auth.login(function(response)
          {
              if (response.session) {
                  /* Successfully logged in */
                  //TODO check settings
                  //if (response.settings)
                  //{
                  user = response.session.user;
                  Common.DEBUG("logged In ");
                  //TODO show login success popup
                  
                  //request user data
                  var code;
                  code = 'return {';
                  code += 'extUser: API.getProfiles({uids: API.getVariable({key: 1280}), fields: "photo_medium"})[0]';
                  code += ',friends: API.getProfiles({uids: API.getAppFriends(), fields: "photo"})';
                  code += '};';
                  VK.Api.call('execute', {'code': code}, function(data)
                  {
                      if (data.response)
                      {
                          extUser = data.response.extUser;//extended user info
                          Common.DEBUG("DATA "+data.response.extUser.photo_medium);
                          // redirect to local login
                          $("#extLoginForm input[name=lastName]").val(user.last_name);
                          $("#extLoginForm input[name=firstName]").val(user.first_name);
                          $("#extLoginForm input[name=nickName]").val(user.nickname);
                          $("#extLoginForm input[name=photo]").val(extUser.photo_medium);
                          $("#extLoginForm input[name=uid]").val(user.id);
                          $("#extLoginForm input[name=provider]").val("vk");
                          $("#extLoginForm").submit();
                      }
                  });
                  
              } else {
                  $("#vkSignName").html(oldVal);
                  Common.DEBUG("Closed");
              }
          }, 2 | 4 | 8);
    }
}

var Facebook =
{
    login: function()
    {
        $("#fbSignName").html("Signing in...");
		 FB.login(function(response) {
			  if (response.authResponse) {
                   $("#extLoginForm input[name=accessToken]").val(response.authResponse.accessToken);
                   FB.api('/me', function(user)
                   {
                       Common.DEBUG("DATA "+JSON.stringify(user));
                       // redirect to local login
                       $("#extLoginForm input[name=lastName]").val(user.last_name);
                       $("#extLoginForm input[name=firstName]").val(user.first_name);
                       $("#extLoginForm input[name=nickName]").val(user.nickname);
                       $("#extLoginForm input[name=photo]").val("http://graph.facebook.com/"+user.id+"/picture?type=large");
                       $("#extLoginForm input[name=uid]").val(user.id);
                       $("#extLoginForm input[name=provider]").val("fb");

                       $("#extLoginForm").submit();
                   });
			  } else {
			    // user is not logged in
			  }
		 }, {scope:'publish_stream, user_events, friends_events'});
    },
    logout: function ()
      {
          FB.api({ method: 'Auth.revokeAuthorization' }, function(response)
          {
             window.location = '';
          });
      }
}

//////////////////////////////////               InitFunc ///////////////
  
  

  
  