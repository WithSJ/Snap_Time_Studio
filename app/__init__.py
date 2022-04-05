from flask import Flask
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config())

from app import routes
from app.routes import (
    photography,
    videography,
    about,
    book_a_session,
    signup,
    login,
    logout,
    adminpannel,
    profile
    )


