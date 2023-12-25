import os
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


class Config(object):
    DEBUG = False
    TESTING = False
    


class ProductionConfig(Config):
    DATABASE_URL = 'postgres://database_url_g3ty_user:4IZeVFg1TEH5CjxlBnBSbo25VABi2urU@dpg-cm4addi1hbls73ack3vg-a/database_url_g3ty'
    #DATABASE_URL = 'здесь наверное должен быть путь к базе данных на render.com???'


class DevelopmentConfig(Config):
    DATABASE_URL = DATABASE_URL
    #DATABASE_URL = 'postgresql://rudi4:password@localhost:5432/hexlet'
    # или же нужно здесь как раз сделать доступ к переменной DATABASE_URL через os.getenv ? чтобы работали тесты