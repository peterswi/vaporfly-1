import csv
import pandas as pd

def clean(csv):
    data=pd.read_csv(csv)
    data['vaporfly']=0

    for i in range(1000):
        #Vaporfly Variable
        shoes=data['shoes'][i]
        if ('NEXT' in shoes.upper()) or ('VAPORFLY'in shoes.upper()) or ('%'in shoes.upper()) or ('ALPHAFLY'in shoes.upper()) :
            data['vaporfly'][i]=1
        
        # Shoes formatting
        shoes=shoes[2:(len(shoes)-1)]
        data['shoes'][i]=shoes

        #Device Formatting
        device=data['device'][i]
        device=device[2:(len(device)-1)]
        data['device'][i]=device

        #Suffer Score Formatting
        suffer=data['suffer'][i]
        suffer=suffer[2:(len(suffer)-1)]
        data['suffer'][i]=suffer

    print('num vaporfly:',len(data[data['vaporfly']==1].index))
    data.to_csv(csv,index=False)

#Cleaned 1-18, 20-25
clean('outputActivityCsv/output19.csv')
