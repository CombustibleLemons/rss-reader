'use strict';

/* Controllers */

angular.module('main.controllers', [])
  .controller('UserController', function($scope, $rootScope, $http, $timeout, $q, APIService) {
    $scope.refreshInterval = 5;
    $scope.refreshUser = function(){
      // Return a function that will keep refreshing the feeds
      var promise = APIService.getUser().then(function(user){
        $scope.user = user;
      });
      $timeout(function(){$scope.refreshUser();}, $scope.refreshInterval * 1000);
      // I have no idea where this returns to when the function calls itself, and what
      // Angular does to garbage collect. But it works.
      return promise;
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
        // Return a promise that we can resolve immediately
        var deferred = $q.defer();
        deferred.resolve($scope.user["topics"]);
        return deferred.promise;
      }
    };
  })
  .controller('NavigationController', function($scope, $http, $timeout, APIService) {
    // Attributes
    $scope.expandedIndex = 0;

    // Methods
    $scope.addTopic = function(topicName) {
      // THIS IS WHERE A FUNCTION GOES, DOO DAH, DOO DAH
    };
    $scope.removeTopic = function(topicName) {
      // THIS IS WHERE THE NEXT ONE GOES, DOO DAH, DOO DAH
    };
    $scope.fetchTopics = function() {
      // Chicken and Egg problem, the UserController may not load before this class so we need to force a promise
      // Ask the UserController if it has data yet
      $scope.$parent.getTopicIds().then(function(topic_ids){
        // TODO: Compare ids to see if we need to update the topics set
        if ($scope.topicIds != topic_ids){
          $scope.topicIds = topic_ids;
          APIService.getTopicsByIds(topic_ids).then(function(topics){
            $scope.topics = topics;
          });
        }
      });
      $timeout(function(){$scope.fetchTopics();}, $scope.refreshInterval * 1000);
    };
    $scope.expandTopic = function(index) {
      $scope.expandedIndex = index
    };
    $scope.minimizeTopic = function(index) {
      // TODO: Decide if there is ANYTHING to do here or if Angular covers it all for us.
    };
    $scope.fetchTopics();
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
  .controller('TopicController', function($scope, $http, $timeout, $rootScope, APIService, FeedService) {
    $scope.addFeedToTopic = function(url) {
      // function function function
    };
    $scope.editName = function(newName) {
      // FUNCTION YEAH
    };
    $scope.refreshTopic = function(){
      $scope.topic = $scope.$parent.topics[$scope.$parent.$index];
      $timeout(function(){$scope.refreshTopic();}, $scope.refreshInterval * 1000);
    }
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
    //this just updates the feedService which the feedController pulls from
    $scope.expandFeed = function(feedID) {
      $rootScope.$broadcast("clickFeed", {
            identifier: feedID
        });
      //FeedService.setFeedID(feedID);
    };
    $scope.fetchFeeds($scope, $http);
    $scope.refreshTopic();
  })
  .controller('FeedController', function($scope, $http, $rootScope,FeedService) { //scope is an angular template, from base.html, index.html
    
    $rootScope.$on("clickFeed", function (event, message) {
        $scope.feedID = message.identifier;
        $scope.fetchPosts();
    });

    $scope.fetchPosts = function() {
      $http.get('feeds/' + $scope.feedID + "/posts").success(function(data) {
        $scope.posts = data;
      });
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
