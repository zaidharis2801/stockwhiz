from .models import User
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db


payment = Blueprint('payment', __name__)


@payment.route('/topup', methods=['GET', 'POST'])
def topup():
    if request.method == 'POST':
        # cardname = request.form.get('cardname')
        # cardnumber = request.form.get('cardnumber')
        # cvc = request.form.get('cvc')
        cardamount = request.form.get('paymentamount')

        # new_note = User(CurrentBalance = cardamount, id=current_user.id)

        admin = User.query.filter_by(id=current_user.id).first()

        money = admin.CurrentBalance + float(cardamount)
        admin.CurrentBalance = money
        db.session.commit()



        flash('Balance Added', category='success')




    return render_template("topup.html", user=current_user)


@payment.route('/withdraw', methods=['GET', 'POST'])

def withdraw():
    if request.method == 'POST':
        cardamount = float(request.form.get('paymentamount'))

        admin = User.query.filter_by(id=current_user.id).first()

        if cardamount <=admin.CurrentBalance:

            money = admin.CurrentBalance - float(cardamount)
            admin.CurrentBalance = money
            db.session.commit()
            flash('Balance withdrawn', category='success')
        else:
            flash('Not Enough Balance', category='error')

    return render_template("withdraw.html", user=current_user)