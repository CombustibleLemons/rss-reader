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
  });
