from flask import Flask
from flask_restful import Resource, Api
from time import time
import requests

app = Flask(__name__)
api = Api(app)

r = requests.Session()
class Hello(Resource):
	def get(self):
		ts = time()
		for i in range(100):
			r.get("https://shopee.co.id/")
		res = time() - ts
		return str(res)
		
api.add_resource(Hello,"/")
if __name__ == "__main__":
	app.run(debug = True)
