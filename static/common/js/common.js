
var Common =
{
    
    csrf: "",
	DEBUG: function(msg)
	{
		$(function() // wait till DOM is ready
		{
			$("#debug").append(msg+"<br/>");
		});
	}

};
