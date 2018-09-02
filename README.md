## Steps to make this work in your local environment

* Create your own dev.settings and test.settings files (do not check these into Git). Each will contain:

``` py
SECRET_KEY = "your generated secret key"
DB_HOST = 'localhost'
BLOG_DATABASE_NAME = 'wolfit_dev'
DB_USERNAME = 'wolfit-app'
DB_PASSWORD = 'the password you choose'
```

* Configure your pipenv environment and download required Python modules. Start by getting pipenv itself working using [these instructions](https://pipenv.readthedocs.io/en/latest/).

``` sh
$ pipenv install
$ pipenv shell
```

Once you have requisite libraries installed, you will *always* need to start your development session by entering the pipenv shell.

## Build / migrate the database

``` sh
$ flask db upgrade
```

## Run tests

``` sh
$ ./runtests.sh
```

## Run dev server

## Test Coverage

To look at test coverage, simply run:

``` sh
$ ./cov.sh
```