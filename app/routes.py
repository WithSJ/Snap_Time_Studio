from logging import error
from flask import render_template,flash,request,make_response,redirect,url_for
from app import firebase
from app.firebase.authentication import SignUp,Login,PasswordReset
from app.forms import SignupForm,LoginForm,ForgotForm,PhotoUploadForm,VideoUploadForm
from app.firebase import config
from app.database import post_new_photo,get_all_photos

from app import app
from datetime import datetime
import time

firebase = config.firebase

@app.route("/")
@app.route("/photography")
def photography():

    allPhotos = get_all_photos()
    return render_template("photography.html", title="Photography",allPhotos=allPhotos)

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
        
        
        # dataSet = {
        #     "photoTitle":photoTitle,
        #         "photo":photo,
        #     "dateTime":dateTime,}
        
        post_new_photo(
            id= str(time.time()).replace(".",""),
            title= photoTitle,dateTime=dateTime,image=photo)
        
        allPhotos = get_all_photos()
        adminTab = {"TabNumber":3}
        return render_template(
            "admin_pannel.html", title="Admin",form=form,adminTab=adminTab,
            allPhotos = allPhotos
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


    allPhotos = get_all_photos()

    return render_template(
        "admin_pannel.html", title="Admin",form=form,adminTab=adminTab,
        allPhotos=allPhotos
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
        loginResp=Login(form.email.data,form.password.data)
        if loginResp["ERROR"]:
            
            flash(loginResp["MESSAGE"],"danger")
        else:
            flash(loginResp["MESSAGE"],"secondary")
            # webResp = make_response(redirect("photography"))
            # webResp.set_cookie("userID","#Admin")
            # return  webResp

        # redirect(url_for('login'))
    
    if forgot_form.reset.data == True:
        resetResp = PasswordReset(forgot_form.email.data)
        if resetResp["ERROR"]:
            
            flash(resetResp["MESSAGE"],"danger")
        else:
            flash(resetResp["MESSAGE"],"secondary")


    return render_template("login.html",title="Log in",form=form,forgot_form=forgot_form)
