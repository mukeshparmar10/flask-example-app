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

@app.route("/student")
def student():
	return render_template("student-add.html")

@app.route('/student-save',methods=['POST'])
def student_save():	
	name = request.form.get("name")
	address = request.form.get("address")
	standard = request.form.get("standard")
	mydb = connection()
	mycursor = mydb.cursor()
	query = f"insert into student(name,address,standard) values('{name}','{address}','{standard}')"
	mycursor.execute(query)
	mydb.commit()
	mydb.close()
	return redirect(url_for("index"))


@app.route("/student-edit/<id>")
def student_edit(id):
	mydb = connection()
	mycursor = mydb.cursor()
	mycursor.execute(f"select * from student where id = {id}")
	data = mycursor.fetchone()
	mydb.close()
	return render_template("student.html",data=data)

@app.route('/student-update',methods=['POST'])
def student_update():
	id = request.form.get("id")
	name = request.form.get("name")
	address = request.form.get("address")
	standard = request.form.get("standard")
	mydb = connection()
	mycursor = mydb.cursor()
	query = f"update student set name='{name}',address='{address}',standard='{standard}' where id={id}"
	mycursor.execute(query)
	mydb.commit()
	mydb.close()
	return redirect(url_for("index"))
	

@app.route("/student-delete/<id>")
def student_delete(id):
	mydb = connection()
	mycursor = mydb.cursor()
	mycursor.execute(f"delete from student where id = {id}")
	mydb.commit()
	mydb.close()
	return redirect(url_for("index"))


if __name__=="__main__":
	app.run(host="0.0.0.0",debug=True)