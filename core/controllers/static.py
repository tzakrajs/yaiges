import tornado.web

from core import route

# Static Assets
route._routes.append(['/assets/(.*)', tornado.web.StaticFileHandler, {'path': 'core/static/assets/'}])
route._routes.append(['/app/(.*)', tornado.web.StaticFileHandler, {'path': 'core/static/app/'}])

# Index for Angular Single Page
@route('/')
class HomePage (tornado.web.RequestHandler):
    def get(self):
        self.render('../static/app/app.index.html')
