$(document).ready(function(){
	$("ul.nav li a.location").click(function(){
		$.ajax({
			type: "GET",
			url: "get_location_groups",
			data: {"location": $(this).data("loc")}
		}).success(function(html){
			var previousLocationGroups = $("div.content-holder div.driver-select-group");
			$("button.navbar-toggle").click();
			previousLocationGroups.fadeOut(function(){
				previousLocationGroups.remove();
				$("div.content-holder").append(html);
			});
		});
	});
});