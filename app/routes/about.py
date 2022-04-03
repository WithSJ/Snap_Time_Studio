from app import app
from app.util import isLogin
from flask import render_template,session

@app.route("/about")
def about():
    """About page for website details and devlopers"""
    LogedIn = isLogin(session)
    return render_template(
        "about.html",
        title="About",
        LogedIn = LogedIn)