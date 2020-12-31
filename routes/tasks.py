from app import app
from flask import render_template, request, redirect, url_for

import users
import tasks

@app.route("/tasks")
def task_view():
  all_tasks = tasks.get_tasks(users.user_id())
  return render_template("tasks.html", tasks=all_tasks)

@app.route("/tasks/<task_id>", methods=["GET", "POST"])
def task_info(task_id):
  task_data = tasks.get_task(task_id)
  if task_data == None:
    return redirect("/tasks")
  if request.method == "GET":
    if task_data[3] == 1:
      accept, reject = tasks.get_tests(task_id)
      results = tasks.get_results(users.user_id(), task_id)
      return render_template("task.html", task=task_data, accept=accept[:2], reject=reject[:2], results=results)
    else:
      return render_template("instruction.html", task=task_data)
  else:
    user_id = users.user_id()
    if user_id == -1:
      return redirect("/login")
    answer = request.form["answer"]
    result_id = tasks.submit(answer, task_id, user_id)
    return redirect(url_for("result", task_id=task_id, result_id=result_id))

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
    if result[5] <= 2:
      return render_template("wrong.html", task=task_data, test=result)
    else:
      return render_template("error.html", task=task_data, message=result[1])

@app.route("/tasks/results/<result_id>")
def admin_result(result_id):
  result = tasks.get_result(result_id)
  if result == None or users.get_status() <= 1:
    return redirect("/tasks")
  task_id = result[3]
  task = tasks.get_task(task_id)
  return render_template("admin_result.html", result=result, task=task)

@app.route("/tasks/<task_id>/edit")
def modify_task(task_id):
  if users.get_status() <= 1:
    return redirect("/tasks")
  task_data = tasks.get_task(task_id)
  if task_data == None:
    return redirect("/tasks")
  accept, reject = tasks.get_tests(task_id)
  accept = '\n'.join(accept)
  reject = '\n'.join(reject)
  return render_template("edit_form.html", task=task_data, accept=accept, reject=reject)

@app.route("/tasks/<task_id>/edit_name", methods=["POST"])
def edit_name(task_id):
  if users.get_status() <= 1:
    return redirect("/tasks")
  name = request.form["name"]
  tasks.edit_name(task_id, name)
  return redirect(url_for('modify_task', task_id=task_id))

@app.route("/tasks/<task_id>/edit_description", methods=["POST"])
def edit_description(task_id):
  if users.get_status() <= 1:
    return redirect("/tasks")
  description = request.form["description"]
  tasks.edit_description(task_id, description)
  return redirect(url_for('modify_task', task_id=task_id))

@app.route("/tasks/<task_id>/edit_tests", methods=["POST"])
def edit_tests(task_id):  
  if users.get_status() <= 1:
    return redirect("/tasks")
  accept = request.form["accept"]
  reject = request.form["reject"]
  tasks.edit_tests(task_id, accept, reject)
  return redirect(url_for('modify_task', task_id=task_id))

@app.route("/tasks/delete/<task_id>")
def delete_task(task_id):
  if users.get_status() <= 1:
    return redirect("/tasks")
  tasks.delete_task(task_id)
  return redirect("/tasks")