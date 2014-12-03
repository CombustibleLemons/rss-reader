'use strict';

/* Controllers */

angular.module('main.controllers', ['main.services'])
  .controller('UserController', function($scope, $rootScope, $timeout, $q, APIService) {
    // Methods
    $scope.refreshUser = function(){
      var promise = APIService.getUser().then(function(user){
        $scope.user = user;
        APIService.getUserSettings().success(function(userSettings) {
          $scope.userSettings = userSettings;
        });
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
    $scope.predicate = "pubDate";
    $scope.reverse = "true";

    $scope.filterUnread = "";
    $scope.activeView = "";
    // End Attributes

    // Event handlers
    $rootScope.$on("showSearchResults", function (event, message) {
      $scope.activeView = "searchResults";
    });

    $rootScope.$on("clickFeed", function (event, message) {
      $scope.activeView = "feedResults";
      $scope.filterUnread = "";
    });

    $rootScope.$on("clickSettings", function (event, message) {
      $scope.activeView = "settingsGroups";
    });

    $rootScope.$on("clickQueueSettings", function (event, message) {
        $scope.activeView = "queueSettings";
        $("#filterUnreadLabel").hide()
    });
    // End Event handlers

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
        APIService.updateTopic(topic).error(function(data, status, headers, config){
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

        APIService.updateTopic(topic).error(function(data, status, headers, config){
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
        $(".nav li input[class^='editTopic']").hide();
        $(".nav li a[class^='editTopic']").hide();
        $(".nav li a[class^='editBtn']").hide();
        $(".removeFeed").hide()
        $(".saveBtn").hide()

        $scope.expandedIndex = [];

        $(".nav-sidebar").nestedSortable('destroy');
        $(".toggleEdit").text("Edit");
      } else {
        $(".nav-sidebar").addClass("sortable");
        $(".nav li a[class^='removeTopic']").show();
        $(".nav li a[class^='editBtn']").show();
        $(".saveBtn").show()
        $(".removeFeed").show()

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
          $scope.topicIds.push(data.id);
          $scope.topics.push(data);
          $scope.hidePopup();
          $("#popupTopic input").val('');
          
        }).error(function(data, status, headers, config){
          console.log(status);
          $(".main-content").prepend("<div class='alert flash fade-in alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span>&nbsp;"+data+"</div>");
            $scope.hidePopup();

            // fade out the alerue
            window.setTimeout(function() {
              $(".flash").fadeTo(500, 0).slideUp(500, function(){
                $(this).remove();
              });
            }, 3000);
      });
    };

    $scope.renameTopic = function(newTopicName, topic) {
      var newTopic = $.extend({}, topic);
      newTopic.name = newTopicName;
      if(newTopicName) {
        APIService.updateTopic(newTopic).success(function(data) {
            $scope.topics = $scope.topics.filter(function(topic){
              return topic.id != data.id;
            });
            $scope.topics.push(data);
          }).error(function(data, status, headers, config){
            console.log(status);
        });
      }
      $(".editTopic"+topic.id).hide();
      $(".editBtn"+topic.id).show();
    };

    $scope.removeTopic = function(topicID) {
      APIService.removeTopic(topicID).success(function(data) {
          $scope.topicIds = $scope.topicIds.filter(function(identifier){
            return identifier != topicID;
          });
          $scope.topics = $scope.topics.filter(function(topic){
            return topic.id != topicID;
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

    $scope.activeFeed = function(feedID) {
      $rootScope.$broadcast("activeFeedIs", {
        identifier: feedID
      });
    };

    $scope.activeTopic = function(topicID) {
      $rootScope.$broadcast("activeTopicIs", {
        identifier: topicID
      });
    };
    //End Methods

    // Initialization
    $scope.fetchTopics();
  })
  .controller('SearchController', function($scope, $rootScope, APIService) {
    // Attributes
    $scope.query = '';
    // End Attributes

    // Methods
    $scope.expandSettings = function() {
      $rootScope.$broadcast("clickSettings", {});
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
          $rootScope.$broadcast("showSearchResults", {searchResults: [data]});
        }).error(function(data, status, headers, config) {
          // Feed already exists in the database, add it
          if(status == 409) {
            if ($("#searchForm").find(".error")) {
              $("#searchForm").find(".error").remove();
            }
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
    // End Methods
  })
  .controller('ResultsController', function($scope, $rootScope,FeedService, APIService) {
    // Attributes
    $scope.searchResults = [];
    $scope.numResults = 0;
    $scope.topics = [];
    $scope.expandedSettingIndex = -1;
    var wpm = 300;
    var startTime;
    var endTime;
    var numClicks = 0;
    var wordCount = 501;
    // End Attributes

    // Event handlers
    $rootScope.$on("showSearchResults", function (event, message) {
        $scope.searchResults = message.searchResults;
        $scope.numResults = message.searchResults.length;
    });

    $rootScope.$on("clickSettings", function (event, message) {
      $scope.expandedPostIndex = -1;
      $("#filterUnreadLabel").hide()
    });
    // End Event handlers

    // Methods
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
      $("#popupTopic .error").html('');
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
            console.log(status);

            // fade out the alerue
            window.setTimeout(function() {
              $(".flash").fadeTo(500, 0).slideUp(500, function(){
                $(this).remove();
              });
            }, 3000);
          }
      });
    };

    $scope.expandSettingsUser = function() {
      $scope.expandedSettingIndex = 1;
    };

    $scope.expandSettingsFeed = function() {
      $scope.expandedSettingIndex = 2;
    };

    $scope.expandSettingsReading = function() {
      $scope.expandedSettingIndex = 3;
    };

    $scope.startTime = function() {
      startTime = new Date();
      document.getElementById("testArea").innerHTML = '"Words can be like X-rays, if you use them properly — they’ll go through anything. You read and you’re pierced. That’s one of the things I try to teach my students — how to write piercingly. But what on earth’s the good of being pierced by an article about a Community Sing, or the latest improvement in scent organs? Besides, can you make words really piercing — you know, like the very hardest X-rays — when you’re writing about that sort of thing? Can you say something about nothing? That’s what it finally boils down to. I try and I try …” <br>Hush!” said Bernard suddenly, and lifted a warning finger; they listened. “I believe there’s somebody at the door,” he whispered. Helmholtz got up, tiptoed across the room, and with a sharp quick movement flung the door wide open. There was, of course, nobody there.';
      numClicks = 1;
    };

    $scope.endTime = function() {
      numClicks++;
      if (numClicks == 2) {
        document.getElementById("testArea").innerHTML = "It wasn't until a number of years later, when they both wound up working at Black Sun Systems, Inc., that he put the other half of the equation together. At the time, both of them were working on avatars. He was working on bodies, she was working on faces. She was the face department, because nobody thought that faces were all that important— they were just flesh-toned busts on top of the avatars. She was just in the process of proving them all desperately wrong. But at this phase, the all-male society of bitheads that made up the power structure of Black Sun Systems said that the face problem was trivial and superficial. It was, of course, nothing more than sexism, the especially virulent type espoused by male techies who sincerely believe that they are too smart to be sexists.";
      }
      if (numClicks == 3) {
        document.getElementById("testArea").innerHTML = "Most of the members of the convent were old-fashioned Satanists, like their parents and grandparents before them. They’d been brought up to it and weren’t, when you got right down to it, particularly evil. Human beings mostly aren’t. They just get carried away by new ideas, like dressing up in jackboots and shooting people, or dressing up in white sheets and lynching people, or dressing up in tie-dye jeans and playing guitars at people. Offer people a new creed with a costume and their hearts and minds will follow. Anyway, being brought up as a Satanist tended to take the edge off it. It was something you did on Saturday nights. And the rest of the time you simply got on with life as best you could, just like everyone else. Besides, Sister Mary was a nurse and nurses, whatever their creed, are primarily nurses, which had a lot to do with wearing your watch upside down, keeping calm in emergencies, and dying for a cup of tea. She hoped someone would come soon; she’d done the important bit, now she wanted her tea.<br>It may help to understand human affairs to be clear that most of the great triumphs and tragedies of history are caused, not by people being fundamentally good or fundamentally bad, but by people being fundamentally people.";
      }
      if (numClicks == 4) {
        endTime = new Date();
        var elapsed = (endTime - startTime) / 1000;
        wpm = Math.round(wordCount / elapsed * 60);
        document.getElementById("testArea").innerHTML = "You read at " + wpm + " words per minute";
        $scope.userSettings["readtime"] = wpm;
        APIService.updateUserSettings($scope.userSettings).error(function(data, status, headers, config) {
          console.log(status_code)
        });  
      };      
    };
    // End Methods
  })
  .controller('TopicController', function($scope, $timeout, $rootScope, APIService, FeedService) {
    // Event handlers
    $rootScope.$on("addedFeedObject", function (event, message) {
        if ($scope.topic.name == message.topic.name){
          $scope.topic = message.topic;

          var flag = 0;
          for(var j =0; j<$scope.feeds.length; j++) {
            flag += ($scope.feeds[j].id == message.feed.id)
          }
          if (!flag) {
            $scope.feeds.push(message.feed);
          }
        }
    });
    // End Event handlers

    // Methods
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
    };

    $scope.fetchFeeds = function() {
      // Get the feed IDs
      var feed_ids = $scope.topic["feeds"];
      var queue_feed_ids = $scope.topic["queue_feeds"];
      // Remember, the ByIds service adds a type attribute to each object
      APIService.getFeedsByIds(feed_ids).then(function(data){
        $scope.feeds = data;
        APIService.getQueueFeedsByIds(queue_feed_ids).then(function(data){
          $scope.queue_feeds = data;
          $scope.feeds = $scope.feeds.concat($scope.queue_feeds)
        });
      });
    };

    //this just updates the feedService which the feedController pulls from
    $scope.expandFeed = function(feedID) {
      $rootScope.$broadcast("clickFeed", {
            identifier: feedID
        });
    };

    $scope.expandQueueFeed = function(feedID, queueFeedID, queuePostsRead, postsReadInQueue) {
      $rootScope.$broadcast("clickQueueFeed", {
            identifier: feedID,
            queue_identifier: queueFeedID,
            queue_posts_read: postsReadInQueue
        });
    };
    // End Methods

    // Initialization
    $scope.refreshTopic();
    $scope.fetchFeeds();
  })
  .controller('FeedController', function($scope, $rootScope, $timeout, FeedService, APIService) { //scope is an angular template, from base.html, index.html
    // Attributes
    $scope.expandedPostIndex = -1;
    $scope.feedID = -1;
    $scope.posts = [];
    // End Attributes

    // Event handlers
    $rootScope.$on("clickFeed", function (event, message) {
        $scope.feedID = message.identifier;
        $scope.fetchPosts();
        $scope.expandedPostIndex = -1;
        $("#filterUnreadLabel").show();
    });

    $rootScope.$on("clickQueueFeed", function (event, message) {
        $scope.queuePostsRead = message.queues_posts_read;
        $scope.queueFeedID = message.queue_identifier;
        $scope.fetchQueuedPosts();
        $scope.expandedPostIndex = -1;
    });

    $scope.$watch('expandedPostIndex', function(newValue, oldValue) {
      if (newValue != -1) {
          $scope.$evalAsync(function() {
            $timeout(function() {
              $scope.scrollToAnchor('post-' + newValue);
            });
          });
      }
    });
    // End Event handlers

    // Methods
    $scope.cleanPostsContent = function(data){
      // This for loop removes unnecessary line breaks
      for(var i=0; i<data.length; i++){
        //create dummy div
        var tmp = document.createElement('div');

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
      return data
    };

    $scope.fetchPosts = function() {
      APIService.fetchPosts($scope.feedID).success(function(data) {
        $scope.posts = $scope.cleanPostsContent(data);
        /* Grab the PostsRead object from the server */
        APIService.getPostsRead($scope.feedID).success(function(data){
          $scope.postsRead = data;
          angular.forEach($scope.posts, function(post){
            post.sortByUnread = data["posts"].indexOf(post.id) == -1;
            post.unread = post.sortByUnread;
          });
          /* Update the 'unread' field of the posts */
        }).error(function(data, status, headers, config){
          console.log(status);
        });
      });
    };

    $scope.fetchQueuedPosts = function() {
      APIService.fetchQueuedPosts($scope.queueFeedID).success(function(data) {
        $scope.posts = $scope.cleanPostsContent(data);
        /* Grab the QueuePostsRead from the model */
        angular.forEach($scope.queuePostsRead, function(post){
          post.sortByUnread = data["posts"].indexOf(post.id) == -1;
          post.unread = post.sortByUnread;
        });
      });
    };

    $scope.expandPost = function(post) {
      // We have to use temporary variables because ngRepeat cannot be delayed
      // on updates
      if ($scope.expandedPostIndex != -1){
        // Get the post from the previous event and mark it as read.
        $scope.posts.map(function(p){
          if (p.id == $scope.expandedPostIndex){
            p.sortByUnread = p.unread;
          }
        });
      }
      $scope.expandedPostIndex = post.id;
    };

    $scope.unexpandPost = function(){
      $scope.expandedPostIndex = -1;
    }

    $scope.closeIfExpanded = function(post) {
      if ($scope.expandedPostIndex == post.id && post.unread == true){
        $scope.unexpandPost();
      }
      post.sortByUnread = post.unread;
    };

    $scope.updatePostsRead = function(isTmp) {
      var postsReadArr = $scope.posts.reduce(function(previousValue, currentValue, index, array){
        if(!currentValue.unread){
          previousValue.push(currentValue.id);
        }
        return previousValue;
      }, new Array());
      $scope.postsRead["posts"] = postsReadArr;
      APIService.updatePostsRead($scope.feedID, $scope.postsRead)
        .error(function(data, status, headers, config){
          console.log(status);
      });
    };

    $scope.scrollToAnchor = function(aid){
      var aTag = $("a[name='"+ aid +"']");
      var navbarHeight = $(".navbar").height() + 50;
      console.log(aTag.offset().top);
      $('html,body').animate({scrollTop: aTag.offset().top - navbarHeight},'slow');
    };

    $scope.printFormattedDateString = function(dateString){
      var date = new Date(dateString);
      return date.toDateString();
    };

    $scope.printReadTimeString = function(postLength){
      var speed = $scope.userSettings["readtime"];
      var time = Math.ceil(postLength/speed);
      var finalString;
      if (time > 1){
        finalString = time + " minutes";
      }
      if (time == 1){
        finalString = time + " minute";
      }
      return finalString;
    };
	// End Methods
  })

.controller('QueueController', function($scope, $rootScope,FeedService, APIService) {
    // Attributes
    $scope.searchResults = [];
    $scope.numResults = 0;
    $scope.topics = [];
    $scope.expandedSettingIndex = -1;
    $scope.activeFeed = 0;
    $scope.activeTopic = 0;
    // End Attributes

    // Event handlers
    $rootScope.$on("clickQueueSettings", function (event, message) {
      $scope.feedID = message.identifier;
    });

    $rootScope.$on("activeFeedIs", function (event, message) {
      $scope.activeFeed = message.identifier;
    });

    $rootScope.$on("activeTopicIs", function (event, message) {
      $scope.activeTopic = message.identifier;
    });
    // End Event handlers

    // Methods
    $scope.addQueueFeedObject = function() { // formerly passed url as an argument

      var timeInterval = getSelectedText("hour-choice") + " hours, " + getSelectedText("day-choice") + " days, " + getSelectedText("month-choice") + " months ";

      var binSize = getSelectedText("post-choice");

      APIService.createQueueFeed({"postnum":binSize, "interval":timeInterval, "topic":ActiveTopic}, activeFeed);
      /*
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
        });*/
    };

    $scope.expandSettingsUser = function() {
      $scope.expandedSettingIndex = 1;
    };

    $scope.expandSettingsFeed = function() {
      $scope.expandedSettingIndex = 2;
    };

    $scope.expandSettingsReading = function() {
      $scope.expandedSettingIndex = 3;
    };

    $scope.exitSettings = function() {
      $rootScope.$broadcast("clickFeed", {});
    };

    $scope.addQueueFeedObject = function() { // formerly passed url as an argument
      var timeInterval = getSelectedText("hour-choice") + " hours, " + getSelectedText("day-choice") + " days, " + getSelectedText("month-choice") + " months ";

      var binSize = getSelectedText("post-choice");

      APIService.createQueueFeed({"postnum":binSize, "interval":timeInterval, "topic":ActiveTopic}, activeFeed);
/*
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

            // fade out the alerue
            window.setTimeout(function() {
              $(".flash").fadeTo(500, 0).slideUp(500, function(){
                $(this).remove();
              });
            }, 3000);
          }
        });*/
    };

    $scope.Range = function(start, end) {
      var result = [];
      for (var i = start; i <= end; i++) {
        result.push(i);
      }
      return result;
    };

    $scope.getSelectedText = function(elementId) {
      var elt = document.getElementById(elementId);

      if (elt.selectedIndex == -1)
        return null;

      return elt.options[elt.selectedIndex].text;
    };
    // End Methods
  });
//*/
