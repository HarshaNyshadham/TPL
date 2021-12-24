
# A very simple Flask Hello World app for you to get started with...

from flask import Flask,render_template,request,redirect,url_for
import pandas as pd
from pandas import ExcelWriter,DataFrame,ExcelFile
from openpyxl import load_workbook
from werkzeug.utils import secure_filename
import os
#File path

TPL_leaderboard='/home/tpl/mysite/uploads/TPL_Leaderboard.xlsx'
TPL_currentSeason='/home/tpl/mysite/uploads/'

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
    return render_template('pointtable.html')

@app.route('/schedule')
def schedule():
    print(TPL_currentSeason)
    return render_template('schedule.html')

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
  #filename=secure_filename(request.form.get("sheet"))
  print(request.files['file'])
  uploadfile = request.files['file']
  print(uploadfile.filename)
  uploadfile.save(TPL_currentSeason+uploadfile.filename)
  return render_template('admin.html')
