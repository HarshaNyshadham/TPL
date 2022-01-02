
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

    df=pd.read_excel(TPL_currentSeason, engine ='openpyxl',sheet_name ='PointTable')
    data=[]
    for index,row in df.iterrows():
      data.append([row['Player'],row['Matches'],row['Won'],row['Loss'],row['Bonus'],row['Points'],row['Group']])
    return render_template('pointtable.html',data=3,pt_data=data)

#     pt_dict={}


#     print(groups_currentseason)
#     pt_dict={1:[['a','0','0','0','0','100'],['z','0','0','0','0','1000']],2:[['a','0','0','0','0','200']],3:[['a','0','0','0','0','140']]}
#     return render_template('pointtable.html',data=3,pt_data=pt_dict)

@app.route('/schedule',methods=['GET', 'POST'])
def schedule():
    df=pd.read_excel(TPL_currentSeason, engine ='openpyxl',sheet_name ='Schedule')
    data=[]
    df_pt=pd.read_excel(TPL_currentSeason, engine ='openpyxl',sheet_name ='PointTable')
    player_list=[]

    for index,row in df_pt.iterrows():
      player_list.append(row['Player'])


    if request.method == "POST":
      select_value=request.form.get("comp_select")
      for index,row in df.iterrows():
        if(select_value==row['Player1'] or select_value==row['Player1']):
          data.append([row['Player1'],row['Player2'],row['Score']])
      return render_template('schedule.html',data=data,players=player_list)

    for index,row in df.iterrows():
      data.append([row['Player1'],row['Player2'],row['Score']])

    return render_template('schedule.html',data=data,players=player_list)

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
