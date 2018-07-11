class Config(object):

    @classmethod
    def DATABASE_URI(cls, app):
        return (
            f"""mysql+pymysql://{app.config['DB_USERNAME']}:"""
            f"""{app.config['DB_PASSWORD']}@"""
            f"""{app.config['DB_HOST']}/"""
            f"""{app.config['BLOG_DATABASE_NAME']}"""
        )

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 10
