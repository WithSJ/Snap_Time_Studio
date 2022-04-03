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


@app.route("/")
@app.route("/photography")
def photography():
    """Show photos page with photos galery"""
    LogedIn = isLogin(session)
    
    allPhotos = get_all_photos()
    # get all photos data
    return render_template(
        "photography.html", 
        title="Photography",
        allPhotos=allPhotos,
        LogedIn = LogedIn)

@app.route("/videography")
def videography():
    """Show Videos page with photos galery"""
    LogedIn = isLogin(session)

    allVideos = get_all_videos()
    # get all videos data
    return render_template(
        "videography.html", 
        title="Videography",
        allVideos=allVideos,
        LogedIn = LogedIn)

@app.route("/about")
def about():
    """About page for website details and devlopers"""
    LogedIn = isLogin(session)
    return render_template(
        "about.html",
        title="About",
        LogedIn = LogedIn)

@app.route("/book_a_session", methods=['GET', 'POST'])
def book_a_session():
    """Booking or orders page for user so they can get our plans"""
    print(session)
    LogedIn = isLogin(session) #check login status
    
    days = get_month_days() 
    # get days and monts for calenders

    today = str(datetime.today()).split()[0]
    #get today date 
    
    selectBookingPlan = SelectBookingPlan()
    # Booking plan form In Studio,Out Studio and On Event
    
    selectDateTimeForm = SelectBookingDateTime()
    # select date time other things 

    """select date time for booking and number of photos"""
    if selectDateTimeForm.submit.data == True:
        # callender booking book btn clicked
        # it redirect to checkout page

        selectDate = selectDateTimeForm.date.data
        selectTime = selectDateTimeForm.time.data
        numPhotos = request.form["numPhotos"]
        
        if selectDate == "" or selectTime == "":
            #if date and time not select than kclick on book
            # than it reload page
            return render_template(
            "booking_calender.html", 
            title="Book A Session",
            days=days,
            today=today,
            form=selectDateTimeForm,
            LogedIn = LogedIn,)
        
        try:
            """
                Try to get user from session if user not lodin
                than it genrate error in so except code run.
            """
            userID = get_cookie("userID")
            userdata = GetData(session[userID])
            print(userdata)
        except:
            flash("You are not Loged In","danger")
            # show msg that you are not login
            
            return render_template(
            "booking_calender.html", 
            title="Book A Session",
            days=days,
            today=today,
            form=selectDateTimeForm,
            LogedIn = LogedIn,)
        
        """data used in checkout page and redirect to checkout """
        data = {
            "selectDate" : selectDate,
            "selectTime" : selectTime,
            "productName" : "Studio Photography",
            "numberPhotos" : numPhotos,
            "selectedTypes" : "Light, Dark, Clasic, Holi, Party",
            "userFullname" : userdata["Fullname"],
            "userUsername" : userdata["Username"],
            "userEmail" : userdata["UserData"]["email"],
            "photosFees" : int(numPhotos) * 100,
            "totalFees" : sum([int(numPhotos) * 100,])
            }
        
        return render_template(
            "booking_checkout.html", 
            title="Book A Session",
            LogedIn = LogedIn,
            data = data)
    

    if selectBookingPlan.inStudio.data == True:
        #This click for InStudio Page
        print("InStudio")
        return render_template(
            "booking_calender.html", 
            title="Book A Session",
            days=days,
            today=today,
            form=selectDateTimeForm,
            LogedIn = LogedIn)
    
    
    if selectBookingPlan.outStudio.data == True:
        #This click for OutStudio Page
        print("OutStudio")
    
    if selectBookingPlan.events.data == True:
        #This click for OnEvent Page
        print("Events")
    
    return render_template(
        "book_a_session.html",
        title="Book A Session",
        form=selectBookingPlan,
        LogedIn = LogedIn)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    """SignUp page show so user can create account"""
    LogedIn = isLogin(session)
    form = SignupForm()
    # Signup form 

    print("SIGNUP")
    if form.submit.data == True:
        # if signup btn click
        
        """it send email pass and user and fullname 
        and wait for any error in bool"""
        isError=SignUp(
            form.email.data,form.password.data,
            form.username.data,form.fullname.data
            )
        if isError["ERROR"]:
            # if error true and show msg
            # print(isError["MESSAGE"])
            flash(isError["MESSAGE"],"danger")
            # error msg show
        else:
            flash(isError["MESSAGE"],"success")
            # Error is false msg show

            
    return render_template(
        "signup.html",
        title="Sign up",
        form=form,
        LogedIn = LogedIn)

@app.route("/login",methods=['POST','GET'])
def login():
    """Show login page for user"""
    LogedIn = isLogin(session)
    
    form = LoginForm()
    # login form 
    
    forgot_form=ForgotForm()
    # forgot form

    if form.submit.data == True:
        # if login btn clicked

        loginResp=Login(form.email.data,form.password.data)
        # get login responce is any error or not
        
        if loginResp["ERROR"]:
            # if any error that show msg
            flash(loginResp["MESSAGE"],"danger")
        else:
            flash(loginResp["MESSAGE"],"secondary")
            # show sccessfull login  msg

            # We need to return responce of login with userID
            # User ID saved in cookies
            webResp = make_response(redirect("photography"))
            userID = get_key() # userId gebrated
            webResp.set_cookie("userID",userID) # userID saved in cookies
            
            session[userID] = loginResp["USERDATA"].localId
            # userID saved in seesion with user login data
            return  webResp

        # redirect(url_for('login'))
    
    if forgot_form.reset.data == True:
        # user password forgot btn clicked
        resetResp = PasswordReset(forgot_form.email.data)
        # password reset responce

        if resetResp["ERROR"]:
            # if any error than show msg
            flash(resetResp["MESSAGE"],"danger")
        else:
            flash(resetResp["MESSAGE"],"secondary")
            # show msg successful reset email send to user Email


    return render_template(
        "login.html",
        title="Log in",
        form=form,
        forgot_form=forgot_form,
        LogedIn = LogedIn)

@app.route("/profile")
def profile():
    """profile page only for user if logout than don't show """
    LogedIn = isLogin(session) #check login status
    if LogedIn == False:
        return redirect("login")
    return render_template(
        "account_profile.html",
        title="Account",
        LogedIn = LogedIn)

@app.route("/logout")
def logout():
    """User logout link remove from session using userid cookie"""

    LogedIn = isLogin(session) # get login status

    if LogedIn == False:
        # if lod out user than redirect to login page
        return redirect("login") 
    
    if LogedIn == True:
        # if user log in than remove user from session
        # and redirect to login page
        session.pop(get_cookie("userID"),None)
        return redirect("login")


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
    
