'use strict';

/* jasmine specs for controller tests */
describe("User controllers", function() {
    beforeEach(module("main.controllers"));

    var userScope, httpBackend, userController;
    beforeEach(inject(function($controller, $rootScope, $httpBackend, $timeout, $q, APIService) {
        httpBackend = $httpBackend;

        userScope = $rootScope.$new();
        userController = $controller('UserController', {$scope: userScope});

        userScope.$digest();
    }));

    afterEach(function() {
        httpBackend.verifyNoOutstandingExpectation();
        httpBackend.verifyNoOutstandingRequest();
    });

    it("should refresh users", function() {
        // There isn't a user yet
        expect(userScope.user).toBe(undefined);
        // Set it up to return a very fake user object
        httpBackend.expectGET('/user/').respond(200, {"topics": 12});
        httpBackend.expectGET('/user/settings/').respond(200, {"user":1, "readtime":300});
        // Call the function
        userScope.refreshUser();
        // Send the response back from fake-server to client
        httpBackend.flush();
        // Make sure that the user variable has been properly set
        expect(userScope.user).toEqual({"topics": 12});

        // Try it again to make sure it doesn't break anything
        httpBackend.expectGET('/user/').respond(200, {"topics":12});
        httpBackend.expectGET('/user/settings/').respond(200, {"user":1, "readtime":300});
        userScope.refreshUser();
        httpBackend.flush();
        expect(userScope.user).toEqual({"topics":12});
        expect(userScope.userSettings).toEqual({"user":1, "readtime":300});

        // What if the user has somehow changed on the server?
        httpBackend.expectGET('/user/').respond(200, {"topics":21});
        httpBackend.expectGET('/user/settings/').respond(200, {"user":4, "readtime":400});
        userScope.refreshUser();
        httpBackend.flush();
        expect(userScope.user).toEqual({"topics":21});
        expect(userScope.userSettings).toEqual({"user":4, "readtime":400});
    });

    it("should getTopicIds", function() {
        // Set it up to return fake user object when refreshUser is called inside getTopicIds
        httpBackend.whenGET('/user/').respond(200, {"topics": []});
        httpBackend.whenGET('/user/settings/').respond(200, {"user":1, "readtime":300});
        // Call the function
        userScope.getTopicIds();
        // Send the response
        httpBackend.flush();
        // Make sure it's what we expect
        expect(userScope.user["topics"]).toEqual([]);
        // Make sure it exists when we already have the user
        userScope.getTopicIds();
        expect(userScope.user["topics"]).toEqual([]);
    });
});

describe("Navigation controllers", function() {
    beforeEach(module("main.controllers"));
    var userScope, navScope, httpBackend;

    beforeEach(inject(function($controller, $rootScope, $httpBackend, $timeout, $q, APIService) {
        httpBackend = $httpBackend;

        userScope = $rootScope.$new();
        $controller('UserController', {$scope: userScope});
        navScope = userScope.$new();
        $controller('NavigationController', {$scope: navScope});
        httpBackend.whenGET('/user/').respond(200, {"topics": []});
        httpBackend.whenGET('/user/settings/').respond(200, {"user":1, "readtime":300});

        userScope.$digest();
        httpBackend.flush();
    }));

    afterEach(function() {
        httpBackend.verifyNoOutstandingExpectation();
        httpBackend.verifyNoOutstandingRequest();
    });

    // saveEdits and toggleEditMode are acceptance tested

    it("should fetch all of the topics", function() {
        navScope.fetchTopics();
        expect(navScope.topicIds).toEqual([]);
        expect(navScope.topics).toEqual([]);
    });

    it("should add topics", function() {
        // should add a first topic
        httpBackend.expectPOST('/topics/', {"name":"topic1"}).respond(200, {"name": "topic1", "id": 12});
        expect(navScope.topics.length).toEqual(0);
        navScope.addTopic("topic1");
        httpBackend.flush();
        expect(navScope.topics[0]).toEqual({"name":"topic1","id":12});
        expect(navScope.topicIds[0]).toEqual(12);

        // should add a second topic
        httpBackend.expectPOST('/topics/', {"name":"topic2"}).respond(200, {"name":"topic2", "id":13});
        expect(navScope.topics.length).toEqual(1);
        navScope.addTopic("topic2");
        httpBackend.flush();
        expect(navScope.topics.length).toEqual(2);
        expect(navScope.topics[0]).toEqual({"name":"topic1","id":12});
        expect(navScope.topics[1]).toEqual({"name":"topic2","id":13});
        expect(navScope.topicIds[0]).toEqual(12);
        expect(navScope.topicIds[1]).toEqual(13);

        // shouldn't add a topic that already exists
        httpBackend.expectPOST('/topics/', {"name":"topic2"}).respond(409, '');
        navScope.addTopic("topic2");
        httpBackend.flush();
        expect(navScope.topics.length).toEqual(2);
        expect(navScope.topicIds).toEqual([12,13]);
    });

    it("should rename topics", function() {
        // need to initialize some variables to mimic things
        httpBackend.expectPOST('/topics/', {"name":"topic1"}).respond(200, {"name": "topic1", "id": 12});
        navScope.addTopic("topic1");
        httpBackend.flush();
        httpBackend.expectPOST('/topics/', {"name":"topic2"}).respond(200, {"name":"topic2", "id":13});
        navScope.addTopic("topic2");
        httpBackend.flush();

        // should rename a topic
        httpBackend.expectPUT('/topics/12', {"name":"topic3", "id":12}).respond(200, {"name":"topic3", "id":12});
        navScope.renameTopic("topic3", navScope.topics[0]);
        httpBackend.flush();
        expect(navScope.topics.length).toEqual(2);
        expect(navScope.topics[0]).toEqual({"name":"topic2","id":13});
        expect(navScope.topics[1]).toEqual({"name":"topic3","id":12});

        // will not allow name to be changed to same as another topic
        httpBackend.expectPUT('/topics/13', {"name":"topic3", "id":13}).respond(409, '');
        navScope.renameTopic("topic3", navScope.topics[0]);
        httpBackend.flush();
        expect(navScope.topics.length).toEqual(2);
        expect(navScope.topics[0]).toEqual({"name":"topic2","id":13});
        expect(navScope.topics[1]).toEqual({"name":"topic3","id":12});
    });

    it("should remove topics", function() {
        // need to initialize some variables to mimic things
        httpBackend.expectPOST('/topics/', {"name":"topic1"}).respond(200, {"name": "topic1", "id": 12});
        navScope.addTopic("topic1");
        httpBackend.flush();
        httpBackend.expectPOST('/topics/', {"name":"topic2"}).respond(200, {"name":"topic2", "id":13});
        navScope.addTopic("topic2");
        httpBackend.flush();

        // shouldn't change anything if the topic doesn't exist
        httpBackend.expectDELETE('/topics/14').respond(409, '');
        navScope.removeTopic(14);
        httpBackend.flush();
        expect(navScope.topics.length).toEqual(2);
        expect(navScope.topics[0]).toEqual({"name":"topic1","id":12});
        expect(navScope.topics[1]).toEqual({"name":"topic2","id":13});

        // delete the topic without breaking anything
        httpBackend.expectDELETE('/topics/12').respond(204, '');
        navScope.removeTopic(12);
        httpBackend.flush();
        expect(navScope.topics.length).toEqual(1);
        expect(navScope.topics[0]).toEqual({"name":"topic2","id":13});

        // what if we remove everything though?
        httpBackend.expectDELETE('/topics/13').respond(204, '');
        navScope.removeTopic(13);
        httpBackend.flush();
        expect(navScope.topics.length).toEqual(0);
        expect(navScope.topics).toEqual([]);
    });

    it("should expand and minimize topics", function() {
        // need to initialize some variables to mimic things
        httpBackend.expectPOST('/topics/', {"name":"topic1"}).respond(200, {"name": "topic1", "id": 12});
        navScope.addTopic("topic1");
        httpBackend.flush();
        httpBackend.expectPOST('/topics/', {"name":"topic2"}).respond(200, {"name":"topic2", "id":13});
        navScope.addTopic("topic2");
        httpBackend.flush();

        // Testing expandedIndex
        expect(navScope.expandedIndex).toEqual([-1]);
        navScope.expandTopic(0);
        expect(navScope.expandedIndex).toEqual([0]);
        navScope.expandTopic(1);
        expect(navScope.expandedIndex).toEqual([1]);
    });

    it("should send active feed  and topic signals", function() {
        var success = false;
        navScope.$on("activeFeedIs", function (event, message) {
            if(message.identifier == 12)
                success = true;
        });
        navScope.activeFeed(12);
        expect(success).toEqual(true);

        success = false;
        navScope.$on("activeTopicIs", function (event, message) {
            if(message.identifier == 12)
                success = true;
        });
        navScope.activeTopic(12);
        expect(success).toEqual(true);
    });
});

describe("Search controllers", function($rootScope) {
    beforeEach(module("main.controllers"));
    var httpBackend, userScope, navScope, topicScope, searchScope;

    beforeEach(inject(function($controller, $rootScope, $httpBackend, $timeout, $q, APIService) {
        httpBackend = $httpBackend;

        userScope = $rootScope.$new();
        $controller('UserController', {$scope: userScope});
        navScope = userScope.$new();
        $.when(function(){
          var deferred = $q.defer();
          deferred.resolve($controller('NavigationController', {$scope: navScope}));
          return deferred.promise;
        }).then(function(x){
          topicScope = navScope.$new();
          var topic = {"name":"Uncategorized", "id":12, "user":1, "feeds": []};
          topicScope.$parent.topics = [topic];
          topicScope.$parent.$index = 0;
          $controller('TopicController', {$scope: topicScope});
          
          searchScope = navScope.$new();
          $controller('SearchController', {$scope: searchScope});
        });

        userScope.$digest();
    }));

    afterEach(function() {
       httpBackend.verifyNoOutstandingExpectation();
       httpBackend.verifyNoOutstandingRequest();
    });

    it("should search properly", function() {
        // Obviously not an RSS feed, but I control the server responses
        var URL = 'http://www.goodURL.com/rss.xml';
        var foofeed = {"name":"foofeed", "id":12};
        var results;
        searchScope.query = URL;
        httpBackend.expectPOST('/feeds/create/', {'url':URL}).respond(200, foofeed);
        searchScope.$on("showSearchResults", function (event, message) {
            results = message.searchResults;
        });
        searchScope.search();
        httpBackend.flush();
        expect(results).toEqual([{"name":"foofeed","id":12}]);
        
        // What if its already in the server?
        foofeed = {"name":"foofeed", "id":15};
        httpBackend.expectPOST('/feeds/create/', {'url':URL}).respond(409, foofeed);
        searchScope.search();
        httpBackend.flush();
        expect(results).toEqual([{"name":"foofeed","id":15}]);

        // What if it's not a feed?
        httpBackend.expectPOST('/feeds/create/', {'url':URL}).respond(400, '');
        searchScope.search();
        httpBackend.flush();
        expect(results).toEqual([{"name":"foofeed","id":15}]);

        // What if it's not even a URL?
        searchScope.query = 'foobar';
        foofeed = {"name":"foofeed", "id":19};
        httpBackend.expectPOST('/search/', {"searchString":'foobar'}).respond(200, [foofeed]);
        searchScope.search();
        httpBackend.flush();
        expect(results).toEqual([foofeed]);
    })
});

describe("Results controllers", function() {
    beforeEach(module("main.controllers"));
    var httpBackend, userScope, navScope, topicScope, searchScope, resultScope;

    beforeEach(inject(function($controller, $rootScope, $httpBackend, $timeout, $q, APIService) {
        httpBackend = $httpBackend;

        userScope = $rootScope.$new();
        $controller('UserController', {$scope: userScope});
        navScope = userScope.$new();
        $.when(function(){
          var deferred = $q.defer();
          deferred.resolve($controller('NavigationController', {$scope: navScope}));
          return deferred.promise;
        }).then(function(x){
          topicScope = navScope.$new();
          var topic = {"name":"Uncategorized", "id":12, "user":1, "feeds": []};
          topicScope.$parent.topics = [topic];
          topicScope.$parent.$index = 0;
          $controller('TopicController', {$scope: topicScope});
          
          searchScope = navScope.$new();
          $controller('SearchController', {$scope: searchScope});

          resultScope = navScope.$new();
          $controller('ResultsController', {$scope: resultScope});
        });

        userScope.$digest();
    }));

    afterEach(function() {
       httpBackend.verifyNoOutstandingExpectation();
       httpBackend.verifyNoOutstandingRequest();
    });

    it("should update their topic lists before showing topic options", function() {
        expect(resultScope.topics).toEqual([]);
        resultScope.showTopicOptions();
        expect(resultScope.topics).toEqual([{"name":"Uncategorized","id":12,"user":1,"feeds":[]}]);
    });

    it("should expand the various settings", function() {
        expect(resultScope.expandedSettingIndex).toEqual(-1);
        resultScope.expandSettingsUser();
        expect(resultScope.expandedSettingIndex).toEqual(1);
        resultScope.expandSettingsFeed();
        expect(resultScope.expandedSettingIndex).toEqual(2);
        resultScope.expandSettingsReading();
        expect(resultScope.expandedSettingIndex).toEqual(3);
    });
});

describe("Topic controllers", function() {
    beforeEach(module("main.controllers"));
    var userScope, navScope, topicScope, httpBackend;

    beforeEach(inject(function($controller, $rootScope, $httpBackend, $timeout, $q, APIService) {
        httpBackend = $httpBackend;

        userScope = $rootScope.$new();
        $controller('UserController', {$scope: userScope});
        navScope = userScope.$new();
        $.when(function(){
          var deferred = $q.defer();
          deferred.resolve($controller('NavigationController', {$scope: navScope}));
          return deferred.promise;
        }).then(function(x){
          topicScope = navScope.$new();
          var topic = {"name":"topic1", "id":12, "user":1, "feeds": []};
          topicScope.$parent.topics = [topic];
          topicScope.$parent.$index = 0;
          $controller('TopicController', {$scope: topicScope});
        });

        userScope.$digest();
    }));

    afterEach(function() {
        httpBackend.verifyNoOutstandingExpectation();
        httpBackend.verifyNoOutstandingRequest();
    });

    it("should refresh its own topic", function() {
        var origTopic = topicScope.topic;
        topicScope.$parent.topics = [origTopic];
        topicScope.$parent.$index = 0;
        topicScope.refreshTopic();
        expect(topicScope.topic).toEqual(origTopic);
    });

    it("should fetch feeds when there are no feeds", function() {
        var origTopic = topicScope.topic;
        topicScope.fetchFeeds();
        expect(topicScope.topic).toEqual(origTopic);
    });

    // it("should add and remove feeds", function() {
    //     // add foofeed
    //     var foofeed = {"name":"foofeed", "id":12};
    //     topicScope.addFeedToTopic(foofeed);
    //     expect(topicScope.topic["feeds"][0]).toEqual(12);
    //     expect(topicScope.feeds[0]).toEqual(foofeed);
    //     // check fetching feeds when there are feeds
    //     httpBackend.expectGET('/feeds/12').respond(200, foofeed);
    //     var origTopic = topicScope.topic;
    //     topicScope.fetchFeeds();
    //     httpBackend.flush();
    //     expect(topicScope.topic).toEqual(origTopic);

    //     // remove nonexistent feed
    //     httpBackend.expectPUT('/topics/12', topicScope.topic).respond(200, '');
    //     topicScope.removeFeedFromTopic(28);
    //     httpBackend.flush();
    //     expect(topicScope.feeds[0]).toEqual(foofeed);
    //     // remove foofeed unsuccessfully
    //     httpBackend.expectPUT('/topics/12', topicScope.topic).respond(400, '');
    //     topicScope.removeFeedFromTopic(12);
    //     httpBackend.flush();
    //     expect(topicScope.feeds[0]).toEqual(foofeed);
    //     // remove foofeed successfully
    //     httpBackend.expectPUT('/topics/12', topicScope.topic).respond(200, '');
    //     topicScope.removeFeedFromTopic(12);
    //     httpBackend.flush();
    //     expect(topicScope.feeds).toEqual([]);
    // });

    it("should test that the expand feed signal is properly sent", function() {
        var success = false;
        topicScope.$on("clickFeed", function (event, message) {
            if(message.identifier == 12) {
                success = true;
            }
        });
        topicScope.expandFeed(48);
        expect(success).toBe(false);
        topicScope.expandFeed(12);
        expect(success).toBe(true);
    });
});

describe("Feed controllers", function() {
    beforeEach(module("main.controllers"));
    var userScope, navScope, topicScope, feedScope, httpBackend;

    beforeEach(inject(function($controller, $rootScope, $httpBackend, $timeout, $q, APIService) {
        httpBackend = $httpBackend;

        userScope = $rootScope.$new();
        $controller('UserController', {$scope: userScope});
        httpBackend.whenGET('/user/').respond(200, {"topics": []});
        httpBackend.whenGET('/user/settings/').respond(200, {"user":1, "readtime":300});
        userScope.refreshUser();
        httpBackend.flush();

        navScope = userScope.$new();
        $.when(function(){
          var deferred = $q.defer();
          deferred.resolve($controller('NavigationController', {$scope: navScope}));
          return deferred.promise;
        }).then(function(x){
          topicScope = navScope.$new();
          var topic = {"name":"topic1", "id":12, "user":1, "feeds": []};
          topicScope.$parent.topics = [topic];
          topicScope.$parent.$index = 0;
          $controller('TopicController', {$scope: topicScope});
        });

        feedScope = topicScope.$new();
        $controller('FeedController', {$scope: feedScope});

        userScope.$digest();
    }));

    afterEach(function() {
        httpBackend.verifyNoOutstandingExpectation();
        httpBackend.verifyNoOutstandingRequest();
    });

    it("should expand posts", function() {
        expect(feedScope.expandedPostIndex).toEqual(-1);
        var post = {"id":12};
        feedScope.expandPost(post);
        expect(feedScope.expandedPostIndex).toEqual(12);
        post = {"id":14};
        feedScope.expandPost(post);
        expect(feedScope.expandedPostIndex).toEqual(14);
    });

    it("should fetch posts", function() {
        // feed has no posts
        httpBackend.expectGET('/feeds/12/posts/').respond(200, []);
        httpBackend.expectGET('/feeds/12/posts/read').respond(200, {"posts":[]});
        topicScope.expandFeed(12);
        httpBackend.flush();
        expect(feedScope.posts).toEqual([]);
        var fake_post_array = [{"steve": "rogers"}, {"bill": "murray"}];
        httpBackend.expectGET('/feeds/12/posts/').respond(200, fake_post_array);
        httpBackend.expectGET('/feeds/12/posts/read').respond(200, {"posts":[]});
        topicScope.expandFeed(12);
        httpBackend.flush();
        expect(feedScope.posts).toEqual([{"steve": "rogers", "content": "", "unread":true, "sortByUnread":true},
           {"bill": "murray", "content":"", "unread":true, "sortByUnread":true}]);
    });
});