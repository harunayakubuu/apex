
(function($){
	"use strict";
	
	$('.css-trigger').on('click', function() {
		$('.style-switcher').toggleClass('active');
	});
	
	// cOLOR cHANGING 
	var a, i = ["default-skin", "red-skin", "green-skin", "blue-skin", "yellow-skin", "purple-skin", "goodgreen-skin", "goodred-skin", "blue2-skin", "oceangreen-skin"];
	function o(e) {
		var a, o;
		return $.each(i, function(e) {
			$("body").removeClass(i[e])
		}), $("body").addClass(e), a = "skin", o = e, "undefined" != typeof Storage ? localStorage.setItem(a, o) : window.alert("Please use a modern browser to properly view this template!"), !1
	}(a = void("undefined" != typeof Storage || window.alert("Please use a modern browser to properly view this template!"))) && $.inArray(a, i) && o(a), $("[data-skin]").on("click", function(e) {
		$(this).hasClass("knob") || (e.preventDefault(), o($(this).data("skin")))
	})	
	
})(jQuery);