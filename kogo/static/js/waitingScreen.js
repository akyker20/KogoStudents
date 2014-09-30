$(document).ready(function(){
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
			$("h1.group-number").text(position);
		}
	});
};