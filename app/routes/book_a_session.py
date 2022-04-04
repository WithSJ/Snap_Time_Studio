from distutils.command import check
from app import app
from app.util import get_key, isLogin,get_month_days,get_cookie
from app.forms import SelectBookingPlan,SelectBookingDateTime,CheckoutForm
from app.firebase.database import GetData,NewBookingOrder
from flask import render_template,session,request,flash,make_response
from datetime import datetime
import time


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

    checkoutForm = CheckoutForm()
    # checkout Form

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
        
        webresp = make_response(
            render_template(
            "booking_checkout.html", 
            title="Book A Session",
            LogedIn = LogedIn,
            data = data,
            form = checkoutForm
            )
        )
        dataID = get_key()
        webresp.set_cookie("_chkout_",dataID)
        session[dataID] = data
 
        return webresp 
    
    if checkoutForm.checkoutSubmit.data == True:
        dataID = get_cookie("_chkout_")
        data = session[dataID]
        data["userPhone"] = checkoutForm.phone.data
        data["userAddress"] = checkoutForm.address.data
        data["userState"] = checkoutForm.state.data
        data["userCity"] = checkoutForm.city.data
        data["userArea"] = checkoutForm.area.data
        userID = get_cookie("userID")
        localID=session[userID]
        timestamp = str(time.time()).split(".")[0]
        NewBookingOrder(localId=localID,orderTimeStamp=timestamp,orderData=data)
        return data


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
