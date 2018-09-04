## First Things First: Python 3 and MySQL

Before you clone and try to get the sample app working, you'll need a valid Python 3 installation ([Python downloads](https://www.python.org/downloads/)).

Next, make sure you either have access to a MySQL server, or [install your own local instance](https://dev.mysql.com/downloads/mysql/).

## Clone this repository to your local dev environment

Your command will look something like this:

``` sh
$ git clone https://github.com/wou-cs/wolfit.git
```

## Steps to make this work in your local environment

* Create two schemas in your MySQL database: one for development, one for testing. The testing database will get built up and broken down each time you test. The development database will be your sandbox for exploring the app.
* Create your own dev.settings and test.settings files (do not check these into Git). Each will contain:

``` py
SECRET_KEY = "your generated secret key"
DB_HOST = 'localhost'
BLOG_DATABASE_NAME = 'wolfit_dev'
DB_USERNAME = 'wolfit-app'
DB_PASSWORD = 'the password you choose'
```

* Configure your pipenv environment and download required Python modules. Start by getting pipenv itself working using [these instructions](https://pipenv.readthedocs.io/en/latest/). Then, in the working directory containing the clone of this app:

``` sh
$ pipenv install
$ pipenv shell
```

Once you have requisite libraries installed, you will *always* need to start your development session by entering the pipenv shell.

## Build / migrate the database

``` sh
$ flask db upgrade
```

You should see all of the migrations being applied to your development database.

## Run tests

``` sh
$ ./runtests.sh
```

## Run dev server (local web server)

``` sh
$ ./rundev.sh
```


## Test Coverage

To look at test coverage, simply run:

``` sh
$ ./cov.sh
```

## Load up some sample posts from Reddit

A great way to load up content into this Reddit clone is to copy some submissions from Reddit to your local sandbox. There's a script to perform this called `load_reddit_posts.py`, but in order to run it you'll need to configure the PRAW API with a praw.ini file. Create such a file in the root of your project, and add these entries:

``` ini
[DEFAULT]
client_id=<your client ID>
client_secret=<your secret>
user_agent=python:edu.wou.<your user ID at WOU>
```

You will get your ID and secret by [creating an app under your Reddit profile](https://www.reddit.com/prefs/apps).

Follow these steps:

1. Click the "create app" at the bottom of the [Reddit apps page](https://www.reddit.com/prefs/apps).
2. Give it a name you will recognize, such as "Load posts for Wolfit".
3. Select the script option.
4. Fill in this for the redirect API: `http://www.example.com/unused/redirect/uri`
5. Client the "create app" button.
6. Under your app name you will see a client ID that looks something like this: `R2jyWgoETNkBfQ`
7. You will also see your secret shown. Copy both the client ID and the secret into your praw.ini file.

Then you can load up some sample posts:

``` sh
$ python load_reddit_posts
```

You can optionally give the name of a subreddit as the first parameter. By default the script will load from [`/r/learnpython`](https://www.reddit.com/r/learnpython/).

*Note* -- This is script is not terribly resilient and may fail with some title and body formatting issues because of the source data from Reddit.