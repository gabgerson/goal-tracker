from flask import (Flask, request, render_template, flash, session, jsonify, redirect, g)
rom jinja2 import StrictUndefined # Ask what this does docs are confusing
from flask_debugtoolbar  import DebugToolbarExtension
from werkzeug.security import generate_password_hash, check_password_hash
import pyrebase
from config import config

firebase = pyrebase.initialize_app(config)

db = firebase.database()

# db.child("users").push({"fname":"Victoria", "lname":"GG"})
# data = {"name": "Mortimer 'Morty' Smith"}

# db.child("users").child("Morty").set(data)
# db.child("users").remove()

app = Flask(__name__)

app.secret_key = "thisisasecretkey"


@app.route("/")
def index():
    """Show homepage"""

    return render_template("homepage.html")

    
@app.route("/sign-up", methods=["GET"])
def sign_up():
    """Show signup form"""

    return render_template("signup.html")


@app.route("/sign-up", methods=["POST"])
def register_process():
    #get email and password from form


    return redirect("/")


@app.route("/login")
def login():
    """Show login form"""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_process():
    #get email and password from form
  
        return redirect("/login")

@app.route("/logout")
def logout_process():

    return redirect("/")



@app.route("/goals")
def show_goals():

    return render_template("goals.html")


if __name__ == "__main__":

  
    # We have to set debug=True here, since it has to be True at the
    
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug



    DebugToolbarExtension(app)

    app.run(debug=True, host='0.0.0.0')

