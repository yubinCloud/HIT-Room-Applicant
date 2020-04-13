from hitapply.common.const import DatabaseConst


class BaseConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(DatabaseConst.MYSQL_USERNAME,
                                                                      DatabaseConst.MYSQL_PASSWORD,
                                                                      DatabaseConst.MYSQL_HOST,
                                                                      DatabaseConst.MYSQL_PORT,
                                                                      DatabaseConst.MYSQL_DBNAME)


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(DatabaseConst.MYSQL_USERNAME,
                                                              DatabaseConst.MYSQL_PASSWORD,
                                                              DatabaseConst.MYSQL_HOST, DatabaseConst.MYSQL_PORT,
                                                              DatabaseConst.MYSQL_DBNAME)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}