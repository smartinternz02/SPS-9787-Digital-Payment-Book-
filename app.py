from flask import Flask, render_template, request, redirect, url_for, session, flash
import re
import MySQLdb.cursors
from flask_mysqldb import MySQL





app = Flask(__name__)
  
app.secret_key = 'kolaaa'


app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'FBYfzJrlLk'
app.config['MYSQL_PASSWORD'] = '8G5IXLpLrY'
app.config['MYSQL_DB'] = 'FBYfzJrlLk'
mysql = MySQL(app)


@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods =['GET', 'POST'])
#users login
def login():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password ))
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
            msg = 'Logged in successfully !'
            
            msg = 'Logged in successfully !'
            return redirect(url_for('dashboard', msg=msg))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

#users registeration
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = % s', (username, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s)', (username, email,password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
#users dashboard
@app.route('/dashboard', methods =['GET'])
def dashboard():
    print(session["username"],session['id'])
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM pay WHERE userid = % s', (session['id'],))
    account = cursor.fetchone()
    print("accountdislay",account)

    
    return render_template('dashboard.html',account = account)



  #contact our services
@app.route('/contact')
def contact():

    return render_template('contact.html')
#logout
@app.route('/logout')
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('login.html')


if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True, port = 8080)