from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .stockprices import stock, stockname, stockbeautiful, closeprice, openprice, totalvolume, highprice, lowprice
import plotly
import json
from .fundamentals import get_dividends as funds, smallerfig, biggerfig

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    price1 = 0
    price2 = 0
    price3 = 0
    price4 = 0

    lprice1 = 0
    lprice2 = 0
    lprice3 = 0
    lprice4 = 0

    plot1 = 0
    plot2 = 0
    plot3 = 0
    plot4 = 0

    plotly_plot1 = 0
    plotly_plot2 = 0
    plotly_plot3 = 0
    plotly_plot4 = 0


    try:




        plotly_plot5 = "search for a stock to Show Graph"
        price1 = stock("btc-usd")
        price2 = stock("eth-usd")
        price3 = stock("shel.l")
        price4 = stock("aapl")
    except:
        flash('Internet Error: Could not load current price', category='error')

    try:
        lprice1 = closeprice("btc-usd")
        lprice2 = closeprice("eth-usd")
        lprice3 = closeprice("shel.l")
        lprice4 = closeprice("aapl")
    except:
        flash('Internet Error: Could not load last price', category='error')

    try:
        plot1 = smallerfig('btc-usd')
        plot2 = smallerfig("eth-usd")
        plot3 = smallerfig("shel.l")
        plot4 = smallerfig("aapl")

        plotly_plot1 = json.dumps(plot1, cls=plotly.utils.PlotlyJSONEncoder)
        plotly_plot2 = json.dumps(plot2, cls=plotly.utils.PlotlyJSONEncoder)
        plotly_plot3 = json.dumps(plot3, cls=plotly.utils.PlotlyJSONEncoder)
        plotly_plot4 = json.dumps(plot4, cls=plotly.utils.PlotlyJSONEncoder)
    except:
        flash('Internet Error: Could not load graph', category='error')


    if request.method == 'POST':
        search = request.form.get('search').capitalize()


        if len(search) < 1:
            flash('Search is too short!', category='error')
        else:

            try:
                if (search != ""):
                    plot5 = biggerfig(search)
                    plotly_plot5 = json.dumps(plot5, cls=plotly.utils.PlotlyJSONEncoder)
            except:
                flash('Stock not found', category='error')






    x = []
    y = []
    z = []
    w = []
    for i in current_user.transaction:
        w.append(i.Qty)

    for i in current_user.transaction:
        xy = round(float(((stock(i.Symbol) -i.StockPrice) / i.StockPrice) * 100), 2)
        x.append(xy)

    for i in current_user.transaction:
        y.append(i.name)

    for i in current_user.transaction:
        z.append(i.StockPrice)

    return render_template("home.html", user=current_user, p1=price1, p2=price2, p3=price3, p4=price4, l1=lprice1, l2=lprice2, l3=lprice3, l4=lprice4, g1=plotly_plot1,
                           g2=plotly_plot2, g3=plotly_plot3, g4=plotly_plot4, g5=plotly_plot5, perc=x, sname=y,
                           buyprice=z, quant=w,
                           zip=zip)

# # plt.rcParams["figure.figsize"] = [7.50, 3.50]
#     # plt.rcParams["figure.autolayout"] = True
#     #
#     # fig = Figure()
#     # axis = fig.add_subplot(1, 1, 1)
#     # xs = np.random.rand(100)
#     # ys = np.random.rand(100)
#     # axis.plot(xs, ys)
#     # output = io.BytesIO()
#     # FigureCanvas(fig).print_png(output)
#     # xy= Response(output.getvalue(), mimetype='image/png')
#
#     # plot_png
#
#     # while(True):
#     #     x = search()
#     #     if (x!= None):
#     #         stock(x)
#     # time.sleep(5)
#     #
#     # return render_template("home.html" , user=current_user)
#
#     if request.method == 'POST':
#         search = request.form.get('search').capitalize()
#
#         if len(search) < 1:
#             flash('Search is too short!', category='error')
#         else:
#             new_name = stockbeautiful(search)
#             last_price = closeprice(search)
#
#             new_note = Search(data=search, name=new_name,lastprice = last_price,  user_id=current_user.id )
#             db.session.add(new_note)
#             db.session.commit()
#
#
#
#
#             flash('Searched', category='success')
#
#     x = []
#     y=[]
#     z = []
#     for i in current_user.search:
#         x.append(stock(i.data))
#
#     for i in current_user.search:
#         y.append(i.name)
#
#     for i in current_user.search:
#         z.append(i.lastprice)

# @views.route("/search", methods=['GET', 'POST'])
#
# def search():
#     if request.method == 'POST':
#         search = request.form.get('search')
#
#     return search
