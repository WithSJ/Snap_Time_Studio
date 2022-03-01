from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms import SelectField,TextAreaField,BooleanField,FileField
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

class PhotoUploadForm(LoginForm):
    title = StringField('Title',validators=[DataRequired(),Length(min=5,max=60)])
    day = SelectField('Day',choices=[_ for _ in range(1,32)])
    month = SelectField('Month',choices=[_ for _ in range(1,13)])
    year = SelectField('Year',choices=[_ for _ in range(2020,2071)])
    autodate = BooleanField('Today Date')
    photo = FileField("Image")
    submit = SubmitField('Upload')
    



