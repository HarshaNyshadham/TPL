
# A very simple Flask Hello World app for you to get started with...

from flask import Flask,render_template,request,redirect,url_for
import pandas as pd
import numpy as np
from pandas import ExcelWriter,DataFrame,ExcelFile
from openpyxl import load_workbook
from werkzeug.utils import secure_filename
from calculation import create_new_season

import os
#File path

TPL_leaderboard='/home/tpl/mysite/uploads/TPL_Leaderboard.xlsx'
TPL_currentSeason='/home/tpl/mysite/uploads/TPL_currentseason.xlsx'
groups_currentseason=0

#global variable to hold current season
SeasonSchedule=pd.DataFrame()
SeasonPointtable=pd.DataFrame()

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():

    df=pd.read_excel(TPL_leaderboard, engine ='openpyxl')
    df.sort_values(by=['Current Rating'],inplace =True,ascending=False)
    data=[]

    for index,row in df.iterrows():
                   data.append([row['Player'],row['Matches'],row['Win'],row['Loss'],row['Current Rating']])


    return render_template('home.html',data=data)

@app.route('/pointtable')
def pointtable():
    return render_template('pointtable.html',data=groups_currentseason)

@app.route('/schedule')
def schedule():
    df=pd.read_excel(TPL_currentSeason, engine ='openpyxl',sheet_name ='Schedule')
    data=[]
    for index,row in df.iterrows():
      data.append([row['Player1'],row['Player2'],row['Score']])

    return render_template('schedule.html',data=data)

@app.route('/playoffs')
def playoffs():
    return render_template('playoffs.html')

@app.route('/admin',methods=['GET', 'POST'])
def admin():

  if request.method == "POST":
    pwd=request.form.get("pwd")
    if pwd == "tpl":
      return render_template('admin.html')

  return redirect(url_for('index'))

@app.route('/upload',methods=['GET', 'POST'])
def upload():
  global groups_currentseason
  groups_currentseason = create_new_season(TPL_currentSeason)
  return render_template('admin.html')
