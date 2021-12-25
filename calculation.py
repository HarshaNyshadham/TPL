import pandas as pd

def create_new_season(filename):
 df=pd.read_excel(filename, engine ='openpyxl',sheet_name ='Groups')
 schedule=pd.DataFrame()
 num_of_groups= len(df.columns)
 for i in range(num_of_groups):
    schedule[df.column[i]]=df.iloc[:,i]

 print(schedule)
 return schedule
