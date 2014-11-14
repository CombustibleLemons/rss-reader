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
        httpBackend.expectGET('users/1').respond(200, {"topics": 12});
        // Call the function
        userScope.refreshUser();
        // Send the response back from fake-server to client
        httpBackend.flush();
        // Make sure that the user variable has been properly set
        expect(userScope.user).toEqual({"topics": 12});
    });

    it("should getTopicIds", function() {
        // Set it up to return fake user object when refreshUser is called inside getTopicIds
        httpBackend.whenGET('users/1').respond(200, {"topics": []});
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
        httpBackend.whenGET('users/1').respond(200, {"topics": []});
        userScope.refreshUser();

        userScope.$digest();
        navScope.$digest();
    }));

    afterEach(function() {
        httpBackend.verifyNoOutstandingExpectation();
        httpBackend.verifyNoOutstandingRequest();
    });

    it("should fetch all of the topics", function() {
        navScope.fetchTopics();
        httpBackend.flush();
        expect(navScope.topicIds).toEqual([]);
        expect(navScope.topics).toEqual([]);
    });

    it("should add topics", function() {
        // need to initialize some topic variables to mimic things
        navScope.fetchTopics();
        httpBackend.flush();

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
        httpBackend.flush();
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

        expect(navScope.expandedIndex).toEqual(-1);
        navScope.expandTopic(0);
        expect(navScope.expandedIndex).toEqual(0);
        navScope.expandTopic(1);
        expect(navScope.expandedIndex).toEqual(1);
    });
});

describe("Topic controllers", function() {
    beforeEach(module("main.controllers"));
    var userScope, navScope, topicScope, httpBackend;

    beforeEach(inject(function($controller, $rootScope, $httpBackend, $timeout, $q, APIService) {
        httpBackend = $httpBackend;

        userScope = $rootScope.$new();
        $controller('UserController', {$scope: userScope});
        httpBackend.whenGET('users/1').respond(200, {"topics": []});
        userScope.refreshUser();
        httpBackend.flush();

        navScope = userScope.$new();
        $.when(function(){
          var deferred = $q.defer();
          deferred.resolve($controller('NavigationController', {$scope: navScope}));
          return deferred.promise;
        }).then(function(x){
          dump('hey');
          topicScope = navScope.$new();
          var topic = {"name":"topic1", "id":12, "user":1, "feeds": []};
          topicScope.$parent.topics = [topic];
          topicScope.$parent.$index = 0;
          $controller('TopicController', {$scope: topicScope})
        });

        dump('ho');
        userScope.$digest();
        navScope.$digest();
        topicScope.$digest();
    }));

    afterEach(function() {
        httpBackend.verifyNoOutstandingExpectation();
        httpBackend.verifyNoOutstandingRequest();
    });

    it("should do things!", function() {

    });
});

/*
describe("Topic controllers", function($rootScope) {
    beforeEach(module("main.controllers"));
    var scope;

    beforeEach(inject(function($controller, $rootScope) {
        scope = $rootScope.$new();
        $controller('TopicController', {$scope: scope});

        scope.$digest();
    }));

    it("should edit names", function() {
        var originalName = scope.topic.name;
        var changedName = scope.topic.editName("bar");
        expect(changedName).toBe(true);
        expect(self.Topic.name).toBe("bar");
    });

    it("should not let names be empty strings", function() {
        var changedName = scope.topic.editName("");
        expect(changedName).toBe(false);
    });

    it("should add feeds", function() {
       var url = "http://xkcd.com/rss.xml";
       var addedFeed = scope.addFeedToTopic(url);
       expect(addedFeed).toBe(true);
       expect(scope.topic.feed_set.all()[0].URL).toBe(url);
       expect(scope.addFeedToTopic(url)).toBe(false);
    });

    it("should fetch all feeds", function() {
        expect(scope.fetchFeeds()).toBe(true);
        expect(scope.topic.feed_set.length).toEqual(0);
        var url = "http://xkcd.com/rss.xml";
        scope.addFeedToTopic(url);
        expect(scope.topic.feed_set.length).toEqual(1);
    });

    it("should expand individual feeds", function() {
        expect(scope.expandFeed('foo')).toBe(true);
        expect(scope.view.h3['feedtitle']).toEqual('foo'); // probably wrong syntax
        scope.addFeedToTopic('url');
        expect(scope.expandFeed('bar')).toBe(true);
        expect(scope.view.h3['feedtitle']).not.toEqual('foo'); // yeahhhh
        expect(scope.view.h3['feedtitle']).toEqual('bar'); // still probably wrong syntax
    });
});
*/

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
        httpBackend.expectPOST('/feeds/create', '{"url":"http://home.uchicago.edu/~jharriman/rss20.xml"}').respond(200,
            'pretend this is feed data');
        searchScope.query = 'http://home.uchicago.edu/~jharriman/rss20.xml';
        var success;
        searchScope.addFeed();
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
/*
describe("Topic controllers", function($rootScope) {
    beforeEach(module("main.controllers"));
    var scope;

    beforeEach(inject(function($controller, $rootScope) {
        scope = $rootScope.$new();
        $controller('TopicController', {$scope: scope});

        scope.$digest();
    }));

    it("should edit names", function() {
        var originalName = scope.topic.name;
        var changedName = scope.topic.editName("bar");
        expect(changedName).toBe(true);
        expect(self.Topic.name).toBe("bar");
    });

    it("should not let names be empty strings", function() {
        var changedName = scope.topic.editName("");
        expect(changedName).toBe(false);
    });

    it("should add feeds", function() {
       var url = "http://xkcd.com/rss.xml";
       var addedFeed = scope.addFeedToTopic(url);
       expect(addedFeed).toBe(true);
       expect(scope.topic.feed_set.all()[0].URL).toBe(url);
       expect(scope.addFeedToTopic(url)).toBe(false);
    });

    it("should fetch all feeds", function() {
        expect(scope.fetchFeeds()).toBe(true);
        expect(scope.topic.feed_set.length).toEqual(0);
        var url = "http://xkcd.com/rss.xml";
        scope.addFeedToTopic(url);
        expect(scope.topic.feed_set.length).toEqual(1);
    });

    it("should expand individual feeds", function() {
        expect(scope.expandFeed('foo')).toBe(true);
        expect(scope.view.h3['feedtitle']).toEqual('foo'); // probably wrong syntax
        scope.addFeedToTopic('url');
        expect(scope.expandFeed('bar')).toBe(true);
        expect(scope.view.h3['feedtitle']).not.toEqual('foo'); // yeahhhh
        expect(scope.view.h3['feedtitle']).toEqual('bar'); // still probably wrong syntax
    });
});

describe("Feed controllers", function($rootScope) {
    beforeEach(module("main.controllers"));
    var scope;

    beforeEach(inject(function($controller, $rootScope) {
        scope = $rootScope.$new();
        $controller('FeedController', {$scope: scope});

        scope.$digest();
    }));

    it("should fetch posts", function() {
        var posts = scope.fetchPosts(validFeed);
        expect(posts).toBe(true);
        expect(scope.foofeed.post_set.length).toBeGreaterThan(0);
        expect(scope.view.div.ul['posts']).toBeGreaterThan(0); // syntax???
    });
});

describe("Post controllers", function($rootScope) {
    beforeEach(module("main.controllers"));
    var scope;

    beforeEach(inject(function($controller, $rootScope) {
        scope = $rootScope.$new();
        $controller('PostController', {$scope: scope});

        scope.$digest();
    }));

    it("should expand posts", function() {
        var height = scope.view.div.attr('height'); // again, syntax
        var expanded = scope.expandPost();
        expect(expanded).toBe(true);
        expect(scope.view.div.height).toBeGreaterThan(height); // syntax again
        expect(scope.expanded).toBe(true);
    });

    it("should leave already expanded posts alone", function() {
        var height = scope.view.div.attr('height'); // syntax
        var expanded = scope.expandPost();
        expect(expanded).toBe(false);
        expect(scope.view.div.height).toEqual(height); // syntax
        expect(scope.expanded).toBe(true);
    });

    it("should collapse posts", function() {
        var height = scope.view.div.attr('height'); // syntax
        var collapsed = scope.collapsePost();
        expect(collapsed).toBe(true);
        expect(scope.view.div.height).toBeLessThan(height); // syntax
        expect(scope.expanded).toBe(false);
    });
});*/
