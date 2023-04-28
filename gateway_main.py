# -*- coding: utf-8 -*-
import os
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
    user_port = os.environ.get('GPT_PORT')
    if user_port == '' or user_port is None:
        user_port = '7799'
    app.listen(int(str(user_port)))
    tornado.ioloop.IOLoop.current().start()
