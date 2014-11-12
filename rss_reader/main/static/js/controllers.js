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
    $scope.expandedPostIndex = 0;
    $rootScope.$on("clickFeed", function (event, message) {
        $scope.feedID = message.identifier;
        $scope.fetchPosts();
    });

    $scope.fetchPosts = function() {
      $http.get('feeds/' + $scope.feedID + "/posts").success(function(data) {

        //this for loop removes unnecessary line breaks
        // TESTED WITH NYT US FEED
        // TEST THIS WITH OTHER FEEDS
        for(var i=0; i<data.length; i++){
          //create dummy div
          var tmp = document.createElement('div');
          
          console.log(data[i])

          //populate dummy div with post content
          $(tmp).html(data[i].content);
          
          //get list of line breaks
          var breakList = $(tmp).find("br");

          //if more than 5 line breaks
          if (breakList.length >= 5) {
            //remove all of them
            $(tmp).find("br").remove();
          }
          //put cleaned post content back into data array
          data[i].content = $(tmp).html();
        }
        $scope.posts = data;
      });
    };
    $scope.expandPost = function(index) {
      $scope.expandedPostIndex = index;
      console.log($scope.expandedPostIndex);
      // expands the post
    };
  })
  .controller('PostController', function($scope, $http) {
    $scope.expandPost = function(index) {
      // expands the post
    };
    $scope.collapsePost = function() {
      // collapses the post
    };
  });
//*/
