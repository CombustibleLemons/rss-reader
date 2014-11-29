'use strict';

/* Filters */

angular.module('main.filters', []).
  filter('interpolate', ['version', function(version) {
    return function(text) {
      return String(text).replace(/\%VERSION\%/mg, version);
    }
  }])
  .filter('unreadSort', function(){
    return function(post, scope){
      console.log(post.pubDate);
      // If post is expanded, keep it where it is.
      return scope.expandedPostIndex == post.id;
    };
  })
  ;
