from app import app
from app.util import isLogin,get_key
from app.firebase.authentication import Login,PasswordReset
from app.forms import LoginForm,ForgotForm
from flask import render_template,session,flash,make_response,redirect


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