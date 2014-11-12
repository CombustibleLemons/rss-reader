###Compiling
~how to compile here~
PYTHON MAGIC?

###Running Code
In the terminal, access the 'rss-reader/rss_reader' directory and type 'manage.py python runserver'. Access 'localhost:8000' via web browser. The rss feed website should be viewable.

###Running Unit Tests
In the terminal, in the 'rss-reader/rss_reader directory', type 'manage.py python test'

###Acceptance Test Suggestions
~suggested acceptance tests here~

###What Is Implemented
An RSS feed that supports a single user, who can make topics, add feeds to topics, delete feeds, and expand and browse posts and feeds.

###Roles and Tasks
Views: Michelle, Jawwad

Controllers: James and Devon (Jawwad and Justyn help)

API: Justyn

Database, models - Lucia

###Changes

We removed the custom User class (RSSUser), as we found the attributes and methods in the default Django User class sufficient. Relatedly, there are no longer unit tests for User.
