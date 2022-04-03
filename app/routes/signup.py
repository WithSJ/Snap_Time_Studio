from app import app
from app.util import isLogin
from app.firebase.authentication import SignUp
from app.forms import SignupForm
from flask import render_template,session,flash


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