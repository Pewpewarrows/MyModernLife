/* Declare a namespace for the site */
var MML = window.MML || {};

/* Create a closure to maintain scope of the '$'
   and remain compatible with other frameworks.  */
(function($) {

    /*
     * http://www.viget.com/inspire/extending-paul-irishs-comprehensive-dom-ready-execution/
     *
     * Essentially, just add 'data-controller' and 'data-action' attributes to the 'body' tag
     * and define those as functions within objects here to get page-specific 'document.ready'
     * code to fire. Big thanks to Paul Irish and Jason Garber.
     *
     * TODO: push the 'exec' and 'init' functions back to a UTIL object that the global site
     *      var can just use as a template above instead of a blank '{}'
     */
    MML = {
        common: {
            init: function() {
            }
        },

        exec: function(controller, action) {
            action = (action === undefined) ? 'init' : action;

            if ((controller !== '') && this[controller] && (typeof this[controller][action] == 'function')) {
                this[controller][action]();
            }
        },

        init: function() {
            var body = document.body,
            controller = body.getAttribute('data-controller'),
            action = body.getAttribute('data-action');

            this.exec('common');
            this.exec(controller);
            this.exec(controller, action);
        }
    };
	
	$(function() {
        MML.init();

	    $('#nav-blog').hover(function() {
	        $('img', this).attr('src', '/static/images/blog.png');
	        $('span', this).removeClass('ir');
	    }, function() {
	        $('img', this).attr('src', '/static/images/blog-grey.png');
	        $('span', this).addClass('ir');
	    });
	    
	    $('#nav-portfolio').hover(function() {
	        $('img', this).attr('src', '/static/images/portfolio.png');
	        $('span', this).removeClass('ir');
	    }, function() {
	        $('img', this).attr('src', '/static/images/portfolio-grey.png');
	        $('span', this).addClass('ir');
	    });
	    
	    $('#nav-activity').hover(function() {
	        $('img', this).attr('src', '/static/images/activity.png');
	        $('span', this).removeClass('ir');
	    }, function() {
	        $('img', this).attr('src', '/static/images/activity-grey.png');
	        $('span', this).addClass('ir');
	    });
	    
	    $('#nav-resume').hover(function() {
	        $('img', this).attr('src', '/static/images/resume.png');
	        $('span', this).removeClass('ir');
	    }, function() {
	        $('img', this).attr('src', '/static/images/resume-grey.png');
	        $('span', this).addClass('ir');
	    });
	    
	    $('#nav-contact').hover(function() {
	        $('img', this).attr('src', '/static/images/contact.png');
	        $('span', this).removeClass('ir');
	    }, function() {
	        $('img', this).attr('src', '/static/images/contact-grey.png');
	        $('span', this).addClass('ir');
	    });
	    
	    $('#nav-about').hover(function() {
	        $('img', this).attr('src', '/static/images/about-me.png');
	        $('span', this).removeClass('ir');
	    }, function() {
	        $('img', this).attr('src', '/static/images/about-me-grey.png');
	        $('span', this).addClass('ir');
	    });
	
	    $('#delete-blog').click(function() {
		    if (confirm('Are you sure you want to delete this blog?')) {
			    return true;
		    } else {
			    return false;
		    }
	    });
	    
	    $('#delete-post').click(function() {
		    if (confirm('Are you sure you want to delete this post?')) {
			    return true;
		    } else {
			    return false;
		    }
	    });
	});

	$(window).bind("load", function() {
	});
	
})(jQuery);
