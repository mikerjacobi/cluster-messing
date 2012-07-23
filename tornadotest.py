import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")

class paintdothtml(tornado.web.RequestHandler):
    def get(self):
        f=open('paint.html','r').read().split('\n')
        for l in f:
            self.write(l+'\n')


class paintdotjs(tornado.web.RequestHandler):
    def get(self):
        f=open('paint.js','r').read().split('\n')
        for l in f:
            self.write(l+'\n')

application = tornado.web.Application([(r"/",MainHandler),(r"/paint.html",paintdothtml),(r"/paint.js",paintdotjs)])

if __name__=="__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
