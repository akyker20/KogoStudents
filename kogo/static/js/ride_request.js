$(document).ready(function(){
	allowForAjaxPostRequests();
	$("div.pickup button").click(function(){
		var pickupLoc = $(this).data("name");
		selectDropoffScreen(pickupLoc);
	});
	$("div.content-holder").on( "click", "div.cancel-request-holder", function() {
		deleteRequest();
	});
});


var selectDropoffScreen = function(pickupLoc){
	$("div.pickup").fadeOut(function(){
		loadPossibleDestinations(pickupLoc);
	});
};

var loadPossibleDestinations = function(pickupLoc){
	$.ajax({
		type: "GET",
		url: "get_destinations/",
		data: {"pickupLoc": pickupLoc}
	}).success(function(html){
		$("div.dropoff").append(html);
		$("div.dropoff").fadeIn();
		$("div.dropoff span.glyphicon-arrow-left").click(function(){
			backToPickupScreen();
		});
		$("div.dropoff button.location-btn").unbind('click');
		$("div.dropoff button.location-btn").click(function(){
			var dropoffLoc = $(this).data("name");
			createRequest(pickupLoc, dropoffLoc);
		});
	});
}

var backToPickupScreen = function(){
	$("div.dropoff").fadeOut(function(){
		$("div.pickup").fadeIn();
		$("div.dropoff").empty();
	});
};

var createRequest = function(pickupLoc, dropoffLoc){
	$.ajax({
			type: "POST",
			url: document.URL,
			data: {
                "pickupLoc": pickupLoc,
                "dropoffLoc": dropoffLoc,
            },
		}).success(function(html) {
			showWaitingScreen(html);
	});
};

var showWaitingScreen = function(html){
	$("div.request-screens").fadeOut(function(){
		backToPickupScreen();
		$("div.content-holder").append(html);
		$("div.content-holder div.wait-background").fadeIn();
	});
};

var deleteRequest = function(){
	$.ajax({
		type: "POST",
		url: "cancel_request"
	}).success(function(){
		$("div.wait-background").remove();
		$("div.request-screens").show();
	});
};

var allowForAjaxPostRequests = function(){
    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });
};