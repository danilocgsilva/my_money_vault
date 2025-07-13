from flask import Blueprint, render_template, request, abort, redirect, url_for
from flask_wtf.csrf import validate_csrf
from src.Repositories.InstitutionRepository import InstitutionRepository
from src.MySQLConnectorWrapper import MySQLConnectorWrapper
from src.Models.Institution import Institution
from src.Repositories.AccountRepository import AccountRepository
from src.Repositories.InstitutionRepository import InstitutionRepository
from src.Repositories.StateRepository import StateRepository
from src.Models.State import State

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

@institutions_routes.route(
    "/institutions/<int:id>", 
    endpoint="institution_show", 
    methods=["GET"]
)
def show_institution(id):
    institutions_repository = InstitutionRepository(MySQLConnectorWrapper().connector)
    institution = institutions_repository.find_by_id(id)
    institutions_repository.fill_accounts(institution)
    if not institution:
        abort(404, description="Institution not found")
    return render_template("models/institutions/show.html", institution=institution)

@institutions_routes.route(
    "/institutions/<int:id>/delete", 
    endpoint="institution_delete_confirmation", 
    methods=["GET"]
)
def delete_institution_form(id):
    mysql_connector = MySQLConnectorWrapper().connector
    institutions_repository = InstitutionRepository(mysql_connector)
    institution = institutions_repository.find_by_id(id)
    if not institution:
        abort(404, description="Institution not found")
    return render_template("models/institutions/delete.html", institution=institution)

@institutions_routes.route(
    "/institutions/<int:account_id>/state",
    endpoint="create_state_form",
    methods=["GET"]
)
def create_state_form(account_id):
    account_repository = AccountRepository(MySQLConnectorWrapper().connector)
    account_repository.prepareWithInstitution()
    account = account_repository.find_by_id(account_id)
    return render_template("models/accounts/add_state.html", account=account)

@institutions_routes.route(
    "/institutions/<int:id>/delete", 
    endpoint="institution_delete", 
    methods=["POST"]
)
def delete_institution(id):
    try:
        validate_csrf(request.form.get('csrf_token'))
    except:
        abort(403, description="CSRF token validation failed")
    
    mysql_connector = MySQLConnectorWrapper().connector
    institutions_repository = InstitutionRepository(mysql_connector)
    
    institutions_repository.delete(id)
    return redirect(url_for("institutions_routes.institution_list"))


@institutions_routes.route(
    "/instituion/<int:account_id>/state",
    endpoint="state_store",
    methods=["POST"]
)
def store_state():
    try:
        validate_csrf(request.form.get('csrf_token'))
    except:
        abort(403, description="CSRF token validation failed")
    state_repository = StateRepository(MySQLConnectorWrapper().connector)
    state = State(
        account_id=request.form["account_id"],
        balance=request.form["balance"]
    )
    state_repository.create(state)
    return redirect(url_for("create_state_form"))