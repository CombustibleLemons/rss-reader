'use strict';

/* Controllers */

angular.module('main.controllers', [])
  .controller('UserController', function($scope, $http) {
    $http.get('user/').success(function(data) {
      $scope.user = data;
    });
    $scope.addTopic = function(topicName) {
      // THIS IS WHERE A FUNCTION GOES, DOO DAH, DOO DAH
    };
  })
    .controller('FeedController', function(id, $scope, $http) { //scope is an angular template, from base.html, index.html
      
      $http.get('feeds/' + id + "/posts").success(function(data) {
        $scope.posts = data;
      };
      $scope.addFeedByUrl = function(url){

      };)
    })
    .controller('PostController', function($scope, $http) {
      $http.get('posts/26').success(function(data){
        $scope.detailed_post = data; //pushes things to detailed post
      });

      /* Other post controller functions go here */
      //expand()
      //minimize()
      //isExpanded()

    });
//*/
