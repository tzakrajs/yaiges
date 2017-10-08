#!/usr/bin/env python3
import socket
import sys

import pytest
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import yaml

from core import logging, main_loop, route

# YAML Config is located at the path below
YAML_CONFIG_PATH = './config.yml'

application = tornado.web.Application(route.get_routes())

def generate_redirect_app(hostname='localhost', port=443):
    if not hostname:
        hostname = socket.getfqdn()
    if port == 443:
        host = hostname
    else:
        host = '{0}:{1}'.format(hostname, port)
    # Define http/ws server (only redirect to https/wss)
    class RedirectToSSL(tornado.web.RequestHandler):
        def get(self, path):
            self.redirect('https://{0}/{1}'.format(host, path))
    return tornado.web.Application([(r"/(.*)", RedirectToSSL),],)

# Load the configuration file
try:
    config_file = open(YAML_CONFIG_PATH, 'r')
except FileNotFoundError:
    error_message = "YAML config not found: {0}".format(YAML_CONFIG_PATH)
    logging.error(error_message)
    sys.exit(error_message)
config = yaml.load(config_file)

if __name__ == "__main__":
    # Load the top level config dictionaries
    general_config = config.get('general', {})
    non_ssl_config = config.get('non_ssl', {})
    ssl_config = config.get('ssl', {})
    # Set our listening IP addresses and ports
    ipv4_ip = general_config.get('ipv4_ip')
    ipv6_ip = general_config.get('ipv6_ip')
    http_port = non_ssl_config.get('port', 8080)
    https_port = ssl_config.get('port', 8443)
    # Non SSL
    if non_ssl_config.get('enabled'):
        # Setup the http/ws server
        if non_ssl_config.get('redirect'):
            # This one only redirects to https, ws does not and cannot be
            # redirected since browsers disallow ws requests originating from
            # https websites
            hostname = general_config.get('hostname')
            external_port = ssl_config.get('external_port', https_port)
            redirect_app = generate_redirect_app(hostname, external_port)
            http_server = tornado.httpserver.HTTPServer(redirect_app)
        else:
            # This one is the full application
            http_server = tornado.httpserver.HTTPServer(application)
        if ipv6_ip:
            # Listen on IPv6 address
            http_server.listen(http_port, ipv6_ip)
        if ipv4_ip:
            # Listen on IPv4 address
            http_server.listen(http_port, ipv4_ip)
    # SSL
    if ssl_config.get('enabled'):
        # Setup https/wss server
        ssl_crt = ssl_config.get('crt_path')
        ssl_key = ssl_config.get('key_path')
        try:
            ssl_options = {'certfile': ssl_crt,
                           'keyfile': ssl_key}
            https_server = tornado.httpserver.HTTPServer(application, ssl_options=ssl_options)
        except Exception as e:
            error_message = "Unable to setup SSL: {0}".format(e)
            logging.error(error_message)
            sys.exit(error_message)
        if ipv6_ip:
            # Listen on IPv6 address
            https_server.listen(https_port, ipv6_ip)
        if ipv4_ip:
            # Listen on IPv4 address
            https_server.listen(https_port, ipv4_ip)
    # Initialize Main Loop
    main_loop.start()

@pytest.fixture
def app():
    return application

@pytest.mark.gen_test
def test_hello_world(http_client, base_url):
    response = yield http_client.fetch(base_url)
    assert response.code == 200
