# rss-reader
## Milestone 3
### Compiling and Installation
We are primarily using Django and Angularjs, so no direct compilation. ;) However, there are a lot of packages that need to be installed in order to get the system up and running.

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
~suggested acceptance tests here~

### What Is Implemented
An RSS feed that supports a single user, who can make topics, add feeds to topics, delete feeds, and expand and browse posts and feeds.

### Roles and Tasks
Views and front-end controllers: Michelle, Jawwad

Controller unit tests: James and Devon

API and back-end controllers: Justyn

Models, API, and Model Unit Tests: Lucia and Justyn

### Changes

We removed the custom User class (RSSUser), as we found the attributes and methods in the default Django User class sufficient. Relatedly, there are no longer unit tests for User. Model methods no longer return bools upon success/failure, and unit tests have been changed to reflect this change. We found a PostController class to be unnecessary, and PostController methods are now implemented in the FeedController.
