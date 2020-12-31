from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv

def init_admin():
  password = getenv("ROOT_PASSWORD")
  password_hash = generate_password_hash(password)
  username = "root"
  find_old = "SELECT * FROM users WHERE username='root'"
  res = db.session.execute(find_old)
  if res.fetchone() != None:
    print("root user already added")
    return
  query = "INSERT INTO users (username, password, status) VALUES (:username, :password, 3)"
  db.session.execute(query, {"username": username, "password": password_hash})
  db.session.commit()
  print("Added root user")

def login(username, password):
  query = "SELECT password, id FROM users WHERE username=:username"
  result = db.session.execute(query, {"username": username})
  user = result.fetchone()
  if user == None:
    return {"status": False, "message": "Väärä käyttäjänimi"}
  
  if check_password_hash(user[0], password):
    session["user_id"] = user[1]
    return {"status": True, "message": "Kirjautuminen onnistui"}
  else:
    return {"status": False, "message": "Väärä salasana"}
  
def logout():
  del session["user_id"]

def register(username, password):
  # tarkista onko jo sama käyttäjä
  query = "SELECT * FROM users WHERE username=:username"
  result = db.session.execute(query, {"username": username})
  if result.fetchone() != None:
    return {"status": False, "message": "Käyttäjänimi on jo varattu"}

  password_hash = generate_password_hash(password)
  try:
    query = "INSERT INTO users (username, password, status) VALUES (:username, :password, 1)"
    db.session.execute(query, {"username": username, "password": password_hash})
    db.session.commit()
  except:
    return {"status": False, "message": "Uuden käyttäjän luonti epäonnistui"}
  login(username, password)
  return {"status": True, "message": "Uusi käyttäjä luotu"}

def user_id():
  return session.get("user_id", -1)

def get_data(user_id):
  query = "SELECT * FROM users WHERE id=:id"
  result = db.session.execute(query, {"id": user_id})
  return result.fetchone()

def get_users():
  query = "SELECT * FROM users ORDER BY status DESC"
  result = db.session.execute(query)
  return result.fetchall()

def get_username():
  res = get_data(user_id())
  if res == None:
    return None
  return res[1]

def get_status():
  res = get_data(user_id())
  if res == None:
    return 0
  return res[3]

def update_status(user_id, status):
  query = "UPDATE users SET status=:status WHERE id=:id"
  db.session.execute(query, {"id": user_id, "status": status})
  db.session.commit()

def is_admin():
  return get_status() >= 2

def logout():
  del session["user_id"]