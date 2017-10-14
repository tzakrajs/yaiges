import asyncio
from aiomysql.sa import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String

CREDS = {'user': 'yaiges',
         'password': 'yaiges',
         'db': 'yaiges',
         'host': 'localhost'}

class MySQL():
    def __init__(self):
        self.metadata = MetaData()

    def _url(self):
        return 'mysql://{user}:{password}@{host}:3306/{db}'.format(**CREDS)

    def _tables(self):
        table = Table('namespace', self.metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String(32)))

    def _create_all(self):
        """Blocking function that sets up the tables that do not exist."""
        from sqlalchemy import create_engine
        import pymysql
        pymysql.install_as_MySQLdb()
        engine = create_engine(self._url())
        metadata.create_all(engine)
    
loop = asyncio.get_event_loop()
