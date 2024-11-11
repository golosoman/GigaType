class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost/giga_type?charset=utf8mb4"


class DevelopmentConfig(Config):
    DEBUG = True


JWT_SECRET_KEY = "kuewasd;'hibbasdtwazxff"