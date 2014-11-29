'use strict';

/* Filters */

angular.module('main.filters', []).
  filter('interpolate', ['version', function(version) {
    return function(text) {
      return String(text).replace(/\%VERSION\%/mg, version);
    }
  }])
  .filter('unreadSort', function(){
    return function(post){
      date = new Date(post.pubDate);
      
      // If post is expanded, keep it where it is.
      return post ? post.id : 0;
    };
  })
  ;
