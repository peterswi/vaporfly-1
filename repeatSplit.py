import csv
import pandas as pd

data=pd.read_csv('csv/repeatAthletes.csv')

used=pd.read_csv('csv/sampledData.csv')
usedActivities=used['data-activity_id'].to_list()

#get the unsampled data
remaining=data[~data['data-activity_id'].isin(usedActivities)]
remaining=remaining.sample(frac=1)
remaining.to_csv('csv/remainingActivities.csv',index=False)
remaining=pd.read_csv('csv/remainingActivities.csv')
#now lets split this dataframe into 25 additional csv files lol


for i in range(25):
    if (i==24):
        start=i*1000
        output=remaining[:][start:]
        filename='inputCsv/input{}.csv'.format(i)
        output.to_csv(filename,index=False)
    else:
        start=i*1000
        finish=(i+1)*1000
        output=remaining[:][start:finish]
        filename='inputCsv/input{}.csv'.format(i)
        output.to_csv(filename,index=False)
        
print(output)
print(filename)