from flask import Flask, render_template, request
from bokeh.plotting import figure
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
  try: #Retrive information from /
    name = request.args.get('sname')
    msg = "Monthly Data for " + name

    #Request data
    monthly_data = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+name+'&apikey=SJFMXK64TWAWK71Y'
    ds = requests.get(monthly_data)

    #format data
    ds = ds.json()
    ds = ds['Time Series (Daily)']
    ds = pd.DataFrame.from_dict(json_normalize(ds))
    #print(ds)

    #Create arrays to pass to bokeh for plotting
    counter = 0
    col_counter = 0
    xs = []
    ys = []
    length = 150 #len(ds.columns)
    while(col_counter<length):
      xs.append(counter)
      ys.append(ds.iloc[0, length-col_counter])
      col_counter+=5
      counter+=1

    #Draw the figure
    fig = figure(title=msg)
    fig.line(xs, ys)
    script, div = components(fig)
    return render_template('pricechart.html', script=script, div=div)

  except:
    return render_template('error.html')




@app.route('/error')
def error():
  return render_template('error.html')


if __name__ == '__main__':
  app.run(port=33507)
