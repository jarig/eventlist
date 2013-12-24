(function( $ ){

    var name = "hDropBox";
    function HDropBox(el, opts)
    {
        this.$this      = $(el);
        this.firstElement = null;
        this.lastElement = null;
        this.moveElement = null;
        this.wrapperElement = null;
        this.leftBorder = 0;
        this.rightBorder = false;
        this.moveElementRightMargin = false;
        this.isMoving = false;
        if ( $(el).prop("tagName").toLowerCase() != "select" )
        {
            console.error("Wrong usage of HDropBox, not select element specified: "+el);
            return;
        }
        this.defaults = {
            multichoice: false
        };

        var meta = this.$this.data(name + '-opts');
        this.opts = $.extend(this.defaults, opts, meta);
        this.$this.data(name, this);
        this.init();
    }
    HDropBox.prototype.selectOption = function(option)
    {
        var $option = $(option);
        if ( $option.hasClass("hdb-option-selected") )
            $option.removeClass("hdb-option-selected");
        else
        {
            $option.addClass("hdb-option-selected");
            //deselect other options if in single-select mode
        }
    };

    HDropBox.prototype.init = function ()
    {
        //create DOM structure
        var $selectDOM = this.$this;
        var self = this;
        $selectDOM.hide();
        var items = $("option", $selectDOM);
        var $hdbScrollContainer = $("<div/>").addClass("hdb-scroll");
        var $hdbContainer = $("<div/>").addClass("hdb-options");
        var $hdbMoveContainer = $("<div/>").addClass("hdb-option-container");
        $hdbContainer.append($hdbMoveContainer);
        $hdbContainer.append($hdbScrollContainer);
        for ( var i=0; i< items.length; i++ )
        {
            var $item = $(items[i]);
            //TODO: replace bootstrap classes in hDropBox plugin
            var $hdbOption = $("<div/>").addClass("hdb-option");
            var $hdbOptionContents = $("<a/>").text($item.text()).attr("value", $item.val());
            $hdbOptionContents.addClass("btn").addClass("btn-link");
            $hdbOption.append($hdbOptionContents);
            $hdbMoveContainer.append($hdbOption);
            if ( i == 0 )
                this.firstElement = $hdbOption;
            if ( i == items.length - 1)
                this.lastElement = $hdbOption;
            $hdbOption.click(function() {
               self.selectOption(this);
            });
            if ( $item.is(':selected'))
                self.selectOption($hdbOption);
        }
        $selectDOM.after($hdbContainer);
        $hdbContainer.show();
        console.log($hdbContainer);
        this.moveElement = $hdbMoveContainer;
        this.wrapperElement = $hdbContainer;
        $hdbContainer.bind('mousewheel', function(event, delta) {
            var deltaY = event.originalEvent.deltaY;
            if ( self.isMoving )
            {
                $(self.moveElement).stop();
            }
            if ( self.rightBorder === false )
            {
                self.rightBorder = self.lastElement.offset().left - self.wrapperElement.innerWidth() + self.lastElement.outerWidth();
                self.moveElementRightMargin = self.lastElement.offset().left - self.wrapperElement.innerWidth() - self.moveElement.offset().left + self.lastElement.outerWidth();
            }
            if ( self.rightBorder < self.wrapperElement.innerWidth() )
                return false;
            var koef = deltaY*8;
            var moveTo = "-=" + koef;
            if (self.firstElement.offset().left >= self.leftBorder && deltaY < 0)
                moveTo = 0;
            if (self.lastElement.offset().left <= self.rightBorder && deltaY > 0 )
                moveTo = -self.moveElementRightMargin;
            self.isMoving = true;
            $(self.moveElement).animate({
                "left": moveTo
            }, 200, "swing", function()
            {
                self.isMoving = false;
            });
            return false;
        });
    };

    $.fn.hDropBox = function( opts ) {
        // Method calling logic
        return this.each(function()
        {
            try
            {
                new HDropBox(this, opts);
            } catch(ex)
            {
                console.log("Failed to create horizontal drop box: " + ex);
            }
        });
    };
})( jQuery );
