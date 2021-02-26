class Config(object):
    SQLALCHEMY_DATABASE_URI = ("mysql+pymysql://root:@localhost:3306/library?charset=utf8")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dev'