

var EventSearch =
{
  initPopup: function(popup, searchURL)
  {
      var $popup = $(popup);
      $("#searchEventInput", $popup).keyup(function(event)
      {
          if ( event.which == $.ui.keyCode.ENTER)
          {
          }
          //send search data to searchURL
      });
  }
};
