import asyncio
import json
from aiomysql.sa import create_engine
from sqlalchemy import MetaData, Table, Sequence, Column, Integer, String, Text

CREDS = {'user': 'yaiges',
         'password': 'yaiges',
         'db': 'yaiges',
         'host': 'localhost'}

engine = None
tables = {}
metadata = MetaData()

def _tables():
    """Creates SQLAlchemy table objects for yaiges"""
    global metadata
    global tables
    assert isinstance(tables, dict)
    if tables:
        return tables
    for table_name in ['Namespace', 'Inventory', 'Monitor', 'Check', 'Alert',
                  'Notification', 'NotificationHistory', 'ContactGroup',
                  'Contact']:
        table =  Table(table_name, metadata,
                       Column('id', Integer, primary_key=True),
                       Column('name', String(128), unique=True),
                       Column('metadata', Text))
        tables[table_name] = table
        link_table_name = 'link_{0}'.format(table_name)
        link_table =  Table(link_table_name, metadata,
                            Column('id', Integer, primary_key=True),
                            Column('target_type', String(128)),
                            Column('target_id', Integer))
        tables[link_table_name] = link_table
    return tables

def _url():
    return 'mysql://{user}:{password}@{host}:3306/{db}'.format(**CREDS)

def _create_all_tables(metadata):
    """Blocking function that sets up the tables that do not exist."""
    from sqlalchemy import create_engine
    import pymysql
    global tables
    pymysql.install_as_MySQLdb()
    engine = create_engine(_url())
    metadata.create_all(engine)
    engine.dispose()

async def get_mysql():
    global engine
    global tables
    global metadata
    if not engine:
        engine = await create_engine(**CREDS)
    if not tables:
        tables = _tables()
        _create_all_tables(metadata)
    mysql = MySQL()
    mysql._init(engine)
    return mysql

class MySQL():
    def _init(self, engine):
        self.engine = engine

    async def recall(self, item):
        item_type = item.class_name()
        table = tables[item_type]
        conn = await engine.acquire()
        try:
            item_id = item.id
            res = await conn.execute(table.select().where(table.c.id==item_id))
        except: 
            item_name = item.name
            res = await conn.execute(table.select().where(table.c.name==item_name))
        rows = [row for row in res]
        if not rows:
            return
        item.id = rows[0][0]
        item.name = rows[0][1]
        item.metadata = json.loads(rows[0][2])
        await conn.close()
        item.links = await self.get_links(item)

    async def get_links(self, item):
        item_id = item.id
        item_type = item.class_name()
        link_table_name = 'link_{0}'.format(item_type)
        link_table = tables[link_table_name]
        conn = await engine.acquire()
        res = await conn.execute(link_table.select())
        links = {}
        for row in res:
            link_id = row[0]
            target_type = row[1]
            target_id = row[2]
            if not links.get(target_type):
                links[target_type] = []
            links[target_type].append(target_id)
        return links

    async def check_link(self, item, target):
        # Check if an item is linked with a target item
        item_id = item.id
        item_type = item.class_name()
        target_id = target.id
        target_type = target.class_name()
        link_table_name = 'link_{0}'.format(item_type)
        link_table = tables[link_table_name]
        conn = await engine.acquire()
        res = await conn.execute(link_table.select().where(link_table.c.target_type==target_type).where(link_table.c.target_id==target_id))
        rows = [row for row in res]
        await conn.close()
        return rows

    async def link(self, item, target):
        # Link an item with a target item
        existing_link = await self.check_link(item, target)
        if existing_link:
            return
        item_id = item.id
        item_type = item.class_name()
        target_id = target.id
        target_type = target.class_name()
        link_table_name = 'link_{0}'.format(item_type)
        link_table = tables[link_table_name]
        conn = await engine.acquire()
        try:
            transaction = await conn.begin()
            try:
                res = await conn.execute(link_table.insert().values(target_type=target_type,
                                                                    target_id=target_id))
            except Exception as e:
                print(e)
                await transaction.rollback()
            else:
                await transaction.commit()
            finally:
                transaction.close()
        finally:
            await conn.close()

    async def save(self, item, **kwargs):
        # First try to see if this item exists
        rows = await self.recall(item)
        if rows:
            await self.update(item)
        else:
            await self.create(item)

    async def update(self, item):
        item_id = item.id
        item_name = item.name
        item_type = item.class_name()
        item_metadata = json.dumps(item.metadata)
        table = tables[item_type]
        conn = await engine.acquire()
        try:
            transaction = await conn.begin()
            try:
                res = await conn.execute(table.update().where(table.c.id==item_id).values(name=item_name,
                                         metadata=item_metadata))
            except Exception as e:
                print(e)
                await transaction.rollback()
            else:
                await transaction.commit()
        finally:
            pass
            #await conn.close()

    async def delete(self, item):
        item_id = item.id
        item_type = item.class_name()
        item_metadata = json.dumps(item.metadata)
        table = tables[item_type]
        conn = await engine.acquire()
        try:
            transaction = await conn.begin()
            try:
                res = await conn.execute(table.delete().where(table.c.id==item_id))
            except Exception as e:
                print(e)
                await transaction.rollback()
            else:
                await transaction.commit()
        finally:
            await conn.close()

    async def create(self, item):
        item_name = item.name
        item_type = item.class_name()
        item_metadata = json.dumps(item.metadata)
        table = tables[item_type]
        conn = await engine.acquire()
        try:
            transaction = await conn.begin()
            try:
                res = await conn.execute(table.insert().values(name=item_name,
                                         metadata=item_metadata))
                item.id = res.lastrowid
            except Exception as e:
                print(e)
                await transaction.rollback()
            else:
                await transaction.commit()
            finally:
                await transaction.close()
        finally:
            await conn.close()

    async def destroy(self):
        engine.close()
        await engine.wait_closed()
