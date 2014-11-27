'use strict';

/* Controllers */

angular.module('main.controllers', ['main.services'])
  .controller('UserController', function($scope, $rootScope, $timeout, $q, APIService) {
    // Methods
    $scope.refreshUser = function(){
      var promise = APIService.getUser().then(function(user){
        $scope.user = user;
      });
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
    // End Methods
  })
  .controller('NavigationController', function($scope, $rootScope, $timeout, APIService) {
    // Attributes
    $scope.topics = [];
    $scope.topicIds = [];
    $scope.expandedIndex = [-1];
    $scope.predicate = "";
    $scope.activeView = "feedResults"
    // End Attributes

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
    // End Event handlers

    // Attributes
    $scope.expandedIndex = [-1];
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

    $scope.saveEdits = function() {
      var listOfTopics = $(".topicHolder");

      // zero out each topic's feed list  to avoid conflicts  
      $.each( listOfTopics, function( i, val ) {
        var topic = $.parseJSON($(val).attr("data"));

        topic.feeds = [];
        APIService.updateTopic(topic).success(function(data) {
          console.log("cleared out feeds");
        }).error(function(data, status, headers, config){
          console.log(topic);
          console.log(status);
        });
      });


      // update the topics with the actual feeds
      $.each( listOfTopics, function( i, val ) {
        var topic = $.parseJSON($(val).attr("data"));

        var divList = $($(val).next("ul")[0]).find("div");
        var feedList = []
        if (divList){
          $.each( divList, function(j, stuff) {
            feedList.push(parseInt($(stuff).attr("id")));
          });
        }

        topic.feeds = feedList;

        APIService.updateTopic(topic).success(function(data) {
          console.log("success");
        }).error(function(data, status, headers, config){
          console.log(status);
        });
      });
      $scope.toggleEditMode();
    };

    $scope.toggleEditMode = function() {
      if($(".nav-sidebar").hasClass("sortable")) {
        $(".nav-sidebar").removeClass("sortable");
        $(".nav-sidebar").removeClass("ui-sortable");
        $(".nav li a[class^='removeTopic']").hide(); 
        $(".nav li a[class^='editBtn']").hide();
        $(".saveBtn").hide()

        $scope.expandedIndex = [];

        $(".nav-sidebar").nestedSortable('destroy');
        $(".toggleEdit").text("Edit");
      } else {
        $(".nav-sidebar").addClass("sortable");
        $(".nav li a[class^='removeTopic']").show(); 
        $(".nav li a[class^='editBtn']").show();
        $(".saveBtn").show()

        for (var i = 0; i <= $(".nav li").length; i++) {
            $scope.expandedIndex.push(i);
        }

        $('.sortable').nestedSortable({
            handle: 'div',
            items: 'li',
            toleranceElement: '> div',
            listType: 'ul',
            protectRoot: true,
            maxLevels: 2,
        });
        $(".toggleEdit").text("Exit edit mode");
      }
    };

    $scope.addTopic = function(topicName) {
      APIService.addTopic(topicName).success(function(data) {
        $rootScope.$broadcast("addedTopic", {
          topic: data
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
            identifier: topicID
          });
        }).error(function(data, status, headers, config){
          console.log(status);
        });
    };

    $scope.removeTopic = function(topicID) {
      APIService.removeTopic(topicID).success(function(data) {
          $rootScope.$broadcast("removedTopic", {
                identifier: topicID
          });
        }).error(function(data, status, headers, config){
          console.log(status);
        });
    };

    $scope.fetchTopics = function() {
      // Chicken and Egg problem, the UserController may not load before this class so we need to force a promise
      // Ask the UserController if it has data yet
      $scope.$parent.getTopicIds().then(function(topic_ids){
        if ($scope.topicIds != topic_ids){
          $scope.topicIds = topic_ids;
          APIService.getTopicsByIds(topic_ids).then(function(topics){
            $scope.topics = topics;
          });
        }
      });
    };

    $scope.expandTopic = function(index) {
      $scope.expandedIndex = [index];
    };
    //End Methods

    // Must be called to populate topics
    $scope.fetchTopics();
  })

  .controller('SearchController', function($scope, $rootScope, APIService) {

    // Methods
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

    $scope.search = function() {
      var testSuccess = false;
      // URL Testing (aggresively borrowed from http://stackoverflow.com/questions/17726427/check-if-url-is-valid-or-not)
      var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
      // Is the query a valid URL?
      testSuccess = regexp.test($scope.query);
      // Query is a valid URL
      if(testSuccess == true) {
        APIService.addFeedByUrl($scope.query).success(function(data) {
          if ($("#searchForm").find(".error")) {
            $("#searchForm").find(".error").remove();
          }
          console.log(data);
          $rootScope.$broadcast("showSearchResults", {searchResults: [data]});
        }).error(function(data, status, headers, config) {
          // Feed already exists in the database, add it
          if(status == 409) {
            if ($("#searchForm").find(".error")) {
              $("#searchForm").find(".error").remove();
            }
            console.log('Hey');
            console.log(data);
            console.log('ho');
            $rootScope.$broadcast("showSearchResults", {searchResults: [data]});
          }
          // URL isn't a feed
          if(status == 400) {
            testSuccess = false;
          }
        });
      } 
      // Query is not a valid URL
      if(testSuccess == false) {
        APIService.search($scope.query).success(function(data) {
          $rootScope.$broadcast("showSearchResults", {
            searchResults: data
          });
          if ($("#searchForm").find(".error")) {
            $("#searchForm").find(".error").remove();
          }
        }).error(function(data, status, headers, config){
          if (status == 409) {
            $("#searchForm").append("<div class='error'>Search failed. Please check your inputs or yell at Jawwad or Justyn</div>");
          }
        });
      }
    };
    // End methods

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
          $scope.topic = message.topic;
          $scope.feeds.push(message.feed);
        }
    });

    $scope.addFeedToTopic = function(feed) {
      // Add the feed to the local side of things
      // Is the feed in the topic already?
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

    $scope.showTopicOptions = function(feed) {
      $scope.topics = $scope.$parent.topics;
      $scope.showPopup(feed);
    };

    $scope.showPopup = function(feed) {
      $(".feedObj").attr("value", JSON.stringify(feed));
      $("#popupWrapperResults").show();
      $("#dimmer").show();
    };

    $scope.hidePopup = function() {
      $("#popupWrapperResults").hide();
      $("#dimmer").hide();
    };

    $scope.addFeedObject = function() { // formerly passed url as an argument
      var feed = $.parseJSON($(".feedObj").attr("value"));
      var topic = $.parseJSON($('input[name=selectedTopic]:checked', '#topicsForm').val());
      topic.feeds.push(feed.id);
      APIService.updateTopic(topic).success(function(data) {
          $rootScope.$broadcast("addedFeedObject", {
              topic: data,
              feed: feed
          });
          if ($("#searchForm").find(".error")) {
            $("#searchForm").find(".error").remove();
          }
          $scope.hidePopup();
          $("#topicsForm")[0].reset();
        }).error(function(data, status, headers, config){
          //if user already subscribed
          if (status == 409) {

            $(".main-content").prepend("<div class='alert flash fade-in alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span>&nbsp;You are already subscribed to that feed.</div>");
            $scope.hidePopup();            

            // fade out the alert
            window.setTimeout(function() {
              $(".flash").fadeTo(500, 0).slideUp(500, function(){
                  $(this).remove();
              });
            }, 3000);
          }
        });
    };

  })
//*/
