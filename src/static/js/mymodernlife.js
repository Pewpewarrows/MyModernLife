var MML = MML || {};

/* Create a closure to maintain scope of the '$',
   ensure that our global variables haven't been messed with,
   and remain compatible with other frameworks.  */
(function(window, document, $, undefined) {

    // It's rare that we'd ever want to cache AJAX responses on the browser
    // side as opposed to a server-side memcached setup for example.
    $.ajaxSetup({
        cache: false
    });

    MML.global = this;

    MML.status = null;

    MML.settings = {
        debug: false,
        static_url: '',
        media_url: ''
    };

    MML.ready = {
        common: {
            // This function will fire on every page first
            init: function() {
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
            }
        },

        blog: {
            init: function() {
            },
            view_post: function() {
                window.addthis_config = {
                    username: 'pewpewarrows',
                    data_track_clickback: true
                };

                $.getScript('http://s7.addthis.com/js/250/addthis_widget.js?domready=1');
            }
        }
    };

    /* DOM Ready */
	$(function() {
        Site.init(MML);

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

    /* Window Ready */
	$(window).bind("load", function() {
	});

})(this, this.document, jQuery);
