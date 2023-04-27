import datetime
import os
import uuid
from tornado.web import RequestHandler
import json
import api.support as support


class ValidateApi(RequestHandler):
    
      def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods",
                        "GET, POST, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization")
        key = self.get_argument('key')
        result = support.had_user_key(key)
        response_json = {
           'code': 1,
           'data':False
        }
        if result :
          response_json['code'] = 0
          response_json['data'] = True
        self.write_data(response_json)

      def write_data(self, result_json):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(result_json)