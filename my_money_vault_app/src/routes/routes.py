from flask import Blueprint, render_template

routes = Blueprint('routes', __name__, template_folder='templates')

@routes.route("/", endpoint="index", methods=["GET"])
def index():
    return render_template("index.html")
