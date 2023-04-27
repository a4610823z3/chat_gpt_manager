# -*- coding: utf-8 -*-
import tornado.web
import tornado.websocket
import tornado.ioloop
from api.validate_api import ValidateApi





# 程序启动
if __name__ == "__main__":
    # 路由设置
    app = tornado.web.Application([
        (r"/users/keys", ValidateApi),

    ])
    # 设置端口号
    port = 9999
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
