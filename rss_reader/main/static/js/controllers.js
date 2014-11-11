'use strict';

/* Controllers */

angular.module('main.controllers', [])
  .controller('UserController', function($scope, $rootScope, $http, $timeout, APIService) {
    $scope.refreshUser = function(){
      return APIService.getUser().then(function(user){
        $scope.user = user;
      });
    };
    $scope.getTopicIds = function(){
      if (this.user == null){
        // Force a refresh
        var promise = $scope.refreshUser().then(function(){
          return $scope.user["topics"];
        });
        return promise;
      }
      else{
        return function(){return $scope.user["topics"]};
      }
    };
  })
  .controller('NavigationController', function($scope, $http, APIService) {
    // Attributes
    $scope.expandedIndex = 0;

    // Methods
    $scope.addTopic = function(topicName) {
      // THIS IS WHERE A FUNCTION GOES, DOO DAH, DOO DAH
    };
    $scope.removeTopic = function(topicName) {
      // THIS IS WHERE THE NEXT ONE GOES, DOO DAH, DOO DAH
    };
    $scope.fetchTopics = function($scope, $http) {
      // Chicken and Egg problem, the UserController may not load before this class so we need to force a promise
      // Ask the UserController if it has data yet
      $scope.$parent.getTopicIds().then(function(topic_ids){
        APIService.getTopicsByIds(topic_ids).then(function(topics){
          $scope.topics = topics;
        });
        /* var topic_list = [];
        for (var i = 0; i < data.length; i++){
          $http.get('topics/' + data[i]).success(function(data){
            topic_list.push(data);
          });
        }*/
        //$scope.topics = topic_list;
      });
    };
    $scope.expandTopic = function(index) {
      $scope.expandedIndex = index
    };
    $scope.minimizeTopic = function(index) {
      // TODO: Decide if there is ANYTHING to do here or if Angular covers it all for us.
    };
    $scope.fetchTopics($scope, $http);
  })
  .controller('SearchController', function($scope, $http) {
    $scope.addFeed = function() { // formerly passed url as an argument
      $http.post('/feeds/create', {"url" : $scope.query}).success(function(data) {
          //alert(data);
          // The server will do the adding to the uncategorized part
        }).error(function(data, status, headers, config){
          //alert(status);
        });
    };
  })
  .controller('TopicController', function($scope, $http, $timeout, APIService) {
    $scope.topic = $scope.$parent.topics[$scope.$parent.$index];
    $scope.refreshInterval = 10;
    $scope.addFeedToTopic = function(url) {
      // function function function
    };
    $scope.editName = function(newName) {
      // FUNCTION YEAH
    };
    $scope.fetchFeeds = function($scope, $http) {
      // Get the feed IDs
      var feed_ids = $scope.topic["feeds"];
      // Accursed asyncronicity!!!
      // Ask for the feed service to fetch all the feed_ids. Returns a promise that we wait to parse (using .then)
      APIService.getFeedsByIds(feed_ids).then(function(data){
        $scope.feeds = data;
      });
      // Poll for feeds every $scope.refreshInterval so that we can get new feed info
      $timeout(function(){$scope.fetchFeeds($scope, $http);}, $scope.refreshInterval * 1000);
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
