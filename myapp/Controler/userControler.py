from flask import (Blueprint,
                   request,
                   render_template,
                   abort,
                   session,
                   redirect,
                   url_for,
                   )

from myapp.Services.userServices import UserManage

user=Blueprint('user',__name__)
from myapp.Models.userModel import User
userService:UserManage=UserManage()

@user.route("/error")
def check_error():
    #raise Exception("Error found!!")
    abort(500)
    
@user.route("/users",methods=["GET"])
def users():
    if session.get("email"):
        return userService.listUsers()
    return redirect(url_for('user.index'))

@user.route("/auth",methods=["POST"])
def auth():
    login = request.form.get("login")
    password = request.form.get("password")
    user:User|None =  userService.auth(login, password) # type: ignore
    if user == None:
        return render_template("authentication.html",error="Login or password incorrect")
    session["email"]=login
    listUsers = userService.listUsers()
    return render_template('Home.html',users=listUsers)

@user.route("/accounts")
def accounts():
    return render_template("accounts.html")

@user.route("/logout")
def logout():
    session.clear()
    return render_template("authentication.html")

@user.route("/Home")
def Home():
    return render_template("Home.html")