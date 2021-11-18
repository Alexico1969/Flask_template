
from os import getenv, environ
from flask import Flask, render_template, session, request, redirect, url_for, g
from users import get_user, add_user, verify_user

app = Flask(__name__)

app.secret_key = 'Bruce Wayne is Batman'

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = verify_user(password=password, email=email)
        if user:
            session['userid'] = user[0]
            return render_template('home.html', user=user);
        else:
            msg = 'Invalid email or password'
            return render_template('login.html', msg=msg);

        return
    elif request.method == 'GET':
        return render_template('login.html');

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm-password']
        msg = None
        if password != confirm:
            msg = 'Passwords Do Not Match'
        elif not email:
            msg = 'Must have an email'
        elif not name:
            msg = 'Must have a name'
        else:
            user = add_user(name=name, password=password, email=email)
            if not user:
                msg = 'Unable To Add User'
            return redirect(url_for('login'))
        return render_template('signup.html', msg=msg);
    elif request.method == 'GET':
        return render_template('signup.html');

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('home_page'))

# Do not alter this if statement below
# This should stay towards the bottom of this file
if __name__ == "__main__":
    flask_env = getenv('FLASK_ENV')
    if flask_env != 'production':
        environ['FLASK_ENV'] = 'development'
        app.debug = True
        app.asset_debug = True
        server = Server(app.wsgi_app)
        server.serve()
    app.run()

    #https://api.nasa.gov/planetary/apod?api_key=VM2f40EQQ0tk58nvmPhpVa6gthc5ma6Chgll56N7