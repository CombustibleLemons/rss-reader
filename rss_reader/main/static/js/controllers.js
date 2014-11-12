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
      //$timeout(function(){$scope.refreshUser();}, $scope.refreshInterval * 1000);
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
  .controller('NavigationController', function($scope, $rootScope, $http, $timeout, APIService) {
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
      //$timeout(function(){$scope.fetchTopics();}, $scope.refreshInterval * 1000);
    };
    $scope.expandTopic = function(index) {
      $scope.expandedIndex = index
    };
    $scope.minimizeTopic = function(index) {
      // TODO: Decide if there is ANYTHING to do here or if Angular covers it all for us.
    };
    $scope.fetchTopics();
  })
  .controller('SearchController', function($scope, $rootScope, $http) {
    $scope.addFeed = function() { // formerly passed url as an argument
      $http.post('/feeds/create', {"url" : $scope.query}).success(function(data) {
          // How do we figuure out where to put it if this creates a new feed?
          $rootScope.$broadcast("addFeed", {
                feed: data,
                topicName: "Uncategorized"
          });
        }).error(function(data, status, headers, config){
          //alert(status);
        });
    };
  })
  .controller('TopicController', function($scope, $http, $timeout, $rootScope, APIService, FeedService) {
    // Dispatch addFeed message to a Topic
    $rootScope.$on("addFeed", function (event, message) {
        if ($scope.topic.name == message.topicName){
          var feed = message.feed;
          $scope.addFeedToTopic(feed);
        }
    });
    $scope.addFeedToTopic = function(feed) {
      $scope.topic["feeds"].push(feed.id);
      $scope.feeds.push(feed);
      $scope.fetchFeeds();
    };
    $scope.removeFeedFromTopic = function(feedId){
      // Remove Feed-Topic relationship from server
      $scope.topic["feeds"] = $scope.topic["feeds"].filter(function(id){
        return id != feedId;
      });
      $http.put("topics/" + $scope.topic["id"], $scope.topic).success(function(data){
        // If successful, trigger feed fetching to update the feed listing
        $scope.fetchFeeds();
      }).error(function(data, status, headers, config){
        // Log the error
        console.log(status);
        // Add the feed back since there was an error
        $scope.topic["feeds"].push(feedId);
      });;
    };
    $scope.editName = function(newName) {
      // FUNCTION YEAH
    };
    $scope.refreshTopic = function(){
      $scope.topic = $scope.$parent.topics[$scope.$parent.$index];
      //$timeout(function(){$scope.refreshTopic();}, $scope.refreshInterval * 1000);
    }
    $scope.fetchFeeds = function() {
      // Get the feed IDs
      var feed_ids = $scope.topic["feeds"];
      APIService.getFeedsByIds(feed_ids).then(function(data){
        $scope.feeds = data;
      });
      // Poll for feeds every $scope.refreshInterval so that we can get new feed info
      //$timeout(function(){$scope.fetchFeeds($scope, $http);}, $scope.refreshInterval * 1000);
    };
    //this just updates the feedService which the feedController pulls from
    $scope.expandFeed = function(feedID) {
      $rootScope.$broadcast("clickFeed", {
            identifier: feedID
        });
    };
    $scope.fetchFeeds();
    $scope.refreshTopic();
  })
  .controller('FeedController', function($scope, $http, $rootScope,FeedService) { //scope is an angular template, from base.html, index.html
    $scope.expandedPostIndex = -1;
    $rootScope.$on("clickFeed", function (event, message) {
        $scope.feedID = message.identifier;
        $scope.fetchPosts();
        $scope.expandedPostIndex = -1;
    });

    $scope.fetchPosts = function() {
      $http.get('feeds/' + $scope.feedID + "/posts").success(function(data) {

        // This for loop removes unnecessary line breaks
        // TESTED WITH NYT US FEED
        // TODO: TEST THIS WITH OTHER FEEDS
        for(var i=0; i<data.length; i++){
          //create dummy div
          var tmp = document.createElement('div');

          // console.log(data[i])

          // Populate dummy div with post content
          $(tmp).html(data[i].content);

          // Get list of line breaks
          var breakList = $(tmp).find("br");

          // If more than 5 line breaks
          if (breakList.length >= 5) {
            //remove all of them
            $(tmp).find("br").remove();
          }
          // Put cleaned post content back into data array
          data[i].content = $(tmp).html();
        }
        $scope.posts = data;
      });
    };
    $scope.expandPost = function(index) {
      // Expand the post
      $scope.expandedPostIndex = index;
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
