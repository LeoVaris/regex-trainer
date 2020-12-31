from db import db
import re

def get_tasks(user_id):
  subquery = "(SELECT MIN(LENGTH(S.submission)) FROM submissions S "
  subquery += "WHERE S.task_id = T.id AND S.result = 'OK' AND S.user_id=:id)"
  query = "SELECT T.id, T.name, COALESCE(" + subquery + ", -1) FROM tasks T"
  result = db.session.execute(query, {"id": user_id})
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

def get_tests_id(task_id):
  query = "SELECT id, data, accept FROM tests WHERE task_id=:task_id"
  result = db.session.execute(query, {"task_id": task_id})
  accept = []
  reject = []
  for id, data, acc in result:
    if acc:
      accept.append((id, data))
    else:
      reject.append((id, data))
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

  result_id = create_submission(user_id, task_id, answer, return_value)
  return result_id

def create_submission(user_id, task_id, answer, result):
  query = "INSERT INTO submissions (user_id, task_id, submission, result, sent_at) "
  query += "VALUES (:user_id, :task_id, :submission, :result, NOW()) RETURNING id"

  variables = {}
  variables["user_id"] = user_id
  variables["task_id"] = task_id
  variables["submission"] = answer
  variables["result"] = result
  result = db.session.execute(query, variables)
  db.session.commit()
  return result.fetchone()[0]

def get_all_submissions():
  query = "SELECT S.id, S.submission, S.result, S.sent_at, T.name, U.username FROM submissions S, tasks T, users U "
  query += "WHERE S.task_id = T.id AND S.user_id = U.id"
  result = db.session.execute(query)
  ret = []
  for i, res in enumerate(result):
    ret.append((i + 1, res))
  return reversed(ret)

def get_submissions(user_id):
  query = "SELECT id, submission, result, sent_at FROM submissions WHERE user_id=:user_id"
  result = db.session.execute(query, {"user_id": user_id})
  ret = []
  for i, res in enumerate(result):
    ret.append((i + 1, res))
  return reversed(ret)

def get_result(result_id):
  query = "SELECT submission, result, sent_at, task_id, user_id FROM submissions WHERE id=:result_id"
  result = db.session.execute(query, {"result_id": result_id})
  return result.fetchone()

def get_results(user_id, task_id):
  query = "SELECT id, submission, result, sent_at FROM submissions WHERE user_id=:user_id AND task_id=:task_id"
  result = db.session.execute(query, {"user_id": user_id, "task_id": task_id})
  ret = []
  for i, res in enumerate(result):
    ret.append((i + 1, res))
  return reversed(ret)

def create_task(task_name, description, accept, reject):
  accept = accept.split("\n")
  reject = reject.split("\n")

  query = "INSERT INTO tasks (name, task_info) VALUES (:task_name, :description) RETURNING id"
  result = db.session.execute(query, {"task_name": task_name, "description": description})
  db.session.commit()
  task_id = result.fetchone()[0]
  query = "INSERT INTO tests (task_id, data, accept) VALUES (:task_id, :test, TRUE)"
  for acc in accept:
    acc = acc.strip()
    if acc == "":
      continue
    db.session.execute(query, {"task_id": task_id, "test": acc})
    db.session.commit()
  query = "INSERT INTO tests (task_id, data, accept) VALUES (:task_id, :test, FALSE)"
  for rej in reject:
    rej = rej.strip()
    if rej == "":
      continue
    db.session.execute(query, {"task_id": task_id, "test": rej})
    db.session.commit()

def edit_name(task_id, name):
  query = "UPDATE tasks SET name=:name WHERE id=:id"
  db.session.execute(query, {"id": task_id, "name": name})
  db.session.commit()

def delete_test(test_id):
  query = "DELETE FROM tests WHERE id=:id"
  db.session.execute(query, {"id": test_id})
  db.session.commit()

def edit_description(task_id, description):
  query = "UPDATE tasks SET task_info=:task_info WHERE id=:id"
  db.session.execute(query, {"id": task_id, "task_info": description})
  db.session.commit()

def add_test(task_id, test, action):
  accept = action == "1"
  print(accept)
  query = "INSERT INTO tests (task_id, data, accept) VALUES (:task_id, :test, :accept)"
  db.session.execute(query, {"task_id": task_id, "test": test, "accept": accept})
  db.session.commit()

def delete_task(task_id):
  query = "DELETE FROM tasks WHERE id=:task_id"
  db.session.execute(query, {"task_id": task_id})
  db.session.commit()

def get_statistics():
  query = "SELECT U.username, (SELECT COUNT(DISTINCT S.task_id) as P FROM submissions S "
  query += "WHERE S.user_id = U.id AND S.result = 'OK') FROM users U WHERE U.status = 1 ORDER BY P DESC"
  results = db.session.execute(query)
  return results.fetchall()