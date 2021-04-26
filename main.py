from flask import Flask
from flask import render_template

from lib.prediction_class import Prediction
from lib.provider import Provider

from dateutil.relativedelta import relativedelta
from datetime import datetime

app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    now = datetime.now()
    
    print(now)
    
    prov = Provider()
    
    three_days_before = now - relativedelta(days=3)
    print(three_days_before)
    response = prov.get_predictions_in_interval_from_db(three_days_before, now)
    prov.get_predictions_in_interval_from_db(three_days_before, now)
    print(response)
    
    return render_template("index.html", appname="Football Prediction")

@app.route('/h2h')
def h2h():   
    return render_template("h2h.html", appname="Football Prediction")

@app.route('/competitions')
def competitions():   
    return render_template("competitions.html", appname="Football Prediction")
