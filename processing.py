from multiprocessing import Pool
from passwords import user_pass
from scrape_strava_activities import scrape_activities

# need an input CSV for each of these
inputs=[[user_pass[1][0],user_pass[1][1],'inputCsv/input5.csv','outputActivityCsv/output5.csv'],
[user_pass[2][0],user_pass[2][1],'inputCsv/input6.csv','outputActivityCsv/output6.csv'],
[user_pass[3][0],user_pass[3][1],'inputCsv/input7.csv','outputActivityCsv/output7.csv']]

pool=Pool(processes=3)
pool.map(scrape_activities, inputs)