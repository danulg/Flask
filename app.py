from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components


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
  msg = "Your input was " + name
  fig = figure(title="Sensor data")
  fig.line([1, 2, 3, 4], [2, 4, 6, 8])
  script, div = components(fig)
  #show(fig) -picture is drawn as required. Issues with render template
  return render_template('pricechart.html', forward_message=msg, div=div, script=script)



if __name__ == '__main__':
  app.run(port=33507)
