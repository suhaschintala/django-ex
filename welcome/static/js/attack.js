angular.module('myApp',[]).controller('attackCtrl',['$scope','$http','$location', '$timeout', function($scope,$http, $location,$timeout){
	$scope.isData = false
	$scope.logs = []
	

	$scope.submitForm = function(){
		$http.get('/attack_analyzer/?session='+$scope.session+'&server='+$scope.server)
		.then(function(res){
			var data = res.data.data
			var totals = []
			for(let s of data){
				s.speed = 14;
				console.log(s.time_reached)
				var dateObj = (new Date(Date.parse(s.time_reached)))
				s.time_arrived = dateObj.toDateString() + ' ' + dateObj.toTimeString()
				totals.push(s);
			}
			console.log(totals);
			$scope.logs = totals;
			$scope.isData = true
		})
	}
}])
.filter('time_sent', function(){
	return function (log){
		var time_arrived = (new Date(Date.parse(log.time_reached)))
		var seconds = (log.distance / log.speed)* 60 * 60;
		time_arrived.setTime(time_arrived.getTime() - seconds);
		return time_arrived.toString();
	}
})