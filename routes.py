from app import app
from flask import render_template, request, redirect, url_for

import users
import tasks

@app.route("/")
def index():    
  return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    result = users.register(username, password)
    if result["status"]:
      return redirect("/")
    else:
      return render_template("register.html")
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
    print("here")
    return redirect("/")
  else:
    return render_template("login.html")

@app.route("/logout")
def logout():
  users.logout()
  return redirect("/")

@app.route("/tasks")
def task_view():
  all_tasks = tasks.get_tasks()
  return render_template("tasks.html", tasks=all_tasks)

@app.route("/tasks/<task_id>", methods=["GET", "POST"])
def task_info(task_id):
  task_data = tasks.get_task(task_id)
  if request.method == "GET":
    accept, reject = tasks.get_tests(task_id)
    return render_template("task.html", task=task_data, accept=accept[:2], reject=reject[:2])
  else:
    user_id = users.user_id()
    if user_id == -1:
      return redirect("/login")
    answer = request.form["answer"]
    tasks.submit(answer, task_id, user_id)
    return redirect(url_for("results", task_id=task_id))

@app.route("/tasks/<task_id>/results")
def results(task_id):
  task_data = tasks.get_task(task_id)
  user_id = users.user_id()
  results = tasks.get_results(user_id, task_id)

  return render_template("results.html", task=task_data, results=results)

@app.route("/admin")
def admin():
  return "secret"