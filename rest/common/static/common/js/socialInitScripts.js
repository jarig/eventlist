  var vkUser=null;
  var fbUser=null;
  var user = null;
  var loggedInWith = new Array();
    
  function vkInit()
  {
     VK.Auth.getLoginStatus(function(response) {
	  if (response.session) 
	  { 
		  $(document).ready(function() 
	      {
		    /* Logged in*/
            $("#debug").append("VK Status: "+ response.status+"<br/>");
		    $("#debug").append("VK: LoggedIn<br/>");
		    $('#vkLoggedIn').css('display','block');
		  });
	    
	    if(response.status != "connected") // VK loggedin, but not logged in to the site
	    {
	       $('#vkSignAvatar').html("<center><img width='100px' src='/imgs/vkLogoBig.jpg'></center>");
	       getVKInitData(showVKLoginProfile);

	    }
	    else // logged and connected
	    {	
	       	getVKInitData(showVKProfile);
	    }
	    
	  } else 
	  {
		  $(document).ready(function() 
	      {
		    $("#debug").append("VK: Logged Out<br/>");
		    
		    $('#vkLoggedIn').css('display','block');
		    $('#vkSignName').html("<br/><a href='#' onclick='doVKLogin()'>Login  with Vkontakt</a>");
	        $('#vkSignAvatar').html("<center><img width='100px' src='/imgs/vkLogoBig.jpg'></center>");
	      });
	  } // else
	 });

    VK.Observer.subscribe('auth.login', function(response) 
        {
            $('#vkSignAvatar').html("<center><img width='100px' src='/imgs/vkLogoBig.jpg'></center>");
            $('#vkSignName').html("<br/><a href='#' onclick='doVKLogout()'>Logout</a>");
        });
	VK.Observer.subscribe('auth.logout', function()
                                       {
                                          
                                       });
  }// vkInit
  
  function showVKProfile(data)
  {
     if (data.response) 
     {
           vkUser = data.response;
	       if(vkUser.me)
	       {
			   user = new User();
			   user.fid = vkUser.me.uid;
			   user.firstName = vkUser.me.first_name;
			   user.lastName = vkUser.me.last_name;
			   user.avatarURL = vkUser.me.photo_medium;
			   user.userType = 'VK';
	       }
     }
  }
  
  function getVKInitData(func) 
  {
      if(vkUser == null)
      {
		  var code;
		  code = 'return {';
		  code += 'me: API.getProfiles({uids: API.getVariable({key: 1280}), fields: "photo_medium"})[0]';
		  code += ',friends: API.getProfiles({uids: API.getAppFriends(), fields: "photo"})';
		  code += '};';
		  VK.Api.call('execute', {'code': code}, func);
	  }else
	      func(vkUser);
  }
  
  function showVKLoginProfile(data) 
  {
	  
	 if (data.response) 
	 {
	    vkUser = data.response;
	    /* Insert user info */
		$(document).ready(function() 
		{
		    if (vkUser.me) 
		    {
            }
		}); // on ready
	 }// if data.response
  }

  
////////////////////////////       FACEBOOK        /////////////////////////////

  // called when FB API is initialized
  function fbInit()
  {  
	  // Facebook Login Listener
	  FB.Event.subscribe('auth.statusChange', function(response) {
		    if (response.session) {
		      
		      // A user has logged in, and a new cookie has been saved
		    } else {
		      // The user has logged out, and the cookie has been cleared
		    }
	  });
	  
	   // check if user logged in using Facebook
	   FB.getLoginStatus(function(response) {
		  if (response.session) 
		  {
		  
			  $(document).ready(function() 
			  {
			    $("#debug").append("FB: LoggedIn: "+response.status + "<br/>");		    
			    $('#fbLoggedIn').css('display','block');
			  }); 

		    if(response.status != "connected")
		    {	 
			    getFBInitData(showFBLoginProfile);         
		    }else
		    {
		        //loggedInBy("FB");
		        getFBInitData(showFBProfile);
		    }
		  } else 
		  {
			  $(document).ready(function() 
			  {
				    $("#debug").append("FB: Logged Out: "+ response.status +"<br/>");
				    $('#fbLoggedIn').css('display','block');
			        $('#fbSignName').html("<br/><a href='#' onclick='doFBLogin()'>Login  with Facebook</a>");
		            $('#fbSignAvatar').html("<center><img width='100px' src='/imgs/fbLogoBig.png'></center>");
	           });
		  }
	   });
	  
   }// fbInit
   
	function showFBLoginProfile(data)
	{
	  fbUser = data;
	  $(document).ready(function()
	  {
		  $('#fbSignName').html(fbUser.name+'<br/>'+"<a href='' onclick='doFBLogin()'>Login with Facebook</a>");
		  $('#fbSignAvatar').html("<center><img width='100px' src='http://graph.facebook.com/"+fbUser.id+"/picture?type=large' ></center>");
	  });
	}
	
	function getFBInitData(func)
	{
	  if(fbUser == null)
	    FB.api('/me', func);
	  else
	    func(fbUser);
	}
	
	function doFBLogin()
	{

	}
	
	function showFBProfile(data)
	{
	   fbUser = data;
	   user = new User();
	   user.fid = data.id;
	   user.firstName = data.first_name;
	   user.lastName = data.last_name;
	   user.avatarURL = 'http://graph.facebook.com/'+fbUser.id+'/picture?type=large';
	   user.logoutProc = 'doFBLogout()';
	   user.userType = 'FB';
   	   user.signinLogoImg= '/static/imgs/fbLogoSmall.png';
       
	}
//////////////////////////////////               InitFunc ///////////////
  
  