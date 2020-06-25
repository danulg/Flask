from flask import Flask, render_template, request, redirect, jsonify
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
import requests
from pandas.io.json import json_normalize
import numpy as np
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
  monthly_data = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+name+'&apikey=SJFMXK64TWAWK71Y'
  dsm = requests.get(monthly_data)

  #format data
  dsm = dsm.json()
  dsm = dsm['Monthly Time Series']
  dsm = pd.DataFrame.from_dict(json_normalize(dsm))

  #prep slice of data for drawing
  dsm = dsm.iloc[:,np.r_[0:72]]
  print(dsm)
  xs = [0,1,2,3,4,5,6,7,8,9,10,11]
  ys = [0,0,0,0,0,0,0,0,0,0,0,0]
  counter = 0
  col_counter = 1
  length = len(dsm.columns)

  #Pick slice for drawing: issue with skip length
  while(col_counter < length) and counter <=11:
    ys[counter] = dsm.iloc[0, col_counter]
    print(ys[counter])
    counter+=1
    col_counter+=6


  print(ys)

  #


  #dsm = json.load(dsm)
  #print(type(dsm))

  #dsm = pd.DataFrame(dsm)
  #dsm_ts = dsm['Monthly Time Series'][4:16]
  #print('time series is', dsm_ts)





  #Draw
  fig = figure(title=msg)
  fig.line(xs, ys)
  script, div = components(fig)
  return render_template('pricechart.html', script=script, div=div)

@app.route('/error')
def error():
  return render_template('error.html')


if __name__ == '__main__':
  app.run(port=33507)
