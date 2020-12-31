from app import app
from flask import render_template, request, redirect, url_for

import users
import tasks

@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    result = users.register(username, password)
    if result["status"]:
      return redirect("/")
    else:
      return render_template("register.html", message=result["message"])
  else:
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "GET":
    return render_template("login.html")

  username = request.form["username"]
  password = request.form["password"]
  result = users.login(username, password)
  if result["status"]:
    return redirect("/")
  else:
    return render_template("login.html", message=result["message"])

@app.route("/logout")
def logout():
  users.logout()
  return redirect("/")