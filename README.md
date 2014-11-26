# RSS-reader
## Milestone 4.B
### Compiling and Installation
We are primarily using Django and AngularJS, so there is no direct compilation. However, there are a lot of packages that need to be installed in order to get the system up and running. We heavily recommend Linux or Ubuntu to install the necessary packages.
###### Step Zero: Clone the Repository
Clone our git repository with the command `git clone https://github.com/CombustibleLemons/rss-reader.git`

###### Step One: Install PostgreSQL v.9.3 (if it is not installed already)
  1. Install postgresql
    2. Run `[your favourite package manager] install postgresql`
  3. Initialize the postgres database and user
    4. There is a script in the `~/rss_reader` folder that can be run with `./postgres-setup.sh`
    5. Alternatively, you can set everything up manually if you want (or if the script does not work with your configuration):
        2.  [For Arch]: run `systemctl start postgresql`. Then run `sudo -i -u postgres` and enter your password when prompted.
        3. [For OSX]: Run `sudo su postgres` and enter the password for your computer to get the shell as a postgres user.
        4. Run `createdb feeddb` to make a database named feeddb
        4. Run `createuser -P combustible` to make a user named combustible
        5. Run `psql -c 'GRANT ALL PRIVILEGES ON DATABASE feeddb TO combustible;'`
        6. Run `exit`
    
        Note: If you would like to change username or password, you can do so in the `~/rss_reader/rss_reader/conf/settings.py` file
    

###### Step Two: Install virtualenv and other packages
  1. Install pip, virtualenv, and virtualenvwrapper (if they are not otherwise installed)
  2. Create a new virtualenv and activate it
  3. Navigate to the repository `~/rss_reader/` and run `pip install -r requirements.txt`

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

  1. Navigate to `~/rss-reader/rss_reader/` and run `./manage.py migrate` to get the database set up
  2. Have a cookie, on us
  3. Aw shucks, have another

And you've started an instance of the RSS-reader!

### Running Code
In the terminal, access the `~/rss-reader/rss_reader/` directory and type `./manage.py runserver`.  Access `localhost:8000` via web browser. The RSS feed website should be viewable.

### Running Unit Tests
To run Django unit tests, make sure you are the postgres user (as described in Step 1.2 above) and run `psql -c 'ALTER ROLE combustible CREATEDB;'` After, navigate to the `~/rss-reader/rss_reader/` directory and enter `./manage.py test` into the terminal. This runs the model and API tests.

To run AngularJS unit tests, navigate to the `~/rss-reader/rss_reader/` directory and enter `./manage.py testjs` into the terminal.

### Acceptance Test Suggestions

1. Automatic initialization (if you want to start with a user and some topics/feeds already initialized)
    2. Run our intitalization script from `~/rss_reader/rss_reader` with `./manage.py shell < init_script.py`
    3. Access `localhost:8000` via web browser, log in with the credentials Username: **lemon** and Password: **lemon**
    4. You should see several Topics (Comics, Science, and Uncategorized) along with a few feeds in each topic
2. Manual initialization (if you want to create a user and add topics/feeds yourself)
    3. Make sure you are running the server as per above and access `localhost:8000` in a web browser
    4. Click on the 'Register here!' link. You will be redirected to a register page. Enter the Username **lemon** and Password **lemon** and press the **register** button. You will be redirected back to the login page. Enter the username and password that you just registered. You should see a blank page with only an Uncategorized section on the left side. 
    5. Click on **Add a topic** and enter **Science**. Click **Add Topic** directly underneath it. The **Science** topic should be on the left side now. Follow the same process to add the **Comics** topic. 
    6. Enter the url "http://xkcd.com/rss.xml" in the search box on the top of the page. Press enter and choose **xkcd** from the list of results that are displayed. In the popup that displays, select the topic **Comics** and click **Subscribe**. Follow the same sequence of events to add the urls "http://www.questionablecontent.net/QCRSS.xml", "http://broodhollow.chainsawsuit.com/feed/", and "http://rss.escapistmagazine.com/videos/list/1.xml" to the **Comics** topic.
    7. Enter the url "http://rss.nytimes.com/services/xml/rss/nyt/Science.xml" in the search box on the top of the page. Press enter and choose **NYT > Science** from the list of results that are displayed. In the popup that displays, select the topic **Science** and lick **Subscribe** Follow the same sequence of events to add the urls "http://feeds.feedburner.com/kernelmag?format=xml" and "http://www.popsci.com/taxonomy/term/100136/feed" to the **Science** topic.

##### Register/Login Tests
1. Registering
    1. If you are logged in, press the logout button. Click the **Register here!** link.
    2. Enter **Supercalifragilisticexpialidocious** in the Username field and **lemon** in the Password field. Press the **register** button. FINISHHHHHH
    3. Enter **~bubbles~** in the Username field and **bub** in the Password field. Press the **register** button. FINISHHHHHH
    4. Re-navigate to the register page and enter the valid Username **Chris** and the Password **bro**. Press the **register** button. You should now have been redirected to the login page.
5. Logging In
    6. Enter **Daisy** in the Username field and **flower** in the Password field. Press the **login** button. You will be redirected back to the same login page because the User **Daisy** does not exist.
    6. Enter **Christopher** in the Username field and **bro** in the Password field. Press the **login** button. You will be redirected back to the same login page again because the username was incorrect.
    6. Enter **Chris** in the Username field and **bub** in the Password field. Press the **login** button. You will be redirected back to the same login page again because the password was incorrect.
    7. Enter correct fields this time (Username=**lemon**, Password=**lemon**). You will be redirected to the rss reader's home page, with your previously-added topics on the left side.

##### Uncategorized Topic Tests
* Look to the navigation bar on the left side. An **Uncategorized** Topic should be automatically present.
* Clicking on the **x** next to **Uncategorized** should have no effect; **Uncategorized** cannot be removed.

##### General Navigation Bar Tests
* Click on **Comics**. The Topic should expand to show 4 feeds: **xkcd.com**, **QC RSS**, **Broodhollow**, and **Zero Punctuation**.
* Click on **Science**. The Topic should expand, and the **Comics** Topic should collapse.
* Click on **Comics** again to expand the Topic again. Click on the **xkcd.com** Feed, and a list of Posts should appear on the right.
* Click on the first Post in the **xkcd.com** Feed's Post list. It should expand to show a the post's content, in this case a comic, and a link labeled **View Source**.
* Click on **View Source** - you should be redirected to the Post's website.

##### Adding, Editing, and Deleting Topics Tests
* Click on **Add a Topic**. You should see a popup asking you to enter a topic name. Click on **Cancel**. The popup should close with no topics having been added.
* Click on **Add a Topic** again. This time, enter **News** and press **Add Topic**. The popup should close, with the new Topic **News** now present on the left side navigation bar. 
* Click on **News**. Click on the **edit** button next to the name. A field should now appear in which the user can enter a new name for the Topic. Type **Sports News** and press enter. The name of the Topic should now be **Sports News**.
* Click on the **x** next **Sports News**. The topic should now no longer be seen on the navigation bar.
* BLANK INPUT
* LONG INPUT

##### Adding, Searching, and Deleting Feeds Tests
* Copy "http://www.eurekalert.org/rss/technology_engineering.xml" to the search box at the top of the page. Press enter. A list of results should display underneath.
* Click on the top link, **Eurekalert**. A popup should display and ask which Topic to enter the feed into. Click on the radio button next to **Science** and press the **Subscribe** button at the bottom. The popup should close. Click on the **Science** topic to the left. It should expand and have **Eurekalert** as a feed in it now.
* Click on **Eurekalert**. It should display the posts in this feed to the right.
* Copy "http://www.eurekalert.org/rss/technology_engineering.xml" once again into the top search box and press enter. Once again, click on the top **Eurekalert** link. Red text should display saying "You are already subscribed to that feed" and the feed should not be added again.
* Click on the **-** (minus) sign before the name of the feed (**Eurekalert**). The feed should now disppear from the list.
* In the search box at the top of the page, enter the keyword **eurekalert** and press enter. Underneath should display the link to **eurekalert** that we saw before when we entered the link. Click on it again. Choose the **Science** topic from the list and again click **Subscribe**.
* In the navigation bar, click the **x** next to the Topic **Science**. This should eliminate **Science** and all of the feeds that it contains, including the newly-added **Eurekalert**.
* INCORRECT INPUT URL
* KEYWORD WITH NO RESULTS
* MOVING FEEDS BETWEEN TOPICS?

### What Is Implemented 
Laterrrrr

### Roles and Tasks
Views and front-end controllers: Michelle, Jawwad

Controller unit tests: James and Devon

API and back-end controllers: Justyn

Models, API, and model unit tests: Lucia and Justyn

### Changes
Queue???



# RSS-reader
## Milestone 3.B
### Compiling and Installation
We are primarily using Django and AngularJS, so there is no direct compilation. However, there are a lot of packages that need to be installed in order to get the system up and running. We heavily recommend Linux or Ubuntu to install the necessary packages.

###### Step One: Install PostgreSQL
  1. Run `[your favourite package manager] install postgresql`
  2.  Depending on your OS:

  For Arch: run `systemctl start postgresql`. Then run `sudo -i -u postgres` and enter your password when prompted.

  For OSX: Run `sudo su postgres` and enter the password for your computer to get the shell as a postgres user.
  3. Run `createdb feeddb` to make a database named feeddb
  4. Run `createuser -P combustible` to make a user named combustible
  5. Run `psql -c 'GRANT ALL PRIVILEGES ON DATABASE feeddb TO combustible;'`
  6. Run `exit`
  7. Run `python manage.py migrate`

###### Step Two: Install virtualenv and other packages
  1. Install pip, virtualenv, and virtualenvwrapper
  2. Create a new virtualenv and activate it
  3. Navigate to the repository and run `pip install -r requirements`

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
  1. Navigate to `rss-reader/rss_reader` and run `./manage.py migrate` to get the database setup
  2. Have a cookie, on us
  3. Aw shucks, have another

And you've started an instance of the RSS-reader!

### Running Code
In the terminal, access the `rss-reader/rss_reader` directory and type `./manage.py python runserver`.  Access `localhost:8000` via web browser. The RSS feed website should be viewable.

### Running Unit Tests
To run Django unit tests, navigate to the `rss-reader/rss_reader` directory and enter `./manage.py test` into the terminal. This runs the model and API tests.

To run AngularJS unit tests, navigate to the `rss-reader/rss_reader` directory and enter `./manage.py testjs` into the terminal.

### Acceptance Test Suggestions

We have provided a script that initializes a user with a few topics and feeds. To run the script, run `./manage.py shell < init_script.py`.

To run front-end acceptance tests, first run the server and access 'localhost:8000' via a web browser. If the `init_script` was successful, there should already be "Comics" and "Science" Topics, alongside an "Uncategorized" Topic.

#### Uncategorized Topic
* Look to the navigation bar on the left side. An 'Uncategorized' Topic should be automatically present.
* Clicking on the 'x' next to 'Uncategorized' should have no effect; 'Uncategorized' cannot be removed.

#### Navigation
* Click on 'Comics'. The Topic should expand to show 4 feeds: 'xkcd.com', 'QC RSS', 'Broodhollow', and 'Zero Punctuation'.
* Click on 'Science'. The Topic should expand, and the 'Comics' Topic should collapse.
* Click on 'Comics' again to expand the Topic again. Click on the 'xkcd.com' Feed, and a list of Posts should appear on the right.
* Click on the first Post in the 'xkcd.com' Feed's Post list. It should expand to show a the post's content, in this case a comic, and a link labeled 'View Source'.
* Click on 'View Source' - you should be redirected to the Post's website.

#### Add a Topic
* Click on 'Add a topic'. A popup should appear with a box to enter a topic name.
* Click on 'Cancel'. The screen should return to the original home page and the popup should disappear.
* Click on 'Add a topic' again and this time enter the name 'Penguins' in the 'Topic Name' bar. Click on 'Add Topic'. The popup should close, the screen returns to the home page, and a topic 'Penguins' is now present in the navigation bar to the left. Try other inputs, including long ones, blank inputs, etc.

#### Edit and Delete a Topic
* Click on 'edit' next to the 'Penguins' Topic. An empty box should appear underneath. Enter 'Giraffes' into the box and click submit. The name of the Topic originally called 'Penguins' should now read 'Giraffes'. Again, please do try different inputs.
* Press the 'x' to the right of the Topic 'Giraffes'. The Topic no longer appear in the list of Topics in the navigation bar.
* Press the 'x' to the right of the Topic 'Science'. This should eliminate 'Science' (checkmate, atheists!), and all the feeds it contains.

#### Add a Feed
* Copy and paste "http://interglacial.com/rss/pokey_the_penguin.rss" into the 'Search for a feed' bar on the left side. Press enter. You should now have a Feed titled 'Pokey the Penguin' under the Topic 'Uncategorized'. Currently moving Feeds to Topics other than the Uncategorized Topic has not been implemented on the front-end (though it works on the back-end!).
* Now copy and paste "http://xkcd.com/rss.xml" into the search bar. The string "You are already subscribed to that feed" should appear beneath the search bar, in soothing red text.
* Now copy and paste "http://rss.nytimes.com/services/xml/rss/nyt/Science.xml" into the 'Search for a feed' bar. The 'NYT > Science' Feed, which had been deleted earlier when the 'Science' Topic was deleted, should be re-added. The red text should disappear.
* Copy and paste a non-existent url, "http://jsfiddle.net" into the search bar. No change should occur in the Feed/Topic list.

#### Miscellaneous
* Click on the 'Login', 'Donate', and 'About' buttons. The page should stay the same because the 'Login' button is to be implemented in Iteration 2, as will redirection 'Donate' and 'About' to their own pages.

### What Is Implemented
An RSS feed that supports a single user, who can make Topics, add Feeds to the Uncategorized Topic, delete Feeds, and expand and browse Posts and Feeds.

### Roles and Tasks
Views and front-end controllers: Michelle, Jawwad

Controller unit tests: James and Devon

API and back-end controllers: Justyn

Models, API, and model unit tests: Lucia and Justyn

### Changes

#### Model
We removed the custom User class (RSSUser), as we found the attributes and methods in the default Django User class sufficient. Consequentially, there are no longer unit tests for User.

Model methods no longer return bools upon success/failure, and unit tests have been modified to reflect this change.

We have specified that Users must have a Uncategorized Topic, with unit tests to reflect this change.

#### Controller/View
A PostController class turned out to be unnecessary, and PostController methods are now implemented in the FeedController.

We have moved adding, deleting, and moving a Feed to a *particular* Topic to Iteration 2. Currently Feeds can only be added and deleted from the Uncategorized Topic.

We have moved searching for Feeds by keyword via the search bar to Iteration 2. Currently, inputting an RSS feed url into the addfeed/search bar causes a search of the database, to ensure that a new model object is not created if the feed already exists in the database.

#### Managerial

Communicatively, we have started using Slack for instant messaging/real-time communication.
