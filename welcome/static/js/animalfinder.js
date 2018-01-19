angular.module('myApp',[]).controller('animCtrl',['$scope','$http', function($scope,$http){
	$scope.onsend = function(pass){
		$http.get('/comx/attacks')
		.then(function(res){
			console.log(res);
		})
	}
}])