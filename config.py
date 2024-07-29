import pandas as pd

#some file names

TPL_leaderboard='/home/tpl/mysite/uploads/TPL_Leaderboard.xlsx'
TPL_currentSeason='/home/tpl/mysite/uploads/TPL_currentseason.xlsx'
Playoff_filename='/home/tpl/mysite/uploads/Playoff.xlsx'

TPL_Doubles_test='/home/tpl/mysite/uploads/TPL_doubles_test.xlsx'

#get leaderboard sorted by points then %games
#returns a list by division
def get_LeaderBoard():

    df_PT=pd.read_excel(TPL_currentSeason, engine ='openpyxl',sheet_name ='PointTable',keep_default_na=False)
    df_PT.sort_values(by=['Points','%games'],inplace =True,ascending=[False,False])
    df_PT['%games']=round(df_PT['%games'].astype(float),2)
    # df['Player']=df['Player'].astype(str)
    # df_PT['Player']=df_PT['Player'].astype(str)

    # df_new=df.merge(df_PT[['Player','Points','%games']],on = 'Player', how = 'left')
    # df_new=df_new.fillna(0)
    # print(df_new.columns)
    # df_new['Points']=df_new['Points'].astype(int)
    # df_new.sort_values(by=['Active','Points','%games'],inplace =True,ascending=[True,False,False])
    
    data_45=[]
    data_40=[]
    data_50=[]

    for index,row in df_PT.iterrows():
                  if(float(row['Division'])==5.0):
                    data_50.append([row['Player'],row['Points'],row['%games'],row['Matches']])
                  if(float(row['Division'])==4.5):
                    data_45.append([row['Player'],row['Points'],row['%games'],row['Matches']])
                  elif(float(row['Division'])==4.0):
                    data_40.append([row['Player'],row['Points'],row['%games'],row['Matches']])

    return data_50,data_45,data_40