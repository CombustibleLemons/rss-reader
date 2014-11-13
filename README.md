# rss-reader
## Milestone 3
### Compiling & Installation
We are primarily using Django and Angularjs, so no direct compilation. ;) However, there are a lot of packages that need to be installed in order to get the system up and runing.

#### Steps
1. Install PostgreSQL
  1. TODO! sub-instructions for getting the PostgresSQL server setup
2. Install pip, virtualenv, and virtualenvwrapper
3. Create a new virtualenv and activate it
4. Navigate to the repository and run `pip install -r requirements`
5. Install karma (DEVON FILL THIS IN)
6. Navigate to `rss-reader/rss_reader` and run `./manage.py migrate` to get the database setup

And you've started an instance of rss-reader!

### Running Code
In the terminal, access the 'rss-reader/rss_reader' directory and type '.manage.py python runserver'. Access 'localhost:8000' via web browser. The rss feed website should be viewable.

### Running Unit Tests
To run unit tests against Django: navigate to the 'rss-reader/rss_reader directory' and enter './manage.py test'

To run unit tests against AngularJS: navigate to the 'rss-reader/rss_reader directory' and enter './manage.py testjs'

### Acceptance Test Suggestions
~suggested acceptance tests here~

### What Is Implemented
An RSS feed that supports a single user, who can make topics, add feeds to topics, delete feeds, and expand and browse posts and feeds.

### Roles and Tasks
Views: Michelle, Jawwad

Controllers: James and Devon (Jawwad and Justyn help)

API: Justyn

Database, models - Lucia

### Changes

We removed the custom User class (RSSUser), as we found the attributes and methods in the default Django User class sufficient. Relatedly, there are no longer unit tests for User.
