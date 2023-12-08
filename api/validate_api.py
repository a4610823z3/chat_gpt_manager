import os
from tornado.web import RequestHandler
import api.support as support
import requests


class ValidateApi(RequestHandler):
    
      def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods",
                        "GET, POST, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization")
        key = self.get_argument('key')
        user_port = os.environ.get('GPT_PORT')
        url = "http://localhost:"+ str(user_port) + "/internal/users/keys/" + key;
        validate_response = requests.get(url);
        self.write_data(validate_response.json())

      def write_data(self, result_json):
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(result_json)