from flask import Flask
from os import getenv


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

from db import db, init_db
import routes
import users

init_db()
users.init_admin()

app.jinja_env.globals.update(get_username=users.get_username)
#app.jinja_env.globals.update(is_admin=users.is_admin)
app.jinja_env.globals.update(get_status=users.get_status)