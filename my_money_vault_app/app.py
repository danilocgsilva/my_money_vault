from flask import Flask, redirect, url_for, request, abort, render_template
from src.Repositories.StateRepository import StateRepository
from src.MySQLConnectorWrapper import MySQLConnectorWrapper
from flask_wtf.csrf import CSRFProtect, validate_csrf
from src.routes.index_routes import index_routes
from src.routes.institutions_routes import institutions_routes

app = Flask(__name__)
app.secret_key = 'your-very-secret-key'

@app.context_processor
def adding_jinja_methods():
    def couning_accounts_string(counting: int) -> str:
        if counting == 0:
            return "No accounts"
        elif counting == 1:
            return "1 account"
        elif counting > 1:
            return f"{counting} accounts"
        else:
            return "Invalid count"
    return dict(get_counting_accounts=couning_accounts_string)

csrf = CSRFProtect(app)

app.register_blueprint(index_routes)
app.register_blueprint(institutions_routes)

@app.route(
    "/account/<int:account_id>/states",
    endpoint="state_history",
    methods=["GET"]
)
def account_state_history(account_id):
    state_repository = StateRepository(MySQLConnectorWrapper().connector)
    account_states = state_repository.find_states_by_account(account_id)
    
    return render_template("models/accounts/state_history.html", account_states=account_states)

