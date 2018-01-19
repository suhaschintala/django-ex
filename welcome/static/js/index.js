angular.module('myApp',[]).controller('myCtrl',['$scope','$http','$window', function($scope,$http, $window){
	$scope.selectServer = true
	$scope.animals = false
	$scope.cropper = false
	$scope.showOld = false
	$scope.lines = []
	$scope.server = ''
	$scope.mode = ''
	$scope.coord = {'x':"0", 'y':"0"}
	$scope.onsend = function(pass){
		$http.get('/comx/attacks')
		.then(function(res){
			console.log(res);
		})
	}
	
	$scope.selectAction = function(server, mode){
		$scope.server = server
		$scope.mode = mode
		if (mode == 'animal'){
			$scope.animals = true
		}
		
		if (mode == 'attacks'){
			$scope.attacks  = true
		}
		if (mode == 'cropper'){
			$scope.cropper  = true
		}
	}

	$scope.animalSearch = function(coords){
		$window.location.href = '/animalsearch/?server='+$scope.server+'&x='+coords.x+'&y='+coords.y
		// $window.location.reload()
		// $http.get('/animalsearch/?server='+$scope.server+'&x='+coords.x+'&y='+coords.y)
		// .then(function(res){
		// 	$scope.lines = res.data.list
		// 	console.log($scope.lines)
		// 	$scope.selectServer = false
		// 	$scope.animals = true
		// })
	}
	$scope.cropperSearch = function(coords){
		$window.location.href = '/croppersearch/?server='+$scope.server+'&x='+coords.x+'&y='+coords.y
		// $window.location.reload()
		// $http.get('/animalsearch/?server='+$scope.server+'&x='+coords.x+'&y='+coords.y)
		// .then(function(res){
		// 	$scope.lines = res.data.list
		// 	console.log($scope.lines)
		// 	$scope.selectServer = false
		// 	$scope.animals = true
		// })
	}
}])