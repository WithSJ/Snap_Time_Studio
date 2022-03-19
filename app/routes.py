from flask import Flask, render_template,request,flash,make_response,redirect, session,url_for
from app import firebase
from app.firebase.authentication import SignUp,Login,PasswordReset
from app.forms import (SignupForm,LoginForm,
ForgotForm,PhotoUploadForm,VideoUploadForm,SelectBookingDateTime,SelectBookingPlan)
from app.firebase import config
from app.database import post_new_photo,get_all_photos,get_all_videos,post_new_video
from app.util import get_month_days, isLogin,get_key
from app import app
from datetime import datetime
import time
from random import randint
firebase = config.firebase


@app.route("/")
@app.route("/photography")
def photography():
    LogedIn = isLogin()
    

    allPhotos = get_all_photos()
    return render_template(
        "photography.html", 
        title="Photography",
        allPhotos=allPhotos,
        LogedIn = LogedIn)

@app.route("/videography")
def videography():
    LogedIn = isLogin()
    allVideos = get_all_videos()
    return render_template(
        "videography.html", 
        title="Videography",
        allVideos=allVideos,
        LogedIn = LogedIn)

@app.route("/about")
def about():
    LogedIn = isLogin()
    return render_template(
        "about.html",
        title="About",
        LogedIn = LogedIn)

@app.route("/book_a_session", methods=['GET', 'POST'])
def book_a_session():
    LogedIn = isLogin()
    days = get_month_days()
    today = str(datetime.today()).split()[0]
    selectBookingPlan = SelectBookingPlan()
    selectDateTimeForm = SelectBookingDateTime()

    if selectDateTimeForm.submit.data == True:
        print(selectDateTimeForm.date.data)
        print(selectDateTimeForm.time.data)
        return render_template(
            "booking_checkout.html", 
            title="Book A Session",
            LogedIn = LogedIn)
    

    if selectBookingPlan.inStudio.data == True:
        print("InStudio")
        return render_template(
            "booking_calender.html", 
            title="Book A Session",
            days=days,
            today=today,
            form=selectDateTimeForm,
            LogedIn = LogedIn)
    
    
    if selectBookingPlan.outStudio.data == True:
        print("OutStudio")
    
    if selectBookingPlan.events.data == True:
        print("Events")
    
    return render_template(
        "book_a_session.html",
        title="Book A Session",
        form=selectBookingPlan,
        LogedIn = LogedIn)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    LogedIn = isLogin()
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

            
    return render_template(
        "signup.html",
        title="Sign up",
        form=form,
        LogedIn = LogedIn)

@app.route("/login",methods=['POST','GET'])
def login():
    LogedIn = isLogin()
    
    form = LoginForm()
    forgot_form=ForgotForm()

    if form.submit.data == True:
        loginResp=Login(form.email.data,form.password.data)
        if loginResp["ERROR"]:
            
            flash(loginResp["MESSAGE"],"danger")
        else:
            flash(loginResp["MESSAGE"],"secondary")
            webResp = make_response(redirect("photography"))
            webResp.set_cookie("userID","#Admin")
            return  webResp

        # redirect(url_for('login'))
    
    if forgot_form.reset.data == True:
        resetResp = PasswordReset(forgot_form.email.data)
        if resetResp["ERROR"]:
            
            flash(resetResp["MESSAGE"],"danger")
        else:
            flash(resetResp["MESSAGE"],"secondary")


    return render_template(
        "login.html",
        title="Log in",
        form=form,
        forgot_form=forgot_form,
        LogedIn = LogedIn)

@app.route("/profile")
def profile():
    LogedIn = isLogin()
    if LogedIn == False:
        return redirect("login")
    return render_template(
        "account_profile.html",
        title="Account",
        LogedIn = LogedIn)




EMAIL = "StudioAdmin"
PASS = "qwerty2000"

@app.route("/admin",methods=['GET', 'POST'])
def admin_login():
    ak = request.cookies.get("_a.k_")
    if "_a.k_" in session:
        if ak == session["_a.k_"]:
            return redirect("/admin/dashboard")


    form = LoginForm()

    if form.submit.data == True:
        if form.email.data == EMAIL and form.password.data == PASS:
            
            AdminKey = get_key()
            session["_a.k_"] = AdminKey
            resp = make_response(redirect("/admin/dashboard"))
            resp.set_cookie("_a.k_",AdminKey)
            return resp


        


    return render_template("admin_pannel_login.html", title="Admin",form=form)


@app.route("/admin/dashboard")
def admin_dashboard():
    ak = request.cookies.get("_a.k_")
    if "_a.k_" not in session:
        return redirect("/admin")
    else:
        if ak != session["_a.k_"]:
            return redirect("/admin")

        
    return render_template("admin_pannel_dashboard.html", title="Admin")



@app.route("/admin/photos",methods=['GET', 'POST'])
def admin_photos():
    ak = request.cookies.get("_a.k_")
    if "_a.k_" not in session:
        return redirect("/admin")
    else:
        if ak != session["_a.k_"]:
            return redirect("/admin")

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
    ak = request.cookies.get("_a.k_")
    if "_a.k_" not in session:
        return redirect("/admin")
    else:
        if ak != session["_a.k_"]:
            return redirect("/admin")

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



@app.route("/admin/signout",methods=['GET', 'POST'])
def admin_signout():
    if "_a.k_" in session:
        session.pop("_a.k_",None)
        return redirect("/")
    
