from flask import Blueprint, render_template

index_routes = Blueprint('index_routes', __name__, template_folder='templates')

@index_routes.route("/", endpoint="index", methods=["GET"])
def index():
    return render_template("index.html")
