# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import  InputRequired, Length, EqualTo, ValidationError
#
# from passlib.hash import pbkdf2_sha256
#
# from models import *
#
# class RegistrationForm(FlaskForm):
#     """ Registration form"""
#
#     username = StringField("username_label",
#                            validators=[InputRequired(message="Username Required"),
#                                        Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
#     password = PasswordField("password_label", validators=[InputRequired(message="Password Required")])
#     confirm_pswd = PasswordField("confirm_pswd_label", validators=[InputRequired(message="password required"),
#                                                                    EqualTo('password', message="password must match")])
#
#     submit_button = SubmitField('Create')
#
#     def validate_username(self, username):
#         user_object = User.query.filter_by(username=username.data).first()
#         if user_object:
#             raise ValidationError("Username already exist")
#
#
# def invalid_credentials(form, field):
#     """ username and password checker """
#
#     username_entered = form.username.data
#     password_entered = field.data
#
#     # check credentials
#     user_object = User.query.filter_by(username=username_entered).first()
#     if user_object is None:
#         raise ValidationError("Username or password is incorrect")
#     elif not pbkdf2_sha256.verify(password_entered, user_object.password):
#         raise ValidationError("Username or password is incorrect")
#
#
# class LoginForm(FlaskForm):
#     """ Login Form"""
#
#     username = StringField("username_label",
#                            validators=[InputRequired(message="username required")])
#     password = PasswordField("password_label",
#                            validators=[InputRequired("password is required"),
#                                        invalid_credentials])


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from passlib.hash import pbkdf2_sha256
from models import User


def invalid_credentials(form, field):
    """ Username and password checker """

    password = field.data
    username = form.username.data

    # Check username is invalid
    user_data = User.query.filter_by(username=username).first()
    if user_data is None:
        raise ValidationError("Username or password is incorrect")

    # Check password in invalid
    elif not pbkdf2_sha256.verify(password, user_data.hashed_pswd):
        raise ValidationError("Username or password is incorrect")


class RegistrationForm(FlaskForm):
    """ Registration form"""

    username = StringField('username', validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="Username must be between 4 and 25 characters")])
    password = PasswordField('password', validators=[InputRequired(message="Password required"), Length(min=4, max=25, message="Password must be between 4 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pswd', validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists. Select a different username.")

class LoginForm(FlaskForm):
    """ Login form """

    username = StringField('username', validators=[InputRequired(message="Username required")])
    password = PasswordField('password', validators=[InputRequired(message="Password required"), invalid_credentials])