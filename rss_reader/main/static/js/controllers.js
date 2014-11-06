'use strict';

/* Controllers */

angular.module('main.controllers', [])
    .controller('FeedCtrl', function($scope, $http) { //scope is an angular template, from base.html, index.html
      $http.get('feeds/4/posts').success(function(data) {
        $scope.posts = data; //pushes data into the scope, so now we can do things with scope.posts
      });

      /* fetchPosts()
         returns a list of feeds, all of which are feed controllers */
    })
    .controller('PostCtrl', function($scope, $http) {
      $http.get('posts/26').success(function(data){
        $scope.detailed_post = data; //pushes things to detailed post
      });

      /* Other post controller functions go here */
      //expand()
      //minimize()
      //isExpanded()

    });
//*/
