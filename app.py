from flask import Flask, request, Response, redirect, url_for, session, render_template
import mysql.connector
import os

mydb = mysql.connector.connect(
	host=os.environ.get("DB_HOST"),
	user=os.environ.get("DB_USER"),
	passwd=os.environ.get("DB_PASSWORD"),
	database=os.environ.get("DB_DATABASE"),
	port=int(os.environ.get("DB_PORT"))	
)

mycursor = mydb.cursor()

app = Flask(__name__)
app.secret_key="supersecret"

@app.route("/")
def index():	
	mycursor.execute("select * from student")
	data = mycursor.fetchall()
	return render_template("index.html",data=data)


if __name__=="__main__":
	app.run(host="0.0.0.0",debug=True)

