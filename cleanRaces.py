import csv
import pandas as pd

def clean(csv):
    data=pd.read_csv(csv)
    data['race']=''
    
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
        
    data.to_csv(csv,index=False)

clean('csv/repeatAthletes.csv')