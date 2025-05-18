from flask import Flask
from flask import Blueprint
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/bulma")
def bulma():
    return render_template("bulma.html")
