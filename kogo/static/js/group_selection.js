$(document).ready(function(){
	$("button.navbar-toggle").addClass("collapsed");
	startPollingForGroups();	
	$("button.navbar-toggle").click(function(){
		if($(this).hasClass("collapsed")){
			stopPollingForGroups();		
		}
		else {
			startPollingForGroups();	
		}
	});

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
		if(!$("button.navbar-toggle").hasClass("collapsed")){
			$("button.navbar-toggle").click();
		}
		//If html is different from the current html
		if(previousLocationGroups.text() != $([$.parseHTML(html)[0]]).text()){
			previousLocationGroups.fadeOut(function(){
				previousLocationGroups.remove();
				$("div.content-holder").append(html);
			});
		}
	});
};

var myInterval = null;

var startPollingForGroups = function() {
	stopPollingForGroups();
	myInterval = setInterval(function () {
			getGroups($("div.driver-select-group").data("pickup"));
	}, 6000);
}

var stopPollingForGroups = function() {
	clearInterval(myInterval);
}