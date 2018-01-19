angular.module('myApp',[]).controller('onlineCtrl',['$scope','$http','$location', '$timeout', function($scope,$http, $location,$timeout){
	$scope.onlineHistory = false
	$scope.logs = []
	

	$scope.submitForm = function(){
		$http.get('/onlinedata/?name='+$scope.playerName+'&server='+$scope.server+'&days='+$scope.days)
		.then(function(res){
			var data = res.data.data
			var totals = []
			for(let s of data){
				var sum =0;
				for(let k of s){
					sum+=k;
				}
				totals.push({'sum':sum, 'vals':s});
			}
			console.log(totals);
			$scope.logs = totals;
			$scope.onlineHistory = true
		})
	}
}])