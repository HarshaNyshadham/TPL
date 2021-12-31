import pandas as pd

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

 writer=pd.DataFrame(schedule_data,columns=['Player1','Player2','Score'])
 #writer.to_excel(filename,sheet_name='Schedule')
 with pd.ExcelWriter(filename,engine='openpyxl',mode='a') as wr:
                     writer.to_excel(wr,sheet_name='Schedule')


 print(player_list)

 print(writer)
 return num_of_groups



