from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():

  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/pricechart', methods=['POST', 'GET'])
def pricechart():
  name = request.args.get('sname', 'GOOG')
  msg = "Your input was " + name
  return render_template('pricechart.html', forward_message=msg)



if __name__ == '__main__':
  app.run(port=33507)
