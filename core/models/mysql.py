import asyncio
from aiomysql.sa import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String

CREDS = {'user': 'yaiges',
         'password': 'yaiges',
         'db': 'yaiges',
         'host': 'localhost'}

loop = asyncio.get_event_loop()
engine = None

async def get_mysql():
    global engine
    if not engine:
        engine = await create_engine(**CREDS, loop=loop)
    mysql = MySQL()
    mysql._init(engine)
    return mysql

class MySQL():
    def _init(self, engine):
        # Get the table models ready for use
        self.metadata = MetaData()
        self._tables()

    def _url(self):
        return 'mysql://{user}:{password}@{host}:3306/{db}'.format(**CREDS)

    def _tables(self):
        self.tables = {'Namespace': Table('namespace', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('name', String(32))),
                       'Inventory': Table('inventory', self.metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('name', String(32)))}

    async def _connect(self):
        self.engine = create_engine(**CREDS, loop=loop)

    def _create_all(self):
        """Blocking function that sets up the tables that do not exist."""
        from sqlalchemy import create_engine
        import pymysql
        pymysql.install_as_MySQLdb()
        engine = create_engine(self._url())
        metadata.create_all(engine)
