import json

import pytest
import tornado.web

from core import route
from core.models.namespace import get_namespace, get_namespaces
from core.models.node import get_node, get_nodes
from core.models.service import get_service, get_services
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

@route('/api/services')
class Services(tornado.web.RequestHandler):
    def get(self, service_name):
        """Returns all services visible to the requestor""" 
        service = get_service(service_name)
        self.write(json.dumps(service))

@route('/api/service/(?P<service_name>.*)', name='service_name')
class Service(tornado.web.RequestHandler):
    def get(self, service_name):
        """Return service for given service_name in URI"""
        service = get_service(service_name)
        self.write(json.dumps(service))

@route('/api/nodes')
class Nodes(tornado.web.RequestHandler):
    def get(self, node_name):
        """Returns all nodes visible to the requestor""" 
        nodes = get_nodes()
        self.write(json.dumps(nodes))

@route('/api/node/(?P<node_name>.*)', name='node_name')
class Node(tornado.web.RequestHandler):
    def get(self, node_name):
        """Return node for given node_name in URI"""
        node = get_node(node_name)
        self.write(json.dumps(node))
