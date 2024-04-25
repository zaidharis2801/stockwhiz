from flask import Blueprint, render_template, request
import yfinance as yf
import json
import plotly
import plotly.express as px

chart = Blueprint('chart', __name__)

@chart.route('/<variable>.png')
# def plot_png(variable):
#     fig = create_figure(variable)
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return (Response(output.getvalue(), mimetype='image/png'))
#
# # @chart.route('/')
# def create_figure(x):
#
#
#     #fig = Figure()
#
#
#     # axis = fig.add_subplot(1, 1, 1)
#     # xs = range(100)
#     # ys = [random.randint(1, 50) for x in xs]
#     # axis.plot(xs, ys)
#     # fig = create_figure()
#     # output = io.BytesIO()
#     # FigureCanvas(fig).print_png(output)
#     #return Response(output.getvalue(), mimetype='image/png')
#
#     a = yf.download(tickers=x, period="1mo", interval="1d")
#     # print(a)
#     print(a.loc[:, "High"].size)
#
#     zaid=a.loc[:, "High"].plot()
#     # buf = BytesIO()
#     # zaid.savefig(buf, format="png")
#     # # Embed the result in the html output.
#     # data = base64.b64encode(buf.getbuffer()).decode("ascii")
#     #
#     # return render_template("joke.html",pictur=data)
#
#     return zaid.get_figure()


def plot_png(endpoint):
    if endpoint == "getStock":
        return create_figure(request.args.get('data'), request.args.get('period'), request.args.get('interval'))
    elif endpoint == "getInfo":
        stock = request.args.get('data')
        st = yf.Ticker(stock)
        return json.dumps(st.info)
    else:
        return "Bad endpoint", 400


# Return the JSON data for the Plotly graph
def create_figure(stock):
    st = yf.Ticker(stock)

    # Create a line graph
    df = st.history(period=('1d'), interval='1m')
    df = df.reset_index()
    df.columns = ['Date-Time'] + list(df.columns[1:])
    max = (df['Open'].max())
    min = (df['Open'].min())
    range = max - min
    margin = range * 0.05
    max = max + margin
    min = min - margin
    fig = px.area(df, x='Date-Time', y="Open",
                  hover_data=("Open", "Close", "Volume"),
                  range_y=(min, max), template="seaborn")

    # Create a JSON representation of the graph
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
