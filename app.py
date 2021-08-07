from flask import Flask, request
from flask_restful import Resource, Api
from time import time
import requests, db, bot

app = Flask(__name__)
api = Api(app)

# db = sqlite3.connect("data.db")
r = requests.Session()
class Hello(Resource):
	def get(self):
		ts = time()
		for i in range(25):
			r.get("https://shopee.co.id/")
		res = time() - ts
		return str(res)
	def post(self):
		json = request.json
		hasil = bot.start(json['link'],json['harga'],json['model'],json['pay'])
		return hasil

# class Database(Resource):
# 	def get(self):
# 		db.row_factory = sqlite3.Row
# 		cur = db.cursor()
# 		cur.execute("SELECT * FROM user")
# 		rows = cur.fetchall()
# 		return rows


		
api.add_resource(Hello,"/")
# api.add_resource(Database,"/db")
if __name__ == "__main__":
	app.run(debug = True)
