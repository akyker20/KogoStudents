$(document).ready(function(){
	if($("h1.group-number").text()==='Riding'){
		removeCancelButton();
	}
	setInterval(function () {
		getNewGroupNumber();
	}, 6000);
});

var getNewGroupNumber = function(){
	$.ajax({
		type: "GET",
		url: "get_group_number"
	}).success(function(position){
		if(position==='None'){
			window.location.reload();
		}
		// Position could be a number of 'Riding'
		else {
			if(position==='Riding'){
				removeCancelButton();
			}
			$("h1.group-number").text(position);
		}
	});
};

var removeCancelButton = function(){
	$("button.cancel-request-holder").remove();
}