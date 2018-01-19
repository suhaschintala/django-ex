angular.module('myApp',[]).controller('playerCtrl',['$scope','$http','$location', '$timeout', function($scope,$http, $location,$timeout){
	$scope.playerHistory = false
	$scope.playerId = "";
	$scope.logs = []
	$scope.chosen1 = null
	$scope.chosen2 = null
	console.log("POPOP  : " + $location.path());
	
	$timeout(onSetup, 500)

	function onSetup() {
		if($location.path().indexOf("name") != -1){
			console.log("POPOP")
			var paths = $location.path().split('?')[1].split('&')
			for(let each of paths){
				if(each.indexOf('name')!=-1){
					$scope.playerName = each.split('=')[1]
				}
				if(each.indexOf('server')!=-1){
					$scope.server = each.split('=')[1]
				}
			}
			// $scope.submitForm()
		}
	}
	

	$scope.submitForm = function(){
		$http.get('/playerdata/?name='+$scope.playerName+'&server='+$scope.server)
		.then(function(res){
			
			for(let s of res.data.logs){
				s.orig_timestamp = s.timestamp + "";
				var dateObj = (new Date(Date.parse(s.timestamp)))
				s.timestamp = dateObj.toDateString() + ' ' + dateObj.toTimeString()

			}
			$scope.logs = res.data.logs
			console.log($scope.logs)
			$scope.playerHistory = true
		})
	}
	$scope.choose = function(log){
		if(!$scope.chosen1){
			$scope.chosen1 = log
		}
		$scope.chosen2 = log

	}
	$scope.unchoose = function(log){
		if($scope.chosen1){
			$scope.chosen1 = null;
		}
	}
}])