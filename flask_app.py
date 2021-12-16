
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

#     wb = load_workbook(filename = TPL_leaderboard)
#     ws = wb.get_sheet_by_name(name='Leaderboard')
#     data=[]
#     for row in ws.iter_rows(min_row=2,max_col=2):
#       temp=[]
#       for cell in row:
#         temp.append(cell.value)
#       data.append(temp)
#     print(data)

    df=pd.read_excel(TPL_leaderboard, engine ='openpyxl')
    df.sort_values(by=['Current Rating'],inplace =True,ascending=False)
    data=[]
    counter=0
    for index,row in df.iterrows():
                   data.append([counter=counter+1,row['Player'],row['Current Rating']])




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
