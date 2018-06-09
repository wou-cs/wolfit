DEBUG = True
DB_USERNAME = 'root'
DB_HOST = 'localhost'
DB_PASSWORD = ''
BLOG_DATABASE_NAME = 'wolfit'
SQLALCHEMY_TRACK_MODIFICATIONS = True

DB_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{BLOG_DATABASE_NAME}"
SQLALCHEMY_DATABASE_URI = DB_URI

# The following will be loaded from the environment. See __init__.py for details.
# DB_PASSWORD = ''
# SECRET_KEY = ''
