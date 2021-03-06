

var somabot = angular.module('Somabot', ['ngMaterial', 'ngRoute']);

/*
somabot.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .dark();
});
*/

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

somabot.controller('RecipeCtrl', ['$scope', '$http', function ($scope, $http) {


$http.get('/get_drinks').then(
  function successCall(response) {
    console.log(response.data);
    $scope.drinks = response.data;
  },
  function errorCall() {
    console.log("Error in call");
    $scope.drinks = [];
  });

  $scope.make_drink = function(name) {
    //
    $scope.pumping = true;

    $http.get('/make_drink', {params: {"name": name}}).then(
      function successCall(response) {
        $scope.pumping = false;
        console.log(response.data);
      },
      function errorCall() {
        $scope.pumping = false;
        console.log("Error in call");
      });
  };


}
]);

somabot.controller('SettingsCtrl', ['$scope', '$http', function($scope, $http) {

$scope.setting = {}

//$scope.ingredients = [1, 2 , 3 , 4 , 5 ];
$http.get('/all_ingredients').then(
  function successCall(response) {
    $scope.ingredients = response.data['ingredients'];
  },
  function errorCall() {
    $scope.ingredients = [];
  });

$http.get('/current_settings').then(
    function successCall(response) {
      var ings = response.data['ingredients'];
      $scope.setting.pump1 = ings[0];
      $scope.setting.pump2 = ings[1];
      $scope.setting.pump3 = ings[2];
      $scope.setting.pump4 = ings[3];
      $scope.setting.pump5 = ings[4];
      $scope.setting.flow_rate = response.data['flow_rate'];
    },
    function errorCall() {
      $scope.ingredients = [];
    });


$scope.save_settings = function(post) {
  data = {};
  data["pump1"] = $scope.setting.pump1 || "";
  data["pump2"] = $scope.setting.pump2 || "";
  data["pump3"] = $scope.setting.pump3 || "";
  data["pump4"] = $scope.setting.pump4 || "";
  data["pump5"] = $scope.setting.pump5 || "";
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
