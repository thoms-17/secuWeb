#!/usr/bin/env python3

from flask import Flask, request, redirect, send_from_directory, render_template, make_response
from random import randrange
import jwt
import sqlite3
import hashlib


app = Flask(__name__, static_folder='html/res/', static_url_path='/static', template_folder='html')

APP_NAME='mybank.io'
JWT_SECRET='secret'

def md5(v):
    return hashlib.md5(v.encode()).hexdigest()

# DB Init

def sqlite3_connect(custom_dbfile=None):
    conn = None
    try:
        if not custom_dbfile:
            conn = sqlite3.connect('./db.sqlite')
        else:
            conn = sqlite3.connect(custom_dbfile)
    except Exception as e:
        print(e)
    return conn

def sql_exec(req, all=False, custom_dbfile=None):
    print('\tExecuting : '+req)
    conn = sqlite3_connect(custom_dbfile)
    cur = conn.cursor()
    try:
        cur.execute(req)
        conn.commit()
    except Exception as e:
        return str(e)
    return cur.fetchone() if not all else cur.fetchall()

# Server Routes

@app.route('/')
def home():
    return render_template('index.html', app_name=APP_NAME)

@app.route('/partials/<file>')
def partials(file):
    user = None
    if request.cookies.get('mb_session_id'):
        user = jwt.decode(request.cookies.get('mb_session_id'), JWT_SECRET, algorithms=['HS256'])

    if file == 'profile.html' or file == 'transfer.html':
        if not user:
            return '<h1>You are not logged in</h1><img src="" onerror="window.location=\'/?view=login\'"/>'
        print(user)
        return render_template('partials/'+file, user=user)

    return render_template('partials/'+file)

# API Routes

@app.route('/api/login', methods=['POST'])
def login():
    if request.form.get('login'):
        if request.form.get('password'):
            login = request.form.get('login')
            password = request.form.get('password')
            req = "SELECT * FROM users WHERE email='"+login+"' AND password='"+md5(password)+"'"
            out = sql_exec(req)
            print(out)
            if out == None:
                return redirect('/?view=login&error=Invalid login or password')
            token = jwt.encode({
                'user_id':out[0], 
                'first_name':out[1], 
                'last_name':out[2],
                'email':out[3],
                'password':out[4],
                'account_number':out[5],
                'account_sum':out[6],
                'otp_token':out[7],
                'pin':out[8]
            }, JWT_SECRET, algorithm="HS256")
            resp = make_response(redirect('/?view=profile'))
            resp.set_cookie('mb_session_id', token)
            return resp
    return redirect('/?view=profile')

@app.route('/api/register', methods=['POST'])
def register():
    if request.form.get('email'):
        if request.form.get('password'):
            if request.form.get('last_name') and request.form.get('first_name'):
                user = {
                    "email":request.form.get('email'), 
                    "password":request.form.get('password'), 
                    "last_name":request.form.get('last_name'), 
                    "first_name":request.form.get('first_name')
                }
                req = f"INSERT INTO users VALUES({randrange(1000,9999)}, '{user['first_name']}', '{user['last_name']}', '{user['email']}', '{md5(user['password'])}', {randrange(1000000000, 9999999999)}, 0, {randrange(100, 999)}, {randrange(1000,9999)})"
                out = sql_exec(req)
                print(out)
                if out is None:
                    return redirect('/?view=login&message=Account successfully created')
                return redirect('/?view=register&message=Database Error - Please try again later') 
    return 


@app.route('/api/transfer', methods=['POST'])
def transfer():
    if request.form.get('sum'):
        if request.form.get('recipient'):
            if request.form.get('pin'):
                user = None
                user = jwt.decode(request.cookies.get('mb_session_id'), JWT_SECRET, algorithms=['HS256'])
                print(request.form.get('pin'))
                if str(request.form.get('pin')) != str(user['pin']):
                    return 'Invalid PIN specified.'
                if request.form.get('sum') > user['account_sum']:
                    return 'You do not have enough money on your account.'
                req1 = f"UPDATE users SET account_sum = account_sum + {request.form.get('sum')} WHERE account_number='{request.form.get('recipient')}'"
                print(req1)
                out1 = sql_exec(req1)
                print(out1)
                req2 = f"UPDATE users SET account_sum = account_sum - {request.form.get('sum')} WHERE account_number='{str(user['account_number'])}'"
                print(req2)
                out2 = sql_exec(req2)
                print(out2)
                if out1 is None and out2 is None:
                    req = "SELECT * FROM users WHERE email='"+user['email']+"'"
                    out = sql_exec(req)
                    print(out)
                    if out == None:
                        return redirect('/?view=login&error=Invalid login or password')
                    token = jwt.encode({
                    'user_id':out[0],
                    'first_name':out[1], 
                    'last_name':out[2],
                    'email':out[3],
                    'password':out[4],
                    'account_number':out[5],
                    'account_sum':out[6],
                    'otp_token':out[7],
                    'pin':out[8]
                    }, JWT_SECRET, algorithm="HS256")
                    resp = make_response(redirect('/?view=profile&message=Transfer successfully done'))
                    resp.set_cookie('mb_session_id', token)
                    return resp
                return 'SQL Error : %s %s' %(out1, out2)


# CREATE TABLE users(user_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT, password TEXT, account_number TEXT, account_sum TEXT, otp_token INTEGER, pin INTEGER)

#mail@lp1.eu test4242

def main():
    app.run(threaded=True, host="0.0.0.0")

if __name__ == "__main__":
    exit(main())
