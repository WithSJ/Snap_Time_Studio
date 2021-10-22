from flask import render_template

from app import app

@app.route("/")
@app.route("/photography")
def photography():
    return render_template("photography.html", title="Photography")