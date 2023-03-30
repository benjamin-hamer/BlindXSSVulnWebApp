import hashlib
from flask import Flask, flash, render_template, request, make_response, session
import os
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('index.html')

@app.route('/thankyou', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        message = request.form['message']
        return render_template('thankyou.html', message=message)
    else:
        response = make_response(render_template('message.html'))
        return response

def check_password(username, password, con):
    # Get the user's salt and password hash from the database
    cur = con.cursor()
    cur.execute("SELECT salt, password_hash FROM users WHERE username=?", (username,))
    result = cur.fetchone()

    if result is not None:
        salt = result[0]
        password_hash = result[1]

        # Hash the password with the salt using SHA-256
        test_password_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

        # Compare the hash with the one in the database
        if test_password_hash == password_hash:
            return True

    return False

@app.route('/login', methods=['POST'])
def do_admin_login():
	password = request.form['psw']
	user = request.form['id']
	con = sqlite3.connect('users.db')
	if check_password(user, password, con):
		session['logged_in'] = True
	else:
		flash('wrong password!')
	return home()

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0')