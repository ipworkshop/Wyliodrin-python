from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
import hashlib
import json

SECRET_KEY = "key"

web = Flask (__name__)
web.config.from_object(__name__)
web.debug = True

client = MongoClient ()
db = client.wyliodrin

def user():
	if "email" in session:
		return session["email"]
	else:
		return None

@web.route ("/")
def start():
	if user() != None:
		return redirect (url_for ("fluid"))
	else:
		return render_template ("start.html")
	
@web.route ("/fluid")
def fluid():
	if user != Nine:
		return render_template ("fluid.html")
	else:
		return redirect (url_for ("start"))

@web.route ("/signup", methods=['POST'])
def signup():
	result = "0";
	email = request.form["email"];
	password = request.form["password"];
	if len(email)>0 and len(password)>0:
		md5pass = hashlib.md5(password).hexdigest()
		if db.users.find ({"email":email}).count() > 0:
			result = "0"
		else:
			if db.users.insert ({"email":email, "password":md5pass}):
				result = "1"
	return json.dumps ({"result":result})

@web.route ("/newproject", methods=['POST'])
def newproject():
	if user() != None:
		result = "0";
		name = request.form["name"]
		email = session["email"]
		if (len(name)>0):
			if db.projects.find ({"name":name, "email": email}).count() > 0:
				result = "0";
			else:
				db.projects.insert ({"name":name, "email": email});
				result = "1";
		return json.dumps ({"result":result})
	else:
		return ""
	
@web.route ("/save")
def save():
	result = "0"
	if user() != None:
		if "project" in session:
			name = session["project"]
			email = user ()
			program = request.form["program"]
			
			
			
		return json.dumps ({"result":result})	
	else:
		return ""

@web.route ("/login", methods=['POST'])
def login():
	result = "0";
	email = request.form["email"];
	password = request.form["password"];
	if (len(email)>0):
		md5pass = hashlib.md5(password).hexdigest()
		if db.users.find ({"email":email, "password": md5pass}).count() > 0:
			result = "1";
			session["email"]=email
			session.modified = True
	return json.dumps ({"result":result})

@web.route ("/logout")
def logout ():
	if "email" in session:		
		del session["email"]
	return redirect (url_for ("start"))

if __name__ == '__main__':
	web.run (host="0.0.0.0", port=8000)
