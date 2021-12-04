from flask import render_template,flash,redirect,url_for
from app import firebase
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
    if form.validate_on_submit():
        print("asdadasdasd")
        # auth = firebase.auth()
        # token = auth.create_user_with_email_and_password(
        #     form.email.data,
        #     form.password.data
        #     )
        # print(token)
        # auth.send_email_verification(token["tokenID"])
    return render_template("signup.html",title="Sign up",form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        print(f"{form.email.data} you are log in now...","success")
        redirect(url_for('login'))
    return render_template("login.html",title="Log in",form=form)
