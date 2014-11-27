'use strict';

/* Controllers */

angular.module('main.controllers', ['main.services'])
  .controller('UserController', function($scope, $rootScope, $timeout, $q, APIService) {
    // Intervals will be multiplied by 1000, so these values are in seconds.
    $scope.refreshInterval = 5;
    $scope.statisticsInterval = 5;
    $scope.refreshUser = function(){
      // Return a function that will keep refreshing the feeds
      var promise = APIService.getUser().then(function(user){
        $scope.user = user;
        APIService.getUserSettings().then(function(userSettings){
          $scope.userSettings = userSettings;
          $timeout(function(){$scope.updateUserSettingsStatistics();}, $scope.statisticsInterval * 1000);
        })
      });
      //$timeout(function(){$scope.refreshUser();}, $scope.refreshInterval * 1000);
      // I have no idea where this returns to when the function calls itself, and what
      // Angular does to garbage collect. But it works.
      return promise;
    };
    $scope.updateUserSettingsStatistics = function(){
      console.log(typeof($scope.userSettings["timeOnline"]));
      $scope.userSettings["timeOnline"] = $scope.userSettings["timeOnline"] + $scope.statisticsInterval;
      APIService.updateUserSettings($scope.userSettings).success(function(data){
        // Update this data in one statistics interval
        $timeout(function(){$scope.updateUserSettingsStatistics();}, $scope.statisticsInterval * 1000);
      });
    }
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
  .controller('StatsController', function($scope, $rootScope, $timeout, APIService) {

  })
  .controller('NavigationController', function($scope, $rootScope, $timeout, APIService) {
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
    $rootScope.$on("clickStats", function (event, message) {
        $scope.activeView = "stats";
    });
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
      APIService.addTopic(topicName).success(function(data) {
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
    };

    $scope.showStats = function() {
      $rootScope.$broadcast("clickStats", {});
    };

    //End Methods
    $scope.fetchTopics();
  })

  .controller('SearchController', function($scope, $rootScope, APIService) {

    $scope.expandSettings = function() {
      $rootScope.$broadcast("clickSettings", {});
    };

    $scope.addFeed = function() { // formerly passed url as an argument
      APIService.addFeedByUrl($scope.query).success(function(data) {
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

    $scope.search = function() { // formerly passed url as an argument
      APIService.search($scope.query).success(function(data) {
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
    };
  })
  .controller('TopicController', function($scope, $timeout, $rootScope, APIService, FeedService) {
    // Dispatch addFeed message to a Topic
    $rootScope.$on("addedFeed", function (event, message) {
        if ($scope.topic.name == message.topicName){
          $scope.addFeedToTopic(message.feed);
        }
    });

    $rootScope.$on("addedFeedObject", function (event, message) {
        if ($scope.topic.name == message.topic.name){
          //somehow refresh the topics
          $scope.topic = message.topic;
          //$scope.fetchFeeds();
        }
    });

    $scope.addFeedToTopic = function(feed) {
      // Add the feed to the local side of things
      if ($.inArray( feed.id, $scope.topic["feeds"] ) == -1) {
        $scope.topic["feeds"].push(feed.id);
        $scope.feeds.push(feed);
      } else {
        $("#searchForm").append("<div class='error'>You are already subscribed to that feed</div>");
      }
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
  .controller('FeedController', function($scope, $rootScope,FeedService, APIService) { //scope is an angular template, from base.html, index.html
    $scope.expandedPostIndex = -1;

    $rootScope.$on("clickFeed", function (event, message) {
        $scope.feedID = message.identifier;
        $scope.fetchPosts();
        $scope.expandedPostIndex = -1;
    });

    $scope.fetchPosts = function() {
      APIService.fetchPosts($scope.feedID).success(function(data) {
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
        /* Grab the PostsRead object from the server */
        APIService.getPostsRead($scope.feedID).success(function(data){
          console.log(data);
          $scope.postsRead = data;
          angular.forEach($scope.posts, function(post){
            if (data["posts"].indexOf(post.id) == -1){
              post.unread = true;
            }
            else{
              post.unread = false;
            }
          });
          /* Update the 'unread' field of the posts */
        }).error(function(data, status, headers, config){
          console.log(status);
        });
      });

    };
    $scope.expandPost = function(index) {
      // Expand the post
      $scope.expandedPostIndex = index;
    };
    $scope.clickPostHeader = function(post) {
      if(post.unread){
        post.unread = false;
        $scope.updatePostsRead();
      }
    }
    $scope.updatePostsRead = function() {
      var postsReadArr = $scope.posts.reduce(function(previousValue, currentValue, index, array){
        if(!currentValue.unread){
          previousValue.push(currentValue.id);
        }
        return previousValue;
      }, new Array());
      $scope.postsRead["posts"] = postsReadArr;
      APIService.updatePostsRead($scope.feedID, $scope.postsRead).success(function(data){
        console.log("Success");
      }).error(function(data, status, headers, config){
        console.log(status);
      });
    }
  })
  .controller('ResultsController', function($scope, $rootScope,FeedService, APIService) { //scope is an angular template, from base.html, index.html
    $scope.searchResults = [];
    $scope.numResults = 0;
    $scope.topics = [];
    $rootScope.$on("showSearchResults", function (event, message) {
        console.log(message.searchResults);
        $scope.searchResults = message.searchResults;
        $scope.numResults = message.searchResults.length;
    });

    $scope.showTopicOptions = function(feedID) {
      $scope.topics = $scope.$parent.topics;
      $scope.showPopup(feedID);
    };

    $scope.showPopup = function(feedID) {
      $(".feedID").attr("value", feedID);
      $("#popupWrapperResults").show();
      $("#dimmer").show();
    };

    $scope.hidePopup = function() {
      $("#popupWrapperResults").hide();
      $("#dimmer").hide();
    };

    $scope.addFeedObject = function() { // formerly passed url as an argument
      var feedID = parseInt($(".feedID").attr("value"));
      var topic = $.parseJSON($('input[name=selectedTopic]:checked', '#topicsForm').val());
      topic.feeds.push(feedID);
      APIService.updateTopic(topic).success(function(data) {
          $rootScope.$broadcast("addedFeedObject", {
              topic: data,
          });
          if ($("#searchForm").find(".error")) {
            $("#searchForm").find(".error").remove();
          }
          $scope.hidePopup();
          $("#topicsForm")[0].reset();
        }).error(function(data, status, headers, config){
          //if user already subscribed
          if (status == 409) {
            $("#topicsForm").append("<div class='error'>You are already subscribed to that feed</div>");
          }
        });
    };

  })
//*/
