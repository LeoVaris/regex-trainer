from app import app
from flask import render_template, request, redirect, url_for

import users
import tasks

@app.route("/")
def index():    
  return render_template("index.html")

@app.route("/stats")
def leaderboard():
  results = tasks.get_statistics()
  return render_template("stats.html", results=results)