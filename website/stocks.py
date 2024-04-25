from flask import Blueprint, render_template, request, flash, jsonify
from .models import Search
from flask_login import login_required, current_user
from .stockprices import stock, stockname, stockbeautiful, closeprice
from . import db
import json
import traceback


stocks = Blueprint('stocks', __name__)
search = ""


@stocks.route('/stocks', methods=['GET', 'POST'])
@login_required
def stockpage():
    # plt.rcParams["figure.figsize"] = [7.50, 3.50]
    # plt.rcParams["figure.autolayout"] = True
    #
    # fig = Figure()
    # axis = fig.add_subplot(1, 1, 1)
    # xs = np.random.rand(100)
    # ys = np.random.rand(100)
    # axis.plot(xs, ys)
    # output = io.BytesIO()
    # FigureCanvas(fig).print_png(output)
    # xy= Response(output.getvalue(), mimetype='image/png')

    # plot_png

    # while(True):
    #     x = search()
    #     if (x!= None):
    #         stock(x)
    # time.sleep(5)
    #
    # return render_template("home.html" , user=current_user)

    if request.method == 'POST' and "search" in request.form:

        # if request.form['button'] == 'search':
        print("snahksaasaasasaaaaaaaaaaaaaaaaaaaaa")
        search = request.form.get('search').capitalize()
        if len(search) < 1:
            flash('Search is too short!', category='error')
        else:
        
            
            try:
                new_name = stockbeautiful(search)
                last_price = closeprice(search)
                new_note = Search(data=search, name=new_name, lastprice=last_price, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Searched', category='success')
            except Exception as e:
                flash('Stock not found22'+ str(e), category='error')
                print(f'An error occurred: {e}')
                traceback.print_exc()

        # else:
        #     print("atta ")
        #     return redirect(url_for('transactions.buy'))

    x = []
    y = []
    z = []
    for i in current_user.search:
        x.append(stock(i.data))

    for i in current_user.search:
        y.append(i.name)

    for i in current_user.search:
        z.append(i.lastprice)

    return render_template("stocks.html", user=current_user, price=x, sname=y, laspri=z, zip=zip)


# @views.route("/search", methods=['GET', 'POST'])
#
# def search():
#     if request.method == 'POST':
#         search = request.form.get('search')
#
#     return search


@stocks.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Search.query.get(noteId)
    db.session.delete(note)
    db.session.commit()

    return jsonify({})
