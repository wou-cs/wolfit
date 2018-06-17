
## Steps to make this work in your local environment

* Create your own dev.settings and test.settings files (do not check these into Git). Each will contain:

``` py
SECRET_KEY = "your generated secret key"
DB_HOST = 'localhost'
BLOG_DATABASE_NAME = 'wolfit_dev'
DB_USERNAME = 'wolfit-app'
DB_PASSWORD = 'the password you choose'
```

## Test Coverage

To look at test coverage, simply run:

``` sh
./cov.sh
```