from flask import Flask, request, Response, redirect, url_for, session, render_template

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

