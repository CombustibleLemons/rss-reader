'use strict';

/* jasmine specs for controllers go here */

describe("Navigation controllers", function() {
    beforeEach(module("main.controllers"));
    var scope, navigationController;
    scope = $rootScope.$new();
    navigationController = $controller('NavigationController', {$scope: scope});

    it("should add topics", function() {
        var origTopicSet = scope.user.topic_set;
        expect(scope.addTopic('foo')).toBe(true);
        var newTopicSet = scope.user.topic_set;
        expect(origTopicSet.length + 1).toEqual(newTopicSet.length);
        // expect topic to be in topic set, uncertain of syntax at this time
    });

    it("should remove topics", function() {
        var origTopicSet = scope.user.topic_set;
        expect(scope.removeTopic('foo')).toBe(false);
        scope.addTopic('foo');
        expect(scope.removeTopic('foo')).toBe(true);
        expect(scope.user.topic_set.length).toEqual(0);
    });

    it("should fetch all of the topics", function() {
        expect(scope.fetchTopics()).toBe(true);
        expect(scope.user.topic_set.length).toEqual(0);
        scope.addTopic('foo');
        expect(scope.fetchTopics()).toBe(true);
        expect(scope.topic_set.length).toEqual(1);
    });

    it("should expand and minimize topics", function() {
        scope.addTopic('foo');
        expect(scope.expandTopic('foo')).toBe(true);
        scope.user.topic_set['foo'].controller.addFeedtoTopic('validURL');
        expect(scope.view.div.ul[feeds].css('display')).toBe('visible'); // again, totally wrong syntax probably
        expect(scope.minimize('foo')).toBe(true);
        expect(scope.view.div.ul[feeds].css('display')).toBe('none'); // probably even more wrong syntax
    });
});

describe("Search controllers", function() {
    beforeEach(module("main.controllers"));
    var scope, searchController;
    scope = $rootScope.$new();
    searchController = $controller('SearchController', {$scope: scope});

    it("should add feeds to uncategorized", function() {
        var originalFeedSet = scope.user.topic_set['uncategorized']; // again, bad syntax
        expect(scope.addFeed('pretendthisisavalidurl')).toBe(true);
        var newFeedSet = scope.user.topic_set['uncategorized']; // yet again
        expect(originalFeedSet.length).toEqual(newFeedSet.length + 1);
        // expect feed to be in uncategorized topic, uncertain of syntax at this time
    });
});

describe("Topic controllers", function() {
    beforeEach(module("main.controllers"));
    var scope, topicController;
    scope = $rootScope.$new();
    topicController = $controller('TopicController', {$scope: scope});

    it("should edit names", function(), {
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

describe("Feed controllers", function() {
    beforeEach(module("main.controllers"));
    var scope, feedController;
    scope = $rootScope.$new();
    feedController = $controller('FeedController', {$scope: scope});

    it("should fetch posts", function() {
        var posts = scope.fetchPosts(validFeed);
        expect(posts).toBe(true);
        expect(scope.foofeed.post_set.length).toBeGreaterThan(0);
        expect(scope.view.div.ul['posts']).toBeGreaterThan(0); // syntax???
    });

describe("Post controllers", function() {
    beforeEach(module("main.controllers"));
    var scope, postController;
    scope = $rootScope.$new();
    postController = $controller('PostController', {$scope: scope});

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
});