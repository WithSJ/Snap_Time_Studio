from app import app
from app.util import isLogin,get_cookie
from flask import render_template,session,redirect
from app.firebase.database import GetMyBookingOrders
@app.route("/profile")
def profile():
    """profile page only for user if logout than don't show """
    LogedIn = isLogin(session) #check login status
    if LogedIn == False:
        return redirect("login")
    userID = get_cookie("userID")
    localID = session[userID]

    bookingData = GetMyBookingOrders(localID)

    return render_template(
        "account_profile.html",
        title="Account",
        LogedIn = LogedIn,
        myBooking = bookingData)
