from flask import Flask, render_template

web = Flask (__name__)

@web.route ("/")
def start():
	return render_template ("start.html")


if __name__ == '__main__':
	web.run (host="0.0.0.0")
