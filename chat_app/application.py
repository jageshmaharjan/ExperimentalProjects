from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy

from passlib.hash import pbkdf2_sha256

from wtform_fields import *
from models import *

from flask_socketio import SocketIO, send, join_room, leave_room

app = Flask(__name__)
app.secret_key = 'key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xhvnuzkxbhsivk:fa7f00137c71ec173592c355e57e9c79bd2c3d3de12d98fa2647e58b56e15d82@ec2-3-91-112-166.compute-1.amazonaws.com:5432/dbnoo6hc4hkbah'
db = SQLAlchemy(app)

socketio = SocketIO(app)
# ROOMS = ["lounge", "news", "games", "coding"]

login = LoginManager()
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # Allow login if validate is succes
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        # if current_user.is_authenticated:
        #     return "Logged in with flask login"
        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)


@app.route("/chat", methods=['GET', 'POST'])
@login_required
def chat():
    if not current_user.is_authenticated:
        flash("Please login", 'danger')
        return redirect(url_for('login'))
    return "chat here"


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out successfully!', 'success')
    return redirect(url_for('login'))


# @app.route("/chat", methods=['GET', 'POST'])
# def chat():
#     # if not  current_user.is_authenticated:
#     #     flash('Please login.', 'danger')
#     #     return redirect(url_for('login'))
#     return render_template('chat.html', username=current_user.username,
#                            rooms=ROOMS)
#
#
# @socketio.on('message')
# def message(data):
#     print(f'\n\n{data}\n\n')
#     send({'msg':data['msg'], 'username':data['username'],
#           'time_stamp':strftime('%b-%d %I:%M%p', localtime())}, room=data['room'])
#
# @socketio.on('join')
# def join(data):
#     join_room(data['room'])
#     send({'msg': data['username'] + " has joined the " + data['room'] + "room"}, room=data['room'])
#
# @socketio.on('leave')
# def leave(data):
#     leave_room(data['room'])
#     send({'msg': data['username'] + " has left the " + data['room'] + "room"}, room=data['room'])


@app.route('/', methods=['GET', 'POST'])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # hashing the password
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Check username exist
        # user_object = User.query.filter_by(username=username).first()
        # if user_object:
        #     return "someone else has taken this username"

        # Add user to Db
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash("registered Successfully. Please login.", "success")
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)


if __name__ == '__main__':
    # app.run(debug=True)
    socketio.run(app, debug=True, host='0.0.0.0', port=3000)