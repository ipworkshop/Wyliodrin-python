from flask import Flask, render_template
from pymongo import MongoClient
import hashlib

web = Flask (__name__)
web.debug = True

client = MongoClient ()

@web.route ("/")
def start():
	return render_template ("start.html")

@web.route ("/signup", mathods=['POST'])
def signup():

@web.route ("/login", mathods=['POST'])
def signup():
md5pass = hashlib.md5(password).hexdigest()
	if db.find ({"email":username, "password", md5pass}).count() > 0:

if __name__ == '__main__':
	web.run (host="0.0.0.0", port=8000)
