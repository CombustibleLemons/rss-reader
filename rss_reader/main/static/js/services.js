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
          return this.urlsDeferred(topic_ids, '/topics/');
        },
        getFeedsByIds : function(feed_ids){
          return this.urlsDeferred(feed_ids, '/feeds/');
        },
        getPostsByIds : function(post_ids){
          return this.urlsDeferred(post_ids, '/posts/');
        },
        urlsDeferred : function(ids, leadUrl) {
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
                return res["data"];
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
        // Topic functions
        addTopic : function(topicName) {
          var promise = $http.post('/topics/', {"name":topicName});
          return promise;
        },
        renameTopic : function(newTopicName, topicID) {
          var promise = $http.put('/topics/' + topicID, {"name":newTopicName, "index":topicID});
          return promise;
        },
        removeTopic : function(topicID) {
          var promise = $http.delete('/topics/' + topicID, {"index":topicID});
          return promise;
        },
        updateTopic : function(topic) {
          var promise = $http.put('/topics/' + topic["id"], topic);
          return promise;
        }
    };
  })
