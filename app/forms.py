from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Email

class SignupForm(FlaskForm):
    
    email = StringField('Email',validators=[DataRequired(),Email()])
    fullname = StringField('Full name',validators=[DataRequired(),Length(max=25)])
    username = StringField('Username',validators=[DataRequired(),Length(min=5,max=25)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=8)])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Log in')


class ForgotForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    reset = SubmitField('Reset')
    

