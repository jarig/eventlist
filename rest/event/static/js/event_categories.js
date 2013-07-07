

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
    console.log("activating live tiles");
    //make tiles active
    this.each(function()
    {
        var $this = $(this);
        var slides = $this.find(".metro-slide-content");
        var delay = Math.random()*settings["randomRange"] + settings["delay"];
        if ( slides.length > 0 )
        {
            var $firstSlide = $(slides[0]);
            var slideHeight = $firstSlide.height(); //assume the same for all of them
            $this.data("offset", 0);
            (function($this, slideHeight, $firstSlide, slideLength){
                setInterval(function()
                {
                    var currentOffset = $this.data("offset");
                    currentOffset -= slideHeight;
                    currentOffset %= slideHeight*slideLength;
                    $this.data("offset", currentOffset);
                    console.log("Offset " + currentOffset);
                    $firstSlide.transition({
                        marginTop: currentOffset + "px"
                    });
                }, delay * 1000);
            })($this, slideHeight, $firstSlide, slides.length);
        }
    });
};