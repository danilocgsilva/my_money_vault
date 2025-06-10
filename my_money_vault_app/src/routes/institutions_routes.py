from flask import Blueprint, render_template, request, abort, redirect, url_for
from flask_wtf.csrf import validate_csrf
from src.Repositories.InstitutionRepository import InstitutionRepository
from src.MySQLConnectorWrapper import MySQLConnectorWrapper
from src.Models.Institution import Institution

institutions_routes = Blueprint('institutions_routes', __name__, template_folder='templates')

@institutions_routes.route("/institutions/create", endpoint="institution_create", methods=["GET"])
def create_form():
    return render_template("models/institutions/create.html")

@institutions_routes.route("/institutions", endpoint="institution_store", methods=["POST"])
def create():
    try:
        validate_csrf(request.form.get('csrf_token'))
    except:
        abort(403, description="CSRF token validation failed")
    
    institutions_repository = InstitutionRepository(MySQLConnectorWrapper().connector)
    institution = Institution()
    institution.name = request.form["name"]
    institution.description = request.form["description"]
    institutions_repository.create(institution)
    return redirect(url_for("bulma"))

@institutions_routes.route("/institutions", endpoint="institution_list", methods=["GET"])
def list_institutions():
    institutions_repository = InstitutionRepository(MySQLConnectorWrapper().connector)
    institutions_list = institutions_repository.find_all_with_accounts_counts()
    return render_template("models/institutions/index.html", institutions=institutions_list)