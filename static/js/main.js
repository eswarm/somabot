

var somabot = angular.module('Somabot', ['ngMaterial', 'ngRoute']);
somabot.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/settings', {
        templateUrl: '/static/ngtemplates/settings.html',
        controller: 'SettingsCtrl'
      }).
      when('/', {
        templateUrl: '/static/ngtemplates/recipes.html',
        controller: 'RecipeCtrl'
      }).
      otherwise({
        redirectTo: '/'
      });
  }]);

somabot.controller('RecipeCtrl', function ($scope) {

$scope.recipes = [1, 2 , 3 , 4 , 5 , 6 , 7 ];

});

somabot.controller('SettingsCtrl', ['$scope', '$http', function($scope, $http) {

//$scope.ingredients = [1, 2 , 3 , 4 , 5 ];
$http.get('/all_ingredients').then(
  function successCall(response) {
    $scope.ingredients = response.data['ingredients'];
  },
  function errorCall() {
    $scope.ingredients = [];
  });

$scope.save_settings = function(post) {
  data = {};
  data["pump1"] = $scope.setting.pump1 | "";
  data["pump2"] = $scope.setting.pump2 | "";
  data["pump3"] = $scope.setting.pump3 | "";
  data["pump4"] = $scope.setting.pump4 | "";
  data["pump5"] = $scope.setting.pump5 | "";
  data["flow_rate"] = $scope.setting.flow_rate;

  $http.post("/save_settings", data).then(
    function successCall(response) {
      console.log("settings saved");
    },
    function errorCall() {
      console.log("error in post");
    }
  );

};

}]);
