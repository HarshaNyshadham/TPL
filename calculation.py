import pandas as pd
import openpyxl

def generate_sch_from_list(lst):
  temp=[]
  for i in range(len(lst)):
    for j in range(i+1,len(lst)):
      temp.append([lst[i],lst[j],'x'])

  return temp

def create_new_season(filename):
 df=pd.read_excel(filename, engine ='openpyxl',sheet_name ='Groups')
 grpdata=pd.DataFrame()
 num_of_groups= len(df.columns)
 schedule_data=[]

 player_list=[]

 for i in range(num_of_groups):
    grpdata[df.columns[i]]=df.iloc[:,i]
    player_list.extend(df.iloc[:,i])
 for i in range(num_of_groups):
    schedule_data.extend(generate_sch_from_list(df.iloc[:,i]))

    #writer for schedule
 writer=pd.DataFrame(schedule_data,columns=['Player1','Player2','Score'])
 #delete the sheet if already exist

 workbook=openpyxl.load_workbook(filename)
 if 'Schedule' in workbook.sheetnames:
     del workbook['Schedule']
     workbook.save(filename)
 #writer.to_excel(filename,sheet_name='Schedule')
 with pd.ExcelWriter(filename,engine='openpyxl',mode='a') as wr:
                     writer.to_excel(wr,sheet_name='Schedule')

  #writer for pointtable
 pointtable_data=[]
 for i in range(num_of_groups):
    for j in range(len(df.index)):
      pointtable_data.extend([[df.iloc[j,i],'0','0','0','0','0',i+1]])

 writer=pd.DataFrame(pointtable_data,columns=['Player','Matches','Won','Loss','Bonus','Points','Group'])

 workbook=openpyxl.load_workbook(filename)
 if 'PointTable' in workbook.sheetnames:
     del workbook['PointTable']
     workbook.save(filename)
 with pd.ExcelWriter(filename,engine='openpyxl',mode='a') as wr:
                     writer.to_excel(wr,sheet_name='PointTable')



 return num_of_groups


def update_score(filename,row_id,p1s1,p1s2,p1s3,p2s1,p2s2,p2s3):
  #update leaderboard rating and past matches
  # update Score in Schedule and pointable
  score= str(p1s1)+'-'+str(p2s1)
  df_sch=pd.read_excel(filename, engine ='openpyxl',sheet_name ='Schedule')
  for index,row in df_sch.iterrows():
    if(row_id==index):
      print(index,score)

  return True
