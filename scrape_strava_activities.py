from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

import time

tic=time.perf_counter()
#GOING TO NEED TO BE LOGGED IN FOR THIS ONE-- NEED TO CHECK ON THAT.
# Check this link for log-in method: https://stackoverflow.com/questions/23102833/how-to-scrape-a-website-which-requires-login-using-python-and-beautifulsoup

#loading data into dataframe
data = pd.read_csv("strava_results_test.csv") #change to wmm_results.csv 

#getting activities in a list
activities= data['data-activity_id'].to_list()


url = "strava.com/activities/{}"

for activity in activities:
    #get our URL
    activity_url=url.format(activity)+"/overview"
    
    html_content = requests.get(activity_url).text

    soup = BeautifulSoup(html_content, "html.parser")

    gear=soup.find_all("span",{"class":"gear-name"})
    print(gear)










toc =time.perf_counter()
duration = toc - tic
print(f"Completed Execution in {duration:0.2f} seconds")