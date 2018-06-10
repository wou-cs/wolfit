import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    print("Config: setting up CONFIG")
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    if os.environ.get('DB_HOST'):
        print(f"Config: found a real DB_HOST config <{os.environ.get('DB_HOST')}>")
        SQLALCHEMY_DATABASE_URI = (
            f"""mysql+pymysql://{os.environ.get('DB_USERNAME')}:"""
            f"""{os.environ.get('DB_PASSWORD')}@"""
            f"""{os.environ.get('DB_HOST')}/"""
            f"""{os.environ.get('BLOG_DATABASE_NAME')}"""
        )
    else:
        load_dotenv(verbose=True, dotenv_path="test.env")
        print(f"Config: trying a test DB_HOST config <{os.environ.get('DB_HOST')}>")
        SQLALCHEMY_DATABASE_URI = (
            f"""mysql+pymysql://{os.environ.get('DB_USERNAME')}:"""
            f"""{os.environ.get('DB_PASSWORD')}@"""
            f"""{os.environ.get('DB_HOST')}/"""
            f"""{os.environ.get('BLOG_DATABASE_NAME')}"""
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
