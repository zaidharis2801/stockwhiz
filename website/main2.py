from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import yfinance as yf
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Models
class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Symbol = db.Column(db.String(50))
    Qty = db.Column(db.Float)
    name = db.Column(db.String(1000))
    StockPrice = db.Column(db.Float)
    user_id = db.Column(db.Integer)

# Utility functions
def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    current_price = ticker.history(period='1d')['Close'].iloc[-1]
    return current_price

def stockbeautiful(name):
    name1 = str(name)
    url = f"https://finance.yahoo.com/quote/{name1}"
    headers = {'User-agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    company = soup.select('h1.svelte-ufs8hf')[0].text.strip()
    return company

# Routes
@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    data = request.get_json()
    user_id = data.get('user_id')
    symbol = data.get('symbol')
    qty = data.get('qty')

    # Fetch current price and stock name
    current_price = get_current_price(symbol)
    stock_name = stockbeautiful(symbol)

    # Calculate total cost
    total_cost = current_price * qty

    # Create transaction record
    transaction = Transactions(
        Symbol=symbol,
        Qty=qty,
        name=stock_name,
        StockPrice=current_price,
        user_id=user_id
    )

    # Add transaction to database
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'message': 'Transaction successful'})

if __name__ == '__main__':
    app.run(debug=True, port=3000)
