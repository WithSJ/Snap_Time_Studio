from app import app
from app.util import isLogin
from app.database import get_all_videos
from flask import render_template,session


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