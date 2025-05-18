from flask import Flask, redirect, url_for, request, abort
from flask import Blueprint
from flask import render_template
from src.Repositories.InstitutionRepository import InstitutionRepository
from src.MySQLConnectorWrapper import MySQLConnectorWrapper
from src.Models.Institution import Institution
from flask_wtf.csrf import CSRFProtect, validate_csrf

app = Flask(__name__)
app.secret_key = 'your-very-secret-key'
csrf = CSRFProtect(app)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/bulma", endpoint="bulma")
def bulma():
    return render_template("bulma.html")

@app.route("/institutions/create")
def create_form():
    return render_template("models/institutions/create.html")

@app.route("/institutions", endpoint="institution_store", methods=["POST"])
def create():
    try:
        validate_csrf(request.form.get('csrf_token'))
    except:
        abort(403, description="CSRF token validation failed")
    
    repo = InstitutionRepository(MySQLConnectorWrapper().connector)
    institution = Institution()
    institution.name = request.form["name"]
    institution.description = request.form["description"]
    repo.create(institution)
    return redirect(url_for("bulma"))
