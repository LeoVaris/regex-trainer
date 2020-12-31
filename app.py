from flask import Flask
from os import getenv


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

# used to reduce dev errors likely caused by on-reset database reload
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from db import db, init_db

# routing
import routes.admin
import routes.index
import routes.tasks
import routes.users

import users

# if dev environment, always reset database
if getenv("FLASK_ENV") == "development":
  init_db()

# initializes root user with .env password
users.init_admin()

# this allows templates to easily find status and username
app.jinja_env.globals.update(get_username=users.get_username)
app.jinja_env.globals.update(get_status=users.get_status)