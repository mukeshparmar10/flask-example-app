from flask import Flask, request, Response, redirect, url_for, session, render_template
import mysql.connector
import os

def connection():
	mydb = mysql.connector.connect(
		host=os.environ.get("DB_HOST"),
		user=os.environ.get("DB_USER"),
		passwd=os.environ.get("DB_PASSWORD"),
		database=os.environ.get("DB_DATABASE"),
		port=int(os.environ.get("DB_PORT"))	
	)
	return mydb

app = Flask(__name__)

@app.route("/")
def index():
	mydb = connection()
	mycursor = mydb.cursor()
	mycursor.execute("select * from student")
	data = mycursor.fetchall()
	mydb.close()
	return render_template("index.html",data=data)	

if __name__=="__main__":
	app.run(host="0.0.0.0",debug=True)