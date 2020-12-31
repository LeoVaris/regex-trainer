from flask import Flask
from os import getenv


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from db import db, init_db
import routes
import users

if getenv("FLASK_ENV") == "development":
  init_db()
users.init_admin()

app.jinja_env.globals.update(get_username=users.get_username)
app.jinja_env.globals.update(get_status=users.get_status)