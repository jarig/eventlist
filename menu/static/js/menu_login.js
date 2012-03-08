var User = 
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
             height: '420',
             width: "540",
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
	}

};