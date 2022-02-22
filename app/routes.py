from logging import error
from flask import render_template,flash,redirect,url_for
from app import firebase
from app.firebase.authentication import SignUp,Login
from app.forms import SignupForm,LoginForm
from app.firebase import config

from app import app

firebase = config.firebase

@app.route("/")
@app.route("/photography")
def photography():
    return render_template("photography.html", title="Photography")

@app.route("/videography")
def videography():
    return render_template("videography.html", title="Videography")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/book_a_session")
def book_a_session():
    return render_template("book_a_session.html", title="Book A Session")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    print("SIGNUP")
    if form.submit.data == True:
        isError=SignUp(
            form.email.data,form.password.data,
            form.username.data,form.fullname.data
            )
        if isError["ERROR"]:
            # print(isError["MESSAGE"])
            flash(isError["MESSAGE"],"danger")
        else:
            flash(isError["MESSAGE"],"success")

            
    return render_template("signup.html",title="Sign up",form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    
    if form.submit.data == True:
        isError=Login(form.email.data,form.password.data)
        if isError["ERROR"]:
            
            flash(isError["MESSAGE"],"danger")
        else:
            flash(isError["MESSAGE"],"success")

        redirect(url_for('login'))
    return render_template("login.html",title="Log in",form=form)
