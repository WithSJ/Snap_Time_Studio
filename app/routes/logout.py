
from app import app
from app.util import isLogin,get_cookie
from flask import redirect,session

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
