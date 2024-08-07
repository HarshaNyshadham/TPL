import pandas as pd

#some file names

TPL_leaderboard='/home/tpl/mysite/uploads/TPL_Leaderboard.xlsx'
TPL_currentSeason='/home/tpl/mysite/uploads/TPL_currentseason.xlsx'
TPL_Doubles='/home/tpl/mysite/uploads/TPL_Doubles.xlsx'
Playoff_filename='/home/tpl/mysite/uploads/Playoff.xlsx'

TPL_Doubles_test='/home/tpl/mysite/uploads/TPL_doubles_test.xlsx'

#get leaderboard sorted by points then %games
#returns a list by division
def get_LeaderBoard(league='Singles'):
    name_col=''
    if league=='Singles':
             df_PT=pd.read_excel(TPL_currentSeason, engine ='openpyxl',sheet_name ='PointTable',keep_default_na=False)
             name_col='Player'
    elif league=='Doubles':
            df_PT=pd.read_excel(TPL_Doubles, engine ='openpyxl',sheet_name ='PointTable',keep_default_na=False)
            name_col='Team'
    df_PT.sort_values(by=['Points','%games'],inplace =True,ascending=[False,False])
    df_PT['%games']=round(df_PT['%games'].astype(float),2)
    
    data_45=[]
    data_40=[]
    data_50=[]

    for index,row in df_PT.iterrows():
                  if(float(row['Division'])==5.0):
                    data_50.append([row[name_col],row['Points'],row['%games'],row['Matches']])
                  if(float(row['Division'])==4.5):
                    data_45.append([row[name_col],row['Points'],row['%games'],row['Matches']])
                  elif(float(row['Division'])==4.0):
                    data_40.append([row[name_col],row['Points'],row['%games'],row['Matches']])

    return data_50,data_45,data_40

#get leaderboard sorted by points then %games
#returns leaderboard data dict by Div 
def get_LeaderBoard_League(league='Singles'):
    name_col=''
    if league=='Singles':
             df_PT=pd.read_excel(TPL_currentSeason, engine ='openpyxl',sheet_name ='PointTable',keep_default_na=False)
             name_col='Player'
    elif league=='Doubles':
            df_PT=pd.read_excel(TPL_Doubles, engine ='openpyxl',sheet_name ='PointTable',keep_default_na=False)
            name_col='Team'
    df_PT.sort_values(by=['Points','%games'],inplace =True,ascending=[False,False])
    df_PT['%games']=round(df_PT['%games'].astype(float),2)
    
    data_45=[]
    data_40=[]
    data_50=[]

    for index,row in df_PT.iterrows():
                  if(float(row['Division'])==5.0):
                    data_50.append([row[name_col],row['Points'],row['%games'],row['Matches']])
                  if(float(row['Division'])==4.5):
                    data_45.append([row[name_col],row['Points'],row['%games'],row['Matches']])
                  elif(float(row['Division'])==4.0):
                    data_40.append([row[name_col],row['Points'],row['%games'],row['Matches']])

    return data_50,data_45,data_40