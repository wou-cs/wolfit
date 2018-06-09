# Sample local settings - modify this and save to a local file
# that you do not check into version control.
# Then set the environment variable WOLFIT_DEV_SETTINGS to point
# to this file.

DB_HOST = 'localhost'
BLOG_DATABASE_NAME = 'wolfit'
DB_USERNAME = 'wolfit-app'
DB_PASSWORD = 'please do not use blank'
SECRET_KEY = "make it secret!"

DB_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{BLOG_DATABASE_NAME}"
SQLALCHEMY_DATABASE_URI = DB_URI
