'use strict';

/* jasmine specs for controllers go here */

describe('main controllers', function(){
  beforeEach(module('main.controllers'));
    var scope, scope2, ctrl, ctrl2, $httpBackend, response;
    beforeEach(inject(function(_$httpBackend_, $controller, $rootScope) {
      response = [
    {
        "id": 50,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By EVAN J. MANDERY",
        "category": [
            "Oil (Petroleum) and Gasoline",
            "Global Warming",
            "Energy and Power",
            "Colleges and Universities",
            "Endowments"
        ],
        "rights": "",
        "title": "Opinion: The Missing Campus Climate Debate",
        "subtitle": "",
        "content": "Universities must consider divesting from fossil fuels.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/400f58b2/sc/31/mf.gif\" width=\"1\" /><br clear=\"all\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/opinion/sunday/the-missing-campus-climate-debate.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/400f58b2/sc/31/l/0L0Snytimes0N0C20A140C110C0A20Copinion0Csunday0Cthe0Emissing0Ecampus0Eclimate0Edebate0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-01T19:30:04Z",
        "updated": "2014-11-01T19:30:04Z",
        "ackDate": 1414962290.76152,
        "feed": 4
    },
    {
        "id": 49,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By NATE COHN",
        "category": [
            "Presidential Election of 2016",
            "Democratic Party",
            "Midterm Elections (2014)",
            "Republican Party"
        ],
        "rights": "",
        "title": "Midterm Calculus: Why 2014 Isn\u2019t as Good as It Seems for the Republicans",
        "subtitle": "",
        "content": "The party is favored to win the Senate and expand its House majority. But there are few signs that it is making progress toward a national majority.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/400f6956/sc/1/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597119263/u/57/f/642562/c/34625/s/400f6956/sc/1/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597119263/u/57/f/642562/c/34625/s/400f6956/sc/1/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597119263/u/57/f/642562/c/34625/s/400f6956/sc/1/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597119263/u/57/f/642562/c/34625/s/400f6956/sc/1/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597119263/u/57/f/642562/c/34625/s/400f6956/sc/1/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597119263/u/57/f/642562/c/34625/s/400f6956/sc/1/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597119263/u/57/f/642562/c/34625/s/400f6956/sc/1/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597119263/u/57/f/642562/c/34625/s/400f6956/sc/1/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597119263/u/57/f/642562/c/34625/s/400f6956/sc/1/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/upshot/why-2014-is-actually-shaping-up-as-a-bad-republican-year.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/400f6956/sc/1/l/0L0Snytimes0N0C20A140C110C0A20Cupshot0Cwhy0E20A140Eis0Eactually0Eshaping0Eup0Eas0Ea0Ebad0Erepublican0Eyear0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-01T19:30:04Z",
        "updated": "2014-11-01T19:30:04Z",
        "ackDate": 1414962290.75304,
        "feed": 4
    },
    {
        "id": 48,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By LOUISE ARONSON",
        "category": [
            "Elder Care",
            "Design",
            "Elderly",
            "Disabilities",
            "Architecture"
        ],
        "rights": "",
        "title": "Opinion: New Buildings for Older People",
        "subtitle": "",
        "content": "\u201cSilver\u201d design should ensure accessibility and safety.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/400f6959/sc/28/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597119261/u/57/f/642562/c/34625/s/400f6959/sc/28/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597119261/u/57/f/642562/c/34625/s/400f6959/sc/28/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597119261/u/57/f/642562/c/34625/s/400f6959/sc/28/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597119261/u/57/f/642562/c/34625/s/400f6959/sc/28/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597119261/u/57/f/642562/c/34625/s/400f6959/sc/28/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597119261/u/57/f/642562/c/34625/s/400f6959/sc/28/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597119261/u/57/f/642562/c/34625/s/400f6959/sc/28/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597119261/u/57/f/642562/c/34625/s/400f6959/sc/28/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597119261/u/57/f/642562/c/34625/s/400f6959/sc/28/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/opinion/sunday/new-buildings-for-older-people.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/400f6959/sc/28/l/0L0Snytimes0N0C20A140C110C0A20Copinion0Csunday0Cnew0Ebuildings0Efor0Eolder0Epeople0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-01T19:30:04Z",
        "updated": "2014-11-01T19:30:04Z",
        "ackDate": 1414962290.74476,
        "feed": 4
    },
    {
        "id": 47,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By RICHARD FAUSSET",
        "category": [
            "North Carolina",
            "Elections, Senate",
            "Hagan, Kay R",
            "Midterm Elections (2014)",
            "Tillis, Thomas R"
        ],
        "rights": "",
        "title": "North Carolina: In North Carolina, Campaigns for Senate Play to Dislikes in an Effort to Stoke Interest",
        "subtitle": "",
        "content": "Thom Tillis is partial to Exhibit A from his party\u2019s national playbook this year: mentioning his Democratic opponent, Senator Kay Hagan, in the same breath as President Obama, and doing so as often as possible.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/400fa669/sc/1/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597083825/u/57/f/642562/c/34625/s/400fa669/sc/1/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083825/u/57/f/642562/c/34625/s/400fa669/sc/1/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597083825/u/57/f/642562/c/34625/s/400fa669/sc/1/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083825/u/57/f/642562/c/34625/s/400fa669/sc/1/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597083825/u/57/f/642562/c/34625/s/400fa669/sc/1/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083825/u/57/f/642562/c/34625/s/400fa669/sc/1/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597083825/u/57/f/642562/c/34625/s/400fa669/sc/1/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083825/u/57/f/642562/c/34625/s/400fa669/sc/1/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597083825/u/57/f/642562/c/34625/s/400fa669/sc/1/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/us/politics/north-carolina-senate-campaigns-play-to-dislikes-in-effort-to-stoke-interest.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/400fa669/sc/1/l/0L0Snytimes0N0C20A140C110C0A20Cus0Cpolitics0Cnorth0Ecarolina0Esenate0Ecampaigns0Eplay0Eto0Edislikes0Ein0Eeffort0Eto0Estoke0Einterest0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-01T19:52:40Z",
        "updated": "2014-11-01T19:52:40Z",
        "ackDate": 1414962290.73642,
        "feed": 4
    },
    {
        "id": 46,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By JENNIFER STEINHAUER",
        "category": [
            "Elections, Senate",
            "Facebook Inc|FB|NASDAQ",
            "Iowa",
            "Grassley, Charles E",
            "Braley, Bruce",
            "Midterm Elections (2014)"
        ],
        "rights": "",
        "title": "Iowa: Endurance Test of a Race, for Candidates and Voters in Iowa",
        "subtitle": "",
        "content": "Bruce Braley and Joni Ernst have visited all 99 of Iowa\u2019s counties in their Senate race, and voters have been subjected to a litany of negative campaign advertisements.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/400fa66b/sc/1/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597083826/u/57/f/642562/c/34625/s/400fa66b/sc/1/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083826/u/57/f/642562/c/34625/s/400fa66b/sc/1/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597083826/u/57/f/642562/c/34625/s/400fa66b/sc/1/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083826/u/57/f/642562/c/34625/s/400fa66b/sc/1/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597083826/u/57/f/642562/c/34625/s/400fa66b/sc/1/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083826/u/57/f/642562/c/34625/s/400fa66b/sc/1/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597083826/u/57/f/642562/c/34625/s/400fa66b/sc/1/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083826/u/57/f/642562/c/34625/s/400fa66b/sc/1/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597083826/u/57/f/642562/c/34625/s/400fa66b/sc/1/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/us/politics/endurance-test-of-a-race-for-candidates-and-voters-in-iowa.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/400fa66b/sc/1/l/0L0Snytimes0N0C20A140C110C0A20Cus0Cpolitics0Cendurance0Etest0Eof0Ea0Erace0Efor0Ecandidates0Eand0Evoters0Ein0Eiowa0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-01T19:53:40Z",
        "updated": "2014-11-01T19:53:40Z",
        "ackDate": 1414962290.72805,
        "feed": 4
    },
    {
        "id": 45,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By JACK HEALY",
        "category": [
            "Gardner, Cory S",
            "Colorado",
            "Hickenlooper, John W",
            "Democratic Party",
            "Midterm Elections (2014)",
            "Udall, Mark",
            "Endorsements",
            "Republican Party"
        ],
        "rights": "",
        "title": "Colorado: Republicans Setting the Early Pace in Colorado With 104,000 More Ballots",
        "subtitle": "",
        "content": "Early voter returns tracking Colorado\u2019s first major election run entirely through mail-in ballots showed that Republicans had turned in 104,000 more ballots than Democrats.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/400fa668/sc/7/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597083827/u/57/f/642562/c/34625/s/400fa668/sc/7/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083827/u/57/f/642562/c/34625/s/400fa668/sc/7/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597083827/u/57/f/642562/c/34625/s/400fa668/sc/7/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083827/u/57/f/642562/c/34625/s/400fa668/sc/7/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597083827/u/57/f/642562/c/34625/s/400fa668/sc/7/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083827/u/57/f/642562/c/34625/s/400fa668/sc/7/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597083827/u/57/f/642562/c/34625/s/400fa668/sc/7/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083827/u/57/f/642562/c/34625/s/400fa668/sc/7/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597083827/u/57/f/642562/c/34625/s/400fa668/sc/7/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/us/politics/republicans-setting-the-early-pace-in-colorado-with-104000-more-ballots.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/400fa668/sc/7/l/0L0Snytimes0N0C20A140C110C0A20Cus0Cpolitics0Crepublicans0Esetting0Ethe0Eearly0Epace0Ein0Ecolorado0Ewith0E10A40A0A0A0Emore0Eballots0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-01T19:56:28Z",
        "updated": "2014-11-01T19:56:28Z",
        "ackDate": 1414962290.71971,
        "feed": 4
    },
    {
        "id": 44,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By TAMAR LEWIN",
        "category": [
            "Yale University",
            "Annarita Di Lorenzo",
            "Sexual Harassment",
            "New Haven (Conn)",
            "Dr. Michael Simons",
            "Yale School of Medicine"
        ],
        "rights": "",
        "title": "Handling of Sexual Harassment Case Poses Larger Questions at Yale",
        "subtitle": "",
        "content": "Concerns grew about the climate for women at the Yale School of Medicine after a sexual misconduct committee\u2019s ruling to remove the cardiology chief went unheeded.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/400fa659/sc/8/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597083828/u/57/f/642562/c/34625/s/400fa659/sc/8/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083828/u/57/f/642562/c/34625/s/400fa659/sc/8/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597083828/u/57/f/642562/c/34625/s/400fa659/sc/8/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083828/u/57/f/642562/c/34625/s/400fa659/sc/8/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597083828/u/57/f/642562/c/34625/s/400fa659/sc/8/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083828/u/57/f/642562/c/34625/s/400fa659/sc/8/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597083828/u/57/f/642562/c/34625/s/400fa659/sc/8/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083828/u/57/f/642562/c/34625/s/400fa659/sc/8/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597083828/u/57/f/642562/c/34625/s/400fa659/sc/8/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/us/handling-of-sexual-harassment-case-poses-larger-questions-at-yale.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/400fa659/sc/8/l/0L0Snytimes0N0C20A140C110C0A20Cus0Chandling0Eof0Esexual0Eharassment0Ecase0Eposes0Elarger0Equestions0Eat0Eyale0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-01T20:38:14Z",
        "updated": "2014-11-01T20:38:14Z",
        "ackDate": 1414962290.71141,
        "feed": 4
    },
    {
        "id": 43,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By JONATHAN MARTIN",
        "category": [
            "States (US)",
            "CBS Corporation|CBS|NYSE",
            "Elections, State Legislature",
            "Elections, House of Representatives",
            "Democratic Party",
            "Campaign Finance",
            "Midterm Elections (2014)",
            "Republican Party"
        ],
        "rights": "",
        "title": "Both Parties See Campaign Tilting to Republicans",
        "subtitle": "",
        "content": "Republicans entered the final weekend before the midterm elections clearly holding the better hand, but a sour electorate and a large number of undecided voters added a measure of suspense.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/400fa65e/sc/1/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597083829/u/57/f/642562/c/34625/s/400fa65e/sc/1/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083829/u/57/f/642562/c/34625/s/400fa65e/sc/1/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597083829/u/57/f/642562/c/34625/s/400fa65e/sc/1/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083829/u/57/f/642562/c/34625/s/400fa65e/sc/1/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597083829/u/57/f/642562/c/34625/s/400fa65e/sc/1/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083829/u/57/f/642562/c/34625/s/400fa65e/sc/1/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597083829/u/57/f/642562/c/34625/s/400fa65e/sc/1/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597083829/u/57/f/642562/c/34625/s/400fa65e/sc/1/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597083829/u/57/f/642562/c/34625/s/400fa65e/sc/1/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/us/politics/both-parties-see-campaign-tilting-to-republicans.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/400fa65e/sc/1/l/0L0Snytimes0N0C20A140C110C0A20Cus0Cpolitics0Cboth0Eparties0Esee0Ecampaign0Etilting0Eto0Erepublicans0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-01T20:40:41Z",
        "updated": "2014-11-01T20:40:41Z",
        "ackDate": 1414962290.70302,
        "feed": 4
    },
    {
        "id": 42,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By REUTERS",
        "category": [
            "Customs and Border Protection (US)",
            "Post-Traumatic Stress Disorder",
            "Mexico",
            "United States International Relations",
            "Tahmooressi, Andrew"
        ],
        "rights": "",
        "title": "U.S. Marine Veteran Back Home After Months in Mexican Jail",
        "subtitle": "",
        "content": "Andrew Tahmooressi, held for seven months on weapons charges, arrived in his home state of Florida after a court in Mexico ordered his release.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/400ff2d7/sc/42/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597098282/u/57/f/642562/c/34625/s/400ff2d7/sc/42/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597098282/u/57/f/642562/c/34625/s/400ff2d7/sc/42/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597098282/u/57/f/642562/c/34625/s/400ff2d7/sc/42/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597098282/u/57/f/642562/c/34625/s/400ff2d7/sc/42/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597098282/u/57/f/642562/c/34625/s/400ff2d7/sc/42/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597098282/u/57/f/642562/c/34625/s/400ff2d7/sc/42/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597098282/u/57/f/642562/c/34625/s/400ff2d7/sc/42/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597098282/u/57/f/642562/c/34625/s/400ff2d7/sc/42/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597098282/u/57/f/642562/c/34625/s/400ff2d7/sc/42/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/world/americas/us-marine-veteran-back-home-after-months-in-mexican-jail.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/400ff2d7/sc/42/l/0L0Snytimes0N0C20A140C110C0A20Cworld0Camericas0Cus0Emarine0Eveteran0Eback0Ehome0Eafter0Emonths0Ein0Emexican0Ejail0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-01T20:51:08Z",
        "updated": "2014-11-01T20:51:08Z",
        "ackDate": 1414962290.69478,
        "feed": 4
    },
    {
        "id": 41,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By THE ASSOCIATED PRESS",
        "category": [],
        "rights": "",
        "title": "DNA Tests Confirm 3 Dead in Mexico Were U.S. Citizens",
        "subtitle": "",
        "content": "The bodies of the three Americans were among four found shot near the Texas border more than two weeks after they went missing on a visit to Mexico, prosecutors announced.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/40116a69/sc/3/mf.gif\" width=\"1\" /><br clear=\"all\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/aponline/2014/11/01/world/americas/ap-lt-mexico-missing-americans.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/40116a69/sc/3/l/0L0Snytimes0N0Caponline0C20A140C110C0A10Cworld0Camericas0Cap0Elt0Emexico0Emissing0Eamericans0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-01T23:21:46Z",
        "updated": "2014-11-01T23:21:46Z",
        "ackDate": 1414962290.6863,
        "feed": 4
    },
    {
        "id": 40,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By WILLIAM YARDLEY",
        "category": [
            "National Public Radio",
            "Deaths (Obituaries)",
            "Mayes, Bernard",
            "Suicides and Suicide Attempts"
        ],
        "rights": "",
        "title": "Bernard Mayes, 85, Dies; Started First U.S. Suicide Hotline",
        "subtitle": "",
        "content": "Mr. Mayes, a multifaceted Anglican priest, started the first suicide hotline in the United States and a decade later became the founding chairman of National Public Radio.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/40104d46/sc/30/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597087334/u/57/f/642562/c/34625/s/40104d46/sc/30/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087334/u/57/f/642562/c/34625/s/40104d46/sc/30/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597087334/u/57/f/642562/c/34625/s/40104d46/sc/30/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087334/u/57/f/642562/c/34625/s/40104d46/sc/30/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597087334/u/57/f/642562/c/34625/s/40104d46/sc/30/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087334/u/57/f/642562/c/34625/s/40104d46/sc/30/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597087334/u/57/f/642562/c/34625/s/40104d46/sc/30/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087334/u/57/f/642562/c/34625/s/40104d46/sc/30/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597087334/u/57/f/642562/c/34625/s/40104d46/sc/30/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/us/bernard-mayes-85-dies-started-first-us-suicide-hotline.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/40104d46/sc/30/l/0L0Snytimes0N0C20A140C110C0A20Cus0Cbernard0Emayes0E850Edies0Estarted0Efirst0Eus0Esuicide0Ehotline0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-02T00:46:16Z",
        "updated": "2014-11-02T00:46:16Z",
        "ackDate": 1414962290.67795,
        "feed": 4
    },
    {
        "id": 39,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By PETER BAKER and MICHAEL D. SHEAR",
        "category": [
            "Obama, Barack",
            "United States Politics and Government",
            "Democratic Party",
            "Midterm Elections (2014)"
        ],
        "rights": "",
        "title": "Braced for a Shift in Congress, Obama Is Setting a New Agenda",
        "subtitle": "",
        "content": "Expecting a less friendly Congress after the election, aides are mapping out possible compromises with Republicans to expand trade, overhaul taxes and build roads and bridges.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/40104d43/sc/24/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597087335/u/57/f/642562/c/34625/s/40104d43/sc/24/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087335/u/57/f/642562/c/34625/s/40104d43/sc/24/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597087335/u/57/f/642562/c/34625/s/40104d43/sc/24/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087335/u/57/f/642562/c/34625/s/40104d43/sc/24/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597087335/u/57/f/642562/c/34625/s/40104d43/sc/24/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087335/u/57/f/642562/c/34625/s/40104d43/sc/24/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597087335/u/57/f/642562/c/34625/s/40104d43/sc/24/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087335/u/57/f/642562/c/34625/s/40104d43/sc/24/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597087335/u/57/f/642562/c/34625/s/40104d43/sc/24/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/us/braced-for-a-shift-in-congress-obama-is-setting-a-new-agenda.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/40104d43/sc/24/l/0L0Snytimes0N0C20A140C110C0A20Cus0Cbraced0Efor0Ea0Eshift0Ein0Econgress0Eobama0Eis0Esetting0Ea0Enew0Eagenda0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-02T01:10:27Z",
        "updated": "2014-11-02T01:10:27Z",
        "ackDate": 1414962290.6696,
        "feed": 4
    },
    {
        "id": 38,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By ROBERT PEAR",
        "category": [
            "Small Business",
            "Patient Protection and Affordable Care Act (2010)",
            "Health Insurance and Managed Care"
        ],
        "rights": "",
        "title": "Defects Found Before Debut of Health Insurance Site for Small Businesses",
        "subtitle": "",
        "content": "The Obama administration has discovered a number of defects in the online marketplace that will offer health insurance to small-business employees, but said they would be fixed before Nov. 15.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/40104d3d/sc/36/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597087336/u/57/f/642562/c/34625/s/40104d3d/sc/36/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087336/u/57/f/642562/c/34625/s/40104d3d/sc/36/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597087336/u/57/f/642562/c/34625/s/40104d3d/sc/36/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087336/u/57/f/642562/c/34625/s/40104d3d/sc/36/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597087336/u/57/f/642562/c/34625/s/40104d3d/sc/36/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087336/u/57/f/642562/c/34625/s/40104d3d/sc/36/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597087336/u/57/f/642562/c/34625/s/40104d3d/sc/36/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087336/u/57/f/642562/c/34625/s/40104d3d/sc/36/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597087336/u/57/f/642562/c/34625/s/40104d3d/sc/36/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/us/defects-found-before-debut-of-health-insurance-site-for-small-businesses.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/40104d3d/sc/36/l/0L0Snytimes0N0C20A140C110C0A20Cus0Cdefects0Efound0Ebefore0Edebut0Eof0Ehealth0Einsurance0Esite0Efor0Esmall0Ebusinesses0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-02T01:35:42Z",
        "updated": "2014-11-02T01:35:42Z",
        "ackDate": 1414962290.66129,
        "feed": 4
    },
    {
        "id": 37,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By ASHLEY SOUTHALL",
        "category": [
            "Fires and Firefighters",
            "Portland (Me)",
            "Halloween"
        ],
        "rights": "",
        "title": "Fire Kills 5 in Building Near College in Maine",
        "subtitle": "",
        "content": "A three-alarm fire swept through a duplex building in Portland early Saturday morning, killing five people and critically injuring one.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/40104d41/sc/8/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597087337/u/57/f/642562/c/34625/s/40104d41/sc/8/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087337/u/57/f/642562/c/34625/s/40104d41/sc/8/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597087337/u/57/f/642562/c/34625/s/40104d41/sc/8/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087337/u/57/f/642562/c/34625/s/40104d41/sc/8/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597087337/u/57/f/642562/c/34625/s/40104d41/sc/8/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087337/u/57/f/642562/c/34625/s/40104d41/sc/8/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597087337/u/57/f/642562/c/34625/s/40104d41/sc/8/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087337/u/57/f/642562/c/34625/s/40104d41/sc/8/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597087337/u/57/f/642562/c/34625/s/40104d41/sc/8/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/us/fire-kills-people-in-building-near-college-in-maine.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/40104d41/sc/8/l/0L0Snytimes0N0C20A140C110C0A20Cus0Cfire0Ekills0Epeople0Ein0Ebuilding0Enear0Ecollege0Ein0Emaine0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-02T01:40:09Z",
        "updated": "2014-11-02T01:40:09Z",
        "ackDate": 1414962290.65309,
        "feed": 4
    },
    {
        "id": 36,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By KATHARINE Q. SEELYE",
        "category": [
            "Rhode Island",
            "Raimondo, Gina M",
            "Pensions and Retirement Plans",
            "Elections, Governors",
            "Midterm Elections (2014)"
        ],
        "rights": "",
        "title": "In Rhode Island Governor\u2019s Race, Pension Issue Could Hurt Raimondo",
        "subtitle": "",
        "content": "As the state treasurer, Gina M. Raimondo has made painful changes in the pension system. Now running for governor, she is encountering some resentment.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/40104d44/sc/1/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597087338/u/57/f/642562/c/34625/s/40104d44/sc/1/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087338/u/57/f/642562/c/34625/s/40104d44/sc/1/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597087338/u/57/f/642562/c/34625/s/40104d44/sc/1/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087338/u/57/f/642562/c/34625/s/40104d44/sc/1/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597087338/u/57/f/642562/c/34625/s/40104d44/sc/1/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087338/u/57/f/642562/c/34625/s/40104d44/sc/1/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597087338/u/57/f/642562/c/34625/s/40104d44/sc/1/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597087338/u/57/f/642562/c/34625/s/40104d44/sc/1/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597087338/u/57/f/642562/c/34625/s/40104d44/sc/1/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/us/politics/in-rhode-island-governors-race-pension-issue-could-hurt-raimondo.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/40104d44/sc/1/l/0L0Snytimes0N0C20A140C110C0A20Cus0Cpolitics0Cin0Erhode0Eisland0Egovernors0Erace0Epension0Eissue0Ecould0Ehurt0Eraimondo0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-02T01:57:40Z",
        "updated": "2014-11-02T01:57:40Z",
        "ackDate": 1414962290.64462,
        "feed": 4
    },
    {
        "id": 35,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By JULIE HIRSCHFELD DAVIS",
        "category": [
            "Obama, Barack",
            "Speeches and Statements",
            "Milwaukee (Wis)",
            "Portland (Me)",
            "Midterm Elections (2014)"
        ],
        "rights": "",
        "title": "Wistful but Having Fun, Obama Gives Last Push",
        "subtitle": "",
        "content": "The energy is different for Mr. Obama now than it has been in campaigns past, as he travels the country on a final get-out-the-vote push for the midterm elections.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/400fa662/sc/7/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597124943/u/57/f/642562/c/34625/s/400fa662/sc/7/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597124943/u/57/f/642562/c/34625/s/400fa662/sc/7/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597124943/u/57/f/642562/c/34625/s/400fa662/sc/7/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597124943/u/57/f/642562/c/34625/s/400fa662/sc/7/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597124943/u/57/f/642562/c/34625/s/400fa662/sc/7/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597124943/u/57/f/642562/c/34625/s/400fa662/sc/7/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597124943/u/57/f/642562/c/34625/s/400fa662/sc/7/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597124943/u/57/f/642562/c/34625/s/400fa662/sc/7/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597124943/u/57/f/642562/c/34625/s/400fa662/sc/7/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/us/politics/wistful-but-having-fun-obama-gives-last-push-.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/400fa662/sc/7/l/0L0Snytimes0N0C20A140C110C0A20Cus0Cpolitics0Cwistful0Ebut0Ehaving0Efun0Eobama0Egives0Elast0Epush0E0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-02T03:06:28Z",
        "updated": "2014-11-02T03:06:28Z",
        "ackDate": 1414962290.63618,
        "feed": 4
    },
    {
        "id": 34,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By THE ASSOCIATED PRESS",
        "category": [],
        "rights": "",
        "title": "Four Dead After Boat Capsizes Off California Coast",
        "subtitle": "",
        "content": "Officials said none of those aboard were wearing life vests when a large wave capsized a fishing boat off the coast of Northern California on Saturday, the authorities said.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/40116a68/sc/3/mf.gif\" width=\"1\" /><br clear=\"all\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/aponline/2014/11/01/us/ap-us-capsized-boat-four-dead.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/40116a68/sc/3/l/0L0Snytimes0N0Caponline0C20A140C110C0A10Cus0Cap0Eus0Ecapsized0Eboat0Efour0Edead0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-02T05:42:49Z",
        "updated": "2014-11-02T05:42:49Z",
        "ackDate": 1414962290.62786,
        "feed": 4
    },
    {
        "id": 33,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By KENNETH CHANG",
        "category": [
            "Michael Alsbury",
            "Aviation Accidents, Safety and Disasters",
            "Mojave Air and Space Port",
            "Private Spaceflight",
            "Virgin Galactic",
            "Branson, Richard"
        ],
        "rights": "",
        "title": "Virgin Galactic Is Rattled, but Undeterred, by Deadly Space Plane Crash",
        "subtitle": "",
        "content": "The company and federal investigators began their investigations into what caused a space plane to crash Friday in the Mojave Desert, while the pilot killed was identified as Michael Alsbury.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/4010157c/sc/30/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597123121/u/57/f/642562/c/34625/s/4010157c/sc/30/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597123121/u/57/f/642562/c/34625/s/4010157c/sc/30/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597123121/u/57/f/642562/c/34625/s/4010157c/sc/30/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597123121/u/57/f/642562/c/34625/s/4010157c/sc/30/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597123121/u/57/f/642562/c/34625/s/4010157c/sc/30/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597123121/u/57/f/642562/c/34625/s/4010157c/sc/30/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597123121/u/57/f/642562/c/34625/s/4010157c/sc/30/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597123121/u/57/f/642562/c/34625/s/4010157c/sc/30/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597123121/u/57/f/642562/c/34625/s/4010157c/sc/30/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/science/space/virgin-galactic-is-rattled-by-crash-but-undeterred.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/4010157c/sc/30/l/0L0Snytimes0N0C20A140C110C0A20Cscience0Cspace0Cvirgin0Egalactic0Eis0Erattled0Eby0Ecrash0Ebut0Eundeterred0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-02T05:49:54Z",
        "updated": "2014-11-02T05:49:54Z",
        "ackDate": 1414962290.61953,
        "feed": 4
    },
    {
        "id": 32,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By ASHLEY SOUTHALL",
        "category": [
            "Fires and Firefighters",
            "Deaths (Fatalities)",
            "Halloween",
            "Traffic Accidents and Safety",
            "Railroad Accidents and Safety"
        ],
        "rights": "",
        "title": "Deadly Halloween Across the Nation",
        "subtitle": "",
        "content": "At least 15 people were killed and nine others injured in accidents and a fire connected to the festivities from California to New York.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/4010eab5/sc/24/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597089951/u/57/f/642562/c/34625/s/4010eab5/sc/24/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597089951/u/57/f/642562/c/34625/s/4010eab5/sc/24/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597089951/u/57/f/642562/c/34625/s/4010eab5/sc/24/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597089951/u/57/f/642562/c/34625/s/4010eab5/sc/24/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597089951/u/57/f/642562/c/34625/s/4010eab5/sc/24/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597089951/u/57/f/642562/c/34625/s/4010eab5/sc/24/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597089951/u/57/f/642562/c/34625/s/4010eab5/sc/24/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597089951/u/57/f/642562/c/34625/s/4010eab5/sc/24/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597089951/u/57/f/642562/c/34625/s/4010eab5/sc/24/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/02/us/deadly-halloween-across-the-nation.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/4010eab5/sc/24/l/0L0Snytimes0N0C20A140C110C0A20Cus0Cdeadly0Ehalloween0Eacross0Ethe0Enation0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-02T06:15:41Z",
        "updated": "2014-11-02T06:15:41Z",
        "ackDate": 1414962290.61121,
        "feed": 4
    },
    {
        "id": 31,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By JUSTIN GILLIS",
        "category": [
            "Global Warming",
            "Intergovernmental Panel on Climate Change",
            "United Nations",
            "Greenhouse Gas Emissions"
        ],
        "rights": "",
        "title": "U.N. Panel Warns of Dire Effects From Lack of Action Over Global Warming",
        "subtitle": "",
        "content": "In the starkest language they have ever used, climate experts said food shortages, mass extinctions and flooding are likely without immediate action.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/4014157e/sc/31/mf.gif\" width=\"1\" /><br clear=\"all\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/03/world/europe/global-warming-un-intergovernmental-panel-on-climate-change.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/4014157e/sc/31/l/0L0Snytimes0N0C20A140C110C0A30Cworld0Ceurope0Cglobal0Ewarming0Eun0Eintergovernmental0Epanel0Eon0Eclimate0Echange0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-02T10:06:22Z",
        "updated": "2014-11-02T10:06:22Z",
        "ackDate": 1414962290.60285,
        "feed": 4
    },
    {
        "id": 30,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By NATE COHN",
        "category": [
            "Colorado",
            "Elections, Senate",
            "Midterm Elections (2014)",
            "Udall, Mark"
        ],
        "rights": "",
        "title": "Midterm Calculus: Republicans Hold Edge in Early Voting in Colorado",
        "subtitle": "",
        "content": "Democrats are starting to see positive trends with early ballots but still have far to go to give Senator Mark Udall a shot at victory.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/4012a651/sc/30/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597127857/u/57/f/642562/c/34625/s/4012a651/sc/30/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597127857/u/57/f/642562/c/34625/s/4012a651/sc/30/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597127857/u/57/f/642562/c/34625/s/4012a651/sc/30/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597127857/u/57/f/642562/c/34625/s/4012a651/sc/30/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597127857/u/57/f/642562/c/34625/s/4012a651/sc/30/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597127857/u/57/f/642562/c/34625/s/4012a651/sc/30/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597127857/u/57/f/642562/c/34625/s/4012a651/sc/30/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597127857/u/57/f/642562/c/34625/s/4012a651/sc/30/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597127857/u/57/f/642562/c/34625/s/4012a651/sc/30/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/03/upshot/republicans-hold-edge-in-early-voting-in-colorado.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/4012a651/sc/30/l/0L0Snytimes0N0C20A140C110C0A30Cupshot0Crepublicans0Ehold0Eedge0Ein0Eearly0Evoting0Ein0Ecolorado0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-02T11:45:17Z",
        "updated": "2014-11-02T11:45:17Z",
        "ackDate": 1414962290.59447,
        "feed": 4
    },
    {
        "id": 29,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By KAREN E. DEMPSEY",
        "category": [
            "Highlights"
        ],
        "rights": "",
        "title": "Motherlode Blog: When a Teacher Is Arrested for Child Pornography, Students Will Talk",
        "subtitle": "",
        "content": "When a teacher at my children\u2019s elementary school was arrested, the school sent an email asking parents to have older children keep quiet to protect the younger kids. But it\u2019s impossible to put a stop to playground talk.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/4012ae75/sc/19/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597128823/u/57/f/642562/c/34625/s/4012ae75/sc/19/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597128823/u/57/f/642562/c/34625/s/4012ae75/sc/19/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597128823/u/57/f/642562/c/34625/s/4012ae75/sc/19/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597128823/u/57/f/642562/c/34625/s/4012ae75/sc/19/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597128823/u/57/f/642562/c/34625/s/4012ae75/sc/19/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597128823/u/57/f/642562/c/34625/s/4012ae75/sc/19/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597128823/u/57/f/642562/c/34625/s/4012ae75/sc/19/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597128823/u/57/f/642562/c/34625/s/4012ae75/sc/19/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597128823/u/57/f/642562/c/34625/s/4012ae75/sc/19/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://parenting.blogs.nytimes.com/2014/11/02/when-a-teacher-is-arrested-for-child-pornography-students-will-talk/",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/4012ae75/sc/19/l/0Lparenting0Bblogs0Bnytimes0N0C20A140C110C0A20Cwhen0Ea0Eteacher0Eis0Earrested0Efor0Echild0Epornography0Estudents0Ewill0Etalk0C0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-02T12:37:51Z",
        "updated": "2014-11-02T12:37:51Z",
        "ackDate": 1414962290.58607,
        "feed": 4
    },
    {
        "id": 28,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By KATIE HAFNER",
        "category": [],
        "rights": "",
        "title": "Bracing for the Falls of an Aging Nation",
        "subtitle": "",
        "content": "As Americans live longer, fall-related injuries and deaths are rising, and homes for the elderly are tackling the problem in ways large and small \u2014 even by changing the color of their carpeting and toilet seats.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/4014157b/sc/36/mf.gif\" width=\"1\" /><br clear=\"all\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/interactive/2014/11/03/health/bracing-for-the-falls-of-an-aging-nation.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/4014157b/sc/36/l/0L0Snytimes0N0Cinteractive0C20A140C110C0A30Chealth0Cbracing0Efor0Ethe0Efalls0Eof0Ean0Eaging0Enation0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-02T13:43:10Z",
        "updated": "2014-11-02T13:43:10Z",
        "ackDate": 1414962290.57772,
        "feed": 4
    },
    {
        "id": 27,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By LYNN VAVRECK",
        "category": [
            "Elections, Senate",
            "United States Politics and Government",
            "Elections, House of Representatives",
            "Voting and Voters",
            "Midterm Elections (2014)"
        ],
        "rights": "",
        "title": "Midterm Calculus: The Economy Elects Presidents. Presidents Elect Congress.",
        "subtitle": "",
        "content": "While presidential elections are shaped largely by economic performance, the largest factor in midterm elections is the president.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/40134217/sc/1/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597098318/u/57/f/642562/c/34625/s/40134217/sc/1/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597098318/u/57/f/642562/c/34625/s/40134217/sc/1/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597098318/u/57/f/642562/c/34625/s/40134217/sc/1/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597098318/u/57/f/642562/c/34625/s/40134217/sc/1/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597098318/u/57/f/642562/c/34625/s/40134217/sc/1/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597098318/u/57/f/642562/c/34625/s/40134217/sc/1/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597098318/u/57/f/642562/c/34625/s/40134217/sc/1/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597098318/u/57/f/642562/c/34625/s/40134217/sc/1/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597098318/u/57/f/642562/c/34625/s/40134217/sc/1/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/03/upshot/the-economy-elects-presidents-presidents-elect-congress.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/40134217/sc/1/l/0L0Snytimes0N0C20A140C110C0A30Cupshot0Cthe0Eeconomy0Eelects0Epresidents0Epresidents0Eelect0Econgress0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-02T14:00:22Z",
        "updated": "2014-11-02T14:00:22Z",
        "ackDate": 1414962290.56938,
        "feed": 4
    },
    {
        "id": 26,
        "feedURL": "http://www.nytimes.com/services/xml/rss/nyt/US.xml",
        "author": "By NATE COHN",
        "category": [
            "Colorado",
            "Democratic Party",
            "Midterm Elections (2014)",
            "Republican Party"
        ],
        "rights": "",
        "title": "Midterm Calculus: It May Be Too Late, but Colorado Early Ballots Are Shifting Toward Democrats",
        "subtitle": "",
        "content": "It\u2019s far from clear if this improvement in Democratic prospects will be enough to whittle away the Republican advantage.<img border=\"0\" height=\"1\" src=\"http://rss.nytimes.com/c/34625/f/642562/s/40145f49/sc/1/mf.gif\" width=\"1\" /><br clear=\"all\" /><br /><br /><a href=\"http://da.feedsportal.com/r/211597133646/u/57/f/642562/c/34625/s/40145f49/sc/1/rc/1/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597133646/u/57/f/642562/c/34625/s/40145f49/sc/1/rc/1/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597133646/u/57/f/642562/c/34625/s/40145f49/sc/1/rc/2/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597133646/u/57/f/642562/c/34625/s/40145f49/sc/1/rc/2/rc.img\" /></a><br /><a href=\"http://da.feedsportal.com/r/211597133646/u/57/f/642562/c/34625/s/40145f49/sc/1/rc/3/rc.htm\" rel=\"nofollow\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597133646/u/57/f/642562/c/34625/s/40145f49/sc/1/rc/3/rc.img\" /></a><br /><br /><a href=\"http://da.feedsportal.com/r/211597133646/u/57/f/642562/c/34625/s/40145f49/sc/1/a2.htm\"><img border=\"0\" src=\"http://da.feedsportal.com/r/211597133646/u/57/f/642562/c/34625/s/40145f49/sc/1/a2.img\" /></a><img border=\"0\" height=\"1\" src=\"http://pi.feedsportal.com/r/211597133646/u/57/f/642562/c/34625/s/40145f49/sc/1/a2t.img\" width=\"1\" />",
        "generator": "",
        "guid": "http://www.nytimes.com/2014/11/03/upshot/it-may-be-too-late-but-colorado-early-ballots-are-shifting-toward-democrats.html",
        "url": "http://rss.nytimes.com/c/34625/f/642562/s/40145f49/sc/1/l/0L0Snytimes0N0C20A140C110C0A30Cupshot0Cit0Emay0Ebe0Etoo0Elate0Ebut0Ecolorado0Eearly0Eballots0Eare0Eshifting0Etoward0Edemocrats0Bhtml0Dpartner0Frss0Gemc0Frss/story01.htm",
        "contributor": "",
        "pubDate": "2014-11-02T17:28:24Z",
        "updated": "2014-11-02T17:28:24Z",
        "ackDate": 1414962290.56102,
        "feed": 4
    }];

      $httpBackend = _$httpBackend_;
      $httpBackend.expectGET('feeds/4/posts').respond(response);
      scope = $rootScope.$new();
      scope2 = $rootScope.$new();
      ctrl = $controller('FeedCtrl', {$scope: scope});
      $httpBackend.flush();
      scope.$digest();
    }));

    it('contains 10 posts', function() {
      expect(scope.posts.length).toBe(25);
    });

    /* feedController */



    /* test fecthPosts()
       a = self.fetchPosts(validFeed)
       expectTrue(a)
       self.view.div.list.count = 0 */


    /* test fecthPosts()
       a = self.fetchPosts(invalidFeed)
       expectFalse(a)
       self.view.div.list.count = 0 */

    /* test unsubscribe()
       a = self.getTopicModel()
       originalCount = len(a.Feedlist)
       b = self.unsubscribe(a)
       expectTrue(b)
       expectZero(len(a.feedList) + originalCount)
       checkList */

    /* postController */

    /* test expand()
       height = self.view.div.attr('height')
       b = self.expand()
       expectTrue(b)
       expectGreater(self.view.div.height, height)
       viewsrc = self.view.dir.a.viewsrc_link()
       self.expanded == True */

});
