import csv 
import pandas as pd

# grabbing our dataset of repeat athletes
repeat=pd.read_csv('csv/repeatAthletes.csv')

#splitting into 
pre=repeat[repeat['year']<2017]
post=repeat[repeat['year']>=2017]

#Here, sampling 500 people from each dataset
pre_sample=pre.sample(n=500) #,weights='count' --> OPTION TO WEIGHT TOWARDS HIGHER COUNT ATHLETES
post_sample=post.sample(n=500)#,weights='count' --> OPTION TO WEIGHT TOWARDS HIGHER COUNT ATHLETES

frames=[pre_sample,post_sample]
final_sample=pd.concat(frames)

#export our sample
final_sample.to_csv('csv/sampledData.csv',index=False)

