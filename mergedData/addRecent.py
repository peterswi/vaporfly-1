import csv
import pandas as pd

def clean(csv):
    data=pd.read_csv(csv)
    data['recentTime']=''
    data['raceYear'] =''
    for i in range(25451):
        data['raceYear'][i] = data['race'][i] + str(data['year'][i])
    """
    uniqueIds= data.athlete_id.unique()
    for id in uniqueIds:
        idSet=data[data['athlete_id']==id]
        #for i in idSet:
    """
    data.to_csv(csv,index=False)
    print(data[data['raceYear']=='BOSTON2014'])


clean('mergedData/merge.csv')