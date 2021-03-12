from multiprocessing import Pool
from passwords import user_pass
from scrape_strava_activities import scrape_activities

# need an input CSV for each of these
inputs=[[user_pass[0][0],user_pass[0][1],'inputCsv/input2.csv','outputActivityCsv/output2.csv'],
[user_pass[1][0],user_pass[1][1],'inputCsv/input3.csv','outputActivityCsv/output3.csv'],
[user_pass[2][0],user_pass[2][1],'inputCsv/input4.csv','outputActivityCsv/output4.csv'],
[user_pass[3][0],user_pass[3][1],'inputCsv/input5.csv','outputActivityCsv/output5.csv']]

pool=Pool(processes=4)
pool.map(scrape_activities, inputs)