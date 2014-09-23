$(document).ready(function(){
	$("button.dropoff:not(:first)").addClass("disabled");
	$("button.dropoff:first").click(function(){
		showStartRideScreen($(this).data("id"));
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