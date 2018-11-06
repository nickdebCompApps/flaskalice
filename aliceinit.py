from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = '%&()WOIPJDI()^(O W WYOD!O W GD)'
SQLALCHEMY_DATABASE_URI = "sqlite:///C:/Users/Study/Desktop/Aliceha/alice.db"
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
db.init_app(app)

login = LoginManager(app)
login.login_view = 'login'
