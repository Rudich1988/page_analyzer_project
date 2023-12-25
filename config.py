class Config(object):
    DEBUG = False
    TESTING = False
    #DATABASE = 'postgresql://rudi4:password@localhost:5432/hexlet11111111'
    #DATABASE_URL = 'postgresql://rudi4:password@localhost:5432/hexlet'


class ProductionConfig(Config):
    DATABASE_URL = 'asdfghjkl'


class DevelopmentConfig(Config):
    DATABASE_URL = 'postgresql://rudi4:password@localhost:5432/hexlet'