$(document).ready(function(){
	$("button.dropoff:not(:first)").addClass("disabled");
	$("button.dropoff:first").click(function(){
		showStartRideScreen($(this).data("id"));
	});
	$("div.content-holder").on("click", "button.student", function(){
		$(this).find("span.glyphicon-ok").removeClass("hidden");
		if(allNamesAreChecked()===true){
			alert("All names are checked");
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
	$("span.glyphicon-ok").each(function(index){
		if($(this).hasClass("hidden")){
			alert("Returning false");
			return false;
		}
	});
	return true;
};