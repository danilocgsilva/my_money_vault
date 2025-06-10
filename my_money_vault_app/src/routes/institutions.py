from flask import Blueprint, render_template

routes = Blueprint('routes', __name__, template_folder='templates')

@routes.route("/institutions/create", endpoint="institution_create", methods=["GET"])
def create_form():
    return render_template("models/institutions/create.html")