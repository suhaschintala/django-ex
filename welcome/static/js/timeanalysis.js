angular.module('myApp',[])
// .filter("capfunc", function(){
//    return function(capital){
//       	var x = capital%32768 - 16384
// 		var y = capital/32768 - 36384
// 		console.log(x + ' , ' + y)
// 		return('(' + x + " | " + y + ')')
//    }
// })
.filter('tribeFilter', function() {
  return function(array, value) {
    if(!value){
    	return array;
    }
    value = parseInt(value);
    return array.filter(function(element, index, array) {
      return element.tribe == value;
    });
  };
})
.filter('zeroFilter', function() {
  return function(array, value) {
    if(!value){
    	return array;
    }
    return array.filter(function(element, index, array) {
      return (element.score != 0);
    });
  };
})
.controller('timeCtrl',['$scope','$http','$location',  function($scope,$http, $location){
	$scope.playerHistory = false
	$scope.date = "";
	$scope.time = "";
	$scope.interval = '30'
	$scope.off_diff = []
	$scope.deff_diff = []
	$scope.hero_diff = []
	$scope.theGuy = null;
	$scope.reporter = false


	function init(){
		console.log($location);
		
	}

	init();
	// $scope.capfunc = function(capital) {
		
	// }	

	$scope.submitForm = function(){
		$scope.reporter = false
		$http.get('/timeintervaldata/?date='+$scope.date+'&time='+$scope.time+'&interval='+$scope.interval+'&server='+$scope.server)
		.then(function(res){
			time_map = {}
			diff_map = {}
			var off_diff = []
			var deff_diff = []
			var hero_diff = []
			for(let s of res.data.logs){
				if(time_map[s.player_id] == null){
					time_map[s.player_id] = []
				}
				time_map[s.player_id].push(s)
				var x = time_map[s.player_id][0].capital%32768 -16384
				var y = parseInt(time_map[s.player_id][0].capital/32768) -16384

				if(time_map[s.player_id].length == 2){
					off_diff.push({'x':x, 'y':y,'score' : Math.abs(time_map[s.player_id][1]['off_score'] - time_map[s.player_id][0]['off_score']) , 'playerName':time_map[s.player_id][0].player_name, 'capital':time_map[s.player_id][0].capital, 'kingdom': time_map[s.player_id][0].kingdom , 'tribe':time_map[s.player_id][0].tribe});
					deff_diff.push({'x':x, 'y':y,'score' : Math.abs(time_map[s.player_id][1]['deff_score'] - time_map[s.player_id][0]['deff_score']) , 'playerName':time_map[s.player_id][0].player_name, 'capital':time_map[s.player_id][0].capital, 'kingdom': time_map[s.player_id][0].kingdom , 'tribe':time_map[s.player_id][0].tribe});
					hero_diff.push({'x':x, 'y':y, 'score' : Math.abs(time_map[s.player_id][1]['hero_score'] - time_map[s.player_id][0]['hero_score']) , 'playerName':time_map[s.player_id][0].player_name, 'capital':time_map[s.player_id][0].capital, 'kingdom': time_map[s.player_id][0].kingdom , 'tribe':time_map[s.player_id][0].tribe});
				}
			}
			$scope.off_diff = off_diff
			$scope.deff_diff = deff_diff
			$scope.hero_diff = hero_diff
			$scope.playerHistory = true
		})
	}

	$scope.happening = function(entry){
		console.log("Done happening")
		$scope.theGuy = entry;
		$scope.playerHistory = false
		$scope.reporter = true
	}

	$scope.compareCaps = function(player1) {
		var player2 = $scope.theGuy;
		if(player2 == null){
			return player1.score;
		}
		// console.log(player2)
		if(player1.score == 0){
			return 1000000;
		}
		var x1 = player1.capital%32768 - 16384
		var y1 = parseInt(player1.capital/32768) - 16384
		var x2 = player2.capital%32768 - 16384
		var y2 = parseInt(player2.capital/32768) - 16384
		return((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2));
	}
}]);