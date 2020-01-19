import os
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = "Ivan is PNU's student, lol!"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
    os.path.join(basedir, "site.db")

from tournaments import routes