import asyncio
from aiomysql.sa import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String

MYSQL_CREDENTIALS = {'user': 'yaiges',
                     'password': 'yaiges',
                     'db': 'yaiges',
                     'host': 'localhost'}
def db_url():
    return 'mysql://{user}:{password}@{host}:3306/{db}'.format(**MYSQL_CREDENTIALS)

metadata = MetaData()
table = Table('Example',metadata,
              Column('id',Integer, primary_key=True),
              Column('name',String(16)))

def setup():
    from sqlalchemy import create_engine
    import pymysql
    pymysql.install_as_MySQLdb()
    engine = create_engine(db_url())
    metadata.create_all(engine)
setup()

loop = asyncio.get_event_loop()
