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
 for i in range(num_of_groups):
    grpdata[df.columns[i]]=df.iloc[:,i]
 for i in range(num_of_groups):
    schedule_data.append(generate_sch_from_list(df.iloc[:,i]))
 print(schedule_data)
 return grpdata



