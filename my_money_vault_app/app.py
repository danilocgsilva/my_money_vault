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

@app.route("/", endpoint="index", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/bulma", endpoint="bulma")
def bulma():
    return render_template("bulma.html")

@app.route("/institutions/create", endpoint="institution_create", methods=["GET"])
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

@app.route("/institutions", endpoint="institution_list", methods=["GET"])
def list_institutions():
    repo = InstitutionRepository(MySQLConnectorWrapper().connector)
    institutions_list = repo.find_all()
    return render_template("models/institutions/index.html", institutions=institutions_list)

@app.route("/institutions/<int:id>", endpoint="institution_show", methods=["GET"])
def show_institution(id):
    institutions_repository = InstitutionRepository(MySQLConnectorWrapper().connector)
    institution = institutions_repository.find_by_id(id)
    institutions_repository.fill_accounts(institution)
    if not institution:
        abort(404, description="Institution not found")
    return render_template("models/institutions/show.html", institution=institution)

@app.route("/institutions/<int:id>/delete", endpoint="institution_delete_confirmation", methods=["GET"])
def delete_institution_form(id):
    mysql_connector = MySQLConnectorWrapper().connector
    repo = InstitutionRepository(mysql_connector)
    institution = repo.find_by_id(id)
    if not institution:
        abort(404, description="Institution not found")
    return render_template("models/institutions/delete.html", institution=institution)
