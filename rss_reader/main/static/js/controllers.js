'use strict';

/* Controllers */

angular.module('main.controllers', ['main.services'])
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

    $scope.expandSettingsPart = function(index) {
      // Expand the post
      $scope.expandedSettingIndex = index;
    };
  })
  .controller('NavigationController', function($scope, $rootScope, $http, $timeout, APIService) {
    $scope.topics = [];
    $scope.topicIds = [];

    // Event handlers

    // when addedTopic event is fired
    $rootScope.$on("addedTopic", function (event, message) {
      $scope.topicIds.push(message.topic.id);
      $scope.topics.push(message.topic);
    });

    // when removedTopic event is fired
    $rootScope.$on("removedTopic", function (event, message) {
      $scope.topicIds = $scope.topicIds.filter(function(topicId){
        return topicId != message.identifier;
      });
      $scope.topics = $scope.topics.filter(function(topic){
        return topic.id != message.identifier;
      });
    });

    //when renamedTopic event is fired
    $rootScope.$on("renamedTopic", function (event, message) {
      $scope.topics = $scope.topics.filter(function(topic){
        return topic.id != message.identifier;
      });
      $scope.topics.push(message.topic);
    });

    $rootScope.$on("showSearchResults", function (event, message) {
        $scope.activeView = "searchResults";
    });

    $rootScope.$on("clickFeed", function (event, message) {
        $scope.activeView = "feedResults";
    });
    
    $rootScope.$on("clickSettings", function (event, message) {
        $scope.activeView = "settingsGroups";

    });
    
    $rootScope.$on("search", function (event, message) {
      $scope.activeView = "searchResult";
    })

    // End Event handlers

    // Attributes
    $scope.expandedIndex = -1;
    $scope.predicate = "";
    $scope.activeView = "feedResults"
    // End Attributes

    // Methods
    $scope.showPopup = function() {
      $("#popupWrapper").show();
      $("#dimmer").show();
    };

    $scope.hidePopup = function() {
      $("#popupWrapper").hide();
      $("#dimmer").hide();
    };

    $scope.toggleEdit = function(topicID) {
      $(".editTopic"+topicID).show();
      $(".editBtn"+topicID).hide();
    };

    $scope.addTopic = function(topicName) {
      var promise = APIService.addTopic(topicName);
      promise.success(function(data) {
        $rootScope.$broadcast("addedTopic", {
          topic: data,
        });
        $scope.hidePopup();
        $("#popupTopic input").val('');
      }).error(function(data, status, headers, config){
        console.log(status);
      });
    };

    $scope.renameTopic = function(newTopicName, topicID) {
      APIService.renameTopic(newTopicName, topicID).success(function(data) {
          $rootScope.$broadcast("renamedTopic", {
            topic: data,
            identifier: topicID,
          });
        }).error(function(data, status, headers, config){
          console.log(status);
        });
    };

    $scope.removeTopic = function(topicID) {
      APIService.removeTopic(topicID).success(function(data) {
          $rootScope.$broadcast("removedTopic", {
                identifier: topicID,
          });
        }).error(function(data, status, headers, config){
          console.log(status);
        });
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
      $scope.expandedIndex = index;
    }
//searchID does not currently exist, need to fix
    $scope.expandSearch = function(index) {
      $rootScope.$broadcast("search", {
            identifier: index
        });
    };

    $scope.expandSettings = function() {
      $rootScope.$broadcast("clickSettings", {
       
        });
    };

    //End Methods
    $scope.fetchTopics();
  })

 


  .controller('TopicController', function($scope, $http, $timeout, $rootScope, APIService, FeedService) {
    // Dispatch addFeed message to a Topic
    $rootScope.$on("addedFeed", function (event, message) {
        if ($scope.topic.name == message.topicName){
          $scope.addFeedToTopic(message.feed);
        }
    });

    $scope.addFeedToTopic = function(feed) {
      $scope.topic["feeds"].push(feed.id);
      $scope.feeds.push(feed);
      APIService.updateTopic($scope.topic).error(function(data, status, headers, config) {
          // Log the error
          console.log(status);
          // Try again
          $scope.addFeedToTopic(feed);
        });
    };
    $scope.removeFeedFromTopic = function(feedId){
      // Remove Feed-Topic relationship from server
      $scope.topic["feeds"] = $scope.topic["feeds"].filter(function(id){
        return id != feedId;
      });
      APIService.updateTopic($scope.topic).success(function(data) {
        $scope.feeds = $scope.feeds.filter(function(feed) {
          return feed["id"] != feedId;
        });
      }).error(function(data, status, headers, config){
          // Log the error
          console.log(status);
          // Add the feed back since there was an error
          $scope.topic["feeds"].push(feedId);
      });
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
    $scope.refreshTopic();
    $scope.fetchFeeds();
  })
/*
.controller('SettingsController', function($scope, $http, $root, FeedService) {
      $scope.expandedSettingIndex = -1;

      $rootScope.$on("clickSetting", function (event, message) {
              $scope.expandedPostIndex = -1;
          });

      
      $scope.expandSettingsPart1 = function() {
      // Expand the post
      $scope.expandedSettingIndex = 1;
    };

      $scope.expandSettingsPart2 = function() {
        $scope.expandedSettingIndex = 2;
      };

      $scope.expandSettingsPart3 = function() {
        $scope.expandedSettingIndex = 3;
      };
  })*/

  .controller('ResultsController', function($scope, $http, $rootScope) { //scope is an angular template, from base.html, index.html
    $scope.searchResults = [];

    $rootScope.$on("showSearchResults", function (event, message) {
        $scope.searchResults = message.searchResults;
    });

    $rootScope.$on("search", function (event, message) {
    });


    $scope.addFeed = function() { // formerly passed url as an argument
      $http.post('/feeds/create', {"url" : $scope.query}).success(function(data) {
          // How do we figure out where to put it if this creates a new feed?
          $rootScope.$broadcast("addedFeed", {
                feed: data,
                topicName: "Uncategorized"
          });
          if ($("#searchForm").find(".error")) {
            $("#searchForm").find(".error").remove();
          }
        }).error(function(data, status, headers, config){
          if (status == 409) {
            $("#searchForm").append("<div class='error'>You are already subscribed to that feed</div>");
          }
        });
    };

    $scope.search = function(index) { // formerly passed url as an argument
      $http.post('/search/', {"searchString" : $scope.query}).success(function(data) {
          // How do we figure out where to put it if this creates a new feed?
          $rootScope.$broadcast("showSearchResults", {
                searchResults: data,
          });
          if ($("#searchForm").find(".error")) {
            $("#searchForm").find(".error").remove();
          }
        }).error(function(data, status, headers, config){
          if (status == 409) {
            $("#searchForm").append("<div class='error'>Search failed. Please check your inputs or yell at Jawwad or Justyn</div>");
          }
        });
        $scope.showingResults = index;
    };

    $scope.showQueuePopup = function() {
      $("#popupQueueWrapper").show();
      $("#dimmer").show();
    };

    $scope.hidePopup = function() {
      $("#popupQueueWrapper").hide();
      $("#dimmer").hide();
    };

      $scope.expandedSettingIndex = -1;

      $rootScope.$on("clickSetting", function (event, message) {
              $scope.expandedPostIndex = -1;
          });

      
      $scope.expandSettingsUser = function() {
      // Expand the post
      $scope.expandedSettingIndex = 1;
    };

      $scope.expandSettingsFeed = function() {
        $scope.expandedSettingIndex = 2;
      };

      $scope.expandSettingsReading = function() {
        $scope.expandedSettingIndex = 3;
      };
    
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





 
//*/
