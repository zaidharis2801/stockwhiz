import yfinance as yf
import time
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests



def stock(hello):
    # stockname = input("Input Stock Name ").capitalize()

    # a = yf.download(tickers=stockname, period="1mo", interval="1d")
    # # print(a)
    # print(a.loc[:, "High"].size)
    # a.loc[:, "High"].plot()
    # plt.pause(2)
    # # plt.show(block = False)
    # # time.sleep(5)
    while (True):
        tickers = [hello]
        for ticker in tickers:
            ticker_yahoo = yf.Ticker(ticker)
            data = ticker_yahoo.history()
            last_quote = round(data['Close'].iloc[-1],2)
            return last_quote

        time.sleep(2)




# ticker_yahoo = yf.Ticker('aapl')
# name = ticker_yahoo.info

def stockname(hello):
    ticker_yahoo = yf.Ticker(hello)

    # if ticker_yahoo.info['longName'] is not None:
    #     name = ticker_yahoo.info['longName']
    # else:
    #     name = ticker_yahoo.info['name']
    # # name = ticker_yahoo.info['name']
    name = ticker_yahoo.info['shortName']
    # return str(name)
    return (str(name) +"(" + hello +")" )

# print(stockname("btc-usd"))

# def graph():
#     a = yf.download(tickers=stockname,period="1mo",interval="1d")
#     #print(a)
#     print(a.loc[:,"High"].size)
#     a.loc[:,"High"].plot()
#     plt.show()


def stockbeautiful(name):
    name1 = str(name)
    url = f"https://finance.yahoo.com/quote/{name1}"
    headers = {
        'User-agent': 'Mozilla/5.0',
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')


    company = soup.select('h1.svelte-ufs8hf')[0].text.strip()   
    return company
    # fullname = soup.find('h1', class_='D(ib) Fz(18px)').text
    # return fullname


# print(stockbeautiful())


def closeprice(name):
    ticker_yahoo = yf.Ticker(name)
    # print(round(ticker_yahoo.history()['Close'].iloc[-1],2))
    return round(ticker_yahoo.history(period = '2d')['Close'].iloc[0],2)


def openprice(name):
    ticker_yahoo = yf.Ticker(name)
    # print(round(ticker_yahoo.history()['Close'].iloc[-1],2))
    return round(ticker_yahoo.history(period = '1d')['Open'].iloc[0],2)

def highprice(name):
    ticker_yahoo = yf.Ticker(name)
    # print(round(ticker_yahoo.history()['Close'].iloc[-1],2))
    return round(ticker_yahoo.history(period = '1d')['High'].iloc[0],2)

def lowprice(name):
    ticker_yahoo = yf.Ticker(name)
    # print(round(ticker_yahoo.history()['Close'].iloc[-1],2))
    return round(ticker_yahoo.history(period = '1d')['Low'].iloc[0],2)

def totalvolume(name):
    ticker_yahoo = yf.Ticker(name)
    # print(round(ticker_yahoo.history()['Close'].iloc[-1],2))
    return round(ticker_yahoo.history(period='1d')['Volume'].iloc[0], 2)



# print(totalvolume('aapl'))
