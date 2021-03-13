import csv
import pandas as pd

data=pd.read_csv('outputActivityCsv/output3.csv')
data['vaporfly']=0
print(data)

for i in range(1000):
    #Vaporfly Variable
    shoes=data['shoes'][i]
    if ('NEXT' in shoes.upper()) or ('VAPORFLY'in shoes.upper()) or ('%'in shoes.upper()) or ('ALPHAFLY'in shoes.upper()) :
        data['vaporfly'][i]=1
    
    #Device Formatting
    device=data['device'][i]
    device=device[2:(len(device)-1)]
    if device=='\xe2\x80\x94':
        data['device'][i]=''
    else:
        data['device'][i]=device

    #Suffer Score Formatting
    suffer=data['suffer'][i]
    suffer=suffer[2:(len(device)-1)]
    if suffer=='\xe2\x80\x94':
        data['suffer'][i]=''
    else:
        data['suffer'][i]=suffer

print('num vaporfly:',len(data[data['vaporfly']==1].index))
data.to_csv('outputActivityCsv/output3.csv',index=False)