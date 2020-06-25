from flask import Flask, render_template, request, redirect, jsonify
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
import requests
from pandas.io.json import json_normalize
import simplejson as json
import pandas as pd


app = Flask(__name__)

@app.route('/')
def index():

  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/pricechart', methods=['POST', 'GET'])
def pricechart():
  name = request.args.get('sname')
  msg = "Monthly Data for " + name
  monthly_data = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+name+'&apikey=SJFMXK64TWAWK71Y'
  dsm = requests.get(monthly_data)
  dsm = dsm.json()
  dsm = pd.DataFrame(dsm)
  dsm_date = dsm['Meta Data']
  dsm_ts = dsm['Monthly Time Series'][4:16]
  #dsm_ts = pd.DataFrame.from_dict(dsm_ts)
  print('time series is', dsm_ts)
  print('meta data is', dsm_date)

  


  fig = figure(title=name)
  fig.line([1, 2, 3, 4], [2, 4, 6, 8])
  script, div = components(fig)
  return render_template('pricechart.html', script=script, div=div)



if __name__ == '__main__':
  app.run(port=33507)
