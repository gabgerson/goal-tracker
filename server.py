from flask import (Flask, request, render_template, flash, session, jsonify, redirect, g)
from jinja2 import StrictUndefined # Ask what this does docs are confusing
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

def val_(query):
    print(query.val().items())

    return query.val().items()

app.jinja_env.globals.update(val_= val_)
    
@app.route("/")
def index():
    """Show homepage"""

    return render_template("homepage.html")

    
@app.route("/sign-up")
def sign_up():
    """Show signup form"""

    return render_template("signup.html")


@app.route("/sign-up", methods=["POST"])
def register_process():
    #get email and password from form
       #get email and password from form
    username = request.form.get("username")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    # if that use is not in database add them
    user_in_db = db.child("users").child(username).get()
    if "username" in session:
        flash("Please logout")
    elif user_in_db.each() is None:
        password = generate_password_hash(password)
        db.child("users").child(username).set({"fname":fname, "lname":lname, "email":email, "password":password})
        # user.set_password(password)
        return redirect("/login")
    else:
        #if user in database flash user already exists
        flash('This user already exists.')
    
        return redirect("/login")


@app.route("/login")
def login():
    """Show login form"""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_process():
    #get email and password from form
  
            #get email and password from form
    username = request.form.get('username')
    print(username)
    password = request.form.get('password')
    print(password)
    #search for user in database 
    user_in_db = db.child("users").child(username).get()
    
    #if use in database add then to session
    if user_in_db.each() is not None and check_password_hash(user_in_db.val()["password"], password): 
        session["username"] = username
        print(session["username"])
    
        flash('Logged in')
        return redirect("/goals")
    else: 
        flash('Username and password do not match.')
        return redirect("/login")


@app.route("/logout")
def logout_process():

    return redirect("/")



@app.route("/goals")
def show_goals():
    username = session["username"]
    goals = db.child("goals").child(username).get()
    print(goals.val().items)
    print("lookatme")
    
    
    # for goal in goals.each():
    #     print(goal.key())

    #     for k,v in :
    #         print(k)
    #         print(v)

    return render_template("goals.html", goals = goals)


@app.route("/add-goal", methods=["POST", "GET"])
def add_goal():

    title = request.form.get("title")
    print(title)
    username = session["username"]

    print(username)
    
    user = db.child("goals").child(username).child(title).get()
    print(user.val())
    print(user is None)
    if user.val() is None:
        db.child("goals").child(username).child(title).set({"task": "no task yet"})
    return redirect("/goals")
    

@app.route("/add-task", methods=["POST"])
def add_task():
    username = session["username"]
    title = request.form.get("title")
    
    task = request.form.get("task")
    user = db.child("goals").child(username).child(title).get()

    if user.val().get("task"):
       db.child("goals").child(username).child(title).set({task:False})
    else:
        db.child("goals").child(username).child(title).update({task:False})
    return redirect("/goals")



if __name__ == "__main__":

  
    # We have to set debug=True here, since it has to be True at the
    
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug



    DebugToolbarExtension(app)

    app.run(debug=True, host='0.0.0.0')

