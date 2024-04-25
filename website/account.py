from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user




account = Blueprint('account', __name__)


@account.route('/accounts', methods=['GET', 'POST'])
def personal():





    return render_template("account.html", user=current_user)