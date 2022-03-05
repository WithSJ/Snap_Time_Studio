from logging import error
from flask import render_template,flash,request,make_response,redirect,url_for
from app import firebase
from app.firebase.authentication import SignUp,Login,PasswordReset
from app.forms import SignupForm,LoginForm,ForgotForm,PhotoUploadForm,VideoUploadForm
from app.firebase import config
from app.database import post_new_photo,get_all_photos,get_all_videos,post_new_video

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
    allVideos = get_all_videos()
    return render_template("videography.html", title="Videography",allVideos=allVideos)

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





@app.route("/admin/dashboard")
@app.route("/admin")
def admin_dashboard():
    
    return render_template("admin_pannel_dashboard.html", title="Admin")



@app.route("/admin/photos",methods=['GET', 'POST'])
def admin_photos():
    form=PhotoUploadForm()
    
    if form.submit.data == True:
        photo = form.photo.data
        photoTitle = form.title.data
        
        # GEt Date
        if form.autodate.data == True:
            dateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            dateTime = str(
                form.year.data) + "-"+ str(
                form.month.data) +"-"+ str(
                form.day.data)
        # End Geting Date
        
        post_new_photo(
            id= str(time.time()).replace(".",""),
            title= photoTitle,dateTime=dateTime,image=photo)

    allPhotos = get_all_photos()

    return render_template("admin_pannel_photos.html", title="Admin",
                            form=form,allPhotos=allPhotos)



@app.route("/admin/videos",methods=['GET', 'POST'])
def admin_videos():
    
    form= VideoUploadForm()
        
    if form.submit.data == True:
        videoTitle = form.title.data
        videoUrl = form.videoUrl.data

        dateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        post_new_video(
            id= str(time.time()).replace(".",""),
            title=videoTitle,
            dateTime=dateTime,
            videoUrl=videoUrl)

    allVideos = get_all_videos()

    return render_template(
        "admin_pannel_videos.html", title="Admin",form=form,allVideos=allVideos
    )
