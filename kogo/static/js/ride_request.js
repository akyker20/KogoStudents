$(document).ready(function(){
	var pickupLoc, dropoffLoc;
	$("div.pickup button").click(function(){
		pickupLoc = $(this).text();
		$("div.dropoff strong.dropoff-loc").text(pickupLoc);
		$("div.pickup").fadeOut(function(){
			$("div.dropoff").fadeIn(function(){

			});
		})

	});
});