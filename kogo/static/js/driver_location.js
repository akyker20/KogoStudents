$(document).ready(function(){
	allowForAjaxPostRequests();
	window.setInterval(function(){
		  // Try HTML5 geolocation
  		if(navigator.geolocation) {
		    navigator.geolocation.getCurrentPosition(function(position) {
				$.ajax({
					type: "POST",
					url: "update_driver_loc",
					data: {"lat": position.coords.latitude, "long": position.coords.longitude}
				});
	    	}, function() {});
  		} else {
    		alert('Contact Austin, geolocation not working.');
  		}
	}, 5000);
});


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