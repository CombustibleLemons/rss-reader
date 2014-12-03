# RSS-reader
## Milestone 5
### Compiling and Installation
We are primarily using Django and AngularJS, so there is no direct compilation. However, there are several packages that need to be installed in order to get the system up and running. We **heavily recommend** Linux to install the necessary packages.
###### Step Zero: Clone the Repository
In the terminal, clone our git repository with the command `git clone https://github.com/CombustibleLemons/rss-reader.git`

###### Step One: Install PostgreSQL v.9.3 (if it is not installed already)
  1. Install postgresql
    * Run `[your favourite package manager] install postgresql`
  2. Initialize the postgres database and user
    * The root folder contains the initialization script. Run `./postgres-setup.sh`
    * If there are problems with initializing with the script, manually initialize the database and user:
        2.  ~~[For Arch]: run `systemctl start postgresql`. Then run `sudo -i -u postgres` and enter your password when prompted.~~
        3. [For OSX]: Run `sudo su - postgres` and enter the password for your computer. Access the postgres shell with `. ./pg_env.sh`.
        4. Run `createdb feeddb;` to make a database named feeddb
        4. Run `createuser -P combustible;` to make a user named combustible
        5. Run `psql -c 'GRANT ALL PRIVILEGES ON DATABASE feeddb TO combustible;'`
        6. Run `exit` to exit the postgres shell.

        Note: If you would like to change username or password, you can do so in the `~/rss_reader/rss_reader/conf/settings.py` file


###### Step Two: Install virtualenv and other packages
  1. Install pip, virtualenv, and virtualenvwrapper (if they are not otherwise installed)
  2. It is easiest to set up a virtualenv by following [this tutorial](https://virtualenvwrapper.readthedocs.org/en/latest/).
  3. After adding the `source` command to your shell startup file, use `mkvirtualenv YOUR_ENV_NAME` to make a new virtualenv.
  4. Access your virtual environment with `workon YOUR_ENV_NAME`
  4. Navigate to the repository `~/rss_reader/` and run `pip install -r requirements.txt` to install the required packages.

###### Step Three: Install karma
 1. Install npm
  2. Run `npm install -g karma`
  3. Run `npm install -g jasmine`
  4. Run `npm install -g karma-jasmine`
  5. Run `npm install -g karma-chrome-launcher`
  6. Run `npm install -g karma-cli` This is not strictly necessary, but makes things much easier.

    *Note:* the `-g` is a global install. You can install locally to a project with `--save-dev`. The official
guidelines recommend you do both if you have trouble.

###### Step Four: Start the RSS-reader

  1. Navigate to `~/rss-reader/rss_reader/` and run `./manage.py migrate` to set up the database.
  3. In the terminal, run `./manage.py installwatson`, then `./manage.py buildwatson`. These commands initialize watson, a Django search application.

And you've started an instance of the RSS-reader!

###### Flushing the Database

If the database is mistakenly edited when creating Feed objects, you will need to flush the database.
######  Ubuntu:
1. Navigate to `~/rss-reader/rss_reader/`
2. Run `./flush_database.sh` to flush the database
3. Run `./postgres-setup.sh` to reset the database (see Step One of the installation)

######  Other:
* ~~`sudo -i -u postgres` (or Mac equivalent)~~
* `sudo su - postgresql`, and enter the password if prompted
* `drop database feeddb`
* `drop user combustible`
* `createdb feeddb`
* `createuser -P combustible`
* `psql -c 'GRANT ALL PRIVILEGES ON DATABASE feeddb TO combustible;'`
    * If psql does not work, run `../pg_env.sh`


After remaking the database, do Step Four of installation to make migrations and reinitialize watson.

### Functionality

######  Main functionality
Curatr basically allows you to subscribe to feeds and group them within particular topic categories. The user can add and remove topics to put feeds in. The user can search for feeds, using either an rss url or a string. Once subscribed to a feed, the user selects a topic to add the feed to, with a default Uncategorized topic. Each feed can only belong under one topic, but feeds can be moved from one topic to another. The user can also unsubscribe from feeds. 

Regarding posts in one feed, the user can sort the posts alphabetically, by date, by length, and by read/unread status. The user can expand posts to read them as well as mark them as read or unread. The user can also filter the posts to only view unread posts.

The user has the ability to queue feeds at their pleasure, which releases a certain number of posts to the user in a specified time interval. 
Scenario 1: Say that the user wants to read 1 post per week of the comic **xkcd**. The user would be able to set the **xkcd** feed to be a queue and could choose the time interval of 1 week for which he or she receives 1 post. Every week, then, the user would receive one **xkcd** post rather than the daily post that a normal, unqueued **xkcd** feed would give. 
Scenario 2: Conversely, if the user chose to get 5 posts of **xkcd** per day, old posts that are stored in the database will be pulled to give the user these additional posts, starting from the oldest and converging to the newest. 

This gives the user several functionalities:
* read fewer posts of a feed than usual
* read more posts of a feed than usual
* read old posts that are stored in the database
* set a convenient time interval for receiving new posts

######  Settings functionality
The user can change their password in the user settings and can measure their reading speed in the Reading Test section.


### Usage Tutorial
###### Automatic initialization (if you want to start with a user and some topics/feeds already initialized)
1. Run our intitalization script from `~/rss_reader/rss_reader` with `./manage.py shell < init_script.py`
2. Access `localhost:8000` via web browser, log in with the credentials Username: **lemon** and Password: **lemon**
3. You should see several Topics (Comics, Science, and Uncategorized) along with a few feeds in each topic

###### Manual initialization

######  Register a user
1. Access `localhost:8000` via web browser and click on 'Register Here'
2. Enter a username and password
3. You're done!

######  Add a Topic
1. Click on "Add a topic" in the sidebar
2. You should see a popup. Enter the name of your topic in the field and click on "Add Topic"

######  Search for a feed
1. Enter keywords or an rss url in the searchbar
2. If you enter keywords, the results shown will be the search results from our database of feeds (and therefore it is possible that the feed you expect may not show up). If you entered a url, Curatr will fetch the feed for you

######  Subscribe to feeds
1. Search for a feed (as above)
2. Click on the add icon to the right of your desired feed
3. A popup should open asking you to choose a topic
4. Choose your desired topic and click "Subscribe"

######  View a feed
1. Expand one of your topics in the sidebar
2. Click on the feed you wish to view

######  Unsubscribe from a feed
1. Click on "Edit" in the sidebar
2. Click the "X" next to the feed you wish to unsubscribe from
3. Click on "Save changes"

######  Rename a topic
1. Click on "Edit" in the sidebar
2. Click on the edit icon to the right of the topic. The icon is a diagonal pencil
3. Enter the new name of the topic in the field that appears
4. Click on "Submit"
5. If you wish to not rename the topic after you click the icon, just leave the field blank and click "submit" 

######  Rearrange feeds within topics
1. Click on "Edit" in the sidebar
2. Drag and drop the feeds as you please
3. You can drag and drop the feeds among different topics
4. Click on "Save changes"

######  Delete a topic
1. Click on "Edit" in the sidebar
2. Click on the "X" to the right of the topic you wish to delete
3. Click on "Save changes"

######  Expand a post
1. View a feed (instructions above)
2. Click on a post to expand it

######  Mark a post as read/unread
1. View a feed (instructions above)
2. Click on the read/unread switch to the right of the post you wish to mark

######  Sort posts 
1. View a feed (instructions above)
2. Click on "Sort by" in the top-right corner
3. Choose to sort by alphabet, time, length or unread status

###### Only see unread posts
1. View a feed (instructions above)
2. Click on "View only unread" at the top-right
3. You can reverse this by clicking on "View all posts"

######  Change password
1. Click on the gear icon to the right of the searchbar
2. Click on user settings
3. Enter your new password in the field and click "Submit"

