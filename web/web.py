from flask import Flask, render_template, request
from pymongo import MongoClient
import hashlib
import json

web = Flask (__name__)
web.debug = True

client = MongoClient ()
db = client.wyliodrin

@web.route ("/")
def start():
	return render_template ("start.html")
	
@web.route ("/fluid")
def fluid():
	return render_template ("fluid.html")

@web.route ("/signup", methods=['POST'])
def signup():
	result = "0";
	email = request.form["email"];
	password = request.form["password"];
	md5pass = hashlib.md5(password).hexdigest()
	if db.users.find ({"email":email}).count() > 0:
		result = "0"
	else:
		if db.users.insert ({"email":email, "password":md5pass}):
			result = "1"
	return json.dumps ({"result":result})

@web.route ("/login", methods=['POST'])
def login():
	result = "0";
	email = request.form["email"];
	password = request.form["password"];
	md5pass = hashlib.md5(password).hexdigest()
	if db.users.find ({"email":email, "password": md5pass}).count() > 0:
		result = "1";
	return json.dumps ({"result":result})
		

if __name__ == '__main__':
	web.run (host="0.0.0.0", port=8000)
