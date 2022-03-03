from logging import error
from flask import render_template,flash,request,make_response,redirect,url_for
from app import firebase
from app.firebase.authentication import SignUp,Login,PasswordReset
from app.forms import SignupForm,LoginForm,ForgotForm,PhotoUploadForm,VideoUploadForm
from app.firebase import config

from app import app
from datetime import date, datetime

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

@app.route("/admin",methods=['GET', 'POST'])
def admin():
    form = dict()
    form["photoUploadForm"]=PhotoUploadForm()
    form["videoAddForm"]= VideoUploadForm()
    adminTab = {"TabNumber":1}
    
    if form["photoUploadForm"].submit.data == True:
        photo = form["photoUploadForm"].photo.data
        photoTitle = form["photoUploadForm"].title.data
        
        # GEt Date
        if form["photoUploadForm"].autodate.data == True:
            dateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            dateTime = str(
                form["photoUploadForm"].year.data) + "-"+ str(
                form["photoUploadForm"].month.data) +"-"+ str(
                form["photoUploadForm"].day.data)
        # End Geting Date
        
        
        dataSet = {
            "photoTitle":photoTitle,
                "photo":photo,
            "dateTime":dateTime,}
        
        print(dataSet)
        
        # adminTab = {"TabNumber":3}
        return render_template(
            "admin_pannel.html", title="Admin",form=form,adminTab=adminTab
        )

    
    if form["videoAddForm"].submit.data == True:
        videoTitle = form["videoAddForm"].title.data
        videoUrl = form["videoAddForm"].videoUrl.data

        dataSet = {
            "videoTitle":videoTitle,
            "videoUrl" : videoUrl
        }
        print(dataSet)

        # adminTab = {"TabNumber":4}
        return render_template(
            "admin_pannel.html", title="Admin",form=form,adminTab=adminTab
        )


    
    return render_template(
        "admin_pannel.html", title="Admin",form=form,adminTab=adminTab
    )

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

@app.route("/login",methods=['POST','GET'])
def login():

    # userID = request.cookies.get("userID")
    # if userID != None :
    #     print(userID)
    form = LoginForm()
    forgot_form=ForgotForm()

    if form.submit.data == True:
        isError=Login(form.email.data,form.password.data)
        if isError["ERROR"]:
            
            flash(isError["MESSAGE"],"danger")
        else:
            flash(isError["MESSAGE"],"secondary")
            # webResp = make_response(redirect("photography"))
            # webResp.set_cookie("userID","#Admin")
            # return  webResp

        # redirect(url_for('login'))
    
    if forgot_form.reset.data == True:
        isError = PasswordReset(forgot_form.email.data)
        if isError["ERROR"]:
            
            flash(isError["MESSAGE"],"danger")
        else:
            flash(isError["MESSAGE"],"secondary")


    return render_template("login.html",title="Log in",form=form,forgot_form=forgot_form)
