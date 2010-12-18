/*
 * Utility objects and functions, jQuery additions, and Javascript prototype extensions.
 */

/*
 * Scope reference:
 *
 * var foo; // Global
 * bar; // Global
 *
 * function () {
 *     var baz; // Local
 *     waldo; // Global
 * }
 * 
 */

/*
 * JSDoc reference:
 * 
 * This is a generic description, with a link to a class: {@link ClassName},
 * and a link to a method: {@link ClassName#methodName}.
 * 
 * @author name
 * @version number
 * @deprecated
 * @requires OtherClassName description
 * @throws ExceptionType description
 * @see #methodName
 * @see ClassName
 * @see ClassName#methodName
 * @this ObjectTypeThisIs
 * @constructor
 * @addon
 * @member ClassName
 * @base ParentClassName
 * @param {Type} param_name description
 * @returns description_of_returned_value
 * @type ReturnType
 */

/*
 * Extensions to default Javascript prototypes, objects, and types
 */


/*
 * Utility functions and objects
 *
 * I would wrap these in an anonymous function to utilize jQuery,
 * but I'd rather keep them library-agnostic as much as possible.
 */

/*
 * http://www.viget.com/inspire/extending-paul-irishs-comprehensive-dom-ready-execution/
 *
 * Essentially, just add 'data-controller' and 'data-action' attributes to the 'body' tag
 * and define those as functions within objects here to get page-specific 'document.ready'
 * code to fire. Big thanks to Paul Irish and Jason Garber.
 *
 * Dependant on: underscore.js for prototype extending
 */
var Site = {
    exec: function(controller, action) {
        action = (action === undefined) ? 'init' : action;

        if ((controller !== '') && this[controller] && (typeof this[controller][action] === 'function')) {
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
        this.exec('common', 'finalize');
    },

    extend: function(props) {
        return _.extend(this, props);
    }
};

/*
var g_condition;
var g_callback;

function when(condition, callback) {
	if (!condition()) {
		g_condition = condition;
		g_callback = callback;
		setTimeout('when(g_condition, g_callback)', 100);
	} else {
		callback();
	}
}
*/

function compare(a, b) {
	return ((a < b) ? -1 : ((a > b) ? 1 : 0));
}

function isInt(x) {
	var y = parseInt(x);
	
	if (isNaN(y)) return false;
	
	return (x == y) && (x.toString() == y.toString());
}

// usage: log('inside coolFunc',this,arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function() {
	log.history = log.history || [];   // store logs to an array for reference
	log.history.push(arguments);
	
	if (this.console) {
		console.log(Array.prototype.slice.call(arguments));
	}
};


/*
 * jQuery mini-plugins and existing plugin extensions
 */

/*
 * Quick .data() wrapper
 * 
 * http://yehudakatz.com/2009/04/20/evented-programming-with-jquery/
 */
var $$ = function(param) {
	var node = $(param)[0];
	var id = $.data(node);
	$.cache[id] = $.cache[id] || {};
	$.cache[id].node = node;
	return $.cache[id];
};

/*
 * http://chris-barr.com/entry/disable_text_selection_with_jquery/
 * modified to be "$" safe by Dakkar Daemor [www.imaginific.com]
 */
(function($) {
	$.fn.disableTextSelect = function() {
		return this.each(function() {
			if ($.browser.mozilla) { // Firefox
					$(this).css('MozUserSelect', 'none');
				} else if ($.browser.msie) { // IE
					$(this).bind('selectstart', function() {
						return false;
					});
				} else { // Opera, etc.
					$(this).mousedown(function() {
						return false;
					});
				}
			});
	}
	$(function($) {
		// No text selection on elements with a class of 'noSelect'
		$('.noSelect').disableTextSelect();
	});
})(jQuery);
