$(document).ready(function(){
	setInterval(function () {
		getNewGroupNumber();
	}, 10000);
});

var getNewGroupNumber = function(){
	$.ajax({
		type: "GET",
		url: "get_group_number"
	}).success(function(number){
		$("h1.group-number").text(number);
	});
};