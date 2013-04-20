from flask import Flask, render_template
frpm pymongo import MongoClient

web = Flask (__name__)
web.debug = True

client = MongoClient ()

@web.route ("/")
def start():
	return render_template ("start.html")

@web.route ("/signup", mathods=['POST'])
def signup

if __name__ == '__main__':
	web.run (host="0.0.0.0", port=8000)
