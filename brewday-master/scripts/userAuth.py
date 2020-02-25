import logging
from flask import Flask, request, render_template, Response, session, redirect, url_for
from scripts.database import connectDB, closeConnection
import mysql.connector
import re

def validateUser(request):
       password = ""
       username = ""
       if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
       return username, password

def registerUser(username, password):   
        cnx, cursor = connectDB()
        cursor.execute('SELECT * from BrewDayDB.user WHERE name = "%s"', username)
        print("connected")
        user = cursor.fetchone()
        print(user)
        if user:
            return 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            return 'Username should contain only characters and number!'
        else:
            insert = ('INSERT INTO BrewDayDB.user' '(name,password)' 'VALUES (%s, %s)')
            newUser = (username, password)
            cursor.execute(insert, newUser)
            cnx.commit()
            return loginUser(username, password)
        closeConnection(cnx, cursor)

def loginUser(username, password):
        cnx, cursor = connectDB()
        cursor.execute('SELECT * from BrewDayDB.user WHERE name = %s and password = %s', (username, password))
        user = cursor.fetchone()
        closeConnection(cnx, cursor)

        if user:
            session['login'] = True
            session['username'] = user[0]
            session['id'] = user[2]
            print('Hello ' + session['username'] + ": Your user id is " + str(session['id']))
            return 'landing'
        else:
            return 'login'
    
