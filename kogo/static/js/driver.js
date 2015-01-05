$(document).ready(function(){
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