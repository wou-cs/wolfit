# Chris' local settings - do not check into source control.

DB_HOST = 'localhost'
BLOG_DATABASE_NAME = 'wolfit'
DB_USERNAME = 'wolfit-app'
DB_PASSWORD = 'please do not use blank'
SECRET_KEY = "make it secret!"

DB_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{BLOG_DATABASE_NAME}"
SQLALCHEMY_DATABASE_URI = DB_URI
