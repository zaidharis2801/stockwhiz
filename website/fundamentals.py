# import yfinance as yf
# import pandas as pd
from .plotly_layout import create_plotly as ply
# import datetime as dt
# 
# def get_dividends(ticker):
# 
#     # tickerr = yf.Ticker(ticker)
# 
#     ## Dividends
#     dividends = yf.download(tickers=ticker, period="1d", interval="1m")
#     # dividends = dividends.to_frame()
#     # dividends = dividends.reset_index()
#     # dividends["year"] = dividends["Date"].dt.year
#     dividends = dividends.loc[:, "High"]
#     dividends = dividends.to_frame()
#     dividends = dividends.reset_index()
#     return ply(dividends)

import plotly.graph_objs as go
import plotly.express as px
import yfinance as yf

def get_dividends(ticker):
    data = yf.download(tickers=ticker, period = '1d', interval = '1m', rounding= True)
    # fig = go.Figure()
    #
    # fig = ply(data)

    color_palette = ["#add8e6"]

    fig = px.line(data, x=data.index, y=data['High'], title=ticker + ' share price', color_discrete_sequence =color_palette[:1])

    # # fig.add_trace(go.Candlestick(x=data.index,open = data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name = 'market data'))
    # fig.add_trace(
    #     go.line(x=data.index))
    fig.update_layout(title = ticker + ' share price', yaxis_title = 'Stock Price (USD)',  autosize=False,
    width=580,
    height=340, margin=dict(l=0, r=0, t=0, b=0), yaxis={'visible': True, 'showticklabels': True} , xaxis={'visible': True}, paper_bgcolor = "#28373f", plot_bgcolor = "#28373f", font=dict(
            # family="Courier New, monospace",
            size=12,
            color="white"
        ))


    for axis in fig.layout:
        if type(fig.layout[axis]) == go.layout.YAxis:
            fig.layout[axis].title.text = ''
        if type(fig.layout[axis]) == go.layout.XAxis:
            fig.layout[axis].title.text = ''

    fig.update_yaxes(matches=None, showticklabels=True, visible=True)

    return fig

def smallerfig(ticker):
    data = yf.download(tickers=ticker, period = '1d', interval = '1m', rounding= True)
    # fig = go.Figure()
    #
    # fig = ply(data)
    color_palette = ["#ffffe0"]

    fig = px.line(data, x=data.index, y=data['High'], title=ticker + ' share price',  color_discrete_sequence =color_palette[:1])

    # # fig.add_trace(go.Candlestick(x=data.index,open = data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name = 'market data'))
    # fig.add_trace(
    #     go.line(x=data.index))

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)

    # remove facet/subplot labels
    fig.update_layout(annotations=[], overwrite=True)

    # strip down the rest of the plot
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="#1B2028",
        margin=dict(t=0, l=0, b=0, r=0),
        width=120,
        height =110,
    )


    # fig.update_layout(title = ticker + ' share price', yaxis_title = 'Stock Price (USD)',  autosize=False,
    # width=120,
    # height=50, margin=dict(l=0, r=0, t=0, b=0), yaxis={'visible': False, 'showticklabels': True} , xaxis={'visible': False},
    # paper_bgcolor = "#28373f", plot_bgcolor = "#28373f",)


    # for axis in fig.layout:
    #     if type(fig.layout[axis]) == go.layout.YAxis:
    #         fig.layout[axis].title.text = ''
    #     if type(fig.layout[axis]) == go.layout.XAxis:
    #         fig.layout[axis].title.text = ''
    #
    # fig.update_yaxes(matches=None, showticklabels=True, visible=True)

    return fig

def biggerfig(ticker):
    data = yf.download(tickers=ticker, period = '1d', interval = '1m', rounding= True)
    # fig = go.Figure()
    #
    # fig = ply(data)

    color_palette = ["#fadadd"]

    fig = px.line(data, x=data.index, y=data['High'], title=ticker + ' share price',
                  color_discrete_sequence=color_palette[:1])

    # # fig.add_trace(go.Candlestick(x=data.index,open = data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name = 'market data'))
    # fig.add_trace(
    #     go.line(x=data.index))
    fig.update_layout(title=ticker + ' share price', yaxis_title='Stock Price (USD)', autosize=False,
                      width=660,
                      height=330, margin=dict(l=0, r=0, t=50, b=0), yaxis={'visible': True, 'showticklabels': True},
                      xaxis={'visible': True}, paper_bgcolor="#1B2028", plot_bgcolor="#1B2028", font=dict(
            # family="Courier New, monospace",
            size=12,
            color="white"
        ))


    for axis in fig.layout:
        if type(fig.layout[axis]) == go.layout.YAxis:
            fig.layout[axis].title.text = ''
        if type(fig.layout[axis]) == go.layout.XAxis:
            fig.layout[axis].title.text = ''

    fig.update_yaxes(matches=None, showticklabels=True, visible=True)

    return fig
