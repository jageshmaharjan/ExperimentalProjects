from flask import Flask, render_template, redirect
from flask_login import current_user, LoginManager, login_required, logout_user
from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy

# from models import *
# from wtform_fields import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

#configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xhvnuzkxbhsivk:fa7f00137c71ec173592c355e57e9c79bd2c3d3de12d98fa2647e58b56e15d82@ec2-3-91-112-166.compute-1.amazonaws.com:5432/dbnoo6hc4hkbah'
db = SQLAlchemy(app)

socket = SocketIO(app)

# login = LoginManager(app)
# login.init_app(app)
#
# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))
#
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     reg_form = RegistrationForm()
#     if reg_form.validate_on_submit():
#         username = reg_form.username.data
#         password = reg_form.password.data
#
#         user_object = User.query.filter_by(username=username).first()
#         if user_object:
#             return "someonelse have the username"
#
#         user = User(username=username, password=password)
#         db.session.add(user)
#         db.session.commit()
#         return "Inserted to DB"
#
#     render_template("index.html", form=reg_form)
#
#
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect('login.html')


@socket.on('message')
def message(data):
    print(f'\n\n{data}\n\n')
    send(data)
    emit('some-event', 'this is a custom event message')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('webrtc-stream.html', boardcast=True)


if __name__ == "__main__":
    socket.run(app, debug=True, host='0.0.0.0', port=3000)