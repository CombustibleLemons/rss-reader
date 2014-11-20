'use strict';

/* jasmine specs for controllers go here */
describe("User controllers", function() {
    beforeEach(module("main.controllers"));

    var userScope, httpBackend, userController;
    beforeEach(inject(function($controller, $rootScope, $httpBackend, $timeout, $q, APIService) {
        userScope = $rootScope.$new();
        userController = $controller('UserController', {$scope: userScope});
        httpBackend = $httpBackend;

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
        // Call the function
        userScope.refreshUser();
        // Send the response back from fake-server to client
        httpBackend.flush();
        // Make sure that the user variable has been properly set
        expect(userScope.user).toEqual({"topics": 12});
    });

    it("should getTopicIds", function() {
        // Set it up to return fake user object when refreshUser is called inside getTopicIds
        httpBackend.whenGET('/user/').respond(200, {"topics": []});
        // Call the function
        userScope.getTopicIds();
        // Send the response
        httpBackend.flush();
        // Make sure it's what we expect
        expect(userScope.user["topics"]).toEqual([]);
    });
});

describe("Navigation controllers", function() {
    beforeEach(module("main.controllers"));
    var userScope, navScope, httpBackend;

    beforeEach(inject(function($controller, $rootScope, $httpBackend, $timeout, $q, APIService) {
        userScope = $rootScope.$new();
        $controller('UserController', {$scope: userScope});

        navScope = userScope.$new();
        $controller('NavigationController', {$scope: navScope});

        httpBackend = $httpBackend;
        httpBackend.whenGET('/user/').respond(200, {"topics": []});
        userScope.refreshUser();
        httpBackend.flush();
        userScope.$digest();
        navScope.$digest();
    }));

    afterEach(function() {
        httpBackend.verifyNoOutstandingExpectation();
        httpBackend.verifyNoOutstandingRequest();
    });

    it("should fetch all of the topics", function() {
        navScope.fetchTopics();
        expect(navScope.topicIds).toEqual([]);
        expect(navScope.topics).toEqual([]);
    });

    it("should add topics", function() {
        // need to initialize some topic variables to mimic things
        navScope.fetchTopics();

        // should add a first topic
        httpBackend.expectPOST('/topics/create', {"name":"topic1"}).respond(200, {"name": "topic1", "id": 12});
        var success = false;;
        expect(navScope.topics.length).toEqual(0);
        navScope.addTopic("topic1");
        navScope.$on("addedTopic", function (event, message) {
            success = true;
        });
        httpBackend.flush();
        expect(success).toBe(true);
        expect(navScope.topics[0]["name"]).toEqual("topic1");
        expect(navScope.topics[0]["id"]).toEqual(12);

        // should add a second topic
        success = false;
        httpBackend.expectPOST('/topics/create', {"name":"topic2"}).respond(200, {"name":"topic2", "id":13});
        expect(navScope.topics.length).toEqual(1);
        navScope.addTopic("topic2");
        httpBackend.flush();
        expect(success).toBe(true);
        expect(navScope.topics.length).toEqual(2);
        expect(navScope.topics[0]["name"]).toEqual("topic1");
        expect(navScope.topics[0]["id"]).toEqual(12);
        expect(navScope.topics[1]["name"]).toEqual("topic2");
        expect(navScope.topics[1]["id"]).toEqual(13);

        // shouldn't add a topic that already exists
        success = false;
        httpBackend.expectPOST('/topics/create', {"name":"topic2"}).respond(409, '');
        navScope.addTopic("topic2");
        httpBackend.flush();
        expect(success).toBe(false);
        expect(navScope.topics.length).toEqual(2);
    });

    it("should rename topics", function() {
        // need to initialize some variables to mimic things
        navScope.fetchTopics();
        httpBackend.expectPOST('/topics/create', {"name":"topic1"}).respond(200, {"name": "topic1", "id": 12});
        navScope.addTopic("topic1");
        httpBackend.flush();
        httpBackend.expectPOST('/topics/create', {"name":"topic2"}).respond(200, {"name":"topic2", "id":13});
        navScope.addTopic("topic2");
        httpBackend.flush();

        // should rename a topic
        httpBackend.expectPOST('/topics/rename', {"name":"topic3", "index":12}).respond(200, {"name":"topic3", "id":12});
        navScope.renameTopic({"name":"topic3"}, 12);
        httpBackend.flush();
        expect(navScope.topics.length).toEqual(2);
        expect(navScope.topics[0]["name"]).toEqual("topic2");
        expect(navScope.topics[0]["id"]).toEqual(13);
        expect(navScope.topics[1]["name"]).toEqual("topic3");
        expect(navScope.topics[1]["id"]).toEqual(12);
    });

    it("should remove topics", function() {
        // need to initialize some variables to mimic things
        navScope.fetchTopics();
        httpBackend.expectPOST('/topics/create', {"name":"topic1"}).respond(200, {"name": "topic1", "id": 12});
        navScope.addTopic("topic1");
        httpBackend.flush();
        httpBackend.expectPOST('/topics/create', {"name":"topic2"}).respond(200, {"name":"topic2", "id":13});
        navScope.addTopic("topic2");
        httpBackend.flush();
        expect(navScope.topics.length).toEqual(2);
        expect(navScope.topics[0]["name"]).toEqual("topic1");
        expect(navScope.topics[0]["id"]).toEqual(12);
        expect(navScope.topics[1]["name"]).toEqual("topic2");
        expect(navScope.topics[1]["id"]).toEqual(13);

        // shouldn't change anything if the topic doesn't exist
        httpBackend.expectPOST('/topics/delete', {"index":14}).respond(409, '');
        navScope.removeTopic(14);
        httpBackend.flush();
        expect(navScope.topics.length).toEqual(2);
        expect(navScope.topics[0]["name"]).toEqual("topic1");
        expect(navScope.topics[0]["id"]).toEqual(12);
        expect(navScope.topics[1]["name"]).toEqual("topic2");
        expect(navScope.topics[1]["id"]).toEqual(13);

        // delete the topic without breaking anything
        httpBackend.expectPOST('/topics/delete', {"index":12}).respond(204, '');
        navScope.removeTopic(12);
        httpBackend.flush();
        expect(navScope.topics.length).toEqual(1);
        expect(navScope.topics[0]["name"]).toEqual("topic2");
        expect(navScope.topics[0]["id"]).toEqual(13);
    });

    it("should expand and minimize topics", function() {
        // need to initialize some variables to mimic things
        navScope.fetchTopics();
        httpBackend.expectPOST('/topics/create', {"name":"topic1"}).respond(200, {"name": "topic1", "id": 12});
        navScope.addTopic("topic1");
        httpBackend.flush();
        httpBackend.expectPOST('/topics/create', {"name":"topic2"}).respond(200, {"name":"topic2", "id":13});
        navScope.addTopic("topic2");
        httpBackend.flush();
        expect(navScope.topics.length).toEqual(2);
        expect(navScope.topics[0]["name"]).toEqual("topic1");
        expect(navScope.topics[0]["id"]).toEqual(12);
        expect(navScope.topics[1]["name"]).toEqual("topic2");
        expect(navScope.topics[1]["id"]).toEqual(13);

        expect(navScope.expandedIndex).toEqual(-1);
        navScope.expandTopic(0);
        expect(navScope.expandedIndex).toEqual(0);
        navScope.expandTopic(1);
        expect(navScope.expandedIndex).toEqual(1);
    });

    it("should move feeds from topic to topic", inject(function($controller) {
        var topicScope1 = navScope.$new();
        var topic1 = {"name":"topic1", "id":12, "user":1, "feeds": []};
        topicScope1.$parent.topics.push(topic1);
        topicScope1.$parent.$index = 0;
        $controller('TopicController', {$scope: topicScope1});

        var topicScope2 = navScope.$new();
        var topic2 = {"name":"topic2", "id":13, "user":1, "feeds": []};
        topicScope2.$parent.topics.push(topic2);
        topicScope2.$parent.$index = 1;
        $controller('TopicController', {$scope: topicScope2});
        dump('moving feeds tests not fully implemented');
/*
        // need to initialize some variables to mimic things
        navScope.fetchTopics();
        httpBackend.flush();
        httpBackend.expectPOST('/topics/create', {"name":"topic1"}).respond(200, {"name": "topic1", "id": 12});
        navScope.addTopic("topic1");
        httpBackend.flush();
        httpBackend.expectPOST('/topics/create', {"name":"topic2"}).respond(200, {"name":"topic2", "id":13});
        navScope.addTopic("topic2");
        httpBackend.flush();
        expect(navScope.topics.length).toEqual(2);
        expect(navScope.topics[0]["name"]).toEqual("topic1");
        expect(navScope.topics[0]["id"]).toEqual(12);
        expect(navScope.topics[1]["name"]).toEqual("topic2");
        expect(navScope.topics[1]["id"]).toEqual(13);
        */
    }));

});

describe("Topic controllers", function() {
    beforeEach(module("main.controllers"));
    var userScope, navScope, topicScope, httpBackend;

    beforeEach(inject(function($controller, $rootScope, $httpBackend, $timeout, $q, APIService) {
        httpBackend = $httpBackend;

        userScope = $rootScope.$new();
        $controller('UserController', {$scope: userScope});
        httpBackend.whenGET('/user/').respond(200, {"topics": []});
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

        userScope.$digest();
        navScope.$digest();
        topicScope.$digest();
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

    it("should add and remove feeds", function() {
        // add foofeed
        var foofeed = {"name":"foofeed", "id":12};
        httpBackend.expectPUT('/topics/12').respond(200, '');
        topicScope.addFeedToTopic(foofeed);
        httpBackend.flush();
        expect(topicScope.topic["feeds"][0]).toEqual(12);
        expect(topicScope.feeds[0]).toEqual(foofeed);
        // check fetching feeds when there are feeds
        httpBackend.expectGET('/feeds/12').respond(200, foofeed);
        var origTopic = topicScope.topic;
        topicScope.fetchFeeds();
        httpBackend.flush();
        expect(topicScope.topic).toEqual(origTopic);

        // remove nonexistent feed
        httpBackend.expectPUT('topics/12', topicScope.topic).respond(200, '');
        topicScope.removeFeedFromTopic(28);
        httpBackend.flush();
        expect(topicScope.feeds[0]).toEqual(foofeed);
        // remove foofeed unsuccessfully
        httpBackend.expectPUT('topics/12', topicScope.topic).respond(400, '');
        topicScope.removeFeedFromTopic(12);
        httpBackend.flush();
        expect(topicScope.feeds[0]).toEqual(foofeed);
        // remove foofeed successfully
        httpBackend.expectPUT('topics/12', topicScope.topic).respond(200, '');
        topicScope.removeFeedFromTopic(12);
        httpBackend.flush();
        dump(topicScope.feeds);
        expect(topicScope.feeds).toEqual([]);
    });

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

describe("Search controllers", function($rootScope) {
    beforeEach(module("main.controllers"));
    var searchScope, httpBackend;

    beforeEach(inject(function($controller, $rootScope, $httpBackend) {
        searchScope = $rootScope.$new();
        $controller('SearchController', {$scope: searchScope});
        httpBackend = $httpBackend;

        searchScope.$digest();
    }));

    afterEach(function() {
       httpBackend.verifyNoOutstandingExpectation();
       httpBackend.verifyNoOutstandingRequest();
    });

    it("should add feeds", function() {
        httpBackend.expectPOST('/feeds/create', '{"url":"http://home.uchicago.edu/~jharriman/example-rss.xml"}').respond(200, 'pretend this is feed data');
        searchScope.query = 'http://home.uchicago.edu/~jharriman/example-rss.xml';
        var success;

        //searchScope.addFeed();
        searchScope.search();

        searchScope.$on("addedFeed", function (event, message) {
            // check message
            success = true;
        });
        httpBackend.flush();
        expect(success).toBe(true);
        // var newFeedSet = scope.user.topic_set['uncategorized']; // yet again
        // expect(originalFeedSet.length).toEqual(newFeedSet.length + 1);
        // expect feed to be in uncategorized topic, uncertain of syntax at this time
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
        navScope.$digest();
        topicScope.$digest();
        feedScope.$digest();
    }));

    afterEach(function() {
        httpBackend.verifyNoOutstandingExpectation();
        httpBackend.verifyNoOutstandingRequest();
    });

    it("should expand posts", function() {
        expect(feedScope.expandedPostIndex).toEqual(-1);
        feedScope.expandPost(12);
        expect(feedScope.expandedPostIndex).toEqual(12);
    });

    it("should fetch posts", function() {
        // feed has no posts
        httpBackend.expectGET('feeds/12/posts').respond(200, []);
        topicScope.expandFeed(12);
        httpBackend.flush();
        expect(feedScope.posts).toEqual([]);
        var fake_post_array = [{"steve": "rogers"}, {"bill": "murray"}];
        httpBackend.expectGET('feeds/12/posts').respond(200, fake_post_array);
        topicScope.expandFeed(12);
        httpBackend.flush();
        expect(feedScope.posts).toEqual([{"steve": "rogers", "content": ""}, {"bill": "murray", "content":""}]);
    });

describe("Speedtest controllers", function() {
    beforeEach(module("main.controllers"));
    var userScope, navScope, topicScope, httpBackend;

    beforeEach(inject(function($controller, $rootScope, $httpBackend, $timeout, $q, APIService) {
        httpBackend = $httpBackend;

        userScope = $rootScope.$new();
        $controller('UserController', {$scope: userScope});
        httpBackend.whenGET('/speedtest/').respond(200, {"test": []});
        userScope.refreshUser();
        httpBackend.flush();

        navScope = userScope.$new();
        $.when(function(){
          var deferred = $q.defer();
          deferred.resolve($controller('NavigationController', {$scope: navScope}));
          return deferred.promise;
        }).then(function(x){
          SpeedScope = navScope.$new();
          var test = {"user":1, "id":12};
          topicScope.$parent.topics = [topic];
          topicScope.$parent.$index = 0;
          $controller('SpeedtestController', {$scope: speedtestScope})
        });

        userScope.$digest();
        navScope.$digest();
        topicScope.$digest();
    }));

    afterEach(function() {
        httpBackend.verifyNoOutstandingExpectation();
        httpBackend.verifyNoOutstandingRequest();
    });


    it("should test that the expand feed signal is properly sent", function() {
        var success = false;
        topicScope.$on("clickTest", function (event, message) {
            if(message.identifier == 2) {
                success = true;
            }
        });
        userScope.expandTest(1);
        expect(success).toBe(false);
        userScope.expandFeed(2);
        expect(success).toBe(true);
    });
    // This is all that can be done, as it exists since js stops running if you
    // have a confirm box. Or so I've been told
    // Actually if the user stuff moved, then maybe we should test setting
    // the wpm variable here

});
/*
    it("should fetch posts", function() {
        var posts = scope.fetchPosts(validFeed);
        expect(posts).toBe(true);
        expect(scope.foofeed.post_set.length).toBeGreaterThan(0);
        expect(scope.view.div.ul['posts']).toBeGreaterThan(0); // syntax???
    });
});
*/