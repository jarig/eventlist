

var Init =
{
	init: function ()
	{
        // register async functions
		window.fbAsyncInit = function() {
		    FB.init({
		      appId  : '122871594431190',
		      status : false, // check login status
		      cookie : true, // enable cookies to allow the server to access the session
		      xfbml  : true  // parse XFBML
		    });
		    Common.DEBUG("Inited FB");
		  };
		 window.vkAsyncInit = function() {
	        VK.init({
	          apiId: '633169',
	          nameTransportPath: '/xd_receiver.html'
	        });
	        Common.DEBUG("Inited VK");
		 };
	},

	apiInit: function(type)
	{
		this.init();
		if (type == "vk" || type == "all")
			this.vkAPI();
		if( type == "fb" || type == "all")
			this.fbAPI();
	},
	
	vkAPI: function()
	{
		setTimeout(function() {
	        var el = document.createElement('script');
	        el.type = 'text/javascript';
	        el.src = 'http://vkontakte.ru/js/api/openapi.js';
	        el.async = true;
	        document.getElementById('vk_api_transport').appendChild(el);
	    }, 0);

		setTimeout(function() {
	        var el = document.createElement('script');
	        el.type = 'text/javascript';
	        el.src = 'http://vkontakte.ru/js/api/share.js?9';
	        el.async = true;
	        $('head').append(el);
	    }, 0);
	},
	
	fbAPI: function()
	{
		setTimeout(function() {
		    var e = document.createElement('script');
		    e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js';
		    e.async = true;
		    document.getElementById('fb-root').appendChild(e);
		  },0);
	}
	
}