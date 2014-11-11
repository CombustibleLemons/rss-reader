'use strict';

/* Services */

// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('main.services', []).
  value('version', '0.1')
  .factory('UserService', function ($http, $q) {
      return {
          getUser: function() {
              // the $http API is based on the deferred/promise APIs exposed by the $q service
              // so it returns a promise for us by default
              return $http.get('users/1')
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
          }
      };
  })
  .factory('TopicService', function ($http, $q) {
      return {
          getTopic: function(topic_num) {
              // the $http API is based on the deferred/promise APIs exposed by the $q service
              // so it returns a promise for us by default
              return $http.get('topics/' + topic_num)
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
          }
      };
  })
  .factory('FeedService', function($http, $q){
    return {
      getFeedsByIds : function(feed_ids){
        var deferred = $q.defer();
        var urlCalls = [];
        angular.forEach(feed_ids, function(feed_id){
          urlCalls.push($http.get('feeds/' + feed_id));
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
      }
    };
  });
