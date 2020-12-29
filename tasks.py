from db import db
import re

def get_tasks():
  query = "SELECT * FROM tasks"
  result = db.session.execute(query)
  return result.fetchall()

def get_task(task_id):
  query = "SELECT * FROM tasks WHERE id=:id"
  result = db.session.execute(query, {"id": task_id})
  return result.fetchone()

def get_tests(task_id):
  query = "SELECT data, accept FROM tests WHERE task_id=:task_id"
  result = db.session.execute(query, {"task_id": task_id})
  accept = []
  reject = []
  for data, acc in result:
    if acc:
      accept.append(data)
    else:
      reject.append(data)
  return (accept, reject)

def submit(answer, task_id, user_id):
  query = "SELECT data, accept FROM tests WHERE task_id=:task_id"
  result = db.session.execute(query, {"task_id": task_id})

  prog = re.compile(answer)

  return_value = "OK"

  for data, accept in result:
    res = prog.fullmatch(data)
    if (accept and res == None) or (not accept and res != None):
      return_value = data
      break

  create_submission(user_id, task_id, answer, return_value)
  return return_value

def create_submission(user_id, task_id, answer, result):
  query = "INSERT INTO submissions (user_id, task_id, submission, result) "
  query += "VALUES (:user_id, :task_id, :submission, :result)"

  variables = {}
  variables["user_id"] = user_id
  variables["task_id"] = task_id
  variables["submission"] = answer
  variables["result"] = result
  db.session.execute(query, variables)
  db.session.commit()

def get_results(user_id, task_id):
  query = "SELECT submission, result FROM submissions WHERE user_id=:user_id AND task_id=:task_id"
  result = db.session.execute(query, {"user_id": user_id, "task_id": task_id})
  return result.fetchall()