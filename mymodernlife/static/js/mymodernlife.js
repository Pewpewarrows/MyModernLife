/* Declare a namespace for the site */
var MML = window.MML || {};

/* Create a closure to maintain scope of the '$'
   and remain compatible with other frameworks.  */
(function($) {
	
	$(function() {
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
