from app import app
from flask import render_template, request, redirect, url_for

import users
import tasks

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
    if users.get_status() == 3:
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

@app.route("/admin/create_note", methods=["GET", "POST"])
def create_instruction():
  if users.get_status() <= 1:
    return redirect("/")
  if request.method == "GET":
    return render_template("instruction_form.html")
  else:
    task_name = request.form["name"]
    description = request.form["description"]

    tasks.create_note(task_name, description)
    return redirect("/tasks")

@app.route("/admin/reorder", methods=["GET", "POST"])
def reorder():
  if users.get_status() <= 1:
    return redirect("/")
  if request.method == "GET":
    all_tasks = tasks.get_order_data()
    return render_template("reorder_form.html", tasks=all_tasks)
  else:
    for task_id, position in request.form.items():
      tasks.update_order(int(task_id), int(position))
    return redirect("/admin/reorder")