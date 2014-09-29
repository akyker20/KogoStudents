$(document).ready(function(){
	setInterval(function () {
		getGroups($("div.driver-select-group").data("pickup"));
	}, 10000);

	$("ul.nav li a.location").click(function(){
		getGroups($(this).data("loc"));
	});
});

var getGroups = function(location){
	$.ajax({
			type: "GET",
			url: "get_location_groups",
			data: {"location": location}
	}).success(function(html){
		var previousLocationGroups = $("div.content-holder div.driver-select-group");
		$("button.navbar-toggle").click();
		previousLocationGroups.fadeOut(function(){
			previousLocationGroups.remove();
			$("div.content-holder").append(html);
		});
	});
};