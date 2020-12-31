from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

# init database
# below code from stackoverflow
# resets db and inserts dev data
def init_db():
  sql_file = open("schema.sql","r")

  sql_command = ""
  for line in sql_file:
    if not line.startswith("--") and line.strip("\n"):
      sql_command += line.strip("\n")
      if sql_command.endswith(";"):
        try:
          db.session.execute(str(sql_command))
          db.session.commit()
        except Exception as e:
          print("Error", e)
        finally:
          sql_command = ""
  print("Initialized database")
  sql_file = open("example_data.sql","r")

  sql_command = ""
  for line in sql_file:
    if not line.startswith("--") and line.strip("\n"):
      sql_command += line.strip("\n")
      if sql_command.endswith(";"):
        try:
          db.session.execute(str(sql_command))
          db.session.commit()
        except Exception as e:
          print("Error", e)
        finally:
          sql_command = ""
  print("Added example data")