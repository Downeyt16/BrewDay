import logging
from flask import Flask, request, render_template, Response, session, redirect, url_for
from scripts.database import connectDB, closeConnection
from scripts.userAuth import loginUser, validateUser
import mysql.connector
import re

app = Flask(__name__)
app.secret_key = 'bH\xc0\x9aN\x9b\x7f\xc8{\x95\x12\xcf\xff\xa3tJ$jX\xe8\xb5\x18f\xc4\xb9'

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        ##Seperate DB connection to seperate file
        cnx, cursor = connectDB()
        cursor.execute('SELECT * from BrewDayDB.user WHERE name = "%s"', username)
        user = cursor.fetchone()

        if user:
            error = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            error = 'Username should contain only characters and number!'
        else:
            insert = ('INSERT INTO BrewDayDB.user' '(name,password)' 'VALUES (%s, %s)')
            newUser = (username, password)
            cursor.execute(insert, newUser)
            cnx.commit()

        closeConnection(cnx, cursor)
        return redirect(url_for('login'))

    elif request.method == 'POST':
        error = "Please fill out the form"
        
    return render_template('registration.html', msg = error)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(username)

        cnx, cursor = connectDB()
        cursor.execute('SELECT * from BrewDayDB.user WHERE name = %s and password = %s', (username, password))
        user = cursor.fetchone()
        closeConnection(cnx, cursor)

        if user:
            session['login'] = True
            session['username'] = user[0]
            session['id'] = user[2]
            print('Hello ' + session['username'] + ": Your user id is " + str(session['id']))
            return redirect(url_for('landing'))
        else:
            print("This account doesnt exist")
    return render_template('signin.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
   session.pop('login', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route('/landing')
def landing():
    if 'login' in session:
        return render_template('landing.html', username = session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'login' in session:
        cnx, cursor = connectDB()
        cursor.execute('SELECT * from BrewDayDB.user WHERE userid = %s', [session['id']])
        user = cursor.fetchone()
        closeConnection(cnx, cursor)
        return render_template('profile.html', user = user)
    return redirect(url_for('login'))

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
