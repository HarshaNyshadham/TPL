
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

    df=pd.read_excel(TPL_leaderboard, engine ='openpyxl')
    df.sort_values(by=['Current Rating'],inplace =True,ascending=False)
    data=[]

    for index,row in df.iterrows():
                   data.append([row['Player'],row['Matches'],row['Win'],row['Loss'],row['Current Rating']])


    return render_template('home.html',data=data)

@app.route('/pointtable')
def pointtable():
    return render_template('pointtable.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/playoffs')
def playoffs():
    return render_template('playoffs.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')
