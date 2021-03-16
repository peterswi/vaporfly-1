import csv
import pandas as pd

def clean(csv):
    data=pd.read_csv(csv)
    data['race']=''
    data['timeSec']=0
    
    for i in range(25451):
        full=data['race_name'][i]
        
        if ('TOKYO' in full.upper()):
            data['race'][i]='TOKYO'

        elif ('LONDON' in full.upper()):
            data['race'][i]='LONDON'

        elif ('BERLIN' in full.upper()):
            data['race'][i]='BERLIN'
        
        elif ('YORK' in full.upper()):
            data['race'][i]='NYC'

        elif ('CHICAGO' in full.upper()):
            data['race'][i]='CHICAGO'
        else:
            data['race']='BOSTON'

        # Rank formatting
        rank=data['Rank'][i]
        rank=rank[2:(len(rank)-1)]
        data['Rank'][i]=rank

        # Name formatting
        name=data['Name'][i]
        name=name[2:(len(name)-1)]
        data['Name'][i]=name
        
        # Gender formatting
        gender=data['Gender'][i]
        gender=gender[2:(len(gender)-1)]
        data['Gender'][i]=gender

        # Age formatting
        age=data['Age'][i]
        age=age[2:(len(age)-1)]
        data['Age'][i]=age

        # Finish formatting
        finish=data['Finish'][i]
        finish=finish[2:(len(finish)-1)]
        data['Finish'][i]=finish
        if(len(finish)>=7):    
            hours= int(finish[0])*60*60
            minu=int(finish[2:4])*60
            sec=int(finish[5:])
            data['timeSec'][i]=hours+minu+sec
        
        # Finish formatting
        pace=data['Pace'][i]
        pace=pace[2:(len(pace)-1)]
        data['Pace'][i]=pace

        
    
    data.to_csv('csv/CleanResults.csv',index=False)

clean('csv/repeatAthletes.csv')