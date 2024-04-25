from . import db, loginn_manager
from flask_login import UserMixin, login_manager
from sqlalchemy.schema import Sequence, Identity
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


id_seq = Sequence('id_seq')


@loginn_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Search(db.Model):
    id = db.Column(db.Integer, Identity(start=1), primary_key=True)
    data = db.Column(db.String(1000))
    name = db.Column(db.String(1000))
    lastprice = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Transactions(db.Model):
    id = db.Column(db.Integer, Identity(start=1), primary_key=True)
    Symbol = db.Column(db.String(50))
    Qty = db.Column(db.Float)
    name = db.Column(db.String(1000))
    StockPrice = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, Identity(start=1), primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    CurrentAddress = db.Column(db.String(150))
    AccountNumber = db.Column(db.String(150))
    CurrentBalance = db.Column(db.Float)
    profile_pic = db.Column(db.String(150), nullable=True)


    search = db.relationship('Search')

    transaction = db.relationship('Transactions')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer('hahahaha', expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer('hahahaha')
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
