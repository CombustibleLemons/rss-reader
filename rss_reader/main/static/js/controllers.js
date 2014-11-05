'use strict';

/* Controllers */

angular.module('main.controllers', []).
    controller('FeedCtrl', function($scope, $http) {
      $http.get('feeds/4/posts').success(function(data) {
        $scope.posts = data;
      };
      $scope.addFeedByUrl = function(url){

      };)
    })
    .controller('PostCtrl', function($scope, $http) {
      $http.get('posts/26').success(function(data){
        $scope.detailed_post = data;
      });
    });
//*/
