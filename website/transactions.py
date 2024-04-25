from .models import User, Transactions
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .stockprices import stock, stockname, stockbeautiful, closeprice, openprice, totalvolume, highprice, lowprice
from . import db
import plotly
import json
from .fundamentals import get_dividends as funds, smallerfig, biggerfig

transactions = Blueprint('transactions', __name__)


@transactions.route('/transactions', methods=['GET', 'POST'])
@login_required
def buy():
    new_name = ""
    pricern = 0
    last_price = 0
    open_price = 0
    tot_vol = 0
    high_price = 0
    low_price = 0
    search =""

    if request.method == 'POST' and "search" in request.form:
        search = request.form.get('search').capitalize()

        if len(search) < 1:
            flash('Search is too short!', category='error')
        else:

            try:
                print("started")
                
                new_name = stockbeautiful(search)
                print(f"New Name: {new_name}")

                pricern = stock(search)
                print(f"Current Price: {pricern}")

                last_price = closeprice(search)
                print(f"Last Closing Price: {last_price}")

                open_price = openprice(search)
                print(f"Opening Price: {open_price}")

                high_price = highprice(search)
                print(f"High Price: {high_price}")

                low_price = lowprice(search)
                print(f"Low Price: {low_price}")

                tot_vol = totalvolume(search)
                print(f"Total Volume: {tot_vol}")

            except:
                flash('Stock not found', category='error')


    if request.method == 'POST' and "stockvolumes" in request.form:
        stockprice = float(request.form.get('paymentamount'))
        stockvol = float(request.form.get('stockvolumes'))
        bbprice = float(stockprice) * float(stockvol)
        buysell = request.form.get('options')
        symbol = request.form.get('symbolname')


        admin1 = Transactions.query.filter_by(user_id=current_user.id, Symbol=symbol).first()
        admin = User.query.filter_by(id=current_user.id).first()

        if (buysell == "buy"):
            if bbprice <= admin.CurrentBalance:

                if admin1 is not None:
                    newQty = stockvol + admin1.Qty
                    admin1.Qty = newQty
                    db.session.commit()
                    flash('Stock Updated', category='success')
                else:
                    new_name = stockbeautiful(symbol)
                    new_note = Transactions(Symbol=symbol, Qty=stockvol, StockPrice=stockprice, user_id=current_user.id, name=new_name,)
                    db.session.add(new_note)
                    db.session.commit()

                money = admin.CurrentBalance - (bbprice)
                admin.CurrentBalance = money
                db.session.commit()
                flash('Balance withdrawn', category='success')
            else:
                flash('Not Enough Balance', category='error')
        else:


            if admin1 is not None:

                if stockvol <= admin1.Qty:

                    newQty = admin1.Qty - stockvol
                    admin1.Qty = newQty

                    money = admin.CurrentBalance + bbprice
                    admin.CurrentBalance = money

                    db.session.commit()


                    flash('Stock Sold & Balance Updated', category='success')


                else:
                    flash('Not Enough Stocks', category='error')


            else:
                flash("You Don't Own This Stock", category='error')


    plotly_plot = "search for a stock to Show Graph"
    try:

        if(search!=""):


            plot = funds(search)
            #
            plotly_plot = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)


    except:
        flash("Graph could not be made", category='error')
        search = ''

    return render_template("transactions.html", user=current_user, name=new_name, prn = pricern, oprice = open_price, lprice = last_price, hprice = high_price, lowprice = low_price, tvol = tot_vol, search = search , plotly_plot = plotly_plot)
