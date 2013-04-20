import hashlib

def signup_user(db, username, password):
	md5pass = hashlib.md5(password).hexdigest()
	if db.find ({"email":username, "password", md5pass}).count() > 0:
		