from flask import Flask, render_template, request #, redirect, jsonify
from bokeh.plotting import figure #, show, output_file
from bokeh.embed import components
from bokeh.models import SingleIntervalTicker, LinearAxis
import requests
from pandas.io.json import json_normalize
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
  #Retrive information from /
  name = request.args.get('sname')
  msg = "Monthly Data for " + name

  #Request data
  monthly_data = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+name+'&apikey=SJFMXK64TWAWK71Y'
  ds = requests.get(monthly_data)

  #format data
  ds = ds.json()
  #print(ds)

  ds = ds['Time Series (Daily)']
  ds = pd.DataFrame.from_dict(json_normalize(ds))
  print(ds)

  counter = 0
  col_counter = 0
  xs = []
  ys = []
  length = len(ds.columns)
  while(col_counter<length):
    xs.append(counter)
    ys.append(ds.iloc[0, col_counter])
    col_counter+=5
    counter+=1

  max_y = max(ys)
  min_y = min(ys)
  print(max_y, min_y)

  fig = figure(title=msg)
  fig.line(xs, ys)
  script, div = components(fig)
  return render_template('pricechart.html', script=script, div=div)

@app.route('/error')
def error():
  return render_template('error.html')


if __name__ == '__main__':
  app.run(port=33507)
