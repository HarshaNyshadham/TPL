
# A very simple Flask Hello World app for you to get started with...

from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/pointtable')
def pointtable():
    return render_template('pointtable.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/playoffs')
def playoffs():
    return render_template('playoffs.html')
