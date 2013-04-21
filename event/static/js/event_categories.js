

EventCategories =
{
    init: function()
    {

    }
};

/*
    jQuery plugin for showing dynamic information in tile
 */
$.fn.activeTile = function( options )
{
    var settings = $.extend({
        //defaults
        dataSourceFunction: null,
        delay: 5,
        randomRange: 5 //in seconds
    }, options);

    //make tiles active
    this.each(function()
    {
        var $this = $(this);
        var allDivs = $this.children("div");
        var delay = Math.random()*settings["randomRange"] + settings["delay"];
        if ( allDivs.length > 0 )
        {
            //hide all divs except first one
            for( var i=1; i< allDivs.length; i++)
                $(allDivs[i]).hide().css("opacity", 0);
            $this.data("currentDivNum", 0);

            setInterval(function()
            {
                if ( typeof settings["dataSourceFunction"] === "function" )
                    settings["dataSourceFunction"]($this);
                //
                var currentDivNum = $this.data("currentDivNum");
                var currentDiv = allDivs[currentDivNum];
                var nextDivNum = (currentDivNum+1) % allDivs.length;
                var nextDiv = allDivs[ nextDivNum ];
                //TODO: add configurable animations
                //hide current div and show next one
                $(currentDiv).transition({
                    //perspective: '100px',
                    //rotateY: '180deg',
                    opacity: 0
                    //easing: 'snap',
                    //duration: 200
                });
                $(currentDiv).hide();
                $(nextDiv).show();
                $(nextDiv).transition({
                    //perspective: '100px',
                    //rotateY: '180deg',
                    opacity: 100
                    //easing: 'snap',
                    //duration: 200
                });
                $this.data("currentDivNum", nextDivNum);
            }, delay*1000);
        }
    });
};