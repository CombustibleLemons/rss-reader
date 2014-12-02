'use strict';

/* Services */

// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('main.services', []).
  value('version', '0.1')
  .factory('FeedService', function($q){
    var feedID = 0;
    return {
      getFeedID: function() {
        return feedID;
      },
      setFeedID: function(value) {
        feedID = value;
      }
    }
  })
  .factory('APIService', function($http, $q){
    return {
      // Getter functions
      getUser: function() {
        return this.getSingle('', '/user/');
      },
      getTopic: function(topic_num) {
        return this.getSingle(topic_num, '/topics/');
      },
      getFeed: function(feed_num) {
        return this.getSingle(feed_num, '/feeds/');
      },
      getSingle : function(id, leadUrl) {
        return $http.get(leadUrl + id)
        .then(function(response) {
          if (typeof response.data === 'object') {
            return response.data;
          } else {
            // invalid response
            return $q.reject(response.data);
          }
        }, function(response) {
          // something went wrong
          return $q.reject(response.data);
        });
      },
      getTopicsByIds : function(topic_ids){
        return this.urlsDeferred(topic_ids, '/topics/', 'topic');
      },
      getFeedsByIds : function(feed_ids){
        return this.urlsDeferred(feed_ids, '/feeds/', 'feed');
      },
      getQueueFeedsByIds : function(feed_ids){
        return this.urlsDeferred(feed_ids, '/queue_feeds/', 'queue_feed');
      },
      getPostsByIds : function(post_ids){
        return this.urlsDeferred(post_ids, '/posts/', 'post');
      },
      urlsDeferred : function(ids, leadUrl, type) {
        var deferred = $q.defer();
        var urlCalls = [];
        angular.forEach(ids, function(id){
          urlCalls.push($http.get(leadUrl + id));
        });
        $q.all(urlCalls)
        .then(function(results){
          // For each result pluck out the data
          // TODO: This should probably check that the status codes are all 200s
          var ret = results.map(function(res){
            var data = res["data"];
            data["type"] = type;
            return data;
          });
          deferred.resolve(ret);
        },
        function(errors){
          deferred.reject(errors);
        },

        function(updates){
          deferred.update(updates);
        });
        return deferred.promise;
      },
      // End Getter functions

      // User functions
      getUserSettings : function() {
        var promise = $http.get("/user/settings/");
        return promise;
      },
      updateUserSettings : function(userSetttings) {
        var promise = $http.put("/user/settings/", userSetttings);
        return promise;
      },
      // End User functions

      // Topic functions
      addTopic : function(topicName) {
        var promise = $http.post('/topics/', {"name":topicName});
        return promise;
      },
      removeTopic : function(topicID) {
        var promise = $http.delete('/topics/' + topicID, {"index":topicID});
        return promise;
      },
      updateTopic : function(topic) {
        var promise = $http.put('/topics/' + topic["id"], topic);
        return promise;
      },
      // End Topic Functions

      // Search controller functions
      addFeedByUrl : function(url) {
        var promise = $http.post('/feeds/create/', {"url":url});
        return promise;
      },
      search : function(searchString) {
        var promise = $http.post('/search/', {"searchString" : searchString});
        return promise;
      },
      // End Search controller functions

      // Feed functions
      fetchPosts : function(feedID) {
        var promise = $http.get('/feeds/' + feedID + '/posts/');
        return promise;
      },
      fetchQueuedPosts : function(queueFeedID) {
        var promise = $http.get('/queue_feeds/' + queueFeedID + '/posts/');
        return promise;
      },
      updatePostsRead : function(feedID, postsRead){
        return $http.put("/feeds/" + feedID + "/posts/read", postsRead);
      },
      getPostsRead : function(feedID){
        var promise = $http.get("/feeds/" + feedID + "/posts/read");
        return promise;
      }
      // End Feed functions

        search : function(searchString) {
          var promise = $http.post('/search/', {"searchString" : searchString});
          return promise;
        },
        // Feed controller functions
        fetchPosts : function(feedID) {
          var promise = $http.get('/feeds/' + feedID + '/posts/');
          return promise;
        },
        fetchQueuedPosts : function(queueFeedID) {
          var promise = $http.get('/queue_feeds/' + queueFeedID + '/posts/');
          return promise;
        },
        updatePostsRead : function(feedID, postsRead){
          return $http.put("/feeds/" + feedID + "/posts/read", postsRead);
        },
        getPostsRead : function(feedID){
          var promise = $http.get("/feeds/" + feedID + "/posts/read");
          return promise;
        },
        getUserSettings : function() {
          var promise = $http.get("/user/settings/");
          return promise;
        },
        updateUserSettings : function(userSetttings) {
          var promise = $http.put("/user/settings/", userSetttings);
          return promise;
        },
        createQueueFeed : function(queueFeed, feedID){
          var promise = $http.post("/queue_feeds/create/" + feedID + "/", queueFeed);
          return promise;
        }

    };
  });
  