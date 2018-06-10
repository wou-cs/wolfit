import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    if os.environ.get('DB_HOST'):
        SQLALCHEMY_DATABASE_URI = (
            f"""mysql+pymysql://{os.environ.get('DB_USERNAME')}:"""
            f"""{os.environ.get('DB_PASSWORD')}@"""
            f"""{os.environ.get('DB_HOST')}/"""
            f"""{os.environ.get('BLOG_DATABASE_NAME')}"""
        )
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
