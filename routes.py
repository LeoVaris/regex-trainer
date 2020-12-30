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
  if task_data == None:
    return redirect("/tasks")
  user_id = users.user_id()
  results = tasks.get_results(user_id, task_id)

  return render_template("results.html", task=task_data, results=results)

@app.route("/tasks/<task_id>/results/<result_id>")
def result(task_id, result_id):
  result = tasks.get_result(result_id)
  task_data = tasks.get_task(task_id)
  if result == None:
    return redirect("/tasks")
  if result[1] == "OK":
    return render_template("correct.html", task=task_data, ans_len=len(result[0]))
  else:
    return render_template("wrong.html", task=task_data, test=result[1])

@app.route("/tasks/results/<result_id>")
def admin_result(result_id):
  result = tasks.get_result(result_id)
  if result == None or users.get_status() <= 1:
    return redirect("/tasks")
  task_id = result[3]
  task = tasks.get_task(task_id)
  return render_template("admin_result.html", result=result, task=task)

@app.route("/admin")
def admin():
  if users.get_status() <= 1:
    return redirect("/")
  result_list = tasks.get_all_submissions()
  return render_template("admin.html", results=result_list)

@app.route("/admin/users/<user_id>", methods=["GET", "POST"])
def manage_user(user_id):
  if users.get_status() <= 1:
    return redirect("/")
  if request.method == "GET":
    user = users.get_data(user_id)
    submissions = tasks.get_submissions(user_id)
    return render_template("user.html", user=user, results=submissions)
  else:
    status = int(request.form["status"])
    users.update_status(user_id, status)
    return redirect(url_for("manage_user", user_id=user_id))

@app.route("/admin/users")
def user_list():
  if users.get_status() <= 1:
    return redirect("/")
  user_list = users.get_users()
  return render_template("users.html", user_list=user_list)

@app.route("/admin/create_task", methods=["GET", "POST"])
def create_task():
  if users.get_status() <= 1:
    return redirect("/")
  if request.method == "GET":
    return render_template("task_form.html")
  else:
    task_name = request.form["name"]
    description = request.form["description"]
    accept = request.form["accept"]
    reject = request.form["reject"]

    tasks.create_task(task_name, description, accept, reject)
    return redirect("/tasks")
