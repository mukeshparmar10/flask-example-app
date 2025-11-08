from flask import Flask, request, Response, redirect, url_for, session, render_template
import mysql.connector
import os
from flask_mail import Mail, Message

def connection():
	mydb = mysql.connector.connect(
		host=os.environ.get("DB_HOST"),
		user=os.environ.get("DB_USER"),
		passwd=os.environ.get("DB_PASSWORD"),
		database=os.environ.get("DB_DATABASE"),
		port=int(os.environ.get("DB_PORT"))	
	)
	return mydb

def check_login():
	if 'email' in session:
		email = session['email']
		return "1"
	else:
		return redirect(url_for("index"))

	

app = Flask(__name__)

app.secret_key = 'ddfffssdsdxdsd'

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'False').lower() in ('true', '1', 't')
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False').lower() in ('true', '1', 't')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)

@app.route("/")
def index():
	return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html")	

@app.route("/login",methods=['POST'])
def login():
	email = request.form.get("email")
	password = request.form.get("password")

	query = f"select * from users where email = '{email}' and binary password='{password}'"
	mydb = connection()
	mycursor = mydb.cursor()
	mycursor.execute(query)
	data = mycursor.fetchone()
	mydb.close()

	if data is None:
		return "0"
	else:
		session['email'] = email
		return str(len(data))

@app.route('/logout')
def logout():
	session.pop('email', None)
	session.clear()
	return redirect(url_for('index'))

@app.route("/home")
def home():
	if check_login()!="1":
		return redirect(url_for("index"))	

	mydb = connection()
	mycursor = mydb.cursor()
	mycursor.execute("select * from student")
	data = mycursor.fetchall()
	mydb.close()
	return render_template("home.html",data=data)

@app.route("/student")
def student():
	if check_login()!="1":
		return redirect(url_for("index"))

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
	return redirect(url_for("home"))


@app.route("/student-edit/<id>")
def student_edit(id):
	if check_login()!="1":
		return redirect(url_for("index"))

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
	return redirect(url_for("home"))
	

@app.route("/student-delete/<id>")
def student_delete(id):
	mydb = connection()
	mycursor = mydb.cursor()
	mycursor.execute(f"delete from student where id = {id}")
	mydb.commit()
	mydb.close()
	return redirect(url_for("home"))

@app.route("/send_test_email")
def send_test_email():
    msg = Message(
        subject="Hello from Flask-Mail!",
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=["mukeshparmar10@gmail.com","vedparmar9411@gmail.com"], # List of recipient emails
        body="This is a test email sent from a Flask application."
    )
    
    # Optional: Add HTML body
    # msg.html = "<b>This is an HTML test email</b> from Flask-Mail."
    
    # Optional: Add attachments
    # with app.open_resource("path/to/your/attachment.pdf") as fp:
    #     msg.attach("attachment.pdf", "application/pdf", fp.read())

    try:
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        return f"Error sending email: {e}"


if __name__=="__main__":
	app.run(host="0.0.0.0",debug=True)