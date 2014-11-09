'use strict';

/* Controllers */

angular.module('main.controllers', [])
  .controller('UserController', function($scope, $http) {
    $http.get('user/').success(function(data) {
      $scope.user = data;
    });
  })
  .controller('NavigationController', function($scope, $http) {
    $http.get('user/').success(function(data) {
      $scope.user = data;
    });
    $scope.addTopic = function(topicName) {
      // THIS IS WHERE A FUNCTION GOES, DOO DAH, DOO DAH
    };
    $scope.removeTopic = function(topicName) {
      // THIS IS WHERE THE NEXT ONE GOES, DOO DAH, DOO DAH
    };
    $scope.fetchTopics = function($scope, $http) {
      $http.get('topics/').success(function(data){
        $scope.topics = data;
      });
      // FUNCTION FUNCTION WHAT'S YOUR FUNCTION
    };
    $scope.expandTopic = function() {
      // wheeeeeee
    };
    $scope.minimizeTopic = function() {
      // woahhhhhh
    };
  })
  .controller('SearchController', function($scope, $http) {
    $http.get('user/').success(function(data) {
      $scope.user = data;
    });
    $scope.addFeed = function(url) {
      // function goes here to add to uncategorized
    };
  })
  .controller('TopicController', function($scope, $http) {
    $http.get('user/').success(function(data) {
      $scope.user = data;
    });
    $scope.topic = 'foo'; // unsure how to tie this to specific topics, this is a placeholder
    $scope.addFeedToTopic = function(url) {
      // function function function
    };
    $scope.editName = function(newName) {
      // FUNCTION YEAH
    };
    $scope.fetchFeeds = function() {
      // functionnnnnn
    };
    $scope.expandFeed = function(feedName) {
      // expand the feed (one feed per topic in iteration one)
    };
  })
  .controller('FeedController', function($scope, $http) { //scope is an angular template, from base.html, index.html
    $http.get('feeds/' + id + "/posts").success(function(data) {
      $scope.posts = data;
    });
    $scope.feed = 'foofeed'; // again unsure how to tie, placeholder
    $scope.fetchPosts = function() {
      // fetch the posts!
    };
  })
  .controller('PostController', function($scope, $http) {
    $http.get('posts/26').success(function(data){
      $scope.detailed_post = data; //pushes things to detailed post
    });
    $scope.expanded = false;
    $scope.expandPost = function() {
      // expands the post
    };
    $scope.collapsePost = function() {
      // collapses the post
    };
  });
//*/
