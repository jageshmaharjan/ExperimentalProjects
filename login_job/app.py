import flask
from flask import Flask
from flask_login import LoginManager, current_user, logout_user, login_required, login_user, UserMixin
from sqlalchemy.testing.pickleable import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

login_manager = LoginManager()
login_manager.init_app(app)

users = {'foo@bar.tld' : {'password': 'secret'}}


class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    print(user)
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    user.is_authenticated = request.form['password'] == users[email]['password']
    return user

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         login_user(user)
#
#         flask.flash('Logged In Successfully!')
#         next = flask.request.args.get('next')
#         if not is_safe_url(next):
#             return flask.abort(400)
#         return flask.abort(400)
#     return flask.render_template('login.html', form=form)

@app.route('/')
def index():
    return "Hello Boy!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3030, debug=True)