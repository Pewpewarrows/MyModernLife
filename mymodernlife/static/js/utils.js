/*
 * Utility functions, jQuery additions, and Javascript prototype extensions.
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

if (!String.prototype.startsWith) {
    String.prototype.startsWith = function(str) {
        return !this.indexOf(str);
    };
}

if (!String.prototype.endsWith) {
	String.prototype.endsWith = function(str) {
		var lastIndex = this.lastIndexOf(str);
		return (lastIndex != -1) && (lastIndex + str.length == this.length);
	};
}


/*
 * Utility functions
 */

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

function compare(a, b) {
	return ((a < b) ? -1 : ((a > b) ? 1 : 0));
}

function isFunction(x) { 
    return Object.prototype.toString.call(x) === "[object Function]";
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
 * Javascript sprintf
 * http://www.webtoolkit.info/
 * http://www.webtoolkit.info/javascript-sprintf.html
 */
sprintfWrapper = {
 
	init : function () {
 
		if (typeof arguments == "undefined") { return null; }
		if (arguments.length < 1) { return null; }
		if (typeof arguments[0] != "string") { return null; }
		if (typeof RegExp == "undefined") { return null; }
 
		var string = arguments[0];
		var exp = new RegExp(/(%([%]|(\-)?(\+|\x20)?(0)?(\d+)?(\.(\d)?)?([bcdfosxX])))/g);
		var matches = new Array();
		var strings = new Array();
		var convCount = 0;
		var stringPosStart = 0;
		var stringPosEnd = 0;
		var matchPosEnd = 0;
		var newString = '';
		var match = null;
 
		while (match = exp.exec(string)) {
			if (match[9]) { convCount += 1; }
 
			stringPosStart = matchPosEnd;
			stringPosEnd = exp.lastIndex - match[0].length;
			strings[strings.length] = string.substring(stringPosStart, stringPosEnd);
 
			matchPosEnd = exp.lastIndex;
			matches[matches.length] = {
				match: match[0],
				left: match[3] ? true : false,
				sign: match[4] || '',
				pad: match[5] || ' ',
				min: match[6] || 0,
				precision: match[8],
				code: match[9] || '%',
				negative: parseInt(arguments[convCount]) < 0 ? true : false,
				argument: String(arguments[convCount])
			};
		}
		strings[strings.length] = string.substring(matchPosEnd);
 
		if (matches.length == 0) { return string; }
		if ((arguments.length - 1) < convCount) { return null; }
 
		var code = null;
		var match = null;
		var i = null;
 
		for (i=0; i<matches.length; i++) {
 
			if (matches[i].code == '%') { substitution = '%'; }
			else if (matches[i].code == 'b') {
				matches[i].argument = String(Math.abs(parseInt(matches[i].argument)).toString(2));
				substitution = sprintfWrapper.convert(matches[i], true);
			}
			else if (matches[i].code == 'c') {
				matches[i].argument = String(String.fromCharCode(parseInt(Math.abs(parseInt(matches[i].argument)))));
				substitution = sprintfWrapper.convert(matches[i], true);
			}
			else if (matches[i].code == 'd') {
				matches[i].argument = String(Math.abs(parseInt(matches[i].argument)));
				substitution = sprintfWrapper.convert(matches[i]);
			}
			else if (matches[i].code == 'f') {
				matches[i].argument = String(Math.abs(parseFloat(matches[i].argument)).toFixed(matches[i].precision ? matches[i].precision : 6));
				substitution = sprintfWrapper.convert(matches[i]);
			}
			else if (matches[i].code == 'o') {
				matches[i].argument = String(Math.abs(parseInt(matches[i].argument)).toString(8));
				substitution = sprintfWrapper.convert(matches[i]);
			}
			else if (matches[i].code == 's') {
				matches[i].argument = matches[i].argument.substring(0, matches[i].precision ? matches[i].precision : matches[i].argument.length);
				substitution = sprintfWrapper.convert(matches[i], true);
			}
			else if (matches[i].code == 'x') {
				matches[i].argument = String(Math.abs(parseInt(matches[i].argument)).toString(16));
				substitution = sprintfWrapper.convert(matches[i]);
			}
			else if (matches[i].code == 'X') {
				matches[i].argument = String(Math.abs(parseInt(matches[i].argument)).toString(16));
				substitution = sprintfWrapper.convert(matches[i]).toUpperCase();
			}
			else {
				substitution = matches[i].match;
			}
 
			newString += strings[i];
			newString += substitution;
 
		}
		newString += strings[i];
 
		return newString;
 
	},
 
	convert : function(match, nosign){
		if (nosign) {
			match.sign = '';
		} else {
			match.sign = match.negative ? '-' : match.sign;
		}
		var l = match.min - match.argument.length + 1 - match.sign.length;
		var pad = new Array(l < 0 ? 0 : l).join(match.pad);
		if (!match.left) {
			if (match.pad == "0" || nosign) {
				return match.sign + pad + match.argument;
			} else {
				return pad + match.sign + match.argument;
			}
		} else {
			if (match.pad == "0" || nosign) {
				return match.sign + match.argument + pad.replace(/0/g, ' ');
			} else {
				return match.sign + match.argument + pad;
			}
		}
	}
};
sprintf = sprintfWrapper.init;


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
