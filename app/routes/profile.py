from app import app
from app.util import isLogin
from flask import render_template,session,redirect

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
