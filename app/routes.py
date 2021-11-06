from flask import render_template

from app import app

@app.route("/")
@app.route("/photography")
def photography():
    return render_template("photography.html", title="Photography")

@app.route("/videography")
def videography():
    return render_template("videography.html", title="Videography")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/book_a_session")
def book_a_session():
    return render_template("book_a_session.html", title="Book A Session")
