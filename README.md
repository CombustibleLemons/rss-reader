# rss-reader
## Milestone 3
### Compiling and Installation
We are primarily using Django and Angularjs, so there is no direct compilation. However, there are a lot of packages that need to be installed in order to get the system up and running.

##### Steps
1. Install PostgreSQL:
  1. TODO! sub-instructions for getting the PostgresSQL server setup
2. Install pip, virtualenv, and virtualenvwrapper
3. Create a new virtualenv and activate it
4. Navigate to the repository and run `pip install -r requirements`
5. Install karma:
  1. Install npm
  2. Run `npm install -g karma`
  3. Run `npm install -g jasmine`
  4. Run `npm install -g karma-jasmine`
  5. Run `npm install -g karma-chrome-launcher`
  6. Run `npm install -g karma-cli` (not strictly necessary but it makes it much easier)
  7. Have a cookie on us.
  8. Aw shucks, have another.
    NOTE: the -g is a global install. you can install locally to a project with --save-dev. the official
guidelines recommend you do both if you have trouble.
6. Navigate to `rss-reader/rss_reader` and run `./manage.py migrate` to get the database setup

And you've started an instance of rss-reader!

### Running Code
In the terminal, access the `rss-reader/rss_reader` directory and type `.manage.py python runserver`.  Access `localhost:8000` via web browser. The rss feed website should be viewable.

### Running Unit Tests
To run unit tests against Django, navigate to the `rss-reader/rss_reader` directory and enter `./manage.py test` into the terminal. This runs the model and API tests.

To run unit tests against AngularJS: navigate to the `rss-reader/rss_reader directory` and enter `./manage.py testjs` into the terminal.

### Acceptance Test Suggestions
To run front-end acceptance tests, first run the server and access 'localhost:8000' via a web browser.

#### Uncategorized Topic
* Look to the navigation bar on the left side. A section of topics called 'Uncategorized' should be automatically present.
* Click on the 'x' next to 'Uncategorized'. The topic should not disappear because 'Uncategorized' cannot be removed.

#### Add a Topic
* Click on 'Add a topic'. A popup should appear with a box to enter a topic name.
* Click on 'Cancel'. The screen should return to the original home page and the popup should disappear.
* Click on 'Add a topic' again and this time enter the name 'Penguins' in the 'Topic Name' bar. Click on 'Add Topic'. The popup should close, the screen returns to the home page, and a topic 'Penguins' is now present in the navigation bar to the left.

#### Edit and Delete a Topic
* Click on 'edit' next to the 'Penguins' Topic. An empty box should appear to its right. Enter 'Giraffes' into the box and press enter. The name of the Topic originally called 'Penguins' should now read as 'Giraffes'.
* Press the 'x' to the right of the Topic 'Giraffes'. The Topic should now not appear in the list of Topics in the navigation bar.

#### Add a Feed
* Copy and paste 'http://interglacial.com/rss/pokey_the_penguin.rss' into the 'Search for a feed' bar on the left side. Press enter. You should now have a feed 'Pokey the Penguin' under the Topic 'Uncategorized'. Currently moving Feeds to Topics other tha Uncategorized has not been implemented on the front-end, though it works on the back-end.

#### View a Feed
* Click on 'Pokey the Penguin' in the navigation bar. One post titled 'pokey and the dust storm' should show in the middle of the screen now.
* Click on the 'pokey and the dust storm' post. The grey section will expand and the link 'View Source' will appear.
* Click on 'View Source'. You will be redirected to a webcomic involving a penguin.

#### Miscellaneous
* Click on the 'Login', 'Donate', and 'About' buttons. The page should stay the same because the 'login' button is to be implemented in iteration 2 and the other two have not been directed to pages yet.

### What Is Implemented
An RSS feed that supports a single user, who can make topics, add feeds to topics, delete feeds, and expand and browse posts and feeds.

### Roles and Tasks
Views and front-end controllers: Michelle, Jawwad

Controller unit tests: James and Devon

API and back-end controllers: Justyn

Models, API, and Model Unit Tests: Lucia and Justyn

### Changes

#### Model
We removed the custom User class (RSSUser), as we found the attributes and methods in the default Django User class sufficient. Relatedly, there are no longer unit tests for User.

Model methods no longer return bools upon success/failure, and unit tests have been changed to reflect this change.

We have specified that Users must have a Uncategorized Topic, with unit tests to reflect this change.

#### Controller/View
We found a PostController class to be unnecessary, and PostController methods are now implemented in the FeedController.

We have moved adding, deleting, and moving a Feed to a particular Topic to iteration 2. Currently Feeds can only be added and deleted from the Uncategorized Topic.

We have moved searching for feeds by keyword via the addfeed/search bar to iteration 2. Currently, inputting an rss feed *url* into the addfeed/search bar causes a search of the database, to ensure that a new model object is not created if the feed already exists.

#### Managerial

Communicatively, we have started using Slack for instant messaging and realtime communication.
