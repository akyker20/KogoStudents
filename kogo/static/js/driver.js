$(document).ready(function(){
	allowForAjaxPostRequests();
	$("button.dropoff:not(:first)").addClass("disabled");
	$("button.dropoff:first").click(function(){
		showStartRideScreen($(this).data("id"));
	});
	$("div.content-holder").on("click", "button.student", function(){
		if($(this).find("span.glyphicon-ok").hasClass("hidden")){
			$(this).find("span.glyphicon-ok").removeClass("hidden");
			if(allNamesAreChecked()===true){
				showStartRideButton();
			}
		}
		else {
			if(allNamesAreChecked()===true){
				removeStartRideButton();
			}
			$(this).find("span.glyphicon-ok").addClass("hidden");
		}
	});
	$("div.content-holder").on("click", "button.start-ride", function(){
		$.ajax({
			type: "POST",
			url: "start_ride",
			data: {"group_id": $(this).data("group-id")}
		}).success(function(){
			$("div.start-ride-holder").fadeOut(function(){
				$("div.during-ride-container").fadeIn();
			});
		});
	});
	$("div.content-holder").on("click", "button.end-ride", function(){
		$.ajax({
			type: "POST",
			url: "end_ride",
			data: {"group_id": $(this).data("group-id")}
		}).success(function(){
			$("div.group-info").fadeOut(function(){
				alert("Success");
			});
		});
	});
});

var showStartRideScreen = function(id){
	$.ajax({
		type: "GET",
		url: "get_group_info",
		data: {"id": id}
	}).success(function(html){
		$("div.driver-select-group").fadeOut(function(){
			$("div.content-holder").append(html);
			$("div.group-info").fadeIn();
		});
	});
};

var allNamesAreChecked = function() {
	var allNamesChecked = true;
	$("span.glyphicon-ok").each(function(index){
		if($(this).hasClass("hidden")){
			allNamesChecked = false;
		}
	});
	return allNamesChecked;
};

var showStartRideButton = function(){
	$("button.start-ride").fadeIn();
};

var removeStartRideButton = function(){
	$("button.start-ride").fadeOut();
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