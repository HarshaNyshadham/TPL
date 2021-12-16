
# A very simple Flask Hello World app for you to get started with...

from flask import Flask,render_template
import pandas as pd
from pandas import ExcelWriter,DataFrame,ExcelFile
from openpyxl import load_workbook

#File path

TPL_leaderboard='/home/tpl/mysite/uploads/TPL_Leaderboard.xlsx'

app = Flask(__name__)

@app.route('/')
def index():

    wb = load_workbook(filename = TPL_leaderboard)
    ws = wb.get_sheet_by_name(name='Leaderboard')
    print(ws)
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
