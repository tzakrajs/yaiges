import logging
import os
import tornado.ioloop
from tornroutes import route

import core.models.persistence

# config log format
format="%(asctime)-21s %(levelname)s %(name)s (%(funcName)-s) " + \
       "%(process)d:%(thread)d - %(message)s"
logging.basicConfig(level=logging.DEBUG,
                    format=format,
                    filename='./cloud-fortress-www.log')

# initialize the main ioloop
tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
main_loop = tornado.ioloop.IOLoop.instance()

# import our routes from the controllers
core_path = os.path.dirname(os.path.abspath(__file__))
static_path = '{}/static'.format(core_path)
from core.controllers import *
