## First Things First: Python 3 and MySQL

Before you clone and try to get the sample app working, you'll need a valid Python 3 installation ([Python downloads](https://www.python.org/downloads/)).

Next, make sure you either have access to a MySQL server, or [install your own local instance](https://dev.mysql.com/downloads/mysql/).

## Clone this repository to your local dev environment

Your command will look something like this:

``` sh
$ git clone https://github.com/wou-cs/wolfit.git
```

In addition, you probably want to connect this local repo to your own remote, detaching from the master repository.

``` sh
$ cd wolfit
$ git remote set-url origin https://new.url.here
```

## Configure your databases

You should create two databases in your local MySQL environment, one for development and one for test. The development database is a *sandbox* that you can use for interactive play and testing. It will retain data and allow you to interact with the app. The test database will get torn down and recreated **every time you run the test suite**.

I recommend naming the databases something like `wolfit_test` and `wolfit_dev`.

Below is an example of an interaction with MySQL where I create the test database and a user to interact with it.

``` sh
$ mysql --user=root --password mysql
Enter password:
mysql> CREATE USER 'wolfit-test'@'localhost' IDENTIFIED BY 'testing';
Query OK, 0 rows affected (0.00 sec)
mysql> CREATE DATABASE wolfit_test;
Query OK, 1 row affected (0.00 sec)
mysql> GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,INDEX,REFERENCES,ALTER ON wolfit_test.* TO 'wolfit-test'@'localhost';
Query OK, 0 rows affected (0.00 sec)
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