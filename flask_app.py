
# A very simple Flask Hello World app for you to get started with...

from flask import Flask,render_template,request,redirect,url_for
import pandas as pd
import numpy as np
from pandas import ExcelWriter,DataFrame,ExcelFile
from openpyxl import load_workbook
from werkzeug.utils import secure_filename
from calculation import create_new_season,update_score,Leaderboard_writer,ScoreCheck,Schedule_writer,calc_points,update_points_doubles

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

    df=pd.read_excel(TPL_leaderboard, engine ='openpyxl',sheet_name ='Leaderboard',keep_default_na=False)
    df.sort_values(by=['Active','Current Rating'],inplace =True,ascending=[True,False])
    data=[]

    for index,row in df.iterrows():
                   data.append([row['Player'],row['Active'],row['Win'],row['Loss'],row['Current Rating']])


    return render_template('home.html',data=data)

@app.route('/pointtable')
def pointtable():
    message=request.args.get('message')
    if(message):
      message='Winner is '+ str(message)
    else:
      message=''
    df=pd.read_excel(TPL_currentSeason, engine ='openpyxl',sheet_name ='PointTable',keep_default_na=False)
    df.sort_values(by=['Points'],inplace =True,ascending=False)
    data=[]
    for index,row in df.iterrows():
      data.append([row['Player'],row['Matches'],row['Won'],row['Loss'],row['Bonus'],row['Points'],row['Group']])
    return render_template('pointtable.html',data=4,pt_data=data,message=message)

#     pt_dict={}


#     print(groups_currentseason)
#     pt_dict={1:[['a','0','0','0','0','100'],['z','0','0','0','0','1000']],2:[['a','0','0','0','0','200']],3:[['a','0','0','0','0','140']]}
#     return render_template('pointtable.html',data=3,pt_data=pt_dict)

@app.route('/schedule',methods=['GET', 'POST'])
def schedule():
    df=pd.read_excel(TPL_currentSeason, engine ='openpyxl',sheet_name ='Schedule',keep_default_na=False)
    data=[]
    df_pt=pd.read_excel(TPL_currentSeason, engine ='openpyxl',sheet_name ='PointTable',keep_default_na=False)
    player_list=[]

    for index,row in df_pt.iterrows():
      player_list.append(row['Player'])


    if request.method == "POST":
      select_value=request.form.get("comp_select")
      for index,row in df.iterrows():
        if(select_value==row['Player1'] or select_value==row['Player2']):
          data.append([row['Player1'],row['Player2'],row['Score']])
      return render_template('schedule.html',data=data,players=player_list)

    for index,row in df.iterrows():
      data.append([row['Player1'],row['Player2'],row['Score']])

    return render_template('schedule.html',data=data,players=player_list)

@app.route('/playoffs')
def playoffs():
    return render_template('playoffs.html')


@app.route('/enterScore',methods=['GET', 'POST'])
def enterScore():
    player1=request.args.get('player1')
    player2=request.args.get('player2')
    row_index=request.args.get('id')
    print(row_index,player1,player2)
    error=''
    return render_template('enterScore.html',p1=player1,p2=player2,row_index=row_index,error=error)

@app.route('/submitScore',methods=['GET', 'POST'])
def submitScore():
  if request.method == "POST":
      p1s1=request.form.get("p1set1")
      p1s2=request.form.get("p1set2")
      p1s3=request.form.get("p1set3")
      p2s1=request.form.get("p2set1")
      p2s2=request.form.get("p2set2")
      p2s3=request.form.get("p2set3")
      p1forefeit=request.form.get("p1forefeit")
      p2forefeit=request.form.get("p2forefeit")
      row_index=request.args.get('row_id')
      player1=request.args.get('player1')
      player2=request.args.get('player2')


      print(row_index,player1,player2,p1s1,p1s2,p1s3,p2s1,p2s2,p2s3,p1forefeit,p2forefeit)

      #check score

      #update score
      message=update_score(TPL_currentSeason,TPL_leaderboard,row_index,player1,player2,p1s1,p1s2,p1s3,p2s1,p2s2,p2s3,p1forefeit,p2forefeit)
      name=''
      if(message):
        if(message=='p1'):
           name=player1
        elif(message=='p2'):
          name=player2
        return redirect(url_for('pointtable',message=name))
      else:
        error="incorrect score"
        return render_template('enterScore.html',p1=player1,p2=player2,row_index=row_index,error=error)
  return redirect(url_for('enterScore'))

@app.route('/admin',methods=['GET', 'POST'])
def admin():

  if request.method == "POST":
    pwd=request.form.get("pwd")
    if pwd == "tpl22":
      return render_template('admin.html')

  return redirect(url_for('index'))

@app.route('/upload',methods=['GET', 'POST'])
def upload():
  global groups_currentseason
  groups_currentseason = create_new_season(TPL_currentSeason)
  return render_template('admin.html')

@app.route('/clearLB',methods=['GET', 'POST'])
def clearLB():
 df=pd.read_excel(TPL_leaderboard, engine ='openpyxl',sheet_name ='Leaderboard',keep_default_na=False)
 for index,row in df.iterrows():
  df.at[index,'Current Rating']=1000
  df.at[index,'Prev Rating']=1000
  df.at[index,'Matches']=0
  df.at[index,'Win']=0
  df.at[index,'Loss']=0
 Leaderboard_writer(df,TPL_leaderboard)
 return render_template('admin.html')

@app.route('/modal',methods=['GET', 'POST'])
def modal():
  return render_template('modal.html')

@app.route('/rules')
def rules():
  return render_template('rules.html')

# ************** Doubles ****************

@app.route('/TplDoubles',methods=['GET', 'POST'])
def TplDoubles():

  pt_df=pd.read_excel('/home/tpl/mysite/uploads/TPL_Doubles.xlsx', engine ='openpyxl',sheet_name ='PointTable',keep_default_na=False)
  pt_df.sort_values(by=['Points','%games'],inplace =True,ascending=[False,False])
  pt_data=[]
  sch_data=[]
  error=request.args.get('error')
  message=request.args.get('message')
  players=pt_df.iloc[:,0]

  for index,row in pt_df.iterrows():
    pt_data.append([row['Team'],row['Matches'],row['Won'],row['Loss'],row['Bonus'],row['Points'],row['GamesWon'],row['GamesTotal'],row['%games']])

  sch_df=pd.read_excel('/home/tpl/mysite/uploads/TPL_Doubles.xlsx', engine ='openpyxl',sheet_name ='Schedule',keep_default_na=False)



  if request.method == "POST":
      select_value=request.form.get("comp_select")
      for index,row in sch_df.iterrows():
        if(select_value==row['Team1'] or select_value==row['Team2']):
          sch_data.append([row['Team1'],row['Team2'],row['Score']])
      return render_template('TplDoubles.html',pt_data=pt_data,sch_data=sch_data,players=players,error=error,message=message)

  for index,row in sch_df.iterrows():
    sch_data.append([row['Team1'],row['Team2'],row['Score']])

  return render_template('TplDoubles.html',pt_data=pt_data,sch_data=sch_data,players=players,error=error,message=message)

@app.route('/doublescore',methods=['GET', 'POST'])
def doublesubmitscore():
    doubles_filename='/home/tpl/mysite/uploads/TPL_Doubles.xlsx'
    t1=request.args.get('team1')
    t2=request.args.get('team2')
    p1s1=int(request.form.get("p1set1"))
    p1s2=int(request.form.get("p1set2"))
    p1s3=int(request.form.get("p1set3"))
    p2s1=int(request.form.get("p2set1"))
    p2s2=int(request.form.get("p2set2"))
    p2s3=int(request.form.get("p2set3"))
    p1forefeit=bool(request.form.get("p1forefeit"))
    p2forefeit=bool(request.form.get("p2forefeit"))
    print(t1,t2)
    error=''
    message=''
    print(p1s1,p1s2,p1s3,p2s1,p2s2,p2s3,p1forefeit,p2forefeit)
    if not (ScoreCheck(p1s1,p1s2,p1s3,p2s1,p2s2,p2s3,p1forefeit,p2forefeit)):
      error='Invalid Score!!!'
      return redirect(url_for('TplDoubles',error=error,message=message))

    df_sch=pd.read_excel(doubles_filename, engine ='openpyxl',sheet_name ='Schedule',keep_default_na=False)
    score= str(p1s1)+'-'+str(p2s1)+','+str(p1s2)+'-'+str(p2s2)+','+str(p1s3)+'-'+str(p2s3)

    if(p1forefeit or p2forefeit):
      if(p1forefeit):
        score='Forefeit by '+str(t1)
        update_points_doubles(doubles_filename,t1,0,t2,40,'p2',0,0,0)
        message='Winner is '+str(t2)
      elif(p2forefeit):
        score='Forefeit by '+str(t2)
        message='Winner is '+str(t1)
        update_points_doubles(doubles_filename,t1,40,t2,0,'p1',0,0,0)
      for index,row in df_sch.iterrows():
        if((row['Team1']==str(t1)) and  (row['Team2']==str(t2))):
         df_sch.at[index,'Score']= score
         Schedule_writer(df_sch,doubles_filename)
      return redirect(url_for('TplDoubles',error=error,message=message))

    #update Schedule


    for index,row in df_sch.iterrows():
      if((row['Team1']==str(t1)) and  (row['Team2']==str(t2))):
       df_sch.at[index,'Score']= score
       Schedule_writer(df_sch,doubles_filename)

    [t1points,t2points,winner,bonusteam]=calc_points(p1s1,p1s2,p1s3,p2s1,p2s2,p2s3)
    update_points_doubles(doubles_filename,t1,t1points,t2,t2points,winner,bonusteam,(p1s1+p1s2+p1s3),(p2s1+p2s2+p2s3))
    print(t1points,t2points,winner,bonusteam)
    if(winner=='p1'):
      message='Winner is '+str(t1)
    elif(winner=='p2'):
      message='Winner is '+str(t2)
    return redirect(url_for('TplDoubles',error=error,message=message))


# ************** End Doubles ****************

@app.route('/playerprofile',methods=['GET', 'POST'])
def playerprofile():
  playername=request.args.get('player')
  df=pd.read_excel(TPL_currentSeason, engine ='openpyxl',sheet_name ='Schedule',keep_default_na=False)
  data=[]

  for index,row in df.iterrows():
      if(playername==row['Player1'] or playername==row['Player2']):
        data.append([row['Player1'],row['Player2'],row['Score']])
  return render_template('playerprofile.html',playername=playername,data=data)
