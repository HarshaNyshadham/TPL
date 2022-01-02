import pandas as pd
import openpyxl

def generate_sch_from_list(lst):
  temp=[]
  for i in range(len(lst)):
    for j in range(i+1,len(lst)):
      temp.append([lst[i],lst[j],'x'])

  return temp

def Schedule_writer(schedule_dataframe,filename):
   #writer for schedule

 #delete the sheet if already exist

 workbook=openpyxl.load_workbook(filename)
 if 'Schedule' in workbook.sheetnames:
     del workbook['Schedule']
     workbook.save(filename)
 #writer.to_excel(filename,sheet_name='Schedule')
 with pd.ExcelWriter(filename,engine='openpyxl',mode='a') as wr:
                     schedule_dataframe.to_excel(wr,sheet_name='Schedule')
 return True


def PointTable_writer(PT_dataframe,filename):


 workbook=openpyxl.load_workbook(filename)
 if 'PointTable' in workbook.sheetnames:
     del workbook['PointTable']
     workbook.save(filename)
 with pd.ExcelWriter(filename,engine='openpyxl',mode='a') as wr:
                     PT_dataframe.to_excel(wr,sheet_name='PointTable')

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

 writer=pd.DataFrame(schedule_data,columns=['Player1','Player2','Score'])
 Schedule_writer(writer,filename)

  #writer for pointtable
 pointtable_data=[]
 for i in range(num_of_groups):
    for j in range(len(df.index)):
      pointtable_data.extend([[df.iloc[j,i],'0','0','0','0','0',i+1]])
 writer=pd.DataFrame(pointtable_data,columns=['Player','Matches','Won','Loss','Bonus','Points','Group'])
 PointTable_writer(writer,filename)



 return num_of_groups

def update_points(filename,p1,p1points,p2,p2points):
  df=pd.read_excel(filename, engine ='openpyxl',sheet_name ='PointTable')
  p1index=0
  p2index=0
  for index,row in df.iterrows():
    if(row['Player']==str(p1)):
      p1index=index
    if(row['Player']==str(p2)):
      p2index=index


  df.at[p1index,'Points']=df.at[p1index,'Points']+p1points
  df.at[p2index,'Points']=df.at[p2index,'Points']+p2points
  PointTable_writer(df,filename)

def update_score(filename,row_id,player1,player2,p1s1,p1s2,p1s3,p2s1,p2s2,p2s3,p1forefeit,p2forefeit):
  #update leaderboard rating and past matches
  # update Score in Schedule and pointable

  score= str(p1s1)+'-'+str(p2s1)+','+str(p1s2)+'-'+str(p2s2)+','+str(p1s3)+'-'+str(p2s3)

  if(p1forefeit or p2forefeit):
   if(p1forefeit):
     update_points(filename,player1,0,player2,40)
     score='Forefeit by'+ p1
   elif(p2forefeit):
     update_points(filename,player1,40,player2,0)
     score='Forefeit by'+ p2


  df_sch=pd.read_excel(filename, engine ='openpyxl',sheet_name ='Schedule')
  df_sch.at[int(row_id),'Score']= score
  Schedule_writer(df_sch,filename)

  return True
