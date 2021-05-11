#app).py
from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql
import smtplib
from flask_mail import Mail, Message
 
app = Flask(__name__)
app.secret_key = "admin"
  
mysql = MySQL()
   
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'FBYfzJrlLk'
app.config['MYSQL_DATABASE_PASSWORD'] = '8G5IXLpLrY'
app.config['MYSQL_DATABASE_DB'] = 'FBYfzJrlLk'
app.config['MYSQL_DATABASE_HOST'] = 'remotemysql.com'
mysql.init_app(app)
 
@app.route('/')
def home():
    return redirect(url_for('admin_login'))
#admin_login page
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('admin_panel'))
    return render_template('admin_login.html', error=error)
#admin_dashboard    
@app.route('/admin_panel')
def admin_panel():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
 
    cur.execute('SELECT * FROM pay')
    data = cur.fetchall()
  
    cur.close()
    return render_template('admin_panel.html', pay = data)
 
@app.route('/add_contact', methods=['POST'])
#add user payement details
def add_pay():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        username = request.form['username']
        products = request.form['products']
        cost = request.form['cost']
        duedate = request.form['duedate']
        payment_status = request.form['payment_status']
        cur.execute("INSERT INTO pay (username, products, cost, duedate, payment_status) VALUES (%s,%s,%s,%s,%s)", (username, products, cost, duedate, payment_status))
        conn.commit()
        flash('Payment Added successfully')
        return redirect(url_for('admin_panel'))
 
 #edit user payment details
@app.route('/edit/<userid>', methods = ['POST', 'GET'])
def get_pay(userid):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('SELECT * FROM pay WHERE userid = %s', (userid))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', pay = data[0])
 #update user payment details
@app.route('/update/<userid>', methods=['POST'])
def update_pay(userid):
    if request.method == 'POST':
        username = request.form['username']
        products = request.form['products']
        cost = request.form['cost']
        duedate = request.form['duedate']
        payment_status = request.form['payment_status']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE pay
            SET username = %s,
                products = %s,
                cost = %s,
                duedate = %s,
                payment_status = %s
            WHERE userid = %s
        """, (username, products, cost, duedate, payment_status, userid))
        flash('Payment Updated Successfully')
        conn.commit()
        return redirect(url_for('admin_panel'))
 #delete the user payment details
@app.route('/delete/<string:userid>', methods = ['POST','GET'])
def delete_pay(userid):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('DELETE FROM pay WHERE userid = {0}'.format(userid))
    conn.commit()
    flash('Payment Removed Successfully')
    return redirect(url_for('admin_panel'))

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '<youremail>@gmail.com'#put your eamil account
app.config['MAIL_PASSWORD'] = '' #put your email password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'hariharann063@gmail.com'
mail = Mail(app)
#send message to users for due_payment
@app.route('/sendmail', methods=['GET', 'POST'])
def sendmail():
    if request.method == 'POST':
        recipient = request.form['recipient']
        msg = Message('Digitalpay', recipients=[recipient])
        msg.body = ('Dear customer, please pay the pending payment with '
                   'Dgitalpay')
        msg.html = ('<h1>Digitalpay</h1>'
                    '<p>Dear customer, please pay the pending payment with '
                    '<b>Digitalpay</b>!</p>')
        mail.send(msg)
        flash(f'A test message was sent to {recipient}.')
        return redirect(url_for('sendmail'))
    return render_template('sendmail.html')
 
# starting the app
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug = True, port = 8080)
