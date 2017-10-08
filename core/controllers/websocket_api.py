import datetime
import tornado.ioloop
import tornado.websocket
import asyncio

from core import logging, main_loop, route

web_socket_clients = []
messages = []

@route('/ws')
class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True
    
    def open(self):
        if self not in web_socket_clients:
            web_socket_clients.append(self)
            logging.debug("Client Connected, Total Clients: {}".format(len(web_socket_clients)))

    def on_close(self):
        if self in web_socket_clients:
            web_socket_clients.remove(self)
            logging.debug("Client Disconnected, Total Clients: {}".format(len(web_socket_clients)))

    def on_message(self, message):
        timestamp = datetime.datetime.now().strftime('%H:%M:%s')
        if message.startswith('name: '):
            self.user_name = message[6:]
            messages.append("{0} - {1} has joined the room".format(timestamp, self.user_name))
        else:
            messages.append("{0} - {1}: {2}".format(timestamp, self.user_name, message))

def schedule_func():
    for message in messages:
        logging.debug("message: {0}".format(message))
        for client in web_socket_clients:
            client.write_message(message)
        messages.remove(message)

sched = tornado.ioloop.PeriodicCallback(schedule_func, 1000, io_loop=main_loop)
#start your period timer
sched.start()
