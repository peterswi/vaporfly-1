
import csv
import pandas as pd

def findBest(csv):
    data=pd.read_csv(csv)
    data['strava_PR']=0
    #here we basically want to go through each athlete, get their races, find the fastest, save that activity ID, then go through full dataset and set those activities =1
    athletes=list(set(data['athlete_id'].tolist()))
    prActivities=[]
    for athlete in athletes:
        activities=data[data['athlete_id']==athlete]
        fastActivity=activities[activities['timeSec']==activities['timeSec'].min()]
        prActivities.append((fastActivity['data-activity_id'].tolist())[0])
    
    prCount=0
    for i in range(25451):
        activityID=data['data-activity_id'][i]
        if activityID in prActivities:
            data['strava_PR'][i]=1
            prCount=prCount+1
    

    print("Total PRs: ",prCount)
    data.to_csv('csv/CleanResults.csv',index=False)

findBest('csv/CleanResults.csv')