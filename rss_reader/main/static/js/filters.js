'use strict';

/* Filters */

angular.module('main.filters', []).
  filter('interpolate', ['version', function(version) {
    return function(text) {
      return String(text).replace(/\%VERSION\%/mg, version);
    }
  }])
  .filter('filterAllUnreadPosts', function(){
    return function(posts, filterUnread){
      if (!filterUnread){
        return posts;
      }
      return posts.reduce(function(previous, current){
        if (current.unread){
          previous.push(current);
          return previous;
        }
        return previous;
      }, []);
    };
  });
