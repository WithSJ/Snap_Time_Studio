from app import app
from app.util import isLogin
from app.database import get_all_photos
from flask import render_template,session


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
