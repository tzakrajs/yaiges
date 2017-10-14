import json

import pytest
import tornado.web

from core import route
from core.models.namespace import get_namespace, get_namespaces
from core.models.monitor import get_monitor, get_monitors
from core.models.auth import get_user, get_users, authorize_user
#TODO: Add checks, alerts, notifications

@route('/api/user/(?P<user_name>.*)', name='user_name')
class User(tornado.web.RequestHandler):
    def get(self, user_name):
        """Return user for given user_name in URI"""
        user = get_user(user_name)
        self.write(json.dumps(user))

@route('/api/users')
class Users(tornado.web.RequestHandler):
    def get(self):
        """Returns all users visible to the requestor"""
        users = get_users()
        self.write(json.dumps(users))

@route('/api/namespace/(?P<namespace_name>.*)', name='namespace_name')
class Namespace(tornado.web.RequestHandler):
    def get(self, namespace_name):
        """Return namespace for given namespace_name in URI"""
        namespace = get_namespace(namespace_name)
        self.write(json.dumps(namespace))

@route('/api/namespaces')
class Namespaces(tornado.web.RequestHandler):
    def get(self):
        """Returns all namespaces visible to the requestor"""
        namespaces = get_namespaces()
        self.write(json.dumps(namespaces))

@route('/api/monitors')
class Monitors(tornado.web.RequestHandler):
    def get(self, monitor_name):
        """Returns all monitors visible to the requestor""" 
        monitors = get_monitors()
        self.write(json.dumps(monitors))

@route('/api/monitor/(?P<monitor_name>.*)', name='monitor_name')
class Monitor(tornado.web.RequestHandler):
    def get(self, monitor_name):
        """Return monitor for given monitor_name in URI"""
        monitor = get_monitor(monitor_name)
        self.write(json.dumps(monitor))
