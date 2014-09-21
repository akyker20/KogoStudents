
$(document).ready(function(){
	allowForAjaxPostRequests();
	$("div.pickup button").click(function(){
		var pickupLoc = $(this).data("name");
		selectDropoffScreen(pickupLoc);
	});
});


var selectDropoffScreen = function(pickupLoc){
	$("div.dropoff strong.dropoff-loc").text(pickupLoc);
	$("div.pickup").fadeOut(function(){
		$("div.dropoff").fadeIn();
			$("div.dropoff span.glyphicon-arrow-left").click(function(){
				backToPickupScreen();
			});
		$("div.dropoff button").click(function(){
			var dropoffLoc = $(this).data("name");
			createRequest(pickupLoc, dropoffLoc);
		});
	});
};

var backToPickupScreen = function(){
	$("div.dropoff").fadeOut(function(){
		$("div.pickup").fadeIn();
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
		$("div.content-holder").append(html).success(function(){
			$("div.content-holder div.wait-background").fadeIn();
		});
	});
}


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