import csv
import pandas as pd


#loading data into dataframe
data = pd.read_csv("wmm_results.csv") #change to wmm_results.csv 
data=pd.DataFrame(data)
#init count variable in df
data['count']=0
data['year']=0

#init count dict
count={}


for row in data['athlete_id']:
    athlete=row
    if athlete in count:
        count[athlete]=count[athlete]+1
    else:
        count[athlete]=1

for i in range(len(data['athlete_id'])):
    athlete=data['athlete_id'][i]
    data['count'][i]=count[athlete]
    # data.at(i,'count')=count[athlete]

    year=int(data['race_name'][i][:4])
    data['year'][i]=year

#this is now the dataset of repeat marathoners-- 
repeat=data[data['count']>1]


repeat.to_csv('csv/repeatAthletes.csv',index=False)

