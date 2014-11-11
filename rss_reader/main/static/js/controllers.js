'use strict';

/* Controllers */

angular.module('main.controllers', [])
  .controller('UserController', function($scope, $rootScope, $http, UserService) {
    $scope.refreshUser = function(){
      return UserService.getUser()
    }
    $scope.getTopicIds = function(){
      var promise = $scope.refreshUser().then(function(data){
        return data["topics"];
      });
      return promise;
    };
  })
  .controller('NavigationController', function($scope, $http) {
    // Attributes
    $scope.expandedIndex;

    // Functions
    $scope.addTopic = function(topicName) {
      // THIS IS WHERE A FUNCTION GOES, DOO DAH, DOO DAH
    };
    $scope.removeTopic = function(topicName) {
      // THIS IS WHERE THE NEXT ONE GOES, DOO DAH, DOO DAH
    };
    $scope.fetchTopics = function($scope, $http) {
      $scope.$parent.getTopicIds().then(function(data){
        var topic_list = [];
        for (var i = 0; i < data.length; i++){
          $http.get('topics/' + data[i]).success(function(data){
            topic_list.push(data);
          });
        }
        $scope.topics = topic_list;
      });
    };
    $scope.expandTopic = function(index) {
      var topic = $scope.topics[index];
      if ($scope.expandedTopic != null){
        // Set currently expanded topic to unexpanded
        $('.topicButton[href="#' + $scope.expandedTopic["name"] + '"]').find(".arrow-up").removeAttr("style");
        $('.topicButton[href="#' + $scope.expandedTopic["name"] + '"]').find(".arrow-down").attr("style", "display:none");
        // Expand feed list
        $('#' + $scope.expandedTopic["name"]).css("display", "none");
      }
      // Expand topic
      $('.topicButton[href="#' + topic["name"] + '"]').find(".arrow-up").attr("style", "display:none");
      $('.topicButton[href="#' + topic["name"] + '"]').find(".arrow-down").removeAttr("style");

      // Expand feed list
      $('#' + topic["name"]).css("display", "block");

      // Set new expanded topic
      $scope.expandedTopic = topic;
    };
    $scope.minimizeTopic = function() {
      // woahhhhhh
    };
    $scope.fetchTopics($scope, $http);
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
    $scope.topic = $scope.$parent.topics[$scope.$parent.$index]; // unsure how to tie this to specific topics, this is a placeholder
    $scope.addFeedToTopic = function(url) {
      // function function function
    };
    $scope.editName = function(newName) {
      // FUNCTION YEAH
    };
    $scope.fetchFeeds = function($scope, $http) {
      // Get the feed IDs
      var feed_ids = $scope.topic["feeds"];
      var feed_list = [];
      for (var i = 0; i < feed_ids.length; i++){
        $http.get('feeds/' + feed_ids[i]).success(function(data){
          feed_list.push(data);
        });
      }
      $scope.feeds = feed_list;
    };
    $scope.expandFeed = function(feedName) {
      // expand the feed (one feed per topic in iteration one)
    };
    $scope.fetchFeeds($scope, $http);
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
