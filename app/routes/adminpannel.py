from flask import Flask, render_template,request,flash,make_response,redirect, session,url_for
from app import firebase
from app.firebase.authentication import SignUp,Login,PasswordReset
from app.forms import (SignupForm,LoginForm,
ForgotForm,PhotoUploadForm,VideoUploadForm,SelectBookingDateTime,SelectBookingPlan)
from app.firebase import config
from app.database import post_new_photo,get_all_photos,get_all_videos,post_new_video
from app.firebase.database import ( UploadPhotosData_onFirebase, 
                                    UploadVideosData_onFirebase,
                                    GetData)
from app.util import get_month_days, isLogin,get_key,get_cookie
from app import app
from datetime import datetime
import time
from random import randint
firebase = config.firebase










# Admin Pannel Code
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
        id= str(time.time()).replace(".","")
        post_new_photo(
            id,
            title= photoTitle,dateTime=dateTime,image=photo)
        
        # Upload photos data on firebase
        UploadPhotosData_onFirebase(
            id,
            title= photoTitle,dateTime=dateTime,image=photo
        )

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
        id= str(time.time()).replace(".","")
        post_new_video(
            id,
            title=videoTitle,
            dateTime=dateTime,
            videoUrl=videoUrl)

        UploadVideosData_onFirebase(
            id,
            title=videoTitle,
            dateTime=dateTime,
            videoUrl=videoUrl

        )

    allVideos = get_all_videos()

    return render_template(
        "admin_pannel_videos.html", title="Admin",form=form,allVideos=allVideos
    )



@app.route("/admin/signout",methods=['GET', 'POST'])
def admin_signout():
    if "_a.k_" in session:
        session.pop("_a.k_",None)
        return redirect("/")
    
